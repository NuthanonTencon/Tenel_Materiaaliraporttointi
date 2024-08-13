
import streamlit as st
import pandas as pd
import io

uploaded_file = st.file_uploader("Materiaalikohtainen raportti.xlsx", type="xlsx")

def get_elementtityyppi(value):
    parts = value.split('-')
    if len(parts) > 1:
        return parts[0]
    else:
        return value[:2]


if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df = df.drop(df.index[0:3])

    columns_to_drop = [0,1,2,4,5,8]  # Drop columns at indices 1 and 2
    df = df.iloc[:, [i for i in range(len(df.columns)) if i not in columns_to_drop]]
    df = df.fillna(method='ffill')
    df.columns = df.iloc[0]
    df = df[1:]

    df['Elementtityyppi'] = df["Elementtitunnus"].apply(get_elementtityyppi)
    
    
    df = df[df['Elementtityyppi'].str.len() == 2]
    
    # Insert the 'Elementtityyppi' column into the DataFrame
    df.insert(0, 'Elementtityyppi', df.pop('Elementtityyppi'))

    towrite = io.BytesIO()
    with pd.ExcelWriter(towrite, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    towrite.seek(0)

    st.download_button(
            label="Lataa Processoitu data",
            data=towrite,
            file_name="Materiaalikohtainen raportti prosessoitu.xlsx",
        )
