# Gemini Live, Gemini Embedding 2 및 Vector Search 2.0 를 이용한 쇼핑 에이전트
-   https://github.com/cheeunlim/aifb-track1/session2

본 예제는 ['LensMosaic'](https://github.com/kazunori279/lens-mosaic/tree/main)를 기반으로 합니다.

상품 데이터는 ['Amazon Berkeley Objects'](https://amazon-berkeley-objects.s3.amazonaws.com/index.html)를 이용합니다.

## Project Structure

폴더 구조는 아래와 같습니다:

```
multimodal-agent/
├── app/                        # Core agent code
│   ├── main.py                 # Main agent logic
│   ├── prompt.py               # Prompt definition
│   ├── common.py               # Configurations
│   ├── embedding_vector.py     # Utilities for Gemini Embedding 2 and Vector Search 2
│   ├── session.py              # Utilities for session
│   └── static/                 # Frontend application
├── test/                       # Unit, integration, and load tests
├── products_data.ipynb         # Products data pre processor
├── vs2_indexer.ipynb           # Products data indexer for Vector Search 2
├── qr.py                       # QR code generator
├── download_agent_card.py      # Utility for downloading agent card
├── Dockerfile                  # Development commands
└── pyproject.toml              # Project dependencies
```

## Qwiklab 실습

## 실습 Part 1: 상품 DB 생성 (약 20분 소요)

#### 1. 실습 자료의 /aifb-track1/session2/vs2_indexer.ipynb 를 클릭합니다.

#### 2. `첫번째 셀`을 선택 후 (Ctrl + Enter 혹은 메뉴의 Run -> Run Selected Cell) 실행 후 완료될 때 까지 기다립니다. 커널 재시작 팝업이 뜬 이후 Run -> Run All Cells 를 실행합니다.

아래 명령어를 Terminal 에서 실행하면 Long running job 의 상태를 확인할 수 있습니다.
```
gcloud vector-search operations list --location=asia-southeast1
```

## 실습 Part 2: Application 배포 (약 5분 소요)

#### 3. 아래의 명령어를 이용해 Agent 를 Cloud Run 에 배포합니다. -----GEMINI_API_KEY----- 부분을 기록해둔 Key로 교체합니다. (Y/n) 선택이 나오면 엔터를 입력 합니다.
```
cd multimodal-agent
gcloud run deploy lens-mosaic --source . --region "asia-southeast1" --set-env-vars GEMINI_API_KEY="-----GEMINI_API_KEY-----" --concurrency 500 --cpu 2 --memory 4Gi --timeout 3600 --min-instances 1 --max-instances 1 --execution-environment=gen2
```

#### 4. Cloud Run 이 배포되면 메뉴에서 cloud run 검색, lens-mosaic 클릭 후 Security 탭에서 Authentication -> Allow public access 를 클릭 후 Save를 클릭합니다.

![image](https://raw.githubusercontent.com/jk1333/handson/main/images/7/3.png)
![image](https://raw.githubusercontent.com/jk1333/handson/main/images/7/4.png)
![image](https://raw.githubusercontent.com/jk1333/handson/main/images/7/5.png)
![image](https://raw.githubusercontent.com/jk1333/handson/main/images/7/6.png)

## 실습 Part 3
#### 8. 열려있는 Cloud Run 의 lens-mosaic 서비스에서 URL 의 주소값을 복사합니다. (URL 끝에 복사 버튼을 누르면 됩니다.) 복사 후 아래의 명령어에 -------CLOUD RUN URL------- 을 교체 후 실행합니다.
```
pip install qrcode
python qr.py -------CLOUD RUN URL-------
```

#### 9. 생성된 my_qrcode.png 파일을 연 후 모바일의 카메라로 인식하여 Agent를 실행합니다.

## 실습 Part 4

#### 10. A2A 를 위한 Agent Card를 생성합니다.
```
python download_agent_card.py -------CLOUD RUN URL-------
```

#### 11. 다음의 명령어를 이용해 Agent 를 Agent Registry에 등록합니다.
```
gcloud alpha agent-registry services create lens-mosaic --location=global --display-name="LensMosaic" --agent-spec-type=a2a-agent-card --agent-spec-content=agent-card.json
```

#### 12. 다음의 명령어를 이용해 등록된 Agent가 검색되는지 확인합니다.
```
gcloud alpha agent-registry agents search --location=global --search-string="쇼핑"
```

## Qwiklab 실습 완료!