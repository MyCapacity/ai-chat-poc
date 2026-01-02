import xmltodict
import json
import os
print("test")

folder_path = 'C:\\work\\crown\\ddaas-ai-poc\\GCP\\crown_extracts\\'


for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path) and file_path.lower().endswith(".xml"):
        print(f"Found file: {file_path}")
        with open(file_path) as f:
            dict_data = xmltodict.parse(f.read())

            with open(file_path.lower().replace(".xml", ".json") , 'w', encoding='utf-8') as f:

                # Convert dict to JSON string.
                json.dump(dict_data, f, indent=4, ensure_ascii=False)

