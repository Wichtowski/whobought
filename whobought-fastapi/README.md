# WhoBought FastAPI Backend

This is the Python FastAPI backend for the WhoBought application, which manages shared expenses between users.

## Features

- RESTful API with standardized response format
- Integration with Azure Cosmos DB
- Dependency injection with singletons for database connections
- Environment variable configuration

## Requirements

- Python 3.9+
- FastAPI
- Azure Cosmos DB

## Environment Variables

The application uses the following environment variables, which are automatically loaded from Azure App Service settings:

- `COSMOS_CONNECTION_STRING`: The connection string for Azure Cosmos DB
- `COSMOS_DATABASE_NAME`: The name of the Cosmos DB database (default: "whobought")
- `COSMOS_CONTAINER_NAME`: The name of the items container (default: "items")
- `COSMOS_USER_CONTAINER_NAME`: The name of the users container (default: "users")

## Local Development

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   # Windows
   set COSMOS_CONNECTION_STRING=your_connection_string
   
   # Linux/macOS
   export COSMOS_CONNECTION_STRING=your_connection_string
   ```

3. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

The API will be available at http://localhost:8000.

## API Documentation

When running the application, interactive API documentation is available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Azure Deployment

This application is configured to run on Azure App Service. When deploying:

1. Configure the environment variables in the Azure App Service Configuration settings.
2. Deploy using the Dockerfile or Azure App Service's built-in Python support.
3. Make sure the WEBSITES_PORT environment variable is set to 8000 in Azure. 