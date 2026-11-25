import streamlit as st
import pandas as pd
from google import genai

st.title("AI Data Analyst Assistant")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Clean text columns: remove extra spaces and make uppercase
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip().str.upper()

    st.subheader("Preview of your data")
    st.dataframe(df.head(10))

    st.subheader("Basic stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing values", int(df.isnull().sum().sum()))

    st.subheader("Ask a question about your data")
    question = st.text_input("Type your question here")

    if st.button("Get answer") and question:
        info = (
            f"Columns and types:\n{df.dtypes.to_string()}\n\n"
            f"First 5 rows:\n{df.head(5).to_string()}"
        )

        prompt = (
            "You are a Python pandas expert. A DataFrame named df is already loaded.\n\n"
            f"{info}\n\n"
            f"Question: {question}\n\n"
            "Write Python code that answers the question using df. "
            "The last line must be: result = <your answer>. "
            "Return ONLY the code. No explanation, no markdown."
        )

        client = genai.Client()
        with st.spinner("Thinking..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

        code = response.text.replace("```python", "").replace("```", "").strip()

        st.write("Code the AI wrote:")
        st.code(code, language="python")

        try:
            env = {"df": df.copy(), "pd": pd}
            try:
                result = eval(code, env)
            except SyntaxError:
                exec(code, env)
                result = env.get("result")

            st.write("Answer:")
            if isinstance(result, (pd.DataFrame, pd.Series)):
                st.dataframe(result)

                # Draw a bar chart when the answer has a label and a number
                chart_data = result.copy()
                if isinstance(chart_data, pd.Series):
                    chart_data = chart_data.to_frame()
                if len(chart_data.columns) >= 2 and chart_data.iloc[:, 1].dtype.kind in "if":
                    chart_data = chart_data.set_index(chart_data.columns[0])
                if chart_data.select_dtypes("number").shape[1] >= 1:
                    st.bar_chart(chart_data.select_dtypes("number"))
            else:
                st.write(result)
        except Exception as e:
            st.error(f"The code had an error: {e}")