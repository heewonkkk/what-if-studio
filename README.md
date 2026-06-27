# 최애캐 What-if 스튜디오 PoC

가상 캐릭터 이재희의 핵심 성격은 유지하고 세계관과 관계만 바꾸는 Streamlit 기반 인터랙티브 콘텐츠 PoC입니다.

## 실행

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml
streamlit run app.py
```

`.streamlit/secrets.toml`에 실제 `OPENAI_API_KEY`를 입력하면 실시간 AI 응답을 생성합니다. 키가 없거나 API 호출이 실패하면 준비된 데모 응답으로 작동합니다. API 키를 GitHub에 직접 올리면 안 됩니다.

코딩 경험이 없다면 [배포 가이드](DEPLOY_GUIDE.md)를 따라 GitHub 웹 업로드와 Streamlit Community Cloud 배포를 진행하세요.

## PoC 흐름

1. 원래 세계관의 캐릭터 소개 확인
2. 세 가지 What-if 세계관 중 하나 선택
3. 첫 장면 생성
4. 최대 5턴 대화
5. 캐릭터다움과 후속 사용 의향 평가

## 검증 질문

- 세계관이 바뀌어도 같은 캐릭터처럼 느껴지는가?
- 첫 장면 이후 대화를 계속하고 싶은가?
- 같은 캐릭터를 다른 세계관에서도 다시 만나고 싶은가?

캐릭터 이미지는 생성형 AI로 제작한 가상 인물이며 실존 인물과 무관합니다.
