import snowflake.connector
import pandas as pd
import streamlit as st

st.set_page_config(page_title="My Streamlit App", layout="wide", initial_sidebar_state="expanded")
# Create a connection object with your Snowflake credentials
conn = snowflake.connector.connect(
    user=st.secrets["usr"],
    password=st.secrets["pswrd"],
    account=st.secrets["acc"],
    warehouse='COMPUTE_WH',
    database='DEV_DB',
    schema='TEST_SCHEMA'
)
st.title('Hi :wave: Welcome!')
PRODUCT_LINE = ["CL", "PL"]
IN_PROD_LINE = st.sidebar.selectbox("PRODUCT LINE", PRODUCT_LINE)

qry = "SELECT DISTINCT PRODUCT_DESCRIPTION FROM TABLE (DEV_DB.TEST_SCHEMA.INSURANCE_TBL_FUNCTION ('','','','','',''))"
res = pd.read_sql(qry, conn)
INPROD_DESC = st.sidebar.multiselect("PRODUCT DESCRIPTION", ["Select All"] + res["PRODUCT_DESCRIPTION"].tolist(),default=["Select All"])
if "Select All" in INPROD_DESC:
    INPROD_DESC = res["PRODUCT_DESCRIPTION"].tolist()
    IN_PROD_DESC: str = ','.join(f"'{INPROD_DESC}'" for INPROD_DESC in INPROD_DESC)
else:
    IN_PROD_DESC: str = ','.join(f"'{INPROD_DESC}'" for INPROD_DESC in INPROD_DESC)

qry = "SELECT DISTINCT STATE FROM TABLE (DEV_DB.TEST_SCHEMA.INSURANCE_TBL_FUNCTION ('','','','','',''))"
res = pd.read_sql(qry, conn)
INSTATE = st.sidebar.multiselect("STATE", ["Select All"] + res["STATE"].tolist(),default=["Select All"])
if "Select All" in INSTATE:
    INSTATE = res["STATE"].tolist()
    STATE: str = ','.join(f"'{INSTATE}'" for INSTATE in INSTATE)
else:
    STATE: str = ','.join(f"'{INSTATE}'" for INSTATE in INSTATE)

#MIN_AGE = st.slider('MINIMUM AGE', 0, 100, 33)
MAX_AGE_MIN, MAX_AGE_MAX = st.sidebar.slider('MAXIMUM AGE (RANGE)', 0, 100, (25, 75))

date = st.sidebar.date_input('TO-DATE')


def run():
    query = f"SELECT * FROM TABLE (DEV_DB.TEST_SCHEMA.INSURANCE_TBL_FUNCTION ('{IN_PROD_LINE}','','','','','')) where PRODUCT_DESCRIPTION IN ({IN_PROD_DESC}) AND STATE IN ({STATE}) AND MAXIMUM_AGE BETWEEN ({MAX_AGE_MIN}) AND ({MAX_AGE_MAX})" #AND MINIMUM_AGE IN ({MIN_AGE})"
    results = pd.read_sql(query, conn)
    # Display the results in Streamlit
    st.write('OUTPUT IS HERE.!')
    df = st.dataframe(results)
    csv = results.to_csv(index=False).encode('utf-8')
    st.download_button(label='Download CSV', data=csv, file_name='data.csv', mime='text/csv')

if st.sidebar.button("Run Report"):
    run()
