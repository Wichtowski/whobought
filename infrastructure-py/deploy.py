#!/usr/bin/env python
"""
Deployment script for WhoBought application on Azure.
This script automates the Pulumi infrastructure deployment and application deployments.
"""

import os
import argparse
import subprocess
import shutil
import json
import time
from pathlib import Path

def run_command(command, cwd=None, env=None, capture_output=False):
    """Run a shell command and handle errors"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            cwd=cwd, 
            env={**os.environ, **(env or {})},
            capture_output=capture_output,
            text=True
        )
        return result.stdout if capture_output else True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Return code: {e.returncode}")
        if capture_output and e.stdout:
            print(f"Standard output: {e.stdout}")
        if capture_output and e.stderr:
            print(f"Standard error: {e.stderr}")
        return False

def check_prerequisites():
    """Check if all required tools are installed"""
    prerequisites = {
        "pulumi": "Pulumi CLI is required. Install from https://www.pulumi.com/docs/get-started/install/",
        "az": "Azure CLI is required. Install from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli",
        "python": "Python 3.8+ is required. Install from https://www.python.org/downloads/",
        "pip": "pip is required. It should be included with Python installation."
    }
    
    missing = []
    for cmd, message in prerequisites.items():
        if not shutil.which(cmd):
            missing.append(f"{cmd}: {message}")
    
    if missing:
        print("Missing prerequisites:")
        for msg in missing:
            print(f"  - {msg}")
        return False
    return True

def setup_pulumi():
    """Setup Pulumi and initialize the stack"""
    # Check if user is logged in to Pulumi
    if not run_command("pulumi whoami", capture_output=True):
        print("Please login to Pulumi")
        run_command("pulumi login")
    
    # Check if user is logged in to Azure
    if not run_command("az account show", capture_output=True):
        print("Please login to Azure")
        run_command("az login")
    
    # Create or select the dev stack
    stack_output = run_command("pulumi stack ls", capture_output=True)
    if stack_output and "dev" not in stack_output:
        print("Creating dev stack...")
        run_command("pulumi stack init dev")
    else:
        print("Selecting dev stack...")
        run_command("pulumi stack select dev")
    
    return True

def deploy_infrastructure():
    """Deploy Azure infrastructure using Pulumi"""
    print("Deploying infrastructure with Pulumi...")
    if not run_command("pulumi up -y"):
        print("Infrastructure deployment failed.")
        return False
    
    # Get stack outputs
    stack_output = run_command("pulumi stack output --json", capture_output=True)
    if not stack_output:
        print("Failed to get stack outputs.")
        return False
    
    try:
        outputs = json.loads(stack_output)
        return outputs
    except json.JSONDecodeError:
        print("Failed to parse stack outputs.")
        return False

def deploy_dotnet_api(outputs, dotnet_project_path):
    """Deploy .NET API to Azure"""
    if not outputs or "dotnet_api_url" not in outputs:
        print("Missing required outputs for .NET API deployment.")
        return False
    
    app_service_name = outputs.get("dotnet_api_url").replace("https://", "").replace(".azurewebsites.net", "")
    resource_group = outputs.get("resource_group_name")
    
    print(f"Publishing .NET API to {app_service_name}...")
    
    # Build the .NET application
    if not run_command(f"dotnet publish {dotnet_project_path} -c Release -o ./publish"):
        print("Failed to build .NET application.")
        return False
    
    # Create a deployment package
    if not os.path.exists("./publish"):
        print("Publish directory not found.")
        return False
    
    # Navigate to the publish directory and create a zip
    if not run_command("cd ./publish && zip -r ../dotnet-api.zip ."):
        print("Failed to create deployment package.")
        return False
    
    # Deploy the zip package
    if not run_command(f"az webapp deployment source config-zip --resource-group {resource_group} --name {app_service_name} --src ../dotnet-api.zip"):
        print("Failed to deploy .NET API to Azure.")
        return False
    
    print(f"Successfully deployed .NET API to {outputs.get('dotnet_api_url')}")
    return True

def deploy_python_api(outputs, python_project_path):
    """Deploy Python FastAPI to Azure"""
    if not outputs or "python_api_url" not in outputs:
        print("Missing required outputs for Python API deployment.")
        return False
    
    app_service_name = outputs.get("python_api_url").replace("https://", "").replace(".azurewebsites.net", "")
    resource_group = outputs.get("resource_group_name")
    
    print(f"Publishing Python FastAPI to {app_service_name}...")
    
    # Navigate to the Python project directory
    if not os.path.exists(python_project_path):
        print(f"Python project path not found: {python_project_path}")
        return False
    
    # Create a deployment package
    if not run_command(f"cd {python_project_path} && zip -r ../python-api.zip ."):
        print("Failed to create Python deployment package.")
        return False
    
    # Deploy the zip package
    if not run_command(f"az webapp deployment source config-zip --resource-group {resource_group} --name {app_service_name} --src ./python-api.zip"):
        print("Failed to deploy Python API to Azure.")
        return False
    
    print(f"Successfully deployed Python FastAPI to {outputs.get('python_api_url')}")
    return True

def deploy_frontend(outputs, frontend_path):
    """Deploy frontend to Azure"""
    if not outputs or "frontend_url" not in outputs:
        print("Missing required outputs for frontend deployment.")
        return False
    
    app_service_name = outputs.get("frontend_url").replace("https://", "").replace(".azurewebsites.net", "")
    resource_group = outputs.get("resource_group_name")
    
    print(f"Building and deploying frontend to {app_service_name}...")
    
    # Navigate to the frontend directory
    if not os.path.exists(frontend_path):
        print(f"Frontend path not found: {frontend_path}")
        return False
    
    # Set environment variables for build
    build_env = {
        "REACT_APP_API_URL": outputs.get("dotnet_api_url", ""),
        "REACT_APP_FASTAPI_URL": outputs.get("python_api_url", "")
    }
    
    # Build the frontend
    if not run_command("npm install && npm run build", cwd=frontend_path, env=build_env):
        print("Failed to build frontend.")
        return False
    
    # Create a deployment package from the build directory
    build_dir = os.path.join(frontend_path, "build")
    if not os.path.exists(build_dir):
        print("Frontend build directory not found.")
        return False
    
    if not run_command(f"cd {build_dir} && zip -r ../../frontend.zip ."):
        print("Failed to create frontend deployment package.")
        return False
    
    # Deploy the zip package
    if not run_command(f"az webapp deployment source config-zip --resource-group {resource_group} --name {app_service_name} --src ./frontend.zip"):
        print("Failed to deploy frontend to Azure.")
        return False
    
    print(f"Successfully deployed frontend to {outputs.get('frontend_url')}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Deploy WhoBought application to Azure")
    parser.add_argument("--all", action="store_true", help="Deploy infrastructure and all applications")
    parser.add_argument("--infra", action="store_true", help="Deploy only infrastructure")
    parser.add_argument("--dotnet", action="store_true", help="Deploy only .NET API")
    parser.add_argument("--python", action="store_true", help="Deploy only Python API")
    parser.add_argument("--frontend", action="store_true", help="Deploy only frontend")
    parser.add_argument("--dotnet-path", default="../whobought-backend", help="Path to .NET project")
    parser.add_argument("--python-path", default="../whobought-fastapi", help="Path to Python FastAPI project")
    parser.add_argument("--frontend-path", default="../whobought-frontend", help="Path to frontend project")
    
    args = parser.parse_args()
    
    # If no specific deployment is selected, deploy all
    if not (args.all or args.infra or args.dotnet or args.python or args.frontend):
        args.all = True
    
    # Check prerequisites
    if not check_prerequisites():
        return 1
    
    # Setup Pulumi
    if args.all or args.infra:
        if not setup_pulumi():
            return 1
    
    # Deploy infrastructure
    outputs = None
    if args.all or args.infra:
        outputs = deploy_infrastructure()
        if not outputs:
            return 1
    else:
        # Get existing stack outputs if not deploying infrastructure
        stack_output = run_command("pulumi stack output --json", capture_output=True)
        try:
            outputs = json.loads(stack_output) if stack_output else None
        except json.JSONDecodeError:
            print("Failed to parse existing stack outputs.")
            return 1
    
    # Ensure we have outputs for application deployments
    if not outputs:
        print("No infrastructure outputs available for application deployments.")
        return 1
    
    # Deploy applications based on arguments
    success = True
    
    if args.all or args.dotnet:
        if not deploy_dotnet_api(outputs, args.dotnet_path):
            success = False
    
    if args.all or args.python:
        if not deploy_python_api(outputs, args.python_path):
            success = False
    
    if args.all or args.frontend:
        if not deploy_frontend(outputs, args.frontend_path):
            success = False
    
    if success:
        print("\nDeployment completed successfully!")
        print("\nEndpoints:")
        print(f"  .NET API: {outputs.get('dotnet_api_url', 'N/A')}")
        print(f"  Python API: {outputs.get('python_api_url', 'N/A')}")
        print(f"  Frontend: {outputs.get('frontend_url', 'N/A')}")
        return 0
    else:
        print("\nDeployment completed with errors.")
        return 1

if __name__ == "__main__":
    exit(main()) 