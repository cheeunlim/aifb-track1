import google.auth

_, PROJECT_ID = google.auth.default()
LOCATION="asia-northeast1"
COLLECTION_ID="amazon-product-768-compact"

from google.cloud import vectorsearch_v1beta

# Create the client
vector_search_service_client = vectorsearch_v1beta.VectorSearchServiceClient()

# The JSON schema for the data
data_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
    },
}

# The JSON schema for the vector
vector_schema = {
    "image_embedding": {"dense_vector": {"dimensions": 768}},
    "text_embedding": {"dense_vector": {"dimensions": 768}}
}

collection = vectorsearch_v1beta.Collection(
    data_schema=data_schema,
    vector_schema=vector_schema,
)
request = vectorsearch_v1beta.CreateCollectionRequest(
    parent=f"projects/{PROJECT_ID}/locations/{LOCATION}",
    collection_id=COLLECTION_ID,
    collection=collection,
)

# Create the collection
operation = vector_search_service_client.create_collection(request=request)

# Wait for the result (note this may take up to several minutes)
operation.result()

from datetime import datetime
from google.cloud import vectorsearch_v1

# Create the client
vector_search_service_client = vectorsearch_v1.VectorSearchServiceClient()

# Initialize request
request = vectorsearch_v1.ImportDataObjectsRequest(
    name=f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/{COLLECTION_ID}",
    gcs_import={
      "contents_uri": f"gs://{PROJECT_ID}-vs2/data/",
      "error_uri": f"gs://{PROJECT_ID}-vs2/error/",
    },
)

# Make the request
print(datetime.now()) 
operation = vector_search_service_client.import_data_objects(request=request)

import time
while operation.done() == False:
    time.sleep(1)
print(f"Collection created at {datetime.now()}")
time.sleep(30)

from google.cloud import vectorsearch_v1beta

def create_index(index_field: str):
    # Create a client
    client = vectorsearch_v1beta.VectorSearchServiceClient()

    # Initialize request argument(s)
    index = vectorsearch_v1beta.Index(
        index_field=index_field,
        #filter_fields=["year", "genre"],
        store_fields=["name", "description"],
    )
    request = vectorsearch_v1beta.CreateIndexRequest(
        parent=f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/{COLLECTION_ID}",
        index_id=f"idx-{index_field.replace('_', '-')}",
        index=index,
    )
    
    # Make the request
    return client.create_index(request=request)

operation = create_index("image_embedding")
while operation.done() == False:
    time.sleep(1)
print(f"Image embedding index created at {datetime.now()}")
time.sleep(30)

operation = create_index("text_embedding")
while operation.done() == False:
    time.sleep(1)
print(f"Text embedding index created at {datetime.now()}")
time.sleep(30)