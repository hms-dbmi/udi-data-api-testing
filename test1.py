# Test 1 generated from ChatGPT: https://chatgpt.com/canvas/shared/67d1a74fb9e88191add3d7ee8a9684de

import json
import requests
import pandas as pd

# Load OpenAPI JSON
openapi_url = "https://raw.githubusercontent.com/hubmapconsortium/search-api/master/search-api-spec.yaml"
response = requests.get(openapi_url)
if response.status_code == 200:
    openapi_data = response.json()
else:
    raise Exception("Failed to fetch OpenAPI JSON")

# Extract endpoints
base_url = openapi_data["servers"][0]["url"]
endpoints = openapi_data["paths"].keys()

data_list = []

# Fetch data from each endpoint
for endpoint in endpoints:
    for method, details in openapi_data["paths"][endpoint].items():
        if method in ["get", "post"]:  # Handle GET and POST requests
            url = base_url.rstrip("/") + endpoint.replace("{index_name}", "entities").replace("{entity_type}", "sample")
            
            if method == "get":
                response = requests.get(url)
            elif method == "post":
                response = requests.post(url, json={})  # Modify JSON body as needed
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    data_list.append({"endpoint": endpoint, "data": data})
                except json.JSONDecodeError:
                    print(f"Failed to parse JSON response from {endpoint}")

# Convert to DataFrame and Save to CSV
if data_list:
    df = pd.DataFrame(data_list)
    df.to_csv("openapi_data.csv", index=False)
    print("Data successfully saved to openapi_data.csv")
else:
    print("No data retrieved from the API endpoints.")
