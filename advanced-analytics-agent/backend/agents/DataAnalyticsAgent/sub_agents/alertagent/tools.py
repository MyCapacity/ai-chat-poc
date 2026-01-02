# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Top level agent for data agent multi-agents.

-- it get data from database (e.g., BQ) using NL2SQL
-- then, it use NL2Py to do further data analysis as needed
"""

from google.adk.tools import ToolContext
from google.adk.tools.agent_tool import AgentTool
from google.cloud import storage
import os
from ..bigquery.agent import database_agent as db_agent

async def upload_file_to_gcs(
    fileContent: str,
    filePath: str,
    bucketname: str
):
    return upload_content_to_gcs("xw_temp_bucket", filePath, fileContent)
    


def upload_content_to_gcs(bucket_name: str, blob_name: str, content : str, content_type: str = "text/plain"):
    """
    Uploads an in-memory buffer to GCS.

    Args:
        bucket_name (str): Target GCS bucket name.
        blob_name (str): Destination path in the bucket.
        buffer: A BytesIO or StringIO object.
        content_type (str): MIME type of the content.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_string(content, content_type=content_type)
    return f"✅ Buffer uploaded to gs://{bucket_name}/{blob_name}"


