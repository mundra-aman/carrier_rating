import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

import streamlit as st
import plotly
import plotly.express as px


st.set_page_config(page_title='Carrier-Master', 
                   layout='wide',
                   #initial_sidebar_state=st.session_state.get('sidebar_state', 'collapsed'),
                )

st.image("img.png", use_column_width=True )

st.sidebar.title("❄️ FMCSA Cheatsheet 📄")
st.sidebar.caption("Made by an [Ungifted Amateur](https://www.linkedin.com/in/siavash-yasini/)")
st.sidebar.caption("Check out the accompanying Snowflake tutorial [here](https://medium.com/snowflake/the-ungifted-amateurs-guide-to-snowflake-449284e4bd72).")

with st.sidebar.expander("See My Other Streamlit Apps"):
    st.caption("Sophisticated Palette: [App](https://sophisticated-palette.streamlit.app/) 🎈,  [Blog Post](https://blog.streamlit.io/create-a-color-palette-from-any-image/) 📝")
    st.caption("Wordler: [App](https://wordler.streamlit.app/) 🎈,  [Blog Post](https://blog.streamlit.io/the-ultimate-wordle-cheat-sheet/) 📝")
    st.caption("Koffee of the World: [App](https://koffee.streamlit.app/) 🎈")
    
with st.sidebar.expander("ℹ️ **Latest Snowflake Release Notes**"):
    st.markdown("""Stay frosty and keep up with the coolest updates on the Snowflake website [here](https://docs.snowflake.com/en/release-notes/new-features).""")
cols = st.columns(2)

with st.sidebar.expander("🗺 Legend", expanded=True):
    st.markdown("""
    - Text inside `[ BRACKETS ]` indicates *optional parameters* that can be omitted. Drop carefully!
    - Text inside `{ CURLY | BRACKETS }` indicates *available options* for the command. Choose wisely!   
    - Text inside `< angle.brackets >` indicates *entity names* (e.g. table, schema, etc.). Pick responsibly!
    - The [☁️](https://docs.snowflake.com/) icon in each section will snow-flake you to the relevant section on the documentation website.  
    """)

st.sidebar.info("""
Note: This online cheatsheet for Snowflake is based on materials from the [Snowflake documentation website](https://docs.snowflake.com/). 
    The content and logo of Snowflake used in this application are the intellectual property of Snowflake Inc. and are used here with proper attribution. 
    This cheatsheet is not affiliated with or endorsed by Snowflake Inc. Please refer to the official Snowflake documentation for detailed information and updates.
"""
)


st.sidebar.success("""
This guide is limited in scope and offers just a glimpse into the expansive array of Snowflake's *cool* features—pun intended. 
The reason for this is threefold:  
1. Time is finite, as suggested by modern physics. 
2. Snowflake is breaking the laws of physics by adding features faster than the speed of light, making it impossible for any mortal to catch up.
3. I am a mortal.

But here's where you come in, my knowledgeable friend. You likely have insights, cool features, or corrections that could benefit the entire Snowflake community. 
As an open-source project, I warmly (or should I say coolly? 🤔) welcome and eagerly look forward to your invaluable contribution. 
Don't hesitate to jump to the GitHub repository to open an issue or start a pull request (PR) to suggest additions or modifications to the content. 
Your expertise can help us keep this guide up-to-date and comprehensive.
"""
)

with st.sidebar.expander("Acknowledgments"):
    st.markdown("""
    I am incredibly grateful to my amazing Snowflake mentor, [Sang Hai](https://www.linkedin.com/in/sangvhai/), who is always sharing his extensive knowledge about the exciting and innovative features of Snowflake and guiding me in implementing them in my work. 
    I would also like to express my heartfelt appreciation to [Kathryn Reck Harris](https://www.linkedin.com/in/kathrynreck/) and [Varun Chavakula](https://www.linkedin.com/in/varunchavakula/), my awesome Snowflake buddies, who always share the exhilarating ride of exploring Snowflake and provide invaluable insights and support.

    Lastly, a special thanks to [**Jessica Smith**](https://www.linkedin.com/in/jessica-s-095a861b3/), a true champion of the Streamlit platform, for always encouraging me to create fun things in Streamlit and for her continuous support within the vibrant Streamlit community.
    """)
    
    
    
    
#fmcsa_offline = pd.read_parquet('FMCSA_CENSUS1_2023Nov.parquet.gzip')

#fmcsa_online = pd.read_csv('safer_online.csv')
#fmcsa_online = fmcsa_online.rename(columns={"USDOT Number": "DOT_NUMBER"})

#state_codes = pd.read_csv('state_codes.csv')

#merge = pd.merge(fmcsa_offline, fmcsa_online, on='DOT_NUMBER', how='inner')

@st.cache_data
def fmcsa_on_off():
    fmcsa_on_off = pd.read_parquet('fmcsa_on_off.parquet.gzip')
    return fmcsa_on_off

fmcsa_on_off = fmcsa_on_off()

cols = ["DOT_NUMBER", "MC/MX/FF Number(s)", "LEGAL_NAME", "DBA_NAME", "CARRIER_OPERATION", "NBR_POWER_UNIT", 
        "DRIVER_TOTAL", "PHY_STREET", "PHY_CITY", "PHY_STATE", "STATE", "PHY_ZIP", "PHY_COUNTRY", "MAILING_STREET",
        "MAILING_CITY", "MAILING_STATE", "MAILING_ZIP", "MAILING_COUNTRY", "TELEPHONE", "EMAIL_ADDRESS", 
        "MCS150_DATE", "Entity Type", "Operating Status", "Out of Service Date", "Phone" ]

fmcsa_on_off = fmcsa_on_off.filter(cols)

fmcsa_on_off['DRIVER_TOTAL'] = fmcsa_on_off['DRIVER_TOTAL'].fillna(0).astype(int)
fmcsa_on_off['NBR_POWER_UNIT'] = fmcsa_on_off['NBR_POWER_UNIT'].fillna(0).astype(int)


    



container = st.container(border=True)
container.header("🗄 Database", help="The gigantic storage drawer that holds many collections of your data together.")
USDOT, MC, Co, tips = container.tabs(["USDOT", "MC/MC-X", "Co", "❄️"])

with USDOT:
    st.caption("Search with USDOT")
    st.text_input("Enter USDOT number", "10020", key="usdot") #10020
    usdot = fmcsa_on_off[(fmcsa_on_off['DOT_NUMBER'] == int(st.session_state.usdot))].reset_index(drop=True)
    if not usdot.empty:
        #st.dataframe(data=usdot, width=900, height=None, use_container_width=False, hide_index=True)           
        for _, row in usdot.iterrows():
            col1, col2 = st.columns(2)  # Create two columns

            for idx, (key, value) in enumerate(row.items()):
                if idx % 2 == 0:  # Display in col1 for even index (0-based)
                    with col1:
                        st.caption(f'{key}: {value}')
                else:  # Display in col2 for odd index
                    with col2:
                        st.caption(f'{key}: {value}')
                        
    else:
        st.write("USDOT not found")

with MC:
    st.caption("Search with MC")
    st.text_input("Enter MC number", key="mc") #187460
    mc = fmcsa_on_off[(fmcsa_on_off['MC/MX/FF Number(s)'] == (f"MC-{st.session_state.mc}"))].reset_index(drop=True)
    if not mc.empty:
        #st.dataframe(mc)
        for _, row in mc.iterrows():
            col1, col2 = st.columns(2)  # Create two columns

            for idx, (key, value) in enumerate(row.items()):
                if idx % 2 == 0:  # Display in col1 for even index (0-based)
                    with col1:
                        st.caption(f'{key}: {value}')
                else:  # Display in col2 for odd index
                    with col2:
                        st.caption(f'{key}: {value}')
    else:
        st.write("MC not found")

with Co:
    st.caption("Search with Company name")
    st.text_input("Enter company name", key="name") # 'BLUE BIRD'
    legal_name = fmcsa_on_off[(fmcsa_on_off['LEGAL_NAME'].str.contains(st.session_state.name))].reset_index(drop=True)
    st.write(legal_name)


st.header("Search with State/Cities")

st.write("Select States/Cities")

states = fmcsa_on_off[(fmcsa_on_off['PHY_COUNTRY'] == ("US")) & (~fmcsa_on_off['STATE'].isnull())]
distinct_states = states['STATE'].unique()

state = st.selectbox("Please select a US state", sorted(distinct_states.tolist()))



cities = states[(states['STATE'] == state)]
distinct_cities = cities['PHY_CITY'].unique()
cities = st.multiselect("Please select the US cities", sorted(distinct_cities.tolist()))


states_cities = fmcsa_on_off[(fmcsa_on_off['STATE'] == (f"{(state)}")) & (fmcsa_on_off['PHY_CITY'].isin(cities) )].reset_index(drop=True).head(5) 

st.write(states_cities)




        
        

        
        
    
        
        
        
        
        
_, exp_col, _ = st.columns([1,3,1])

        
cols = st.columns(2)


def st_code_block(url, caption=None, code=None):
    # prefill the http address for the sql-reference url
    if not url.startswith("https"):
        url = f"https://docs.snowflake.com/en/sql-reference/sql/{url}"
    st.caption(f"[☁️]({url}) {caption}")
    st.code(code, language="sql")

    
def database_segment():
    st.header("🗄 Database", help="The gigantic storage drawer that holds many collections of your data together.")
    create_tab, alter_tab, drop_tab, describe_tab, show_tab, tips_tab = \
        st.tabs(["MC", "USDOT", "DROP", "DESCRIBE", "SHOW", "❄️"])
    with create_tab:
        st.header("Search with MC")

        mc = fmcsa_on_off[(fmcsa_on_off['MC/MX/FF Number(s)'] == ("MC-187460"))].reset_index(drop=True)

        if not mc.empty:
            st.dataframe(mc)
        else:
            st.write("MC not found")


    with alter_tab:
        st.header("Search with MC")

        mc = fmcsa_on_off[(fmcsa_on_off['MC/MX/FF Number(s)'] == ("MC-187460"))].reset_index(drop=True)

        if not mc.empty:
            st.dataframe(mc)
        else:
            st.write("MC not found")

            
    with drop_tab:
        st_code_block("drop-database", "remove a database",
        """
        DROP DATABASE [ IF EXISTS ] <database_name> 
        """
        )

    with describe_tab:
        st_code_block("desc-database", "describe the database (e.g. show schemas)",
        """
        DESC DATABASE <database_name>
        """
        )

    with show_tab:
        st_code_block("show-databases", "show available databases",
        """
        SHOW DATABASES [ HISTORY ] [ LIKE '<pattern>' ]
        """
        )

    with tips_tab:
    
        st.markdown("""
        💡 **Tips**
        - Follow consistent and meaningful naming conventions for `DATABASE` objects.
        - When you create a new Snowflake database, it also generates two schemas: `PUBLIC` (the default schema) and `INFORMATION_SCHEMA` (containing views and table functions for querying metadata across objects).
        - Use a `TRANSIENT` `DATABASE` to isolate temporary data, and provide a dedicated space for intermediate results or temporary tables during specific analysis or transformation tasks.
        - Utilize zero-copy cloning using `CREATE DATABASE <name> CLONE <source_db>` for efficient, space-saving `DATABASE` copies.
        - Continuously analyze query and resource usage patterns to fine-tune `DATABASE` parameters for optimal performance and cost efficiency.
        """
        )
    


def stage_segment():
    st.header("🚉 Stage", help="The platform where the data sits before moving in and out of Snowflake.")
    
    create_tab, alter_tab, drop_tab, describe_tab, show_tab, list_tab, tips_tab = \
        st.tabs(["CREATE", "ALTER", "DROP", "DESCRIBE", "SHOW", "LIST", "❄️"])
    
    with create_tab:
        
        st_code_block("create-stage", "create or replace an internal stage",
        """
        CREATE [ OR REPLACE ] [ TEMPORARY ] STAGE [ IF NOT EXISTS ] <internal_stage_name>
            [ DIRECTORY = ( ENABLE = { TRUE | FALSE }
                  [ REFRESH_ON_CREATE =  { TRUE | FALSE } ] ) ]
            [ FILE_FORMAT = ( TYPE = { CSV | JSON | AVRO | ORC | PARQUET | XML } ) ]
            [ COPY_OPTIONS = ( ON_ERROR = { CONTINUE | SKIP_FILE | ABORT_STATEMENT }) ]
        """
        )

       

    with alter_tab:
        
        
        st_code_block("alter-stage", "rename a stage",
        """
        ALTER STAGE [ IF EXISTS ] <name> RENAME TO <new_stage_name>
        """
        )

        st_code_block("alter-stage", "change directory settings for the stage",
        """
        ALTER STAGE [ IF EXISTS ] <name> SET DIRECTORY = ( { ENABLE = TRUE | FALSE } )

        ALTER STAGE [ IF EXISTS ] <name> REFRESH [ SUBPATH = '<relative-path>' ]
        """
        )

        st_code_block("alter-stage", "change internal stage parameters",
        """
        ALTER STAGE [ IF EXISTS ] <name> SET {
            [ FILE_FORMAT = ( TYPE = { CSV | JSON | AVRO | ORC | PARQUET | XML } ) ]
            [ COPY_OPTIONS = ( ON_ERROR = { CONTINUE | SKIP_FILE | ABORT_STATEMENT } )  ]
            [ COMMENT = '<string_literal>' ] 
        }
        """
        )


        s3_tab, azure_tab, gcp_tab = st.tabs(["Amazon S3", "Microsoft Azure", "Google Cloud Storage"])
        with s3_tab:
            st_code_block("alter-stage", "change external stage parameters for Amazon S3",
            """
            ALTER STAGE [ IF EXISTS ] <name> SET {
                [ URL = 's3://<bucket>[/<path>/]' ]
                [ { STORAGE_INTEGRATION = <integration_name> } | { CREDENTIALS = ( {  { AWS_KEY_ID = '<string>' AWS_SECRET_KEY = '<string>' [ AWS_TOKEN = '<string>' ] } | AWS_ROLE = '<string>'  } ) } ]
                [ ENCRYPTION = ( [ TYPE = 'AWS_CSE' ] [ MASTER_KEY = '<string>' ] |
                                 [ TYPE = 'AWS_SSE_S3' ] |
                                 [ TYPE = 'AWS_SSE_KMS' [ KMS_KEY_ID = '<string>' ] |
                                 [ TYPE = 'NONE' ] ) ]
                [ FILE_FORMAT = ( TYPE = { CSV | JSON | AVRO | ORC | PARQUET | XML } ) ]
                [ COPY_OPTIONS = ( ON_ERROR = { CONTINUE | SKIP_FILE | ABORT_STATEMENT } )  ]
                [ COMMENT = '<string_literal>' ] }
            }
            """
            )

        with azure_tab:
            st_code_block("alter-stage", "change external stage parameters for Microsoft Azure",
            """
            ALTER STAGE [ IF EXISTS ] <name> SET {
                [ URL = 'azure://<account>.blob.core.windows.net/<container>[/<path>/]' ]
                [ { STORAGE_INTEGRATION = <integration_name> } | { CREDENTIALS = ( [ AZURE_SAS_TOKEN = '<string>' ] ) } ]
                [ ENCRYPTION = ( [ TYPE = { 'AZURE_CSE' | 'NONE' } ] [ MASTER_KEY = '<string>' ] ) ]
                [ FILE_FORMAT = ( TYPE = { CSV | JSON | AVRO | ORC | PARQUET | XML } ) ]
                [ COPY_OPTIONS = ( ON_ERROR = { CONTINUE | SKIP_FILE | ABORT_STATEMENT } )  ]
                [ COMMENT = '<string_literal>' ] }
            }
            """
            )

        with gcp_tab:
            st_code_block("alter-stage", "change external stage parameters for Google Cloud Storage",
            """
            ALTER STAGE [ IF EXISTS ] <name> SET {
                [ URL = 'gcs://<bucket>[/<path>/]' ]
                [ STORAGE_INTEGRATION = <integration_name> } ]
                [ ENCRYPTION = ( [ TYPE = 'GCS_SSE_KMS' ] [ KMS_KEY_ID = '<string>' ] | [ TYPE = 'NONE' ] ) ]
                [ FILE_FORMAT = ( TYPE = { CSV | JSON | AVRO | ORC | PARQUET | XML } ) ]
                [ COPY_OPTIONS = ( ON_ERROR = { CONTINUE | SKIP_FILE | ABORT_STATEMENT } )  ]
                [ COMMENT = '<string_literal>' ] }
            }
            """
            )


    with drop_tab:
        st_code_block("drop-stage", "remove an existing stage",
        """
        DROP STAGE [ IF EXISTS ] <name> 
        """
        )


    with describe_tab:
        st_code_block("desc-stage", "describe the properties of the stage (e.g. file format, copy, location)",
        """
        DESC STAGE <name> 
        """
        )

    with show_tab:
        st_code_block("show-stages", "show available stages",
        """
        SHOW STAGES [ LIKE '<pattern>' ]
            [ IN
                 {
                   ACCOUNT                  |
                   DATABASE                 |
                   DATABASE <database_name> |
                   SCHEMA                   |
                   SCHEMA <schema_name>     |
                   <schema_name>
                 }
            ]
        """
        )

    with list_tab:
        st_code_block("list", "return a list of files that have been staged",
        """
        LIST { 
                @[<namespace>.]<int_stage_name>[/<path>]
                | @[<namespace>.]%<table_name>[/<path>]
                | @~[/<path>]
             } 
             [ PATTERN = '<regex_pattern>' ]
        """
        )

    with tips_tab:
        st.markdown("""
        💡 **Tips**
        - See [this guide](https://docs.snowflake.com/en/user-guide/data-load-s3-config) for various options to configure secure access to a private Amazon S3 bucket. 
        - Use `DIRECTORY` tables to efficiently store and catalog staged files, allowing seamless querying to retrieve URLs for the staged files, along with other essential metadata.
        - Use `EXTERNAL` tables when you want to access and query data that resides in external cloud storage (e.g. AWS S3) without copying or moving the data into Snowflake.
        """)




left_column_defaults = [
    "🗄 database"
    ]

right_column_defaults = [
    "🚉 stage"
    ]

all_segments = left_column_defaults + right_column_defaults

def default_layout():
    st.session_state["layout_left_column"] = left_column_defaults
    st.session_state["layout_right_column"] = right_column_defaults

custom_layout = st.sidebar.expander("🧑‍🎨 Customize Layout")
with custom_layout:
    st.button("Default Layout", on_click=default_layout)
    side_left_col, side_right_col = st.columns(2)
    left_col_segments = side_left_col.multiselect("Left Column", 
                          options=all_segments, 
                          default=left_column_defaults,
                          key="layout_left_column")
                          
    right_col_segments = side_right_col.multiselect("Right Column", 
                          options=all_segments, 
                          default=right_column_defaults,
                          key="layout_right_column")

segment_dict = {
    "🗄 database": database_segment,
    "🚉 stage": stage_segment
}

with cols[0]:
    for seg in left_col_segments:
        segment_dict[seg]()
    

with cols[1]:
    for seg in right_col_segments:
        segment_dict[seg]()
        
        

# Create a choropleth map using Plotly Express
data =  states.groupby(['PHY_STATE']).size().reset_index(name='COUNT')

map_fig = px.choropleth(data, 
                        locations='PHY_STATE', 
                        locationmode='USA-states',
                        color='COUNT',
                        scope="usa",
                        #title='US State Map',
                        color_continuous_scale="Viridis",
                        )

map_fig.update_layout({
    #'paper_bgcolor': "red",
    #'bgcolor': "red",
    'height': 700  # Adjust the height as needed
})

st.plotly_chart(map_fig, use_container_width=True)
        


st.header("Frequently asked questions")

_, exp_col, _ = st.columns([1,3,1])
with exp_col:
    with st.expander("**📖 How do you obtain data on freight businesses?**"):
         st.markdown("""We source the majority of our data directly from two organizations within the U.S. Department of Transportation (DOT): the Federal Motor Carrier Safety Administration (FMCSA) and the National Highway Traffic Safety Administration (NHTSA).""")
       

    with st.expander("**📖 How is the Safety Score determined?**"):
         st.markdown("""The Safety Score is a comprehensive measure of a carrier's overall safety performance. It considers SMS BASIC measures and safety ratings to quickly communicate a carrier's safe operating performance relative to their peer group.""")

st.image("footer.png", use_column_width=True )
