# Workshop Error & Quick Fix Registry 🐛➡️✅

This file serves as an AI-readable index of historical bugs, library dependency collisions, and SDK deprecation adjustments encountered during the workshop environment setup. 

---

## 1. Jupyter Environment Key Caching Issue
* **Symptom**: Updating the API key in a notebook cell still outputs `API key not valid` on downstream calls.
* **Root Cause**: Jupyter kernels cache OS environment variables. Re-assigning `%env` sometimes fails to clear cached credentials in the running Python wrapper.
* **Fix**: Force key setting via Python's standard `os.environ` module directly, followed by a Kernel restart:
  ```python
  import os
  os.environ["GEMINI_API_KEY"] = "your_key"
  ```

## 2. scikit-learn t-SNE Parameter Deprecation (`max_iter` vs `n_iter`)
* **Symptom**: `TypeError: TSNE.__init__() got an unexpected keyword argument 'n_iter'`
* **Root Cause**: In `scikit-learn` v1.6+, the `n_iter` parameter was deprecated and removed in favor of `max_iter`.
* **Fix**: Dynamically inspect the `TSNE` constructor signature to feed the correct argument:
  ```python
  import inspect
  tsne_params = inspect.signature(TSNE.__init__).parameters
  tsne_kwargs = {"n_components": 2, "perplexity": perplexity, "random_state": 42}
  if "max_iter" in tsne_params:
      tsne_kwargs["max_iter"] = 1000
  else:
      tsne_kwargs["n_iter"] = 1000
  tsne = TSNE(**tsne_kwargs)
  ```

## 3. Jupyter Namespace Variable Collision (`client` Overwrite)
* **Symptom**: `AttributeError: 'VectorSearchServiceClient' (or 'RankServiceClient') object has no attribute 'models'`
* **Root Cause**: Initializing local clients (e.g. `client = discoveryengine.RankServiceClient()`) overwrites the global `client` variable representing the developer GenAI client (`client = genai.Client()`).
* **Fix**: Use distinct names for local clients inside functions/cells (e.g., `rank_client`, `vector_search_client`) and avoid using generic `client` namespaces.

## 4. Local Function Scoping Bug (`locals()` vs `globals()`)
* **Symptom**: Searching returns `No indexed chunks available` even though `valid_chunks` is populated in the notebook.
* **Root Cause**: Checking `if 'valid_chunks' not in locals()` inside a function body checks local scope. Since `valid_chunks` is defined globally in the notebook, it is not found in `locals()`.
* **Fix**: Swap to `globals()` to verify global variables:
  ```python
  if 'valid_chunks' not in globals() or not valid_chunks:
  ```

## 5. google-cloud-discoveryengine SDK Typo
* **Symptom**: `AttributeError: module 'google.cloud.discoveryengine_v1' has no attribute 'RankRecord'`
* **Root Cause**: The ranking records helper class is named `RankingRecord`, not `RankRecord`.
* **Fix**: Call `discoveryengine.RankingRecord()`.

## 6. Vector Search 2.0 Split Schema Constraint
* **Symptom**: `400 The request was invalid: data_schema and vector_schema cannot both be empty`
* **Root Cause**: The unified `schema` argument in `Collection` is deprecated. Vector Search 2.0 requires splitting metadata into `data_schema` and vector fields into `vector_schema`.
* **Fix**: Provide `data_schema` and `vector_schema` independently:
  ```python
  collection_config = vectorsearch.Collection(
      data_schema=data_schema,
      vector_schema=vector_schema
  )
  ```

## 7. Vector Search 2.0 Collection Name Underscore Constraint
* **Symptom**: 400 Bad Request / invalid resource name format.
* **Root Cause**: Underscores (`_`) are not allowed in Collection IDs. Only letters, numbers, and hyphens (`-`) are permitted.
* **Fix**: Change `multimodal_media_collection` to `multimodal-media-collection`.

## 8. Vector Search 2.0 DataObject Vector Wrapping
* **Symptom**: `Failed to upsert... Parameter to CopyFrom() must be instance of same class: expected <class 'Vector'> got <class 'google.cloud.vectorsearch_v1beta.types.data_object.DenseVector'>`
* **Root Cause**: The `vectors` map values in `DataObject` must be of type `Vector`, not `DenseVector` or `SparseVector` directly.
* **Fix**: Wrap the vector inside `Vector(dense=...)`:
  ```python
  vectors={
      "content_embedding": vectorsearch.Vector(
          dense=vectorsearch.DenseVector(values=embeddings)
      )
  }
  ```

## 9. Vector Search 2.0 Single Query Structure (`SearchDataObjectsRequest`)
* **Symptom**: `Vector Search 2.0 query failed: type object 'SearchDataObjectsRequest' has no attribute 'CombineResultsOptions'`
* **Root Cause**: `CombineResultsOptions` (and the `combine` parameter) are exclusive to `BatchSearchDataObjectsRequest`. For single queries, parameters must be passed directly into `SearchDataObjectsRequest`.
* **Fix**:
  ```python
  request = vectorsearch.SearchDataObjectsRequest(
      parent=collection.name,
      semantic_search=vectorsearch.SemanticSearch(
          search_text=query_input,
          search_field="content_embedding",
          task_type="QUESTION_ANSWERING",
          top_k=top_k
      )
  )
  ```

## 10. ipywidgets FileUpload Value Type Compatibility (v7.x vs v8.x)
* **Symptom**: `AttributeError: 'tuple' object has no attribute 'keys'` when parsing uploaded files.
* **Root Cause**: In ipywidgets 8.x, `FileUpload.value` is a tuple/list of dicts. In v7.x, it is a dictionary keyed by filename.
* **Fix**: Dynamically inspect the type of `upload_button.value`:
  ```python
  if isinstance(uploaded_files, (tuple, list)):
      filename = uploaded_files[0]['name']
      content = uploaded_files[0]['content']
  elif isinstance(uploaded_files, dict):
      filename = list(uploaded_files.keys())[0]
      content = uploaded_files[filename]['content']
  ```

## 11. Vertex AI Workbench VPC Private Routing Routing Blockage
* **Symptom**: Client initialization or search queries hang indefinitely.
* **Root Cause**: Workbench instances inside VPCs block public routing VIPs. Custom routes only resolve regional endpoints (e.g. `us-central1-aiplatform.googleapis.com`) under Private Google Access.
* **Fix**: If VPC Service Control or private routing is enabled, pass regional endpoints to client options:
  ```python
  client_options = {"api_endpoint": f"{REGION}-aiplatform.googleapis.com"}
  client = vectorsearch.VectorSearchServiceClient(client_options=client_options)
  ```
