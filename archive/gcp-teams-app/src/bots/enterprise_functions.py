import os
import json
import requests
from datetime import datetime as pydatetime, timedelta, timezone, date
from typing import Optional, Callable, Any, Set
from dotenv import load_dotenv
import bots.bq_helper 
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

load_dotenv(override=True)

def fetch_datetime(
    format_str: str = "%Y-%m-%d %H:%M:%S",
    unix_ts: int | None = None,
    tz_offset_seconds: int | None = None
) -> str:
    """
    Returns either the current UTC date/time in the given format, or if unix_ts
    is given, converts that timestamp to either UTC or local time (tz_offset_seconds).

    :param format_str: The strftime format, e.g. "%Y-%m-%d %H:%M:%S".
    :param unix_ts: Optional Unix timestamp. If provided, returns that specific time.
    :param tz_offset_seconds: If provided, shift the datetime by this many seconds from UTC.
    :return: A JSON string containing the "datetime" or an "error" key/value.
    """
    try:
        if unix_ts is not None:
            dt_utc = pydatetime.fromtimestamp(unix_ts, tz=timezone.utc)
        else:
            dt_utc = pydatetime.now(timezone.utc)

        if tz_offset_seconds is not None:
            local_tz = timezone(timedelta(seconds=tz_offset_seconds))
            dt_local = dt_utc.astimezone(local_tz)
            result_str = dt_local.strftime(format_str)
        else:
            result_str = dt_utc.strftime(format_str)

        return json.dumps({"datetime": result_str})
    except Exception as e:
        return json.dumps({"error": f"Exception: {str(e)}"})


def fetch_crown_bigquery_data(
    query: str,
    bqProject:str = "ddaastransformdev"
) -> str:
    """
    Fetches query results from bigquery 
    :param query: the query to run against the server 
    :param bqProject: the billing project to use when running the query
    :return: A JSON string query results or an "error" key if an issue.
    """

    try:
        def datetime_handler(obj):
            if isinstance(obj, (date, pydatetime)):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

        gcp_credentials_json = get_keyvault_secret("kv-aipocdev", "gcp-sa-key")
        results = bots.bq_helper.query_bigquery(query, bqProject, gcp_credentials_json)
        return json.dumps(results, default=datetime_handler)

    except Exception as e:
        return json.dumps({"error": f"Exception occurred: {str(e)}"})


def get_keyvault_secret(vaultName:str, keyName:str):
   
    keyVaultName = vaultName if vaultName  else "kv-aipocdev" 
    KVUri = f"https://{keyVaultName}.vault.azure.net"

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)
    # Fetch the secret from Key Vault
    secret = client.get_secret(keyName)
    # Return the secret (GCP credentials)
    return secret.value

# make functions callable a callable set from enterprise-streaming-agent.ipynb
enterprise_fns: Set[Callable[..., Any]] = {
    fetch_datetime,
    fetch_crown_bigquery_data
}

