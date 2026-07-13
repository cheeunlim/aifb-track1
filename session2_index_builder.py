import google.auth
import time

_, PROJECT_ID = google.auth.default()
LOCATION="asia-northeast1"
COLLECTION_ID="amazon-product-768-compact"

from datetime import datetime
from google.cloud import vectorsearch_v1
from google.api_core import retry as google_retry
from google.api_core import exceptions

# Create the client
vector_search_service_client = vectorsearch_v1.VectorSearchServiceClient()

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

collection = vectorsearch_v1.Collection(
    data_schema=data_schema,
    vector_schema=vector_schema,
)
request = vectorsearch_v1.CreateCollectionRequest(
    parent=f"projects/{PROJECT_ID}/locations/{LOCATION}",
    collection_id=COLLECTION_ID,
    collection=collection,
)

custom_retry = google_retry.Retry(
    predicate=google_retry.if_exception_type(
        exceptions.ServiceUnavailable,
        exceptions.DeadlineExceeded,
        exceptions.InternalServerError,
    ),
    initial=1.0,      # 최초 재시도 전 대기 시간 (1초)
    maximum=10.0,     # 최대 대기 시간 (10초)
    multiplier=2.0,   # 대기 시간 배수 (1초 -> 2초 -> 4초 ...)
    deadline=60.0     # 총 재시도를 시도할 최대 시간 (60초)
)

# Create the collection
operation = vector_search_service_client.create_collection(
    request=request,
    retry=custom_retry,
    timeout=60.0  # 개별 RPC 요청의 타임아웃
    )

# Wait for the result (note this may take up to several minutes)
while operation.done() == False:
    time.sleep(1)
print(f"Collection created at {datetime.now()}")
time.sleep(30)

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
operation = vector_search_service_client.import_data_objects(
    request=request,
    retry=custom_retry,
    timeout=60.0  # 개별 RPC 요청의 타임아웃
    )

while operation.done() == False:
    time.sleep(1)
print(f"Import data finished at {datetime.now()}")
time.sleep(30)

def create_index(client, index_field: str):
    # Initialize request argument(s)
    index = vectorsearch_v1.Index(
        index_field=index_field,
        #filter_fields=["year", "genre"],
        store_fields=["name", "description"],
    )
    request = vectorsearch_v1.CreateIndexRequest(
        parent=f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/{COLLECTION_ID}",
        index_id=f"idx-{index_field.replace('_', '-')}",
        index=index,
    )
    
    # Make the request
    return client.create_index(
        request=request,
        retry=custom_retry,
        timeout=60.0  # 개별 RPC 요청의 타임아웃
        )

operation = create_index(vector_search_service_client, "text_embedding")
while operation.done() == False:
    time.sleep(1)
print(f"Text embedding index created at {datetime.now()}")
time.sleep(30)

operation = create_index(vector_search_service_client, "image_embedding")
while operation.done() == False:
    time.sleep(1)
print(f"Image embedding index created at {datetime.now()}")
time.sleep(30)