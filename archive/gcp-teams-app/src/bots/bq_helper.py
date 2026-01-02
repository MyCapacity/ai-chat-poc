import os
from google.cloud import bigquery
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import json
from google.oauth2 import service_account



def query_bigquery(query_string: str, projectid: str, credentialjson:str):
    
    """
    Queries Google BigQuery using credentials obtained from Azure Key Vault.

    Parameters:
    - query_string: SQL query string to execute.
    - project_id: Google Cloud Project ID.

    Returns:
    - List of query results.
    """
    
    project_id = "ddaastransformdev"
    print (project_id)
    
    try:

        # Set the GCP credentials in the environment variable for authentication
        gcp_credentials_json = credentialjson

        credentials_info = json.loads(gcp_credentials_json)
        credentials = service_account.Credentials.from_service_account_info(credentials_info)

        # Initialize BigQuery client
        client = bigquery.Client(credentials=credentials, project=project_id)

        # Run the query
        query_job = client.query(query_string)
        results = query_job.result()

        # Convert the results into a list of dictionaries
        rows = [dict(row) for row in results]

        return rows
    
    except Exception as e:
        print(e)
        raise e
