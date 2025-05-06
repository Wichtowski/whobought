# WhoBought Azure Infrastructure (Python)

This folder contains the Python version of the infrastructure-as-code setup for deploying the WhoBought application to Azure using Pulumi.

## Requirements

- [Python 3.8+](https://www.python.org/downloads/)
- [Pulumi CLI](https://www.pulumi.com/docs/get-started/install/)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)

## Getting Started

### Local Setup

1. Install the Pulumi CLI following the [instructions here](https://www.pulumi.com/docs/get-started/install/)
2. Login to Pulumi:
   ```
   pulumi login
   ```
3. Login to Azure:
   ```
   az login
   ```
4. Create a Python virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
6. Create a new Pulumi stack (if it doesn't exist):
   ```
   pulumi stack init dev
   ```

### Deploy to Azure

To deploy the infrastructure:

1. Run the Pulumi update command:
   ```
   pulumi up
   ```

2. After the infrastructure is deployed, you can get the URLs from Pulumi outputs:
   ```
   pulumi stack output dotnet_api_url    # Original .NET API URL
   pulumi stack output python_api_url    # Python FastAPI URL
   pulumi stack output frontend_url      # Frontend URL
   ```

3. You can deploy your applications to the created App Services:
   - For .NET API: Use the original deployment script with the new App Service name
   - For Python FastAPI: Use the new App Service with the Python runtime
   - For Frontend: Deploy to the dedicated frontend App Service

## Resources Created

This Pulumi program creates:

- Azure Resource Group
- Azure Cosmos DB account, database, and containers (Items, Users, Groups, Expenses, Settlements)
- Azure App Service Plan (B1 tier)
- Three Azure App Services:
  - Original .NET API
  - Python FastAPI API
  - Frontend Web App

## Configuration

You can modify the configuration in `__main__.py` to customize:

- Resource naming
- Azure regions
- App Service plan tier
- Environment variables and app settings
- Container partitioning strategies

## Differences from C# Version

This Python version has a few enhancements over the original C# version:

1. Added support for Python FastAPI backend deployment
2. Added a dedicated App Service for the frontend
3. Improved environment variable configuration
4. Structured exports for easier CLI access

## Troubleshooting

- If you encounter permission issues, make sure your Azure user has sufficient permissions.
- For deployment issues, check the Pulumi logs and Azure Portal for details.
- To view application logs in Azure:
  ```
  az webapp log tail --name $(pulumi stack output dotnet_api_url) --resource-group $(pulumi stack output resource_group_name)
  ``` 