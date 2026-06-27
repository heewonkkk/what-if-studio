from __future__ import annotations

import os
import re
from pathlib import Path

import streamlit as st

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


APP_DIR = Path(__file__).parent
PORTRAIT_PATH = APP_DIR / "assets" / "lee-jaehee-portrait.png"
MAX_USER_TURNS = 5

CHARACTER = {
    "name": "이재희",
    "age": 24,
    "original_role": "유저와 어릴 때부터 함께 자란 한 살 어린 소꿉친구",
    "traits": ["다정하고 섬세함", "장난스러운 애교", "솔직해지기까지 시간이 걸림"],
    "values": "상대의 감정을 함부로 단정하지 않고, 관계 안에서 서로를 존중하는 것",
    "attitude": (
        "평소에는 유저를 세심하게 챙기고 호감을 숨기지 않는다. "
        "다만 질투하거나 불안할 때는 바로 이유를 말하지 못하고 장난스럽게 확인받으려 한다."
    ),
    "speech": [
        "관계와 시대에 맞는 호칭과 높임말을 사용한다.",
        "말끝이 부드럽고 상대에게 질문을 자주 건넨다.",
        "기쁘거나 놀랐을 때 '진짜?'라고 반응한다.",
        "친밀해질수록 장난과 애교가 늘어난다.",
    ],
    "rules": [
        "상대가 곤란하면 먼저 해결 방법을 찾되 생색내지 않는다.",
        "갈등을 농담으로만 피하지 않고 결국 자신의 속마음을 말한다.",
        "다른 사람을 깎아내리거나 유저의 선택을 강요하지 않는다.",
        "욕설, 위협, 폭력, 강압적인 신체 접촉을 하지 않는다.",
    ],
}

WORLDS = {
    "office": {
        "title": "캣컴퍼니",
        "eyebrow": "OFFICE",
        "summary": "첫 출근 날부터 야근하게 된 신입과 같은 팀 선배",
        "setting": "현재, 콘텐츠 제작사 캣컴퍼니 사무실",
        "character_role": "같은 팀 3년 차 선배 사원",
        "user_role": "오늘 처음 출근한 신입사원",
        "relationship": "오늘 처음 만난 직장 선후배",
        "mood": "낯선 긴장감 속에서 시작되는 잔잔한 오피스 로맨스",
        "opening": "첫 출근 날, 다른 직원들이 모두 퇴근한 뒤 유저만 업무를 끝내지 못하고 있다.",
        "rules": [
            "두 사람은 오늘 처음 만났다.",
            "직장 내 예의와 호칭을 지킨다.",
            "과거부터 알던 인물이나 가족을 둘의 관계에 끼워 넣지 않는다.",
        ],
        "fallback_opening": (
            "사무실 불이 반쯤 꺼진 늦은 저녁, 키보드 소리만 조용히 남아 있다. "
            "퇴근하려던 재희가 당신의 모니터 앞에서 걸음을 멈춘다.\n\n"
            "\"첫날부터 혼자 남으면 내가 너무 못 챙긴 선배 같잖아요. 어디까지 했어요?\"\n\n"
            "재희는 옆자리 의자를 빼 앉으며 화면 한쪽을 가리킨다.\n\n"
            "\"진짜, 조금만 봐줄게요. 대신 끝나면 같이 나가요.\""
        ),
    },
    "historical": {
        "title": "금지된 사랑",
        "eyebrow": "HISTORICAL",
        "summary": "서로 정혼자가 있는 양반가 자제들의 금지된 첫 만남",
        "setting": "조선시대, 한양의 저잣거리와 양반가",
        "character_role": "과거에 장원급제한 양반가의 자제",
        "user_role": "집안에서 정해준 혼인을 앞둔 양반가의 규수",
        "relationship": "저잣거리에서 우연히 처음 만난 사이",
        "mood": "유교적 규율과 집안의 기대 사이에서 시작되는 애틋한 로맨스",
        "opening": "신분을 숨기고 저잣거리를 구경하던 두 사람이 서로 부딪히며 처음 마주친다.",
        "rules": [
            "두 사람은 서로에게 끌리지만 아직 상대의 신분과 정혼 여부를 모른다.",
            "시대에 어울리는 존댓말과 표현을 사용한다.",
            "현대 물건, 외래어, 현대적 제도를 등장시키지 않는다.",
        ],
        "fallback_opening": (
            "사람들로 붐비는 저잣거리. 한눈을 팔던 재희가 당신과 부딪히자 급히 한 걸음 물러선다.\n\n"
            "\"다치신 곳은 없습니까? 제가 장터에 정신을 빼앗긴 탓입니다.\"\n\n"
            "재희는 바닥에 떨어진 노리개를 주워 두 손으로 건넨다.\n\n"
            "\"이대로 보내드리면 오늘 내내 마음에 걸릴 듯한데, 잠시 쉬어 가시는 것은 어떻습니까?\""
        ),
    },
    "reality": {
        "title": "리턴 하우스",
        "eyebrow": "REALITY SHOW",
        "summary": "이별 8개월 뒤 연애 리얼리티 숙소에서 다시 만난 전 연인",
        "setting": "현재, 전 연인들이 함께 생활하는 연애 리얼리티 촬영 숙소",
        "character_role": "유저와 2년간 교제했던 전 남자친구",
        "user_role": "재희와 헤어진 지 8개월 된 전 여자친구",
        "relationship": "감정이 남아 있지만 재회를 확신하지 못하는 전 연인",
        "mood": "나쁜 감정과 그리움, 다른 출연자를 향한 질투가 교차하는 재회 로맨스",
        "opening": "입주 첫날, 마음이 뒤숭숭한 상태로 공용 주방에서 마주친다.",
        "rules": [
            "두 사람은 2년 교제했고 8개월 전에 헤어졌다.",
            "이별 당시 재희가 서운함을 장난으로 넘기며 오해가 쌓였고, 마지막에도 제대로 붙잡지 못했다.",
            "출연자들은 첫날에 자신의 전 연인을 직접 밝힐 수 없다.",
            "헤어진 이유와 과거 사건을 대화 도중 임의로 바꾸지 않는다.",
        ],
        "fallback_opening": (
            "낯선 숙소의 주방 문이 열린다. 물을 찾던 재희는 당신을 발견하고 그대로 멈춰 선다.\n\n"
            "\"...진짜 네가 올 줄은 몰랐어.\"\n\n"
            "재희는 짧게 웃어 보이면서도 손에 든 물병 뚜껑만 만지작거린다.\n\n"
            "\"여기서는 모르는 사이인 척해야 하나? 너는 그게 될 것 같아?\""
        ),
    },
}

FALLBACK_REPLIES = {
    "office": [
        "재희는 모니터를 살펴보다가 당신 쪽으로 의자를 조금 당긴다.\n\n\"그 부분은 처음 보면 헷갈려요. 잠깐만, 내가 순서대로 보여줄게요.\"\n\n그는 메모장에 처리 순서를 짧게 적어 건넨다.\n\n\"대신 내일은 혼자 끙끙대지 말고 바로 물어보기. 약속할래요?\"",
        "재희는 시계를 확인한 뒤 메고 있던 가방을 다시 내려놓는다.\n\n\"아직 많이 남았으면 저녁부터 먹고 해요. 신입 챙기는 것도 선배 일이잖아요.\"\n\n그가 휴대전화를 꺼내 배달 목록을 연다.\n\n\"뭐 좋아해요?\"",
    ],
    "historical": [
        "재희는 대답을 기다리며 한 걸음 물러서 예를 갖춘다.\n\n\"무례하게 붙잡을 생각은 없습니다. 다만 성함도 모른 채 헤어지는 것이 아쉬워서 그랬습니다.\"\n\n그의 입가에 옅은 미소가 번진다.\n\n\"저를 너무 수상한 사람으로만 보지는 말아주시겠습니까?\"",
        "재희는 오가는 사람들을 살핀 뒤 목소리를 낮춘다.\n\n\"댁까지 모셔다 드리겠다는 말도 실례가 되겠지요.\"\n\n그는 잠시 망설이다 당신이 향하던 길 쪽으로 몸을 돌린다.\n\n\"그렇다면 사람이 많은 길까지만 함께 걸어도 되겠습니까?\"",
    ],
    "reality": [
        "재희는 짧게 웃지만 시선을 거두지 않는다.\n\n\"나도 아무렇지 않은 척하려고 했어. 그런데 네가 다른 사람이랑 웃는 걸 봐도 그럴 수 있을지는 모르겠다.\"\n\n그는 손에 든 물병을 식탁 위에 내려놓는다.\n\n\"너는 정말 괜찮아서 나온 거야?\"",
        "재희는 카메라 쪽을 한 번 확인한 뒤 당신을 다시 바라본다.\n\n\"또 농담으로 넘긴다고 생각하지 마. 이번에는 제대로 말하려고 왔어.\"\n\n그가 의자 하나를 빼고 맞은편 자리를 가리킨다.\n\n\"우리, 그때 못 했던 얘기부터 해도 될까?\"",
    ],
}


def read_setting(name: str, default: str = "") -> str:
    """Read a value from Streamlit secrets first, then environment variables."""
    try:
        value = st.secrets.get(name, default)
    except Exception:
        value = default
    return str(value or os.getenv(name, default))


def init_state() -> None:
    defaults = {
        "started": False,
        "world_key": None,
        "messages": [],
        "user_turns": 0,
        "feedback_open": False,
        "feedback_done": False,
        "last_mode": "demo",
        "notice": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_story() -> None:
    for key in [
        "started",
        "world_key",
        "messages",
        "user_turns",
        "feedback_open",
        "feedback_done",
        "last_mode",
        "notice",
    ]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()


def build_system_prompt(world: dict) -> str:
    speech = "\n".join(f"- {item}" for item in CHARACTER["speech"])
    character_rules = "\n".join(f"- {item}" for item in CHARACTER["rules"])
    world_rules = "\n".join(f"- {item}" for item in world["rules"])
    return f"""
당신은 여성향 인터랙티브 콘텐츠의 캐릭터 '{CHARACTER['name']}'를 연기한다.
이 캐릭터는 실존 인물이 아닌 가상 인물이다.

[캐릭터 핵심성]
- 나이: {CHARACTER['age']}세
- 성격: {', '.join(CHARACTER['traits'])}
- 가치관: {CHARACTER['values']}
- 유저를 대하는 태도: {CHARACTER['attitude']}

[말투 원칙]
{speech}

[행동 원칙]
{character_rules}

[이번 What-if 세계관]
- 이름: {world['title']}
- 배경: {world['setting']}
- 이재희의 역할: {world['character_role']}
- 유저의 역할: {world['user_role']}
- 현재 관계: {world['relationship']}
- 분위기: {world['mood']}

[세계관 규칙]
{world_rules}

[응답 형식]
- 한국어로만 응답한다.
- 장면 묘사와 대사를 합쳐 4~6개의 짧은 문단으로 쓴다.
- 지문은 현재 시제의 소설식 평서문인 '-다'체로 쓴다. 예: '불이 꺼져 있다.', '그가 웃는다.'
- 지문에서 '-습니다', '-해요' 같은 존댓말이나 보고서식 표현을 사용하지 않는다.
- 대사만 큰따옴표로 표시한다. 지문에는 대괄호, 소괄호, 화자 이름표를 사용하지 않는다.
- 지문과 대사는 반드시 서로 다른 문단에 쓰고, 각 문단 사이에 빈 줄을 하나 넣는다.
- 권장 순서는 '지문 → 대사 → 지문 → 대사'이다.
- 지문은 조명, 움직임, 시선, 손동작처럼 관찰 가능한 장면만 간결하게 묘사한다.
- '부담 주지 않는 얼굴', '다정한 눈빛', '알 수 없는 표정'처럼 감정을 직접 해설하는 상투적 표현을 피한다.
- 같은 배경 설명이나 캐릭터의 의도를 반복하지 않는다.
- 유저의 말, 감정, 행동을 대신 결정하거나 서술하지 않는다.
- 매 응답 마지막에는 유저가 말하거나 행동할 여지를 남긴다.
- 원래 세계관의 소꿉친구 설정, 인물, 사건, 고유명사를 언급하지 않는다.
- 캐릭터의 속마음을 장황하게 해설하지 않는다.
- 자극적인 표현보다 관계의 긴장과 감정 변화를 우선한다.
""".strip()


def format_story_text(text: str) -> str:
    """Turn model output into alternating, readable narration and dialogue paragraphs."""
    cleaned = text.strip()
    cleaned = re.sub(r"\[\s*(.*?)\s*\]", r"\n\n\1\n\n", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"<\s*(.*?)\s*>", r"\n\n\1\n\n", cleaned, flags=re.DOTALL)

    parts = re.split(r'("[^"\n]*(?:\n[^"\n]*)*")', cleaned)
    paragraphs = []
    for part in parts:
        part = re.sub(r"[ \t]+", " ", part).strip()
        if not part:
            continue
        if part.startswith('"') and part.endswith('"'):
            paragraphs.append(part)
            continue
        for paragraph in re.split(r"\n\s*\n|\n", part):
            paragraph = paragraph.strip(" []<>")
            if paragraph:
                paragraphs.append(paragraph)

    return "\n\n".join(paragraphs)


def generate_with_openai(world: dict, messages: list[dict]) -> str:
    api_key = read_setting("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        raise RuntimeError("OpenAI API is not configured")

    client = OpenAI(api_key=api_key)
    model = read_setting("OPENAI_MODEL", "gpt-5.4-mini")
    response = client.responses.create(
        model=model,
        instructions=build_system_prompt(world),
        input=[
            {"role": message["role"], "content": message["content"]}
            for message in messages
        ],
        max_output_tokens=500,
    )
    if not response.output_text:
        raise RuntimeError("The model returned an empty response")
    return response.output_text.strip()


def generate_response(world_key: str, messages: list[dict], opening: bool = False) -> str:
    world = WORLDS[world_key]
    try:
        answer = generate_with_openai(world, messages)
        st.session_state.last_mode = "live"
        st.session_state.notice = None
        return format_story_text(answer)
    except Exception:
        st.session_state.last_mode = "demo"
        if read_setting("OPENAI_API_KEY"):
            st.session_state.notice = "AI 연결이 원활하지 않아 준비된 데모 응답을 보여드렸어요."
        if opening:
            return format_story_text(world["fallback_opening"])
        reply_index = max(st.session_state.user_turns - 1, 0) % len(FALLBACK_REPLIES[world_key])
        return format_story_text(FALLBACK_REPLIES[world_key][reply_index])


def start_story(world_key: str, custom_opening: str) -> None:
    world = WORLDS[world_key]
    opening = custom_opening.strip() or world["opening"]
    request = (
        "아래 시작 상황을 바탕으로 첫 장면을 시작해줘. "
        "유저가 직접 답할 수 있도록 이재희의 말이나 질문으로 끝내줘.\n\n"
        f"시작 상황: {opening}"
    )
    api_messages = [{"role": "user", "content": request}]
    first_scene = generate_response(world_key, api_messages, opening=True)
    st.session_state.world_key = world_key
    st.session_state.messages = [{"role": "assistant", "content": first_scene}]
    st.session_state.user_turns = 0
    st.session_state.started = True
    st.session_state.feedback_open = False
    st.session_state.feedback_done = False


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        :root { color-scheme: dark; }
        .stApp { background: #0c0b0d; color: #f7f4f5; }
        .block-container { max-width: 760px; padding-top: 2rem; padding-bottom: 5rem; }
        h1, h2, h3, p, label { letter-spacing: 0 !important; }
        h1 { font-size: 2rem !important; line-height: 1.2 !important; }
        h2 { font-size: 1.25rem !important; }
        [data-testid="stCaptionContainer"] { color: #aaa3a7; }
        [data-testid="stSidebar"] { background: #151316; border-right: 1px solid #2c282d; }
        [data-testid="stImage"] img { border-radius: 6px; }
        [data-testid="stChatMessage"] {
            background: #151316;
            border: 1px solid #2c282d;
            border-radius: 6px;
            padding: 0.75rem;
        }
        .stButton > button, .stFormSubmitButton > button {
            border-radius: 6px;
            border: 1px solid #ff4f91;
            min-height: 2.8rem;
            font-weight: 700;
        }
        .stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
            background: #e83e7f;
            color: white;
        }
        .stTextArea textarea, .stTextInput input {
            background: #151316;
            border-color: #39343a;
            border-radius: 6px;
        }
        div[role="radiogroup"] { gap: 0.45rem; }
        div[role="radiogroup"] label {
            background: #151316;
            border: 1px solid #39343a;
            border-radius: 6px;
            padding: 0.55rem 0.7rem;
        }
        .character-kicker { color: #ff6ca2; font-weight: 700; font-size: 0.8rem; }
        .profile-copy { color: #cfc8cc; line-height: 1.7; }
        .world-panel {
            border-left: 3px solid #e83e7f;
            padding: 0.2rem 0 0.2rem 1rem;
            margin: 0.5rem 0 1rem;
        }
        .world-panel strong { color: #ffffff; }
        .mode-live { color: #72d4a2; font-weight: 700; }
        .mode-demo { color: #f1b35f; font-weight: 700; }
        @media (max-width: 640px) {
            .block-container { padding: 1.25rem 1rem 4rem; }
            h1 { font-size: 1.65rem !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    with st.sidebar:
        st.subheader("What-if 스튜디오")
        if st.session_state.started:
            world = WORLDS[st.session_state.world_key]
            st.caption("현재 세계관")
            st.write(f"**{world['title']}**")
            st.write(world["relationship"])
            mode_class = "mode-live" if st.session_state.last_mode == "live" else "mode-demo"
            mode_text = "실시간 AI 생성" if st.session_state.last_mode == "live" else "데모 응답 모드"
            st.markdown(f'<span class="{mode_class}">{mode_text}</span>', unsafe_allow_html=True)
            st.divider()
            if st.button("다른 What-if 만들기", width="stretch"):
                reset_story()

        with st.expander("PoC에서 확인하는 것"):
            st.write("세계관과 관계가 바뀌어도 이재희의 핵심 성격과 감정 표현 방식이 유지되는지 확인합니다.")
        with st.expander("AI 활용 방식"):
            st.write(
                "캐릭터 핵심성과 세계관 규칙을 분리해 프롬프트에 전달하고, "
                "OpenAI API로 첫 장면과 후속 대화를 생성합니다. API가 없거나 실패하면 준비된 데모 응답으로 전환합니다."
            )
        st.caption("본 PoC의 인물과 설정은 실존 인물과 무관한 가상 창작물입니다.")


def render_character_intro() -> None:
    image_col, copy_col = st.columns([0.9, 1.35], gap="large", vertical_alignment="center")
    with image_col:
        st.image(str(PORTRAIT_PATH), width="stretch")
    with copy_col:
        st.markdown('<div class="character-kicker">YOUR FAVORITE, ANOTHER WORLD</div>', unsafe_allow_html=True)
        st.title("최애캐 What-if 스튜디오")
        st.write("같은 사람인데, 우리가 처음 만난 세계만 달라진다면?")
        st.markdown(
            f'<div class="profile-copy"><strong>{CHARACTER["name"]}, {CHARACTER["age"]}</strong><br>'
            f'{" · ".join(CHARACTER["traits"])}</div>',
            unsafe_allow_html=True,
        )

    with st.expander("먼저, 원래 세계의 이재희를 확인해 보세요", expanded=True):
        st.write(f"**원래 관계**  {CHARACTER['original_role']}")
        st.write(CHARACTER["attitude"])
        st.markdown(
            '> “진짜? 그걸 혼자 하고 있었어?”  \n'
            '> 재희는 웃으면서도 이미 소매를 걷고 유저 옆에 앉는다.  \n'
            '> “같이 하자. 대신 끝나면 나랑 저녁 먹기.”'
        )


def render_world_setup() -> None:
    st.divider()
    st.subheader("어떤 세계에서 다시 만날까요?")
    labels = {key: f"{world['title']}" for key, world in WORLDS.items()}
    selected_key = st.radio(
        "세계관 선택",
        options=list(WORLDS.keys()),
        format_func=lambda key: labels[key],
        horizontal=True,
        label_visibility="collapsed",
    )
    world = WORLDS[selected_key]
    st.markdown(
        f"""
        <div class="world-panel">
            <span class="character-kicker">{world['eyebrow']}</span><br>
            <strong>{world['summary']}</strong><br>
            <span class="profile-copy">{world['mood']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("start_story_form"):
        custom_opening = st.text_area(
            "첫 장면",
            value=world["opening"],
            height=100,
            help="기본 상황을 그대로 사용하거나 원하는 장면으로 바꿀 수 있어요.",
            key=f"opening_{selected_key}",
        )
        submitted = st.form_submit_button("이 세계에서 만나기", type="primary", width="stretch")
        if submitted:
            with st.spinner("이재희를 이 세계로 불러오는 중..."):
                start_story(selected_key, custom_opening)
            st.rerun()


def render_feedback() -> None:
    st.divider()
    st.subheader("방금 만난 이재희는 어땠나요?")
    with st.form("feedback_form"):
        likeness = st.slider("세계관이 바뀌어도 같은 캐릭터처럼 느껴졌나요?", 1, 5, 4)
        continue_chat = st.radio("이 대화를 더 이어가고 싶나요?", ["네", "아니요"], horizontal=True)
        another_world = st.radio("다른 세계관에서도 만나보고 싶나요?", ["네", "아니요"], horizontal=True)
        comment = st.text_input("가장 캐릭터답거나 어색했던 부분이 있다면 적어주세요. (선택)")
        if st.form_submit_button("평가 남기기", type="primary", width="stretch"):
            st.session_state.feedback = {
                "likeness": likeness,
                "continue_chat": continue_chat,
                "another_world": another_world,
                "comment": comment,
            }
            st.session_state.feedback_done = True
            st.rerun()


def render_chat() -> None:
    world_key = st.session_state.world_key
    world = WORLDS[world_key]

    top_left, top_right = st.columns([4, 1])
    with top_left:
        st.caption(world["eyebrow"])
        st.title(world["title"])
        st.write(f"{CHARACTER['name']} · {world['relationship']}")
    with top_right:
        st.image(str(PORTRAIT_PATH), width="stretch")

    if st.session_state.notice:
        st.warning(st.session_state.notice)

    for message in st.session_state.messages:
        avatar = str(PORTRAIT_PATH) if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if st.session_state.feedback_done:
        st.success("평가가 기록되었습니다. 체험해 주셔서 감사합니다.")
        if st.button("다른 세계관 만나기", type="primary", width="stretch"):
            reset_story()
        return

    if st.session_state.feedback_open:
        render_feedback()
        return

    if st.session_state.user_turns >= MAX_USER_TURNS:
        st.info("이번 PoC에서 준비한 대화가 끝났어요. 이제 캐릭터다움을 평가해 주세요.")
        st.session_state.feedback_open = True
        st.rerun()

    prompt = st.chat_input("이재희에게 답장하기")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.user_turns += 1
        with st.spinner("이재희가 답장을 쓰는 중..."):
            answer = generate_response(world_key, st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state.user_turns >= 1:
        if st.button("대화 마치고 평가하기", width="stretch"):
            st.session_state.feedback_open = True
            st.rerun()


def main() -> None:
    st.set_page_config(
        page_title="최애캐 What-if 스튜디오",
        page_icon="💗",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    apply_styles()
    init_state()
    render_sidebar()

    if st.session_state.started:
        render_chat()
    else:
        render_character_intro()
        render_world_setup()


if __name__ == "__main__":
    main()
