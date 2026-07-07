# Track 1: Scaling AI Agents
-   https://github.com/cheeunlim/aifb-track1

![image](https://raw.githubusercontent.com/jk1333/handson/main/images/7/0.jpg)

## Project Structure

폴더 구조는 아래와 같습니다:

```
aifb-track1/
├── session1/                   # Session 1 실습자료
├── session2/                   # Session 2 실습자료
├── install.sh                  # 실습 환경 프로비져닝 스크립트
├── session2_index_builder.sh   # 실습 환경 프로비져닝 스크립트
└── README.md                   # Workshop 개요
```

## Qwiklab 실습 준비를 위한 Gemini API Key 확인

#### 1. Gemini API Key 확인을 위해 메뉴에서 credential 검색 후 메뉴로 진입합니다.
![image](https://raw.githubusercontent.com/jk1333/handson/main/images/7/1.png)

#### 2. 기 생성돼 있는 GeminiLabKey 를 확인 후 Show key 를 눌러 값을 확인, 값을 복사해 둡니다.
![image](https://raw.githubusercontent.com/jk1333/handson/main/images/7/2.png)

<h3><ins>이 키는 Session1 과 Session2 에서 동일하게 이용합니다.</ins></h3>

<br>

## Qwiklab 실습 준비를 위한 Workbench 실행 및 실습자료 다운로드

#### 3. 상단 검색 메뉴에서 'workbench' 를 입력하여 'Workbench' 메뉴를 클릭합니다.
![image](https://raw.githubusercontent.com/jk1333/handson/main/images/6/1.png)

#### 4. 'Open Jupyterlab' 버튼을 눌러 환경에 접속합니다.
![image](https://raw.githubusercontent.com/cheeunlim/agent-engine-lab/main/images/workbench_open.png)

실행된 Jupyterlab 환경에서 Terminal에 진입 후 아래 명령어를 실행해 실습자료를 다운로드 받습니다.

```
git clone https://github.com/cheeunlim/aifb-track1
```

아래의 명령어를 실행하여 추가로 필요한 리소스를 설치합니다. 

`install.sh` 스크립트는 백그라운드에서 다음 4가지 작업을 순차적으로 수행합니다:
1. **필수 파이썬 패키지 설치**: `google-cloud-vectorsearch` 등 필수 라이브러리 설치 및 업그레이드
2. **GCS 버킷 생성**: `asia-northeast1` 리전에 `gs://${PROJECT_ID}-vs2` 이름으로 버킷 생성
3. **실습 데이터 복사**: 샘플 상품 임베딩 데이터셋(`amazon-product-dataset-768-compact.jsonl`)을 생성한 버킷 내 `data/` 경로로 복사
4. **인덱스 빌더 구동**: 백그라운드에서 `session2_index_builder.py` 스크립트를 구동하여 Google Cloud Vector Search 컬렉션 및 인덱스 빌드 작업 실행

최소 20분의 시간이 필요하며 이 시간동안 세션1 강의가 진행됩니다.

```
cd ~/aifb-track1
chmod +x ./install.sh
./install.sh
```

## Qwiklab 실습 준비 완료!

<br>

## 세션1: 오후 1시 30분 - 오후 3시 30분
### [`Gemini Embedding 2 & Vector Search 2 기반 크로스 모달(Cross-Modal) 검색 엔진 개발`](https://github.com/cheeunlim/aifb-track1/tree/main/session1)

<br>

## 세션2: 오후 3시 30분 - 오후 5시 00분
### [`Gemini Live API와 크로스 모달(Cross-Modal) 검색 엔진을 결합한 실시간 대화형 멀티모달 쇼핑 에이전트 개발`](https://github.com/cheeunlim/aifb-track1/tree/main/session2)

<br>

### 참고 : 세션2 실습 시작 전 백그라운드 작업 상태 점검

`install.sh` 실행으로 시작된 백그라운드 비동기 작업(Long running job)들의 진행 상태는 아래 명령어로 확인할 수 있습니다.

```bash
gcloud vector-search operations list --location=asia-northeast1
```

명령어 실행 결과로 나타나는 작업 목록의 출력 예시는 다음과 같습니다.

**출력 예시**:
```yaml
---
done: true
metadata:
  '@type': type.googleapis.com/google.cloud.vectorsearch.v1.ImportDataObjectsMetadata
  createTime: '2026-07-07T06:03:02.159943428Z'
name: projects/qwiklabs-gcp-03-80bd6b7713ab/locations/asia-northeast1/operations/operation-1783404182017-655ff24c29591-5d55b3eb-0215e08c
---
metadata:
  '@type': type.googleapis.com/google.cloud.vectorsearch.v1beta.OperationMetadata
  apiVersion: v1beta
  createTime: '2026-07-07T07:26:59.192854721Z'
  requestedCancellation: false
  target: projects/qwiklabs-gcp-03-80bd6b7713ab/locations/asia-northeast1/collections/amazon-product-768-compact/indexes/idx-text-embedding
  verb: create
name: projects/qwiklabs-gcp-03-80bd6b7713ab/locations/asia-northeast1/operations/operation-1783409218856-6560050faa6fd-28a4311e-5661eba3
---
...
```


1. **완료 상태 확인**: 
   - `done: true`가 표시된 항목은 완료된 작업입니다. 진행 중인 작업은 `done` 필드가 나타나지 않으며, 상세 확인은 `describe` 명령어를 사용합니다.
2. **작업 상세 조회 (describe)**:
   - 각 작업 항목의 `name:` 필드에 명시된 전체 경로를 지정하여 상세 조회가 가능합니다.
   ```bash
   gcloud vector-search operations describe <OPERATION_NAME>
   ```
   - **예시**: `gcloud vector-search operations describe projects/qwiklabs-gcp-03-80bd6b7713ab/locations/asia-northeast1/operations/operation-1783409218856-6560050faa6fd-28a4311e-5661eba3`
3. **세션2 실습 진행을 위한 최소 완료 조건 및 소요 시간**:
   - `install.sh` 실행 시 총 4개의 백그라운드 작업이 순차적으로 진행됩니다.
   - **실습 진행 가능 기준**: **1번(컬렉션 생성)과 2번(데이터 임포트) 작업만 완료(`done: true`)되면 세션2 실습을 바로 진행**할 수 있습니다. (생성 소요 시간: 약 20분)
   - **4단계 작업 흐름**:
     1. **컬렉션 생성** (Create Collection): target 경로가 `.../collections/amazon-product-768-compact`인 작업 (**세션2 실습 시작전 완료 필수**)
     2. **데이터 임포트** (Import Data): metadata type이 `...ImportDataObjectsMetadata`인 작업 (**세션2 실습 시작전 완료 필수**)
     3. **이미지 임베딩 인덱스 생성** (Create Index): target 경로가 `.../indexes/idx-image-embedding`인 작업 
     4. **텍스트 임베딩 인덱스 생성** (Create Index): target 경로가 `.../indexes/idx-text-embedding`인 작업

