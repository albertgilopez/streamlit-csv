"""Streamlit app for data analysis.

Run like this:
> PYTHONPATH=. streamlit run data_science/indexing.py
"""
import streamlit as st

from agent_app import query_agent, create_agent

st.title("👨‍💻 Pregunta a tu CSV")

st.write("Cargua tu archivo CSV o Excel a continuación.")

data_file = st.file_uploader("Sube aquí un CSV o un Excel", type=["csv", "xlsx"])

query = st.text_area("Escribe aquí tu pregunta")

if st.button("Enviar Pregunta"):
    if data_file is not None and query:
        with st.spinner('Trabajando en tu respuesta...'):
            try:
                file_type = 'csv' if data_file.type == 'text/csv' else 'excel'
                agent = create_agent(data_file, file_type)
                response = query_agent(agent=agent, query=query)
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload a CSV or Excel file and enter a query.")