import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# url = "https://docs.google.com/spreadsheets/d/1xFcacDgwKPaueNpctErxi0AdMLxnb_1Sh04OOiLi1D0/edit#gid=0"
st.set_page_config(page_title="KHK Business App", layout="wide")#, initial_sidebar_state="expanded"

conn = st.connection("gsheets", type=GSheetsConnection)

col1, col2 = st.columns([1, 1])
if st.button("See data"):
    data=conn.read(worksheet="KHK",ttl=5)
    data=data.dropna(how="all")
    st.write("Here is you data")
    st.dataframe(data)
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button(label='Download CSV', data=csv, file_name='KHKBusiness.csv', mime='text/csv')
    # st.download_button("Download file", data)
# st.dataframe(existing_data)
with st.form(key="form"):
  date=col1.date_input("Date")
  bill=col1.selectbox("Bill",options=["Issued","reciept"])
  Item=["Wedding ring","TV ring","Store ring","Photo ring","Heartin lockets","Dollars","Band rings","MC Ring","Bangles","Kada/Kaapu","Casting","Lot","Customised","Repair","Other entries"]
  Subitem=["Name","Stone-less","Hand cutting bangle","MC Bangle","MC Kaapu/Kada","Baby Kaapu","Punjabi Kada","Rings","Bangles","Studs","Casting","Flat ring","Bol TV ring","Miller ring","Bol wedding ring plain","Bol wedding ring Half cutting","Punjabi kaapu","Miller kaapu","None"]
  items=col1.selectbox("Item*",options=Item)
  newitem=col1.text_input("New Item ?")
  finalitem=items+""+newitem
  subItems=col1.selectbox("Sub Item",options=Subitem)
  newsubitem=col1.text_input("New Sub Item ?")
  finalsubitem=subItems+newsubitem
  shop=col2.selectbox("Shop/Customer",options=["MJ2","TSK","AK","Other"])
  newshop=col2.text_input("New shop ?")
  finalshop=shop+newshop
  melting =col2.text_input("Melting")
  weight=col2.text_input("Weight")
  # values = st.slider("Select 4 melting values", 0, 200, (0, 0, 0, 0))
  # melting=f"{values[0]}/{values[1]}/{values[2]}/{values[3]}"
  wastage=col2.text_input("Wastage")
  comments=col2.text_area("Comments")
  col2.markdown("**required*")
  submit_button = st.form_submit_button(label="Submit Details")
  if submit_button:
    # Check if all mandatory fields are filled
    if not finalitem or not finalshop:
        col2.warning("Item / shop is empty")
        st.stop()
    # elif existing_data["CompanyName"].str.contains(company_name).any():
    #     st.warning("A vendor with this company name already exists.")
    #     st.stop()
    else:
        # Create a new row of vendor data
        vendor_data = pd.DataFrame(
            [
                {
                    "Date": date,
                    "Bill": bill,
                    "Item": finalitem +" - " + finalsubitem,
                    "Shop": finalshop,
                    "Weight": weight,
                    "Melting": melting,
                    "Wastage": wastage,#onboarding_date.strftime("%Y-%m-%d"),
                    "Comments": comments
                }
            ]
        )

        # Add the new vendor data to the existing data
        data = conn.read(worksheet="KHK", ttl=5)
        data = data.dropna(how="all")
        updated_df = pd.concat([data, vendor_data], ignore_index=True)
        conn.update(worksheet="KHK", data=updated_df)
    st.balloons()
    st.success("Details successfully submitted sir!")

