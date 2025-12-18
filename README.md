# 마켓플레이스 요율 관리 시스템

브랜드별 마켓플레이스 배송비율 및 수수료율을 실시간으로 관리할 수 있는 웹 기반 시스템입니다.

## 주요 기능

- ✅ 마켓플레이스 요율 조회 (브랜드별 필터링)
- ✅ 실시간 요율 추가
- ✅ 실시간 요율 수정
- ✅ 실시간 요율 삭제
- ✅ 통계 대시보드 (총 레코드 수, 브랜드 수, 마켓플레이스 수)
- ✅ 반응형 웹 디자인

## 기술 스택

### Backend
- **FastAPI**: 고성능 Python 웹 프레임워크
- **SQLAlchemy**: ORM (Object-Relational Mapping)
- **PyMySQL**: MySQL 데이터베이스 드라이버
- **Pydantic**: 데이터 검증

### Frontend
- **HTML5/CSS3**: 반응형 UI
- **Vanilla JavaScript**: 클라이언트 사이드 로직
- **Fetch API**: RESTful API 통신

### Database
- **MySQL 8.0**: 관계형 데이터베이스

### Infrastructure
- **Docker & Docker Compose**: 컨테이너화 및 오케스트레이션

## 프로젝트 구조

```
ratesdatapi/
├── backend/
│   ├── main.py              # FastAPI 메인 애플리케이션
│   ├── models.py            # SQLAlchemy 데이터 모델
│   ├── database.py          # 데이터베이스 연결 설정
│   ├── schemas.py           # Pydantic 스키마
│   ├── crud.py              # CRUD 작업
│   ├── requirements.txt     # Python 의존성
│   └── Dockerfile           # Backend 컨테이너 설정
├── frontend/
│   ├── index.html           # 메인 웹 페이지
│   ├── styles.css           # 스타일시트
│   └── app.js               # JavaScript 로직
├── database/
│   ├── init.sql             # 데이터베이스 초기화
│   └── seed.sql             # 샘플 데이터
├── docker-compose.yml       # Docker Compose 설정
├── .env.example             # 환경 변수 예제
└── README.md                # 프로젝트 문서
```

## 빠른 시작

### 사전 요구사항

- Docker 및 Docker Compose 설치
- (선택) Python 3.11+ (로컬 개발 시)

### Docker로 실행하기 (권장)

1. **프로젝트 클론**
```bash
git clone <repository-url>
cd ratesdatapi
```

2. **환경 변수 설정**
```bash
cp .env.example .env
```

3. **Docker Compose로 시작**
```bash
docker-compose up -d
```

4. **서비스 확인**
- Backend API: http://localhost:8000
- API 문서: http://localhost:8000/docs
- Frontend: http://localhost:8000/static/index.html
- MySQL: localhost:3306

### 로컬에서 실행하기

#### MySQL 설정

```bash
# MySQL 실행 및 데이터베이스 생성
mysql -u root -p < database/init.sql
mysql -u root -p < database/seed.sql
```

#### Backend 실행

```bash
cd backend
pip install -r requirements.txt

# 환경 변수 설정
export DATABASE_URL="mysql+pymysql://root:rootpassword@localhost:3306/marketplace_rates"

# 서버 시작
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend 접속

브라우저에서 `frontend/index.html` 파일을 직접 열거나, 간단한 HTTP 서버를 실행:

```bash
cd frontend
python -m http.server 8080
```

그 다음 http://localhost:8080 접속

## API 엔드포인트

### 요율 관리

| 메서드 | 엔드포인트 | 설명 |
|--------|------------|------|
| GET | `/api/rates` | 모든 요율 조회 |
| GET | `/api/rates/{id}` | 특정 요율 조회 |
| GET | `/api/rates/brand/{brand}` | 브랜드별 요율 조회 |
| POST | `/api/rates` | 새 요율 생성 |
| PUT | `/api/rates/{id}` | 요율 수정 |
| DELETE | `/api/rates/{id}` | 요율 삭제 |
| GET | `/api/brands` | 모든 브랜드 목록 |
| GET | `/api/marketplaces` | 모든 마켓플레이스 목록 |

### 요청/응답 예제

#### 요율 생성 (POST /api/rates)

**요청:**
```json
{
  "brand": "닥터시드_국내",
  "marketplace": "11번가",
  "shipping": 0.10,
  "commission": 0.11
}
```

**응답:**
```json
{
  "id": 1,
  "brand": "닥터시드_국내",
  "marketplace": "11번가",
  "shipping": 0.10,
  "commission": 0.11,
  "created_at": "2025-12-18T00:00:00",
  "updated_at": "2025-12-18T00:00:00"
}
```

#### 요율 수정 (PUT /api/rates/{id})

**요청:**
```json
{
  "shipping": 0.12,
  "commission": 0.13
}
```

## 데이터베이스 스키마

### marketplace_rates 테이블

| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INT | 기본 키 (자동 증가) |
| brand | VARCHAR(100) | 브랜드명 |
| marketplace | VARCHAR(100) | 마켓플레이스명 |
| shipping | FLOAT | 배송비율 (0-1) |
| commission | FLOAT | 수수료율 (0-1) |
| created_at | TIMESTAMP | 생성 일시 |
| updated_at | TIMESTAMP | 수정 일시 |

**제약 조건:**
- `(brand, marketplace)` 조합은 유일해야 함 (UNIQUE)
- `brand`, `marketplace`에 인덱스 적용

## 샘플 데이터

시스템에는 4개 브랜드의 초기 데이터가 포함되어 있습니다:

- 닥터시드_국내
- 딸로_국내
- 테르스_국내
- 에이더_국내

각 브랜드는 26개의 마켓플레이스 요율 정보를 포함합니다.

## 개발

### 새로운 기능 추가하기

1. **Backend API 엔드포인트 추가**
   - `backend/main.py`에 새 라우트 추가
   - 필요시 `backend/crud.py`에 데이터베이스 작업 추가

2. **Frontend 기능 추가**
   - `frontend/app.js`에 새 함수 추가
   - `frontend/index.html`에 UI 요소 추가
   - `frontend/styles.css`에 스타일 추가

### 데이터베이스 마이그레이션

스키마 변경 시:

```bash
# 1. models.py 수정
# 2. 마이그레이션 스크립트 생성 (Alembic 사용 권장)
# 3. Docker 재시작
docker-compose down
docker-compose up -d
```

## 트러블슈팅

### MySQL 연결 오류

```bash
# MySQL 컨테이너 로그 확인
docker-compose logs mysql

# MySQL 컨테이너 재시작
docker-compose restart mysql
```

### Backend 오류

```bash
# Backend 로그 확인
docker-compose logs backend

# Backend 재빌드
docker-compose up -d --build backend
```

### 데이터베이스 초기화

```bash
# 모든 데이터 삭제 및 재시작
docker-compose down -v
docker-compose up -d
```

## 보안 고려사항

⚠️ **프로덕션 환경에서는 다음을 변경해야 합니다:**

1. MySQL root 비밀번호 변경
2. 환경 변수를 `.env` 파일로 분리하고 `.gitignore`에 추가
3. CORS 설정을 특정 도메인으로 제한
4. HTTPS 사용
5. API 인증/인가 추가

## 라이선스

MIT License

## 문의

문제가 발생하면 이슈를 등록해주세요.
