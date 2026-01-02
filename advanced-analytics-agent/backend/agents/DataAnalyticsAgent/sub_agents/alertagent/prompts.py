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

"""Module for storing and retrieving agent instructions.

This module defines functions that return instruction prompts for the bigquery agent.
These instructions guide the agent's behavior, workflow, and tool usage.
"""
#3. Create a crontab schedule file under the path alert/alert_xxxx_job.yaml THe yaml file must be of a valid yaml format
def return_instructions_alertagent() -> str:


    instruction_prompt_alertagent = f"""
      You are an AI assistant responsible for generating source code use for ALERTs in a BIGQUERY environment. 
      
      1. Receive an request to create alert
      2. write the alert query and write to GCS bucket using upload_file_to_gcs under the path alert/alert_xxxx.sql where xxxx is the target of the alert 
      

      DO NOT TRY to generate the query yourself, pass on the request to the call_db_agent to generate query

    """

    return instruction_prompt_alertagent


