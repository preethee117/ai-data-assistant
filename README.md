\# AI Data Analyst Assistant



Upload a CSV file and ask questions in plain English. The app uses an AI model to write pandas code, runs it on the full dataset, and shows the answer with a chart.



\## Features

\- Upload any CSV file

\- Automatic data cleaning (extra spaces, inconsistent capitalisation)

\- Basic stats: rows, columns, missing values

\- Ask questions in plain English

\- Shows the pandas code the AI wrote, so every answer can be verified

\- Automatic bar chart for grouped results



\## How it works

1\. The app sends the AI only the column names, data types and first 5 rows.

2\. The AI writes pandas code to answer the question.

3\. The code runs locally on all rows, so the numbers are exact.



\## Tech stack

Python, Streamlit, pandas, Google Gemini API



\## Run it locally

1\. Install the libraries: `pip install -r requirements.txt`

2\. Get a free API key from Google AI Studio

3\. Set the key: `set GEMINI\_API\_KEY=your-key` (Windows)

4\. Start the app: `python -m streamlit run app.py`



\## Example

Question: What is the placement rate for each department?

Result: a table and bar chart (for example, AI \& DS 45.2%, ECE 30.8%).



\## Note

The AI-generated code runs on your own machine. Use this app only with your own data and not as a public service.

