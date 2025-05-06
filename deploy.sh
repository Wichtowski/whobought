#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting WhoBought Azure deployment...${NC}"

# Check for required tools
echo -e "${YELLOW}Checking prerequisites...${NC}"
command -v dotnet >/dev/null 2>&1 || { echo -e "${RED}Error: .NET SDK is required but not installed.${NC}"; exit 1; }
command -v pulumi >/dev/null 2>&1 || { echo -e "${RED}Error: Pulumi CLI is required but not installed.${NC}"; exit 1; }
command -v az >/dev/null 2>&1 || { echo -e "${RED}Error: Azure CLI is required but not installed.${NC}"; exit 1; }
command -v zip >/dev/null 2>&1 || { echo -e "${RED}Error: zip is required but not installed.${NC}"; exit 1; }

# Login to Azure if not already logged in
echo -e "${YELLOW}Checking Azure login...${NC}"
az account show >/dev/null 2>&1 || { 
  echo -e "${YELLOW}Please login to Azure:${NC}"
  az login
}

# Navigate to the project root
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$PROJECT_ROOT"

# Build the .NET application
echo -e "${YELLOW}Building .NET application...${NC}"
dotnet publish whobought-backend/whobought-backend.csproj -c Release -o ./publish

# Create a deployment package
echo -e "${YELLOW}Creating deployment package...${NC}"
cd ./publish
zip -r ../whobought-api.zip .
cd ..

# Navigate to infrastructure directory
cd infrastructure

# Login to Pulumi if needed
echo -e "${YELLOW}Checking Pulumi login...${NC}"
pulumi whoami >/dev/null 2>&1 || {
  echo -e "${YELLOW}Please login to Pulumi:${NC}"
  pulumi login
}

# Select or create stack
echo -e "${YELLOW}Selecting Pulumi stack...${NC}"
read -p "Enter stack name (default: dev): " STACK_NAME
STACK_NAME=${STACK_NAME:-dev}

# Check if the stack exists
pulumi stack select $STACK_NAME 2>/dev/null || {
  echo -e "${YELLOW}Stack '$STACK_NAME' does not exist. Creating it...${NC}"
  pulumi stack init $STACK_NAME
}

# Deploy infrastructure
echo -e "${YELLOW}Deploying infrastructure with Pulumi...${NC}"
pulumi up --yes

# Get outputs from Pulumi
echo -e "${YELLOW}Getting deployment outputs...${NC}"
APPSERVICE_NAME=$(pulumi stack output appServiceName)
RESOURCE_GROUP=$(pulumi stack output resourceGroupName)
COSMOSDB_ACCOUNT=$(pulumi stack output cosmosDbAccountName)

# Deploy the application to App Service
echo -e "${YELLOW}Deploying application to App Service...${NC}"
az webapp deployment source config-zip --resource-group "$RESOURCE_GROUP" --name "$APPSERVICE_NAME" --src ../whobought-api.zip

# Get connection information
echo -e "${YELLOW}Getting Cosmos DB connection information...${NC}"
COSMOSDB_CONNECTION_STRING=$(az cosmosdb keys list --name "$COSMOSDB_ACCOUNT" --resource-group "$RESOURCE_GROUP" --type connection-strings --query "connectionStrings[0].connectionString" -o tsv)

# Get application URL
APP_URL=$(pulumi stack output appServiceUrl)

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${GREEN}Your application is deployed at: ${NC}$APP_URL"
echo
echo -e "${YELLOW}For local development, use this Cosmos DB connection string:${NC}"
echo "$COSMOSDB_CONNECTION_STRING"
echo
echo -e "${YELLOW}To view application logs:${NC}"
echo "az webapp log tail --name $APPSERVICE_NAME --resource-group $RESOURCE_GROUP" 