# **Gemini Embedding 2 및 Vector Search 2.0을 이용한 멀티모달 미디어 검색**
이 프로젝트는 최신 **Google GenAI SDK (`google-genai`)**와 **Vertex AI Vector Search 2.0 (Serverless Collections)**을 활용하여 텍스트, 이미지, 오디오 및 장편 동영상이 어우러진 진정한 엔터프라이즈급 크로스 모달(Cross-Modal) 하이브리드 검색 시스템을 구축하는 실습 과정입니다. 

GCP Workbench 환경에서 바로 동작 가능한 노트북 형식에 최적화되었습니다.

---

## **실습 파일**
*   **실습 노트북**: [multimodal_search_v2.ipynb](multimodal_search_v2.ipynb)

---

## **워크플로우 개요 및 아키텍처**
총 7단계의 실습 모듈을 통해 기초 전처리부터 최첨단 검색 최적화 기술까지 단계별로 고도화합니다.

### **1단계: 환경 설정 및 인증**
최신 `google-genai` 클라이언트를 구성하고 Gemini API 키 검증 단계를 거칩니다. 실습자별 고유 GCS 출력 버킷을 생성합니다.

### **2단계: 비디오 전처리 및 고속 청킹**
**FFmpeg Segment Copy (`-c copy`)** 방식으로 오디오를 10초 세그먼트로 자동 분할 후 GCS에 업로드합니다. (노트북 1단계)

### **3단계: 로컬 하이브리드 검색 및 t-SNE 분석**
로컬 인메모리 **SimpleBM25** 모델을 구축해 하이브리드 검색 시뮬레이터를 우선 가동합니다. `gemini-embedding-2` 밀집 벡터와 `gemini-3.5-flash`가 생성한 청크 묘사 텍스트를 연동하여 가중치 제어 실험을 진행하고, 시간 축에 따른 비디오 흐름 궤적(t-SNE Trajectory)을 동적 화살표 차트로 시각화합니다. (노트북 2단계)

### **4단계: 검색 결과 최적화 단계**
시맨틱 검색 결과의 비즈니스 현실성을 극대화하기 위해 두 가지 상용 최적화 기법을 도입합니다: (노트북 3단계)
1.  **비디오 크라우딩 방지 (Video Crowding Mitigation)**: 특정 영상의 중복 청크 도배를 막고 다양한 비디오 출처를 확보하는 필터.
2.  **Vertex AI Ranking API 리랭커**: 후보군 랭킹을 고도화된 정렬 알고리즘으로 즉각 재점수화하는 리랭킹 파이프라인.

### **5단계: 벡터 검색 상용화 구현**
서버리스 컬렉션(`multimodal-media-collection`)을 프로비저닝하고, 정비된 임베딩 데이터셋을 멀티쓰레딩 배치 방식으로 대량 동시 업서트(Upsert) 처리합니다. (노트북 4단계)

### **6단계: 인터랙티브 하이브리드 검색 대시보드**
`ipywidgets`를 활용하여 텍스트 입력뿐만 아니라 이미지, 동영상, 오디오 파일 업로드 쿼리를 모두 수용하는 통합 대시보드를 생성합니다. 알파 슬라이더를 조절하며 실시간으로 Dense와 Sparse 가중치 변화가 검색 결과에 미치는 시각적 변화를 탐색합니다. (노트북 5단계)

### **7단계: 자원 해제 및 정리**
실습이 끝난 후 불필요한 과금 방지를 위해 gcloud 인증 토큰을 동적으로 발행하여 Vector Search 컬렉션을 즉시 안전하게 파괴(Force Delete)해주는 자동 스크립트를 수록했습니다. (노트북 6단계)

---

## **주요 기술 및 스택**
*   **Google GenAI Client SDK**: `google-genai`
*   **Vertex AI Vector Search 2.0**: 서버리스 컬렉션 (10ms 미만 지연 시간의 매니지드 KNN/ANN DB)
*   **Vertex AI Ranking API**: 매니지드 리랭킹 엔진 (`google-cloud-discoveryengine`)
*   **FFmpeg Muxer**: 고속 스트림 복사, 무손실 오디오 분할
*   **IPyWidgets**: 노트북 내 GUI 대시보드 렌더링
*   **SimpleBM25**: 인메모리 파이썬 하이브리드 검색 시뮬레이터

---

## **사용 방법 및 팁**
1.  **노트북 실행**: `multimodal_search_v2.ipynb` 파일을 GCP Workbench 또는 Jupyter 환경에서 엽니다.
2.  **API 키 구성**: Cell 3에 Google AI Studio에서 가져온 Gemini API 키를 입력합니다.
3.  **가속 꿀팁 (Lifeline Fallback)**: API 할당량 제한이나 전처리 시간 단축을 위해 Cell 23에서 미리 생성되어 공개 배포된 `https://storage.googleapis.com/ai-multimodal-data/full_dataset_registry.pkl` 레지스트리를 다운받아 실습을 진행할 수 있습니다.

---

> [!WARNING]
> 실습 완료 후 불필요한 과금 방지를 위해 반드시 **노트북 6단계 (Cell 41) 자원 정리** 스크립트를 마지막으로 구동하여 서버리스 컬렉션을 삭제합니다.

<br><br>
<hr>
<br><br>

# **Cross-Modal Search Engine with Gemini Embedding 2 & Vector Search 2.0**
This project demonstrates how to build an enterprise-grade cross-modal hybrid retrieval system using the modern **Google GenAI SDK (`google-genai`)** and **Vertex AI Vector Search 2.0 (Serverless Collections)**. It handles mixed-modality queries across text, images, audio, and long-form videos.

Optimized as a highly reusable hands-on lab asset designed for **GCP Workbench** and similar cloud notebook environments.

---

## **Active Files**
*   **Active Notebook**: [multimodal_search_v2.ipynb](multimodal_search_v2.ipynb)

---

## **Workflow Overview & Architecture**
The lab consists of 7 core modules (including the 6 phases in the notebook), guiding you from basic preprocessing to advanced search optimization techniques.

### **Phase 1: Setup & Authentication**
Initialize the modern `google-genai` SDK and automatically detect and provision dedicated GCS output buckets.

### **Phase 2: Video Preprocessing & High-Speed Chunking**
Utilize high-performance **FFmpeg segment copy (`-c copy`)** via Python `subprocess`. Split videos into 10-second segments and sync directory paths directly to GCS. (Notebook Phase 1)

### **Phase 3: Local Hybrid Search & t-SNE Trajectory**
Build a custom in-memory **SimpleBM25** sparse index in Python to run a hybrid search simulator instantly without waiting for cloud DB deployment. Generate dense vectors using `gemini-embedding-2` and descriptions via `gemini-3.5-flash`. Visualize chronological video scene shifts (t-SNE Trajectories) with dynamic arrow plots. (Notebook Phase 2)

### **Phase 4: Post-Search Optimization**
Apply professional enterprise-grade search engineering to fine-tune results: (Notebook Phase 3)
1.  **Video Crowding Mitigation Filter**: Prevents a single video source from dominating top ranks by limiting consecutive chunks.
2.  **Vertex AI Ranking API Reranker**: Rescores initial retrieval candidates through a managed cross-encoder LLM reranking pipeline.

### **Phase 5: Vertex AI Vector Search 2.0**
Provision a serverless Vertex AI Vector Search Collection (`multimodal-media-collection`). Perform concurrent batch upserts of multi-modal embedding data objects using multithreading. (Notebook Phase 4)

### **Phase 6: Interactive Search Dashboard**
Create an interactive search GUI inside Jupyter using `ipywidgets`. It accepts text inputs, live media file uploads, or random library shuffles, rendering HBox image displays and video players alongside live-updating Alpha parameter sliders. (Notebook Phase 5)

### **Phase 7: Clean-up & Destruction**
Execute a secure clean-up script to force-delete the serverless collection via a REST request, preventing accidental charges. (Notebook Phase 6)

---

## **Key Technologies & Stack**
*   **Google GenAI Client SDK**: `google-genai`
*   **Vertex AI Vector Search 2.0**: Serverless Collections (Sub-10ms managed KNN/ANN DB)
*   **Vertex AI Ranking API**: Managed Reranking engine (`google-cloud-discoveryengine`)
*   **FFmpeg Muxer**: High-speed streams copy and lossless audio segmenting
*   **IPyWidgets**: Live in-notebook GUI dashboard rendering
*   **SimpleBM25**: In-memory Python keyword-sparse simulator

---

## **Usage & Acceleration Tips**
1.  **Launch**: Open `multimodal_search_v2.ipynb` in GCP Workbench or Colab.
2.  **API Key Setup**: Add your Gemini API key inside Cell 3.
3.  **Acceleration Hack**: Skip heavy extraction times by leveraging the pre-computed registry fallback in Cell 23.

---

> [!WARNING]
> Always ensure you run the final **Notebook Phase 6 / README Phase 7 (Cell 41) resource cleanup** block to prevent any ongoing serverless database provisioning charges.
