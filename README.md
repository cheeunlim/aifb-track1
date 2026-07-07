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

최소 20분의 시간이 필요하며 이 시간동안 강의가 진행됩니다.

```
cd ~/aifb-track1
chmod +x ./install.sh
./install.sh
```

아래 명령어를 Terminal 에서 실행하면 Long running job(인덱스 생성, 데이터 임포트 등)의 상태를 확인할 수 있습니다.
```bash
gcloud vector-search operations list --location=asia-northeast1
```

### 작업 상태 출력 결과 이해하기

`list` 명령을 실행하면 생성된 비동기 작업(Operation)들의 목록이 아래와 같이 출력됩니다.

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
   - 각 작업 정보 중 `done: true`로 표시된 것은 작업이 완료되었음을 의미합니다.
   - 아직 진행 중인 작업은 `list` 출력 결과에서 `done: true` 필드가 나타나지 않고 생략됩니다 (상세 조회인 `describe` 명령어 실행 시에는 `done: false`로 표시됩니다).
2. **작업 종류 (verb)**:
   - `verb: create`는 인덱스나 컬렉션 생성 작업을 뜻합니다.
3. **상세 정보 조회 (describe)**:
   - 특정 작업의 상세 내용(진행 중인 작업의 완료 상태 등)을 확인하려면 `describe` 명령 뒤에 `operations list` 결과의 **`name` 필드에 명시된 전체 경로**(`projects/.../operations/...`)를 지정하여 실행합니다.
   - **명령어**: `gcloud vector-search operations describe <OPERATION_NAME>`
   - **예시** (`list` 결과에서 `name` 필드 값을 복사해 사용):
     ```bash
     gcloud vector-search operations describe projects/qwiklabs-gcp-03-80bd6b7713ab/locations/asia-northeast1/operations/operation-1783404860135-655ff4d2dd7b1-f926234a-de3ac43b
     ```
4. **총 완료되어야 하는 작업 개수**:
   - `install.sh` 실행 시 백그라운드에서 진행되는 작업은 **총 4개**의 비동기 작업(Operation)으로 구성되어 있습니다.
   - `gcloud vector-search operations list` 실행 시 이 4개 작업의 상태가 모두 **`done: true`**로 나타나야 실습 환경 구성이 완전히 완료된 것입니다.
   - **4단계 작업 구성**:
     1. **컬렉션 생성** (Create Collection): `verb: create` (target: `.../collections/amazon-product-768-compact`)
     2. **데이터 임포트** (Import Data): metadata type이 `...ImportDataObjectsMetadata`인 작업
     3. **이미지 임베딩 인덱스 생성** (Create Index): `verb: create` (target: `.../indexes/idx-image-embedding`)
     4. **텍스트 임베딩 인덱스 생성** (Create Index): `verb: create` (target: `.../indexes/idx-text-embedding`)



## Qwiklab 실습 준비 완료!

<br>

## 세션1: 오후 1시 30분 - 오후 3시 30분
### [`Gemini Embedding 2 & Vector Search 2 기반 크로스 모달(Cross-Modal) 검색 엔진 개발`](https://github.com/cheeunlim/aifb-track1/tree/main/session1)

<br>

## 세션2: 오후 3시 30분 - 오후 5시 00분
### [`Gemini Live API와 크로스 모달(Cross-Modal) 검색 엔진을 결합한 실시간 대화형 멀티모달 쇼핑 에이전트 개발`](https://github.com/cheeunlim/aifb-track1/tree/main/session2)

<br>