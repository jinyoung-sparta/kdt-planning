import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import io

# CSV 다운로드 함수 
def create_csv_files(df, filename_prefix):
    """평가 템플릿 데이터를 3개의 CSV 파일로 생성"""
    try:
        csv_files = {}
        
        # 파일 1: 출제자 평가 템플릿
        template_csv = df.to_csv(index=False, encoding='utf-8-sig')
        csv_files['template'] = {
            'data': template_csv,
            'filename': f"{filename_prefix}_출제자평가템플릿.csv"
        }
        
        # 파일 2: 평가 기준표
        criteria_data = []
        for _, row in df.iterrows():
            criteria_row = {
                '대분류': row.get('대분류', ''),
                '중분류': row.get('중분류', ''),
                '소분류': row.get('소분류', ''),
                '상 (90-100점)': row.get('상', ''),
                '중 (70-89점)': row.get('중', ''),
                '하 (50-69점)': row.get('하', ''),
                '미달 (0-49점)': row.get('배점 X', ''),
                '비고': ''
            }
            criteria_data.append(criteria_row)
        
        criteria_df = pd.DataFrame(criteria_data)
        criteria_csv = criteria_df.to_csv(index=False, encoding='utf-8-sig')
        csv_files['criteria'] = {
            'data': criteria_csv,
            'filename': f"{filename_prefix}_평가기준표.csv"
        }
        
        # 파일 3: 점수 집계표
        score_data = []
        for _, row in df.iterrows():
            score_row = {
                '수험생명': '',
                '대분류': row.get('대분류', ''),
                '중분류': row.get('중분류', ''),
                '소분류': row.get('소분류', ''),
                '배점': row.get('배점', ''),
                '획득점수': '',
                '평가자': '',
                '평가일시': '',
                '비고': ''
            }
            score_data.append(score_row)
        
        score_df = pd.DataFrame(score_data)
        score_csv = score_df.to_csv(index=False, encoding='utf-8-sig')
        csv_files['score'] = {
            'data': score_csv,
            'filename': f"{filename_prefix}_점수집계표.csv"
        }
        
        return True, csv_files
        
    except Exception as e:
        return False, f"CSV 파일 생성 중 오류가 발생했습니다: {str(e)}"

# 엑셀 파일 생성 함수
def create_excel_file(track_name=""):
    """평가 템플릿과 문제 템플릿을 포함한 엑셀 파일 생성"""
    try:
        # 파일명 설정
        if track_name.strip():
            filename = f"{track_name.strip()}_{datetime.now().strftime('%y%m%d')}.xlsx"
        else:
            filename = f"스파르타_평가시트_{datetime.now().strftime('%y%m%d')}.xlsx"
        
        # BytesIO 객체 생성
        output = io.BytesIO()
        
        # ExcelWriter 생성
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # 평가 템플릿 시트
            if "template_table" in st.session_state and not st.session_state["template_table"].empty:
                template_df = st.session_state["template_table"].copy()
                template_df.to_excel(writer, sheet_name='출제자_평가_템플릿', index=False)

            # 문제 템플릿 시트
            if "problem_table" in st.session_state and not st.session_state["problem_table"].empty:
                problem_df = st.session_state["problem_table"].copy()
                problem_df.to_excel(writer, sheet_name='출제자_문제_템플릿', index=False)

            # 문제 템플릿 시트
            if "problem_table" in st.session_state and not st.session_state["problem_table"].empty:
                problem_df = st.session_state["problem_table"].copy()
                problem_df.to_excel(writer, sheet_name='검수자_문제_템플릿', index=False)        
            
            # 빈 시트들이 없다면 기본 템플릿 생성
            if ("template_table" not in st.session_state or st.session_state["template_table"].empty) and \
               ("problem_table" not in st.session_state or st.session_state["problem_table"].empty):
                # 기본 평가 템플릿
                default_template = pd.DataFrame({
                    "대분류": ["예시"],
                    "중분류": ["예시"],
                    "소분류": ["예시 평가 항목"],
                    "평가 내용": ["평가 내용을 입력하세요"],
                    "배점": [10],
                    "상": ["상급 기준"],
                    "중": ["중급 기준"],
                    "하": ["하급 기준"],
                    "배점 X": ["미달 기준"]
                })
                default_template.to_excel(writer, sheet_name='출제자_평가_템플릿', index=False)
                
                # 기본 문제 템플릿
                default_problem = pd.DataFrame({
                    "문제명": ["예시 문제"],
                    "하위 기능": [""],
                    "소분류": ["예시 평가 항목"],
                    "평가 내용": ["평가 내용을 입력하세요"],
                    "진행상황": ["진행중"],
                    "유형": ["실무과제"],
                    "난이도": ["중"],
                    "출제 목적": [""],
                    "문제 설명": [""],
                    "필수 요구사항": [""],
                    "선택 요구사항(가산점)": [""],
                    "제약 조건": [""],
                    "요구 기술 스택 및 툴": [""],
                    "제출 형식": [""],
                    "예상 소요시간": [""],
                    "문제 노션 링크": [""],
                    "답안 노션 링크": [""],
                    "출제자 메모": [""]
                })
                default_problem.to_excel(writer, sheet_name='출제자_문제_템플릿', index=False)
        
        output.seek(0)
        return True, output.getvalue(), filename
        
    except Exception as e:
        return False, None, f"엑셀 파일 생성 중 오류가 발생했습니다: {str(e)}"

# 콜백 함수들 정의
def update_template_data():
    """평가 템플릿 데이터 업데이트 콜백"""
    if "template_editor" in st.session_state:
        st.session_state["template_table"] = st.session_state["template_editor"]

def update_problem_data():
    """문제 템플릿 데이터 업데이트 콜백"""
    if "problem_editor" in st.session_state:
        st.session_state["problem_table"] = st.session_state["problem_editor"]

# 페이지 설정
st.set_page_config(
    page_title="스파르타 취업 역량 평가",
    page_icon="🧑🏻‍🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 메인 타이틀
st.title("🧑🏻‍🎓 스파르타 취업 역량 평가")
st.markdown("---")

# 세션 상태 초기화
if 'current_page' not in st.session_state:
    st.session_state.current_page = "평가표"

# 버튼 메뉴
if st.sidebar.button("평가표", use_container_width=True):
    st.session_state.current_page = "평가표"
if st.sidebar.button("출제자 평가 템플릿", use_container_width=True):
    st.session_state.current_page = "출제자 평가 템플릿"
if st.sidebar.button("출제자 문제 템플릿", use_container_width=True):
    st.session_state.current_page = "출제자 문제 템플릿"

# 시트 만들기 버튼 추가
st.sidebar.markdown("---")
st.sidebar.markdown("### 📄 파일 생성")

# 트랙명을 사이드바에서 입력받기
sidebar_track_name = st.sidebar.text_input(
    "트랙명 (파일명용)",
    value="",
    placeholder="예: PM, UXUI, 그래픽디자이너",
    help="엑셀 파일명에 사용될 트랙명을 입력하세요"
)

if st.sidebar.button("📊 시트 만들기", use_container_width=True, type="primary"):
    success, excel_data, filename = create_excel_file(sidebar_track_name)
    
    if success:
        st.sidebar.download_button(
            label="📥 엑셀 파일 다운로드",
            data=excel_data,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        st.sidebar.success("엑셀 파일이 생성되었습니다! 다운로드 버튼을 클릭하세요.")
    else:
        st.sidebar.error(f"엑셀 파일 생성 실패: {filename}")

page = st.session_state.current_page

if page == "평가표":
    st.header("평가표")

    # st.info("""
    #     **📋 평가 템플릿 생성 방법**
    #     1. 개발/비개발 과목을 선택
    #     2. 원하는 평가 항목들을 선택
    #     3. "평가 템플릿에 추가" 버튼 클릭
    # """)
    
    # 개발/비개발 토글
    job_type = st.selectbox("과목 선택", ["개발", "비개발"])
    
    if job_type == "개발":
        st.subheader("개발 평가표")
        # 계층 구조 정의 (예시)
        dev_hierarchy = {
            '코드': {
                '요구사항 해석': ['프로젝트 과제 목적에 맞게 구현했는가', '제공된 입출력 데이터를 통과하는가'],
                '알고리즘/로직': ['기본 문법(반복문, 조건문 등) 적절히 활용했는가', '효율적인 알고리즘 및 자료구조 사용했는가'],
                '코드 품질 및 최적화': ['적절한 함수 분리 및 모듈화가 되어있는가', '시간/공간복잡도 개선 노력이 있었는가', '중복 코드를 최소화하여 간결하게 작성했는가'],
                '예외 처리': ['예상 가능한 예외 사항을 고려했는가', 'try-catch-finally 구문을 적절히 사용했는가']
            },
            '프레임워크': {
                '구조 설계 이해도': ['프레임워크 구조 특성을 이해하고 적용했는가', '디렉토리 구조를 일관성있게 설계했는가'],
                '기능 구현 방식 적절성': ['프레임워크 방식에 맞춰 기능을 구현했는가', '내장 기능과 라이브러리를 알맞게 활용했는가'],
                '역할 분리 및 재사용성': ['로직, 서비스 등을 목적에 따라 분리했는가', '컴포넌트화, 모듈화 등을 통해 재사용을 할 수 있는가'],
                '상태 및 흐름 관리': ['상태 관리나 요청-응답 흐름을 일관되게 처리했는가', '프레임워크에 맞는 상태/라우팅 방식을 사용했는가'],
                '설정 및 의존성 관리': ['환경설정 파일(.env, web.xml 등)을 적절히 구성했는가', '외부 라이브러리, 모듈 의존성을 관리했는가'],
            }
        }
        # 표로 변환
        rows = []
        for 대분류, 중분류_dict in dev_hierarchy.items():
            for 중분류, 소분류_list in 중분류_dict.items():
                for 소분류 in 소분류_list:
                    rows.append({'대분류': 대분류, '중분류': 중분류, '소분류': 소분류})
        df = pd.DataFrame(rows)

    else:
        st.subheader("비개발 평가표")
        # 계층 구조 정의 (예시)
        biz_hierarchy = {
            '기획': {
                '문제 정의': ['해결해야 할 문제와 핵심 이슈를 제대로 설정했는가'],
                '요구사항 분석': ['고객/시장/업무의 요구사항을 잘 분석했는가', '다양한 관계자의 니즈를 반영했는가', '충돌되는 요구사항을 조율했는가'],
                '목표 설정': ['달성 가능한 목표/지표를 설계했는가', '핵심 기능 또는 가치 요소를 제대로 도출했는가'],
                '전략 및 기획': ['목표를 달성하기 위한 구체적인 전략을 수립했는가', '전개 방식이 일관되고 설득력있는 전략/기획인가'],
            },
            '완성도': {
                '결과물 완성도': ['계획한 목표를 달성했는가', '목표 달성 과정이 설득력있게 정리되었는가'],
                '문제 해결력': ['정성적/정량적 데이터를 적절히 활용했는가', '데이터 해석이 설득력을 갖고 판단의 근거로 기능했는가'],
                '전문성': ['직무에 맞는 툴을 목적에 맞게 활용했는가', '직무 용어 및 개념을 올바르게 사용했는가'],
                '성과 분석': ['결과물에 대한 성과 분석을 수행했는가', '문제점과 긍정적인 성과 모두를 도출했는가'],
                '개선 제안': ['수행 과정을 바탕으로 개선 방향을 논리적으로 제시했는가']
            },
            '소프트스킬': {
                '협업 및 전달력': ['다른 직무 담당자와의 협업을 고려했는가', '기획 의도, 결과물을 명확하게 설명했는가'],
                '창의성': ['결과물을 도출하기 위한 과정이 창의적으로 진행됐는가', '다른 수험생들과 비교되는 지점이 있는가'],
            }
        }
        # 표로 변환
        rows = []
        for 대분류, 중분류_dict in biz_hierarchy.items():
            for 중분류, 소분류_list in 중분류_dict.items():
                for 소분류 in 소분류_list:
                    rows.append({'대분류': 대분류, '중분류': 중분류, '소분류': 소분류})
        df = pd.DataFrame(rows)

    
    # 평가 표 편집 가능하게 표시
    # 드롭다운 옵션 준비
    dev_major_options = list(dev_hierarchy.keys()) if job_type == "개발" else []
    dev_mid_options = sum([list(v.keys()) for v in dev_hierarchy.values()], []) if job_type == "개발" else []
    dev_sub_options = sum([sum([vv for vv in v.values()], []) for v in dev_hierarchy.values()], []) if job_type == "개발" else []
    biz_major_options = list(biz_hierarchy.keys()) if job_type == "비개발" else []
    biz_mid_options = sum([list(v.keys()) for v in biz_hierarchy.values()], []) if job_type == "비개발" else []
    biz_sub_options = sum([sum([vv for vv in v.values()], []) for v in biz_hierarchy.values()], []) if job_type == "비개발" else []

    # 각 표에 맞는 옵션 지정
    if job_type == "개발":
        col_config = {
            "대분류": st.column_config.SelectboxColumn("대분류", options=dev_major_options, required=True),
            "중분류": st.column_config.SelectboxColumn("중분류", options=dev_mid_options, required=True),
            "소분류": st.column_config.TextColumn("소분류", width="large"),
        }
    else:
        col_config = {
            "대분류": st.column_config.SelectboxColumn("대분류", options=biz_major_options, required=True),
            "중분류": st.column_config.SelectboxColumn("중분류", options=biz_mid_options, required=True),
            "소분류": st.column_config.TextColumn("소분류", width="large"),
        }

    st.dataframe(df, use_container_width=True)

    # 멀티셀렉트로 행 선택 (인덱스 기준)
    selected_idx = st.multiselect(
        "추가할 행(들)을 선택하세요",
        options=df.index,
        format_func=lambda x: f"{x+1}행: {df.loc[x, '대분류']} / {df.loc[x, '중분류']} / {df.loc[x, '소분류']}"
    )

    # 9개 열 구성 (앞 3개: 대분류, 중분류, 소분류)
    template_columns = [
        "대분류", "중분류", "소분류",
        "평가 내용", "배점", "상", "중", "하", "배점 X"
    ]
    if st.button("평가 템플릿에 추가"):
        if selected_idx:
            selected = df.loc[selected_idx]
            selected_template = pd.DataFrame({
                "대분류": selected["대분류"].values,
                "중분류": selected["중분류"].values,
                "소분류": selected["소분류"].values,
                "평가 내용": "",
                "배점": "",
                "상": "",
                "중": "",
                "하": "",
                "배점 X": ""
            })
            if "template_table" not in st.session_state:
                st.session_state["template_table"] = pd.DataFrame(columns=template_columns)
            st.session_state["template_table"] = pd.concat([
                st.session_state["template_table"], selected_template
            ], ignore_index=True).drop_duplicates()
            st.success("평가 템플릿에 추가되었습니다!")
        else:
            st.warning("추가할 행을 먼저 선택해 주세요.")

elif page == "출제자 평가 템플릿":
    st.header("출제자 평가 템플릿")

    if "template_table" in st.session_state and not st.session_state["template_table"].empty:
        # 텍스트 입력 가능한 컬럼 설정
        col_config = {
            "평가 내용": st.column_config.TextColumn("평가 내용", width="medium"),
            "배점": st.column_config.NumberColumn("배점", width="small", format="%d"),
            "상": st.column_config.TextColumn("상", width="medium"),
            "중": st.column_config.TextColumn("중", width="medium"),
            "하": st.column_config.TextColumn("하", width="medium"),
            "배점 X": st.column_config.TextColumn("배점 X", width="medium"),
        }
        
        # 데이터 편집기 (콜백과 키 추가)
        edited_df = st.data_editor(
            st.session_state["template_table"],
            column_config=col_config,
            use_container_width=True,
            num_rows="dynamic",
            key="template_editor",
            on_change=update_template_data
        )
        
        # 편집된 데이터를 즉시 세션 상태에 저장
        st.session_state["template_table"] = edited_df
        
        # 저장 상태 표시
        if st.session_state.get("template_editor_changed", False):
            st.success("✅ 변경사항이 자동 저장되었습니다!")
           
    else:
        st.info("아직 추가된 항목이 없습니다. 먼저 '평가표' 페이지에서 항목을 추가해주세요.")

    # 문제 만들기 버튼 (현재 평가 템플릿을 문제 템플릿으로 복사)
    if "template_table" in st.session_state and not st.session_state["template_table"].empty:
        if st.button("문제 만들기", key="make_problem"):
            # 문제 템플릿 열 정의
            problem_columns = [
                "문제명", "하위 기능", "소분류", "평가 내용", "진행상황", "유형", "난이도", "출제 목적", "문제 설명",
                "필수 요구사항", "선택 요구사항(가산점)", "제약 조건", "요구 기술 스택 및 툴", "제출 형식",
                "예상 소요시간", "문제 노션 링크", "답안 노션 링크", "출제자 메모"
            ]
            # 평가 템플릿에서 소분류/평가 내용만 추출, 나머지는 공란
            src_df = st.session_state["template_table"]
            problem_df = pd.DataFrame({
                "문제명": "",
                "하위 기능": "",
                "소분류": src_df["소분류"] if "소분류" in src_df.columns else "",
                "평가 내용": src_df["평가 내용"] if "평가 내용" in src_df.columns else "",
                "진행상황": "진행중",
                "유형": "",
                "난이도": "",
                "출제 목적": "",
                "문제 설명": "",
                "필수 요구사항": "",
                "선택 요구사항(가산점)": "",
                "제약 조건": "",
                "요구 기술 스택 및 툴": "",
                "제출 형식": "",
                "예상 소요시간": "",
                "문제 노션 링크": "",
                "답안 노션 링크": "",
                "출제자 메모": ""
            })
            st.session_state["problem_table"] = problem_df[problem_columns]
            st.success("출제자 문제 템플릿이 생성되었습니다! 사이드바에서 '출제자 문제 템플릿'을 확인하세요.")

elif page == "출제자 문제 템플릿":
    st.header("출제자 문제 템플릿")

    if "problem_table" in st.session_state and not st.session_state["problem_table"].empty:
        # 진행상황 컬럼만 진행중/진행 완료 선택 가능한 Selectbox로, 나머지는 기본값
        col_config = {
            "진행상황": st.column_config.SelectboxColumn("진행상황", options=["진행중", "진행 완료"], required=True),
            "유형": st.column_config.SelectboxColumn("유형", options=["코딩테스트", "실무과제", "지필평가"], required=True),
            "난이도": st.column_config.SelectboxColumn("난이도", options=["상", "중", "하"], required=True),
        }
        
        # 데이터 편집기 (콜백과 키 추가)
        edited_df = st.data_editor(
            st.session_state["problem_table"],
            column_config=col_config,
            use_container_width=True,
            num_rows="dynamic",
            key="problem_editor",
            on_change=update_problem_data
        )
        
        # 편집된 데이터를 즉시 세션 상태에 저장
        st.session_state["problem_table"] = edited_df
        
        # 저장 상태 표시
        if st.session_state.get("problem_editor_changed", False):
            st.success("✅ 변경사항이 자동 저장되었습니다!")
            
    else:
        st.info("아직 생성된 문제가 없습니다. '출제자 평가 템플릿'에서 '문제 만들기' 버튼을 눌러주세요.")

# 푸터
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Copyright ⓒ TeamSparta All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)
