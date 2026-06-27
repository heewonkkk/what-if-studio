# 최애캐 What-if 스튜디오

캐릭터의 핵심 성격은 유지하면서, 서로 다른 세계관과 관계에서 새로운 이야기를 시작하는 AI 인터랙티브 콘텐츠 PoC입니다.

- [PoC 직접 체험하기] https://what-if-studio-mt4nbeehyryrwcqnuqhgck.streamlit.app/
- [기획 문서] https://app.notion.com/p/Tain-AI-AI-Native-PM-38b19a8f738d802eb37bf376b3fa885d

## 기획 배경

최애캐에 대한 애착이 남아 있어도 기본 설정과 익숙한 대화 패턴이 소진되면 재방문할 이유가 약해질 수 있습니다.

최애캐의 성격과 감정 표현 방식은 유지하고 세계관만 바꾸면, 익숙한 캐릭터를 새롭게 소비할 동기가 생길 것이라는 가설에서 출발했습니다.

## 핵심 설계

| 유지하는 것 | 바꾸는 것 |
|---|---|
| 성격과 가치관 | 시대와 장소 |
| 말투의 원칙 | 직업과 역할 |
| 감정 표현 방식 | 유저와의 관계 |
| 금지 행동 | 첫 만남 상황 |

캐릭터 설정과 세계관 설정을 별도 컨텍스트로 구성해, 세계관이 달라져도 캐릭터의 핵심 태도가 유지되도록 설계했습니다.

## PoC 흐름

1. 기본 세계관의 캐릭터 소개 확인
2. 세 가지 What-if 세계관 중 하나 선택
3. AI가 세계관에 맞는 첫 장면 생성
4. 사용자 입력을 바탕으로 최대 5턴 대화
5. 캐릭터다움과 후속 사용 의향 평가

## 구현 기능

- 세계관 선택 및 첫 상황 수정
- OpenAI API 기반 첫 장면 생성
- 캐릭터·세계관·대화 기록을 반영한 후속 응답
- API 오류 시 데모 응답 전환
- 캐릭터다움과 재사용 의향 평가

## 기술 구성

- Python
- Streamlit
- OpenAI Responses API
- Streamlit Community Cloud
- GitHub

## 로컬 실행

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .streamlit\secrets.toml.example .streamlit\secrets.toml
streamlit run app.py
