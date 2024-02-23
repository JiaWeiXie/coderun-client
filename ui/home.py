import time
import streamlit as st

from streamlit_ace import st_ace, LANGUAGES, THEMES
from judge0 import Judge0Client
from utils.file import (
    list_folder,
    open_file,
    save_file,
    delete_file,
    folder_exists,
    list_files,
    pair_files,
)
from utils.text import generate_diff


st.set_page_config(page_title="測試程式程式", page_icon="▶️")
st.sidebar.header("測試程式")
st.title("測試程式碼")


st.sidebar.subheader("編輯區塊設定")
language = st.sidebar.selectbox("程式語言", options=LANGUAGES, index=121)
theme = st.sidebar.selectbox("編輯區塊主題", options=THEMES, index=35)
font_size = st.sidebar.slider("文字大小", 5, 24, 14)
tab_size = st.sidebar.slider("Tab 大小", 1, 8, 4)
show_gutter = st.sidebar.checkbox("顯示行號", value=True)
show_print_margin = st.sidebar.checkbox("顯示列印邊距", value=False)
wrap = st.sidebar.checkbox("換行", value=False)
readonly = st.sidebar.checkbox("唯讀模式", value=False)

source_code = ""
in_data, ans_data = "", ""


source_code = st_ace(
    source_code,
    placeholder="輸入驗證測資程式碼",
    language=language or "python",
    theme=theme,  # type: ignore
    keybinding="vscode",
    font_size=font_size,
    tab_size=tab_size,
    show_gutter=show_gutter,
    show_print_margin=show_print_margin,
    wrap=wrap,
    auto_update=True,
    readonly=readonly,
    min_lines=25,
    key="source_code_ace",
)

st.divider()


@st.cache_resource
def new_judge_client():
    return Judge0Client()


judge_client = new_judge_client()

languages_data = judge_client.get_languages()
language_map = {language["name"]: language["id"] for language in languages_data}
st.subheader("執行驗證測資程式")


language = st.selectbox(
    "選擇程式語言",
    options=list(sorted(language_map.keys(), reverse=True)),  # noqa: C413
    index=8,
)
language_id = language_map[language]
input_block, ans_block = st.columns(2)
with input_block:
    st.write("測試測資")
    in_data = st_ace(in_data, height=200, auto_update=True, key="in_data_ace")

with ans_block:
    st.write("測資答案")
    ans_data = st_ace(ans_data, height=200, auto_update=True, key="ans_data_ace")


if st.button("執行"):
    with st.spinner("執行中..."):
        submission = judge_client.create_submission(
            source_code,
            language_id,
            stdin=in_data,
            expected_output=ans_data,
        )
        submission_id = submission["token"]
        submission = judge_client.get_submission(submission_id)
        while submission["status"]["id"] <= 2:
            submission = judge_client.get_submission(submission_id)
            st.toast(submission["status"]["description"])
            time.sleep(1)
        # st.write(submission)
        stdout = submission["stdout"]
        exec_time = submission["time"]
        exec_memory = submission["memory"]
        stderr = submission["stderr"]
        compile_output = submission["compile_output"]
        st.divider()
        if submission["status"]["id"] == 3:
            exec_time_block, exec_memory_block = st.columns(2)
            exec_time_block.metric(label="程式執行時間", value=f"{exec_time} 秒")
            if exec_memory > 1024:
                exec_memory = exec_memory / 1024
                exec_memory_block.metric(
                    label="記憶體使用量", value=f"{exec_memory:.2f} MB"
                )
            else:
                exec_memory_block.metric(
                    label="記憶體使用量", value=f"{exec_memory} KB"
                )
            st.divider()

        if submission["status"]["id"] == 3:
            st.success(submission["status"]["description"])
        else:
            st.error(submission["status"]["description"])
            st.json(submission)
        st.divider()

        if stderr:
            st.error(stderr)
            st.divider()

        if compile_output:
            st.error(compile_output)
            st.divider()

        if stdout:
            diff_left, diff_right = generate_diff(stdout, ans_data)
            st.subheader("程式輸出與測資答案差異")
            left_block, right_block = st.columns(2)
            with left_block:
                st.write("程式輸出:")
                st.caption("- 表示程式輸出錯誤")
                st_ace(
                    diff_left,
                    language="diff",
                    auto_update=True,
                    readonly=True,
                    theme=theme,  # type: ignore
                    key="left_block_ace",
                )

            with right_block:
                st.write("測資答案:")
                st.caption("+ 表示測資正確答案")
                st_ace(
                    diff_right,
                    language="diff",
                    auto_update=True,
                    readonly=True,
                    theme=theme,  # type: ignore
                    key="right_block_ace",
                )
