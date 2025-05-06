"""
Pulumi program for deploying Azure infrastructure for the WhoBought application.
This deploys Azure resources similar to the original C# version.
"""

import pulumi
from pulumi_azure_native import resources, web, documentdb
import pulumi_random as random

# Create an Azure Resource Group
resource_group = resources.ResourceGroup("whobought-rg", 
    location="northeurope"  # Specify a location for your resources
)

# Generate a random password for Cosmos DB
cosmos_password = random.RandomPassword("cosmos-password", 
    length=16,
    special=True
)

# Generate a random JWT secret
jwt_secret = random.RandomPassword("jwt-secret", 
    length=64,
    special=True
)

# Create a Cosmos DB account
cosmos_db_account = documentdb.DatabaseAccount("whoboughtcosmosdb",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    database_account_offer_type=documentdb.DatabaseAccountOfferType.STANDARD,
    locations=[documentdb.LocationArgs(
        location_name="northeurope",
        failover_priority=0,
        is_zone_redundant=False
    )],
    consistency_policy=documentdb.ConsistencyPolicyArgs(
        default_consistency_level=documentdb.DefaultConsistencyLevel.SESSION
    ),
    enable_automatic_failover=False
)

# Get the primary key for the Cosmos DB account
cosmos_db_keys = pulumi.Output.all(resource_group.name, cosmos_db_account.name).apply(
    lambda args: documentdb.list_database_account_keys(
        resource_group_name=args[0],
        account_name=args[1]
    )
)

# Create a Cosmos DB SQL database
cosmos_db = documentdb.SqlResourceSqlDatabase("WhoBoughtDb",
    resource_group_name=resource_group.name,
    account_name=cosmos_db_account.name,
    resource=documentdb.SqlDatabaseResourceArgs(
        id="WhoBoughtDb"
    )
)

# Create the Items container
items_container = documentdb.SqlResourceSqlContainer("items-container",
    resource_group_name=resource_group.name,
    account_name=cosmos_db_account.name,
    database_name=cosmos_db.name,
    resource=documentdb.SqlContainerResourceArgs(
        id="Items",
        partition_key=documentdb.ContainerPartitionKeyArgs(
            paths=["/id"],
            kind="Hash"
        )
    )
)

# Create the Users container
users_container = documentdb.SqlResourceSqlContainer("users-container",
    resource_group_name=resource_group.name,
    account_name=cosmos_db_account.name,
    database_name=cosmos_db.name,
    resource=documentdb.SqlContainerResourceArgs(
        id="Users",
        partition_key=documentdb.ContainerPartitionKeyArgs(
            paths=["/id"],
            kind="Hash"
        )
    )
)

# Create the Groups container
groups_container = documentdb.SqlResourceSqlContainer("groups-container",
    resource_group_name=resource_group.name,
    account_name=cosmos_db_account.name,
    database_name=cosmos_db.name,
    resource=documentdb.SqlContainerResourceArgs(
        id="Groups",
        partition_key=documentdb.ContainerPartitionKeyArgs(
            paths=["/id"],
            kind="Hash"
        )
    )
)

# Create the Expenses container
expenses_container = documentdb.SqlResourceSqlContainer("expenses-container",
    resource_group_name=resource_group.name,
    account_name=cosmos_db_account.name,
    database_name=cosmos_db.name,
    resource=documentdb.SqlContainerResourceArgs(
        id="Expenses",
        partition_key=documentdb.ContainerPartitionKeyArgs(
            paths=["/groupId"],
            kind="Hash"
        )
    )
)

# Create the Settlements container
settlements_container = documentdb.SqlResourceSqlContainer("settlements-container",
    resource_group_name=resource_group.name,
    account_name=cosmos_db_account.name,
    database_name=cosmos_db.name,
    resource=documentdb.SqlContainerResourceArgs(
        id="Settlements",
        partition_key=documentdb.ContainerPartitionKeyArgs(
            paths=["/groupId"],
            kind="Hash"
        )
    )
)

# Create an App Service Plan
app_service_plan = web.AppServicePlan("whobought-plan",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    kind="App",
    sku=web.SkuDescriptionArgs(
        tier="Basic",
        name="B1"
    )
)

# Create the App Service (web app) for API
api_app = web.WebApp("whobought-api",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    server_farm_id=app_service_plan.id,
    site_config=web.SiteConfigArgs(
        app_settings=[
            web.NameValuePairArgs(
                name="WEBSITE_RUN_FROM_PACKAGE",
                value="1"
            ),
            web.NameValuePairArgs(
                name="CosmosDb__EndpointUri",
                value=cosmos_db_account.document_endpoint
            ),
            web.NameValuePairArgs(
                name="CosmosDb__PrimaryKey",
                value=cosmos_db_keys.apply(lambda keys: keys.primary_master_key)
            ),
            web.NameValuePairArgs(
                name="COSMOS_DATABASE_NAME",
                value="WhoBoughtDb"
            ),
            web.NameValuePairArgs(
                name="Jwt__Key",
                value=jwt_secret.result
            ),
            web.NameValuePairArgs(
                name="Jwt__Issuer",
                value="WhoBoughtApp"
            ),
            web.NameValuePairArgs(
                name="Jwt__Audience",
                value="WhoBoughtUsers"
            ),
        ],
        net_framework_version="v8.0",
        always_on=True
    ),
    https_only=True
)

# Create the App Service (web app) for FastAPI Python backend
python_api_app = web.WebApp("whobought-fastapi",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    server_farm_id=app_service_plan.id,
    site_config=web.SiteConfigArgs(
        app_settings=[
            web.NameValuePairArgs(
                name="WEBSITE_RUN_FROM_PACKAGE",
                value="1"
            ),
            web.NameValuePairArgs(
                name="COSMOS_CONNECTION_STRING",
                value=pulumi.Output.all(resource_group.name, cosmos_db_account.name).apply(
                    lambda args: documentdb.list_database_account_connection_strings(
                        resource_group_name=args[0],
                        account_name=args[1]
                    ).connection_strings[0].connection_string
                )
            ),
            web.NameValuePairArgs(
                name="COSMOS_DATABASE_NAME",
                value="WhoBoughtDb"
            ),
            web.NameValuePairArgs(
                name="COSMOS_CONTAINER_NAME",
                value="Items"
            ),
            web.NameValuePairArgs(
                name="COSMOS_USER_CONTAINER_NAME",
                value="Users"
            ),
            web.NameValuePairArgs(
                name="JWT_SECRET_KEY",
                value=jwt_secret.result
            ),
            web.NameValuePairArgs(
                name="JWT_ALGORITHM",
                value="HS256"
            ),
            web.NameValuePairArgs(
                name="JWT_EXPIRATION_MINUTES",
                value="60"
            ),
            web.NameValuePairArgs(
                name="JWT_ISSUER",
                value="WhoBoughtApp"
            ),
            web.NameValuePairArgs(
                name="JWT_AUDIENCE",
                value="WhoBoughtUsers"
            ),
            web.NameValuePairArgs(
                name="WEBSITES_PORT",
                value="8000"
            ),
        ],
        python_version="3.9",
        always_on=True,
        linux_fx_version="PYTHON|3.9"
    ),
    https_only=True
)

# Create the App Service (web app) for Frontend
frontend_app = web.WebApp("whobought-web",
    resource_group_name=resource_group.name,
    location=resource_group.location,
    server_farm_id=app_service_plan.id,
    site_config=web.SiteConfigArgs(
        app_settings=[
            web.NameValuePairArgs(
                name="WEBSITE_RUN_FROM_PACKAGE",
                value="1"
            ),
            web.NameValuePairArgs(
                name="API_URL",
                value=pulumi.Output.format("https://{0}", api_app.default_host_name)
            ),
            web.NameValuePairArgs(
                name="FASTAPI_URL",
                value=pulumi.Output.format("https://{0}", python_api_app.default_host_name)
            ),
        ],
        node_version="~16",
        always_on=True
    ),
    https_only=True
)

# Export the connection strings and resource names
pulumi.export("resource_group_name", resource_group.name)
pulumi.export("cosmos_db_endpoint", cosmos_db_account.document_endpoint)
pulumi.export("cosmos_db_account_name", cosmos_db_account.name)
pulumi.export("dotnet_api_url", pulumi.Output.format("https://{0}", api_app.default_host_name))
pulumi.export("python_api_url", pulumi.Output.format("https://{0}", python_api_app.default_host_name))
pulumi.export("frontend_url", pulumi.Output.format("https://{0}", frontend_app.default_host_name))
pulumi.export("location", resource_group.location) 