import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

import streamlit as st


fmcsa_offline = pd.read_parquet('FMCSA_CENSUS1_2023Nov.parquet.gzip')

fmcsa_online = pd.read_csv('safer_online.csv')
fmcsa_online = fmcsa_online.rename(columns={"USDOT Number": "DOT_NUMBER"})

state_codes = pd.read_csv('state_codes.csv')

merge = pd.merge(fmcsa_offline, fmcsa_online, on='DOT_NUMBER', how='inner')
fmcsa_on_off = pd.merge(merge, state_codes, on='PHY_STATE', how='left')

cols = ["DOT_NUMBER", "MC/MX/FF Number(s)", "LEGAL_NAME", "DBA_NAME", "CARRIER_OPERATION", "NBR_POWER_UNIT", 
        "DRIVER_TOTAL", "PHY_STREET", "PHY_CITY", "PHY_STATE", "STATE", "PHY_ZIP", "PHY_COUNTRY", "MAILING_STREET",
        "MAILING_CITY", "MAILING_STATE", "MAILING_ZIP", "MAILING_COUNTRY", "TELEPHONE", "EMAIL_ADDRESS", 
        "MCS150_DATE", "Entity Type", "Operating Status", "Out of Service Date", "Phone" ]

fmcsa_on_off = fmcsa_on_off.filter(cols)

fmcsa_on_off['DRIVER_TOTAL'] = fmcsa_on_off['DRIVER_TOTAL'].fillna(0).astype(int)
fmcsa_on_off['NBR_POWER_UNIT'] = fmcsa_on_off['NBR_POWER_UNIT'].fillna(0).astype(int)



st.header("Search with MC")

mc = fmcsa_on_off[(fmcsa_on_off['MC/MX/FF Number(s)'] == ("MC-187460"))].reset_index(drop=True)

if not mc.empty:
    st.dataframe(mc)
else:
    st.write("MC not found")
    

    
    
st.header("Search with Company name")

st.text_input("Enter company name", key="name") # 'BLUE BIRD'
st.session_state.name
legal_name = fmcsa_on_off[(fmcsa_on_off['LEGAL_NAME'].str.contains(st.session_state.name))].reset_index(drop=True)
st.write(legal_name)


st.header("Search with State/Cities")

st.write("Select States/Cities")

states = fmcsa_on_off[(fmcsa_on_off['PHY_COUNTRY'] == ("US"))]
distinct_states = states['STATE'].unique()
state = st.selectbox("Please select a US state", sorted(distinct_states.tolist()))

cities = states[(states['STATE'] == state)]
distinct_cities = cities['PHY_CITY'].unique()
cities = st.multiselect("Please select the US cities", sorted(distinct_cities.tolist()))


states_cities = fmcsa_on_off[(fmcsa_on_off['STATE'] == (f"{(state)}")) & (fmcsa_on_off['PHY_CITY'].isin(cities) )].reset_index(drop=True).head(5) 

st.write(states_cities)
