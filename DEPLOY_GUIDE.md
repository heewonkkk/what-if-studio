# GitHub + Streamlit 배포 가이드

이 문서는 코딩 경험이 없는 사람을 위한 순서입니다. 터미널 명령어는 사용하지 않아도 됩니다.

## 전체 구조

```text
GitHub: 앱 파일을 보관하는 곳
   ↓
Streamlit Community Cloud: GitHub의 app.py를 웹사이트로 실행하는 곳
   ↓
OpenAI API: 사용자가 답장할 때 이재희의 다음 대사를 생성하는 곳
```

Streamlit API를 별도로 연결하는 것이 아니라, **Streamlit에 GitHub 저장소를 연결하고 Streamlit의 Secrets에 OpenAI API 키를 등록**하는 방식입니다.

## 1. OpenAI API 키 준비

1. <https://platform.openai.com/api-keys>에 로그인합니다.
2. `Create new secret key`를 눌러 키를 만듭니다.
3. 생성된 키를 잠시 안전한 곳에 보관합니다.
4. 필요한 경우 <https://platform.openai.com/settings/organization/billing/overview>에서 API 결제 수단이나 크레딧을 설정합니다.

ChatGPT Plus 같은 구독과 API 요금은 별도로 관리됩니다. API 키를 다른 사람에게 보내거나 GitHub 파일 안에 적지 마세요.

## 2. GitHub 저장소 만들기

1. <https://github.com/new>에 접속합니다.
2. Repository name에 `what-if-studio`를 입력합니다.
3. 공개 여부는 과제 확인이 편한 `Public`을 권장합니다.
4. `Create repository`를 누릅니다.

## 3. 파일 업로드

1. 만들어진 저장소에서 `Add file` → `Upload files`를 누릅니다.
2. 이 프로젝트 폴더의 아래 항목을 끌어다 놓습니다.

```text
app.py
requirements.txt
README.md
DEPLOY_GUIDE.md
.gitignore
assets 폴더
.streamlit 폴더
```

3. 화면 아래 `Commit changes`를 누릅니다.

주의: 실제 API 키가 들어간 `.streamlit/secrets.toml` 파일은 업로드하지 않습니다. 현재 프로젝트에는 예시 파일만 있고 실제 키는 없습니다.

## 4. Streamlit에 GitHub 연결

1. <https://share.streamlit.io>에 GitHub 계정으로 로그인합니다.
2. GitHub 연결 또는 권한 허용 화면이 나오면 승인합니다.
3. `Create app`을 누릅니다.
4. 다음 값을 선택합니다.

```text
Repository: 내 GitHub 아이디/what-if-studio
Branch: main
Main file path: app.py
```

## 5. API 키 등록

배포 화면에서 `Advanced settings`를 열고 `Secrets`에 아래 형식으로 입력합니다.

```toml
OPENAI_API_KEY = "여기에-실제-API-키"
OPENAI_MODEL = "gpt-5.4-mini"
```

따옴표는 남겨두고 `여기에-실제-API-키` 부분만 바꿉니다. 입력한 다음 `Save`를 누릅니다.

## 6. 배포 및 확인

1. `Deploy`를 누릅니다.
2. 설치가 끝나면 `https://...streamlit.app` 형태의 주소가 생성됩니다.
3. 세계관을 선택하고 첫 장면을 생성합니다.
4. 사이드바에 `실시간 AI 생성`이라고 표시되는지 확인합니다.
5. 생성된 주소를 과제 문서의 PoC 링크로 제출합니다.

`데모 응답 모드`가 표시되면 Streamlit의 `Manage app` → `Settings` → `Secrets`에서 API 키를 다시 확인하세요.

## 절대 하면 안 되는 것

- API 키를 `app.py`에 적기
- 실제 키가 든 `secrets.toml`을 GitHub에 업로드하기
- API 키 전체를 메신저나 과제 문서에 붙여넣기
- 배포 후 테스트하지 않고 바로 링크 제출하기
