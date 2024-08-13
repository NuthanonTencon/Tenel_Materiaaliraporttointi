
import streamlit as st
import pandas as pd
import io

uploaded_file = st.file_uploader("Materiaalikohtainen raportti.xlsx", type="xlsx")
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df = df.drop(df.index[0:3])

    columns_to_drop = [0,1,2,4,5,8]  # Drop columns at indices 1 and 2
    df = df.iloc[:, [i for i in range(len(df.columns)) if i not in columns_to_drop]]
    df = df.fillna(method='ffill')
    df.columns = df.iloc[0]
    df = df[1:]
    df.insert(0, 'Elementtityyppi', df["Elementtitunnus"].str.split('-', n=1, expand=True)[0])

    towrite = io.BytesIO()
    with pd.ExcelWriter(towrite, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    towrite.seek(0)

    st.download_button(
            label="Lataa Processoitu data",
            data=towrite,
            file_name="Materiaalikohtainen raportti prosessoitu.xlsx",
        )
