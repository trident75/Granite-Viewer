import pandas as pd
import streamlit as st

# Load the Excel file, skip the first row (header)
df = pd.read_excel('data.xlsx', header=0,dtype={'Kundennummer': str})

st.title('Urkundenbestand:')
st.write('Testkunden: 8991230001 - Arkham Kliniken, 8992340002 - Wayne Enterprises, 8993450003 - Polar Express GmbH, 8994560004 - Luftnummer AG, 8995670005 - Oversea Shipping')
### Sidebar ###
st.sidebar.text('Auswahl präzisieren:')
suchstring=st.sidebar.text_input('GP-Nummer oder Name eingeben')


filter_status= df['Status Original'].unique().tolist()
filter_dokart= df['Dokumentenart'].unique().tolist()

status_selection = st.sidebar.multiselect('Welche Urkunden sollen angezeigt werden?:',
                                    filter_status, default=filter_status)

dokart_selection = st.sidebar.multiselect('Welche Urkundenarten sollen angezeigt werden?',
                                  filter_dokart, default=filter_dokart)

st.write('Aktuelle Filter:',suchstring)


# Daten-Frame

st.dataframe(df.loc[
    ((df['Kundennummer']==suchstring) | (df['Kundenname']==suchstring))&
        (df['Status Original'].isin(status_selection))&
        (df['Dokumentenart'].isin(dokart_selection))
        ])

#st.dataframe(df)

