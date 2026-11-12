import streamlit as st
from app.ingest import ingest
from app.generate import generate_test
from app.grade import grade_test

import tempfile, os
from pathlib import Path


st.title("QuizzMe")
st.write("Upload a document and test yourself.")
uploaded = st.file_uploader("Document", type=["pdf", "txt"])
difficulty = st.selectbox(
    "Difficulty",
    ["recall", "understand", "apply"],
    index=1,
    help="Recall: facts from the text. Understand: explain in your own words. Apply: use the idea in a new situation.",
)
n_questions = st.slider("Questions", 4, 20, 10)
skip_first =st.checkbox("Skip first page")
# st.write(uploaded, n_questions, difficulty, skip_first)
if st.button("Generate test"):
    if uploaded is None:
        st.warning("Upload a document first.")
    else:
        with st.spinner("Generating questions..."):
            try:
                data = uploaded.getvalue()        # the bytes
                suffix = Path(uploaded.name).suffix      # the extension
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
                    f.write(data)
                    path = f.name
                chunks = ingest(path)      # ingest the path
                quiz = generate_test(chunks, n_questions, difficulty, skip_first)        # generate_test with your widget values
                os.remove(path)
                st.session_state["quiz"] = quiz
            except ValueError as e:
                st.error(str(e))


if "quiz" in st.session_state:
    st.success(f"{len(st.session_state['quiz'].questions)} questions ready.")

if "quiz" in st.session_state:
    quiz = st.session_state["quiz"]
    answers = {}
    with st.form("test"):
        for i, q in enumerate(quiz.questions, start=1):
            st.markdown(f"**{i}. {q.question}**")
            if q.type == "mcq":
                answers[q.id] = st.radio(
                    "Your answer",
                    list(q.options),                                  
                    format_func=lambda k: f"{k}. {q.options[k]}",     
                    index=None,                                       
                    key=q.id,
                ) or ""
            else:
                answers[q.id] = st.text_area('Your answer', key=q.id)
        submitted = st.form_submit_button("Submit")
    if submitted:
        st.write(answers)

        with st.spinner("Grading..."):
            try:
                results, total = grade_test(quiz, answers)
                st.session_state["results"] = results
                st.session_state["total"] = total
                st.session_state["answers"] = answers
            except ValueError as e:
                st.error(str(e))

    if "results" in st.session_state:
        st.metric("Score", f"{st.session_state['total']:.0%}")
        for q, r in zip(quiz.questions, st.session_state["results"]):
            box = {"correct": st.success, "partially_correct": st.warning, "incorrect": st.error}[r.verdict]
            box(f"{q.question} ({r.score:.0%})")
            with st.expander("Details"):
                st.write(st.session_state["answers"][q.id])    # your answer
                st.write(r.feedback)    # feedback
                st.write(r.correct_answer)    # correct answer
                st.caption(f"Page {q.source_page}: {q.source_quote}")  # "Page X: quote"