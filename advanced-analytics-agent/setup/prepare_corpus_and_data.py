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

from google.auth import default
import vertexai
from vertexai.preview import rag
import os
from dotenv import load_dotenv, set_key
import requests
import tempfile
from google.cloud import storage

# Load environment variables from .env file
load_dotenv()

# --- Please fill in your configurations ---
# Retrieve the PROJECT_ID from the environmental variables.
PROJECT_ID = "ddaastransformdev" #os.getenv("GOOGLE_CLOUD_PROJECT")
if not PROJECT_ID:
    raise ValueError(
        "GOOGLE_CLOUD_PROJECT environment variable not set. Please set it in your .env file."
    )
LOCATION = "us-central1" #os.getenv("GOOGLE_CLOUD_LOCATION")
if not LOCATION:
    raise ValueError(
        "GOOGLE_CLOUD_LOCATION environment variable not set. Please set it in your .env file."
    )
CORPUS_DISPLAY_NAME = "crown_dw_template"
CORPUS_DESCRIPTION = "Corpus containing crown datawarehouse metadata for reporting"

# --- Start of the script ---
def initialize_vertex_ai():
  credentials, _ = default()
  vertexai.init(
      project=PROJECT_ID, location=LOCATION, credentials=credentials
  )


def create_or_get_corpus():
  """Creates a new corpus or retrieves an existing one."""
  embedding_model_config = rag.EmbeddingModelConfig(
      publisher_model="publishers/google/models/text-embedding-004"
  )
  print(f"creating a corpus...")
  existing_corpora = rag.list_corpora()
  corpus = None
  for existing_corpus in existing_corpora:
    if existing_corpus.display_name == CORPUS_DISPLAY_NAME:
      corpus = existing_corpus
      print(f"Found existing corpus with display name '{CORPUS_DISPLAY_NAME}'")
      break
  if corpus is None:
    corpus = rag.create_corpus(
        display_name=CORPUS_DISPLAY_NAME,
        description=CORPUS_DESCRIPTION,
        embedding_model_config=embedding_model_config,
    )
    print(f"Created new corpus with display name '{CORPUS_DISPLAY_NAME}'")
  return corpus

def empty_storage_folder ( bucket_name, storage_folder):
    storage_client = storage.Client()
     #empty the folder
    blobs = storage_client.list_blobs(bucket_name, prefix=storage_folder)
    for blob in blobs:
        print(f"Deleting: {blob.name}")
        blob.delete()

def upload_to_gcs(local_file_path, bucket_name, blob_name):
    """Uploads a file to the specified GCS bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_filename(local_file_path)
    print(f"File {local_file_path} uploaded to {bucket_name}/{blob_name}.")
    return f"gs://{bucket_name}/"


def upload_folder_to_gcs_and_corpus(folder_path, bucket_name, corpus_name):
    """Uploads all files from a folder to GCS and then imports them to the corpus."""
    print(f"Uploading files from {folder_path} to GCS bucket {bucket_name} and importing to corpus...")
    
    storage_folder = "crown_dw_templates"

    empty_storage_folder(bucket_name, storage_folder)


    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.xml') or filename.lower().endswith('.sql') or  filename.lower().endswith('.txt') :
            
            local_file_path = os.path.join(folder_path, filename)
            
            if filename.lower().endswith('.txt') :
                blob_name = f"{storage_folder}/{filename}"
            else :       
                blob_name = f"{storage_folder}/{filename}.txt"  #rename to text file
        
        
            try:
                gcs_uri = upload_to_gcs(local_file_path, bucket_name, blob_name)
                display_name = os.path.splitext(filename)[0]  # Remove extension
                description = f"File: {filename}"
        
                print(f"File {filename} uploaded to GCS and imported to corpus.")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
    
          
    # Import the file to the corpus
    rag_file = rag.import_files(
        corpus_name=corpus_name,
        paths=[f'gs://ai-agent-store/{storage_folder}'],
        llm_parser=rag.LlmParserConfig(
            model_name="gemini-2.5-pro-preview-05-06",
            max_parsing_requests_per_min=100,
        ),  # Optional
        max_embedding_requests_per_min=900,  # Optional
    )

    print (rag_file)

    
    return rag_file


def update_env_file(corpus_name, env_file_path):
    """Updates the .env file with the corpus name."""
    try:
        set_key(env_file_path, "RAG_CORPUS", corpus_name)
        print(f"Updated RAG_CORPUS in {env_file_path} to {corpus_name}")
    except Exception as e:
        print(f"Error updating .env file: {e}")

def list_corpus_files(corpus_name):
    """Lists files in the specified corpus."""
    files = list(rag.list_files(corpus_name=corpus_name))
    print(f"Total files in corpus: {len(files)}")
    for file in files:
        print(f"File: {file.display_name} - {file.name}")


def main():
    initialize_vertex_ai()
    corpus = create_or_get_corpus()

    # Update the .env file with the corpus name
    #update_env_file(corpus.name, ENV_FILE_PATH)
    
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the crown_extracts folder
    crown_extracts_path = os.path.abspath(os.path.join(current_dir, '../templates'))
    
        # Upload files to GCS and import to corpus
    gcs_bucket_name = "ai-agent-store"  # Replace with your actual GCS bucket name
    uploaded_files = upload_folder_to_gcs_and_corpus(crown_extracts_path, gcs_bucket_name, corpus.name)
    

    
    # List all files in the corpus
    list_corpus_files(corpus_name=corpus.name)

if __name__ == "__main__":
  main()