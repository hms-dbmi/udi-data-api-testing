# Code generated from: https://chatgpt.com/share/67d1b890-2fb8-8006-a8f3-0fdf26dd30d6

import requests
import pandas as pd
import os

# Base URL for the API
BASE_URL = "https://search.api.hubmapconsortium.org/v3/"

# List of valid entities based on the OpenAPI spec for the `param-search` endpoint
VALID_ENTITIES = ['datasets', 'samples', 'donors', 'files']

# Function to query the search API
def search_entities(entity_type):
    url = BASE_URL + f"param-search/{entity_type}"
    headers = {
        "Authorization": f"Bearer {os.getenv('HUBMAP_ACCESS_TOKEN')}",  # Pull access token from environment variable
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Ensure we handle any potential errors

    return response.json()

# Function to save data to CSV
def save_to_csv(data, entity_type):
    df = pd.json_normalize(data)
    file_name = f"{entity_type}.csv"
    df.to_csv(file_name, index=False)
    print(f"Data for {entity_type} saved to {file_name}")

# Main function to download data for all valid entities
def download_all_data():
    for entity in VALID_ENTITIES:
        print(f"Downloading data for {entity}...")
        try:
            data = search_entities(entity)
            save_to_csv(data, entity)
        except Exception as e:
            print(f"Error downloading {entity}: {e}")

# Function to determine relationships between entities
def determine_relationships():
    # Example of detecting relationships between 'Dataset' and 'Donor'
    dataset_data = search_entities('datasets')
    donor_data = search_entities('donors')
    
    # Let's assume we are matching datasets to their associated donors based on `donor.hubmap_id`
    relationships = []
    for dataset in dataset_data['hits']['hits']:
        dataset_id = dataset['_source']['hubmap_id']
        for donor in donor_data['hits']['hits']:
            donor_id = donor['_source']['hubmap_id']
            if donor_id in dataset['_source'].get('donor', {}):
                relationships.append((dataset_id, donor_id))

    # Print the relationships
    for relationship in relationships:
        print(f"Dataset {relationship[0]} is related to Donor {relationship[1]}")

# Run the functions
if __name__ == "__main__":
    # Create a directory to store the CSVs
    if not os.path.exists("entities_data"):
        os.makedirs("entities_data")
    
    os.chdir("entities_data")
    
    download_all_data()
    determine_relationships()
