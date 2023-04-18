import pandas as pd
import streamlit as st
#import xlsxwriter
import io

buffer = io.BytesIO()

# Load the Excel file, skip the first row (header)
df = pd.read_excel('data.xlsx', header=0,dtype={'Kundennummer': str, 'Kontonummer': str, 'Betrag': str})

#Titel
st.title('Urkundenbestand:')
st.write('Testkunden: 8991230001 - Arkham Kliniken, 8992340002 - Wayne Enterprises, 8993450003 - Polar Express GmbH, 8994560004 - Luftnummer AG, 8995670005 - Oversea Shipping')

### Sidebar ###
st.sidebar.header('Auswahl präzisieren:')
suchstring=st.sidebar.text_input('GP-Nummer oder Name eingeben')

#Filter-Definition
filter_status= df['Status Original'].unique().tolist()
filter_dokart= df['Dokumentenart'].unique().tolist()

#Filter-Eingabe-Elemente
status_selection = st.sidebar.multiselect('Welche Urkunden sollen angezeigt werden?:',
                                    filter_status, default=filter_status)

dokart_selection = st.sidebar.multiselect('Welche Urkundenarten sollen angezeigt werden?',
                                  filter_dokart, default=filter_dokart)

#st.write('Aktuelle Filter:',suchstring, status_selection, dokart_selection)
st.write('Aktuelle Filter:')
st.info(suchstring)

filter_data=(df.loc[
    ((df['Kundennummer']==suchstring) | (df['Kundenname']==suchstring))&
        (df['Status Original'].isin(status_selection))&
        (df['Dokumentenart'].isin(dokart_selection))
        ])

# Daten-Frame
st.dataframe(filter_data, use_container_width=True)

with pd.ExcelWriter(buffer,engine='xlsxwriter') as writer:
    filter_data.to_excel(writer, sheet_name=suchstring, index=False)

writer.save()

st.sidebar.download_button(
    label='Download XLSX',
    data=buffer,
    file_name=('Urkunden-Auswahl_'+suchstring+'.xlsx'),
    mime='application/vnd.ms-excel'
     )