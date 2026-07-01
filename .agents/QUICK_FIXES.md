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

## 12. Vector Search 2.0 SearchResult Score Attribute Name Mismatch
* **Symptom**: `Vector Search 2.0 API 조회 연산 실패: Unknown field for SearchResult: score`
* **Root Cause**: The protocol buffer response message `SearchResult` for managed Collections uses the attribute name `distance` to return similarity scores. There is no attribute named `score`.
* **Fix**: Change `match.score` to `match.distance` when reading matching scores in Python:
  ```python
  results.append({
      'id': item['id'],
      'score': match.distance,
      ...
  })
  ```

## 13. Index Alignment Mismatch in BM25 Sparse Index and Sub-filtered Registries
* **Symptom**: `ValueError: operands could not be broadcast together with shapes (A,) (B,)` during hybrid search scoring.
* **Root Cause**: Swapping or sub-filtering the global `combined_registry` variables (e.g. to isolate video chunks) before calling `combined_hybrid_search` breaks the index mapping alignment with `combined_bm25` (which was built on the entire registry size). This causes dense similarity scoring list size to differ from the sparse scoring array size, leading to numpy broadcasting shape mismatch errors.
* **Fix**: Perform `combined_hybrid_search` on the full registry normally to get raw candidates first, and then filter/extract target media types (like video chunks) POST-search:
  ```python
  raw_results = combined_hybrid_search(query, alpha=alpha, top_k=200)
  video_results = [r for r in raw_results if r['item']['type'] == 'video_chunk'][:top_k]
  ```

## 14. Pydantic Extra Forbidden Validation Error for audio_track_extraction
* **Symptom**: `1 validation error for EmbedContentConfig \n audio_track_extraction \n Extra inputs are not permitted [type=extra_forbidden]`
* **Root Cause**: The active Jupyter kernel has an older version of `google-genai` pre-installed (which did not define `audio_track_extraction` in `EmbedContentConfig`). Because pip install was called without `-U` (upgrade flag), pip skipped upgrading the pre-installed old SDK version.
* **Fix**: Add the `-U` or `--upgrade` flag to the pip install command in **Cell 2** to force-upgrade the packages:
  ```python
  %pip install -U google-genai google-cloud-vectorsearch ...
  ```
  Run the install cell again, which will automatically restart the kernel to load the latest packages.

## 15. audio_track_extraction API Mode Auth Restriction
* **Symptom**: `임베딩 생성 실패: audio_track_extraction parameter is only supported in Gemini Enterprise Agent Platform mode, not in Gemini Developer API mode.`
* **Root Cause**: The `audio_track_extraction` option (which extracts and embeds the audio track of video files) is a Vertex AI-exclusive enterprise feature. It is **not supported** by the Gemini Developer API (Google AI Studio) when initialized with an API key (`Client(api_key=...)`).
* **Fix**: Remove the `audio_track_extraction` configuration from `EmbedContentConfig` to use the default visual-only video embedding mode when running under AI Studio API key context:
  ```python
  # Revert to standard call without config
  response = client.models.embed_content(
      model='gemini-embedding-2',
      contents=contents
  )
  ```





## 16. Developer API GCS Authentication Restriction (Part.from_uri vs Part.from_bytes)
* **Symptom**: `InvalidArgument: 400 Google Cloud Storage URIs are only supported for Service Account authentication.`
* **Root Cause**: The modern Google GenAI SDK's `Part.from_uri()` with `gs://` paths expects GCP authentication credentials (e.g. Service Account). It is rejected when calling the Gemini Developer API (Google AI Studio) via a developer API key.
* **Fix**: Detect `gs://` paths, download the file locally to memory bytes using the Google Cloud Storage client, and wrap it using `types.Part.from_bytes()`:
  ```python
  from google.cloud import storage
  storage_client = storage.Client()
  # Download gs:// bucket/path to bytes
  image_bytes = blob.download_as_bytes()
  contents = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
  ```

## 17. BatchDeleteDataObjectsRequest Parameter Mismatch
* **Symptom**: `AttributeError: Unknown field for BatchDeleteDataObjectsRequest: data_object_ids`
* **Root Cause**: The serverless collections `BatchDeleteDataObjectsRequest` message expects a field named `requests` (a list of individual `DeleteDataObjectRequest` objects), not a direct flat list of ID strings.
* **Fix**: Map the IDs to individual `DeleteDataObjectRequest` objects, then feed them to the `requests` parameter:
  ```python
  delete_reqs = [
      vectorsearch.DeleteDataObjectRequest(name=f"{collection_name}/dataObjects/{dp_id}")
      for dp_id in packet
  ]
  req = vectorsearch.BatchDeleteDataObjectsRequest(parent=collection_name, requests=delete_reqs)
  data_client.batch_delete_data_objects(request=req)
  ```

## 18. Double Printing of Widget Output Logs in Jupyter
* **Symptom**: Console logs and visual galleries inside interactive widget cells are printed twice in the cell output area.
* **Root Cause**: Running widget handler functions synchronously during the cell's initial execution captures stdout twice (once in the cell's standard output stream, and once in the Output widget's local buffer).
* **Fix**: Trigger the initial default search query asynchronously using a background thread timer. This allows the cell to finish execution first, isolating all subsequent prints strictly to the Output widget's local buffer:
  ```python
  import threading
  threading.Timer(0.1, lambda: on_search_clicked(None)).start()
  ```

## 19. Schema Mismatch in Local Metadata vs Precomputed Pickle Registry
* **Symptom**: `표시할 수 있는 매칭 결과가 없습니다.` or missing fields error when rendering local search results.
* **Root Cause**: Local chunk metadata (Part 1) uses keys like `'file_path'` and `'chunk_id'`, while the precomputed registry (Part 2) uses `'path'` and `'id'`.
* **Fix**: Use safe dictionary `.get()` fallback lookups to support both schemas:
  ```python
  path = item.get('path', item.get('file_path', ''))
  item_id = str(item.get('id', item.get('chunk_id', '')))
  media_type = item.get('type', 'video_chunk')
  ```

## 20. FileNotFoundError for Precomputed Video Chunks
* **Symptom**: `FileNotFoundError: [Errno 2] No such file or directory` or `[미디어 파일 없음]` when trying to play precomputed video chunks.
* **Root Cause**: The paths inside `full_dataset_registry.pkl` point to relative server directories that do not exist on the user's local filesystem.
* **Fix**: Implement a 3-step hierarchical fallback path resolution:
  1. Try original path as written.
  2. If video_chunk, check if `./local_chunks/chunk_{index}.mp4` exists.
  3. If missing locally, construct the remote GCS public path and download the bytes: `gs://ai-multimodal-data/vid-chunks/{video_filename}_chunks/chunk_{idx}.mp4`.

## 21. LRO (Long Running Operation) Tracking for Collection Deletion
* **Symptom**: Deleting a serverless collection returns immediately with `'done': False`, leaving the deletion running silently in the background.
* **Root Cause**: Resource deletion is asynchronous. If students immediately run subsequent cells, they will encounter resource conflict or quota errors.
* **Fix**: Poll the REST operation endpoint until the status is returned as `'done': True`:
  ```python
  poll_url = f"https://vectorsearch.googleapis.com/v1beta/{operation_name}"
  while True:
      poll_resp = requests.get(poll_url, headers=headers).json()
      if poll_resp.get('done', False):
          break
      time.sleep(5)
  ```

## 22. Concurrent Widget Event Execution Race Condition (Double Triggering)
* **Symptom**: When loading the cell or clicking search buttons, logs and visual rows are printed twice, with the logs interleaving and one block starting before the first one completes.
* **Root Cause**: Since API calls (like Reranker or Vector Search) block the thread, triggering a new event (e.g. clicking the button before initial cell-load thread finishes) runs the handler concurrently in another thread. Both threads write to the same output area, creating duplicate, messy output logs.
* **Fix**: Introduce a boolean busy flag (`is_searching = False`) as a lock. Guard the handler execution to ignore any incoming calls while the active operation is running:
  ```python
  is_searching = False
  def on_click(b):
      global is_searching
      if is_searching:
          return
      is_searching = True
      try:
          # perform API calls
      finally:
          is_searching = False
  ```

## 23. Jupyter Kernel OOM Crash on Displaying Large Full-Length Videos
* **Symptom**: Clicking the "Shuffle Gallery Query" button occasionally causes the entire Jupyter page to refresh, losing state and reverting the dashboard output area to the default "red" search query results.
* **Root Cause**: The shuffle selector randomly picked items from the entire `combined_registry`. If a full-length video file (like `Eurasia_KBS_130903.mp4` or `newyork_trip_KBS_170218.mp4`, which are 600MB+ in size) was selected, the backend tried to download the entire file and base64 encode it in memory. This exceeded the Jupyter message size limits and exhausted the python memory pool, triggering an Out-Of-Memory (OOM) crash that restarted the kernel and reset the notebook outputs.
* **Fix**: Filter the candidate pool in the shuffle function to exclude large full-length video objects, only choosing images (`type == 'image'`) or small 10s video chunks (`type == 'video_chunk'`):
  ```python
  valid_shuffle_items = [item for item in combined_registry if item['type'] in ['image', 'video_chunk']]
  random_item = random.choice(valid_shuffle_items)
  ```

## 24. KeyError: 'description' in Local Search Trigger before Caption Generation
* **Symptom**: `KeyError: 'description'` when running interactive search queries on local chunks in Cell 22.
* **Root Cause**: The local chunk metadata dictionary created during the initial FFmpeg chunking (Step 1) does not contain a `'description'` key until Step 2 (LLM description generation) is run. If students run searches before Step 2, reading `'description'` directly raises a KeyError.
* **Fix**: Use `.get('description', ...)` to return a safe placeholder string if the caption has not been generated yet:
  ```python
  print(f"청크 상세 설명: {chunk.get('description', '아직 상세 설명이 생성되지 않은 시점입니다.')}")
  ```

## 25. Jupyter Kernel OOM Crash on Displaying Large Search Result Videos
* **Symptom**: Searching or shuffling in the dashboard UI triggers a kernel crash and resets the output area.
* **Root Cause**: Although the shuffle query was filtered, the search results returned by `find_similar_content` could still contain objects of type `'video'` (full-length video files of 150MB+). When `display_media_results` attempted to download and Base64-encode these full videos, the memory spike crashed the Jupyter kernel.
* **Fix**: Restrict the dashboard media player rendering to strictly accept `type == 'video_chunk'` objects (10s segments of 1~3MB) and exclude full-length `type == 'video'` files:
  ```python
  videos = [res for res in deduped_results if res['type'] == 'video_chunk']
  ```

## 26. Architectural Notes & Noteworthy Code Rationales
* **GCS Regional Location Constraints**:
  - GCS buckets do not support `global` as a location. Always use valid regional locations (e.g. `us-central1` or other GCP regions) when provisioning GCS assets, even if Vector Search configurations leverage global configurations.
* **v1beta API Version for Modern API Keys**:
  - When initializing the modern GenAI client with keys starting with the modern `AQ.` prefix, always specify `http_options={'api_version': 'v1beta'}` in the `Client()` initialization block to guarantee API key authentication compatibility.
* **Lexicographical Paging Cutoffs in GCS list_blobs()**:
  - Because Google Cloud Storage lists blobs in alphabetical/lexicographical order, setting a low safety limit (e.g. `max_results=1000`) can cut off lists before reaching files starting with later letters (like `n`, `p`, or `v`). Always raise the limit to cover the expected bucket size (e.g. `max_results=10000`) or filter prefix-wise.
* **Bypassing Workbench/Colab Hardware Driver Crashes with FFmpeg Segment Muxing**:
  - Re-encoding video files using default hardware encoders in Colab or Workbench VPC setups often causes hardware driver failures (e.g. `h264_v4l2m2m`). Using FFmpeg segment copier (`-c copy`) copies raw H.264 video and AAC audio streams directly without re-encoding, avoiding driver crashes and completing in milliseconds.
* **AI Studio Developer API Key GCS Reading Restriction**:
  - Developer API keys cannot authenticate GCS bucket reads natively via `Part.from_uri()`. Download GCS blobs locally to memory bytes using the GCP Storage client, and wrap them using `types.Part.from_bytes()` to keep it compatible with Google AI Studio.
