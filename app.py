import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Company Policy RAG",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Company Policy RAG Assistant")

tab1, tab2 = st.tabs(["Ask Questions", "Check Contradictions"])

# --------------------------
# TAB 1
# --------------------------

with tab1:

    question = st.text_input(
        "Ask a question about company policies:"
    )

    if st.button("Ask"):

        if question:

            response = requests.post(
                f"{API_URL}/ask",
                json={"question": question}
            )

            result = response.json()

            st.subheader("Answer")
            st.success(result["answer"])

            if result["documents_used"]:

                st.subheader("Documents Used")

                for doc in result["documents_used"]:
                    st.write(f"📄 {doc}")

            if result["citations"]:

                st.subheader("Citations")

                for citation in result["citations"]:

                    with st.expander(f"{citation['source']} · Chunk {citation['chunk']} · Page {citation['page']}"):

                        st.write(f"**Source file:** {citation['source']}")
                        st.write(f"**Page:** {citation['page']}")
                        st.write(f"**Chunk:** {citation['chunk']}")

                        st.write("**Snippet used:**")
                        st.write(citation["snippet"])

            else:
                st.warning("No citations returned.")

# --------------------------
# TAB 2
# --------------------------

with tab2:

    files = [
        "01_Code_of_Conduct.pdf",
        "02_Leave_Policy.pdf",
        "03_Work_From_Home_Policy.pdf",
        "04_IT_Security_Policy.pdf",
        "05_Attendance_Policy.pdf"
    ]

    doc1 = st.selectbox(
        "Document 1",
        files
    )

    doc2 = st.selectbox(
        "Document 2",
        files,
        index=1
    )

    if st.button("Check Contradiction"):

        response = requests.post(
            f"{API_URL}/contradict",
            json={
                "doc1": doc1,
                "doc2": doc2
            }
        )

        result = response.json()

        if result["conflict"]:

            st.error("⚠️ Contradiction Found")

            st.write(f"### Topic")
            st.write(result["topic"])

            st.write(f"### Reason")
            st.write(result["reason"])

        else:

            st.success("✅ No Contradiction Found")

            st.write(result["reason"])