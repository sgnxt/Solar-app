import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

st.set_page_config(page_title= "Solar App")

#SIDEBAR (CONTAINS INPUT)
with st.sidebar:
    st.header('SAVE WITH SOLAR')
    st.subheader('Fill in the input below')

    #inputs
    name= st.text_input('Name')
    streetname= st.text_input('Street name')
    streetnumber = st.number_input('Street number')
    monthlybill= st.number_input('Montly Bill Payment ($)')
    monthlyusage= st.number_input('Monthly electric usage (Kwh)')
    yearlyusage = st.number_input('Yearly electric usage')

##Sidebar styling
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #ff000050;
    }
</style>
""", unsafe_allow_html=True)

#st.write(name)
#st.write(streetname)
#st.write(streetnumber)
#st.write(monthlybill)
#st.write(monthlyusage)
#st.write(yearlyusage)

#variables for pandas
##Extra electricity 
currentavgelectricrate = (monthlybill/monthlyusage)
yearlybill = (yearlyusage * currentavgelectricrate)
monthlyavgbill = (yearlybill/12)

extraelec16 = 10602 - yearlyusage 
smy16 = (monthlyavgbill - 194)
rsmy16 = round(smy16, 2)
savings16= round((smy16/monthlyavgbill)*100,2)

extraelec20 = 12583 - yearlyusage 
smy20 = (monthlyavgbill - 231)
rsmy20 = round(smy20, 2)
savings20= round((smy20/monthlyavgbill)*100,2)

##DATAFRAME 1, 16 PANELS vs 20 PANELS 
d1 = {'SUNRUN 16 Panels':['Monthly Bill', 'Electric rate', 'Annual Production', 'More electricity', 'Offset (%)', 'Savings Monthly Year 1', 'Savings Percentage (%)', 'Monthly Extra Electricity', ], '':[194.0, 0.22, 10602, extraelec16, 105, rsmy16, savings16, round(extraelec16/12,2)]}  
d2 = {'SUNRUN 20 Panels':['Monthly Bill', 'Electric rate', 'Annual Production', 'More electricity', 'Offset (%)', 'Savings Monthly Year 1', 'Savings Percentage (%)', 'Monthly Extra Electricity', ], '':[231.0, 0.22, 12583, extraelec20, 125, rsmy20, savings20, round(extraelec20/12,2)]}  
df1 = pd.DataFrame(d1)
df2 = pd.DataFrame(d2)
    
col1, col2 = st.columns(2)
with col1:
    st.header("SUNRUN 16 Panels")
    st.dataframe(df1)
with col2: 
    st.header("SUNRUN 20 Panels")
    st.dataframe(df2)

#DATAFRAME 2 

##DATAFRAME TABLE WITHOUT SOLAR
#Create a list of 25 years, and carry out the percentage increase of 8%
a = list(range(1,26))
a[0] = 298.47
a[0] = (a[0] * 0.08) + a[0]
indexlength = range(1, len(a))
for i in indexlength: 
    a[i] = (a[i-1] * 0.08) + a[i-1]
    i += 1
#Assign the list to a dataframe, and start the index at 1, letting the index represent the years
df3 = pd.DataFrame(a, columns=['Monthly Payment'])
df3.index = df3.index + 1
#st.dataframe(df3)

##DATAFRAME TABLE WITH SOLAR
b = list(range(1,26))
b[0] = 194
indexlength = range(1, len(b))
for i in indexlength: 
    b[i] = (b[i-1] * 0.035) + b[i-1]
    i += 1
df4 = pd.DataFrame(b, columns=['Monthly Payment'])
df4.index = df4.index + 1

st.header('What will it look like in 25 years?')
col3, col4 = st.columns(2)
with col3:
    st.subheader("Without Solar (100% offset)")
    st.dataframe(df3)
with col4:
    st.subheader("With Solar (105% offset)")
    st.dataframe(df4)

st.subheader("So how much do you save in 25 years by switching to Solar? (105% offset)")
suma = 0
for i in a:
    suma += i
    i += 1
sumb = 0
for i in b:
    sumb += i
    i += 1
c = ((suma - sumb)*12)
c = round(c,2)
st.metric(label="Amount saved in $", value=c)

##DATAFRAMES 25%offset
higheroffsetbill = (12583 * currentavgelectricrate)/12

###Without solar
d = list(range(1,26))
d[0] = higheroffsetbill
d[0] = (d[0] * 0.08) + d[0]
indexlength = range(1, len(d))
for i in indexlength: 
    d[i] = (d[i-1] * 0.08) + d[i-1]
    i += 1
df5 = pd.DataFrame(d, columns=['Monthly Payment'])
df5.index = df5.index + 1

###With Solar
e = list(range(1,26))
e[0] = 231
indexlength = range(1, len(e))
for i in indexlength: 
    e[i] = (e[i-1] * 0.035) + e[i-1]
    i += 1
df6 = pd.DataFrame(e, columns=['Monthly Payment'])
df6.index = df5.index + 1

col5, col6 = st.columns(2)
with col5:
    st.subheader("Without Solar (125% offset)")
    st.dataframe(df5)
with col6:
    st.subheader("With Solar (125% offset)")
    st.dataframe(df6)
sumc = 0
for i in d:
    sumc += i
    i += 1
sumd = 0
for i in e:
    sumd += i
    i += 1
f = ((sumc - sumd)*12)
f = round(f,2)
st.subheader('So how much do you save in 25 years by switching to Solar? (125% offset)')
st.metric(label="Amount saved in $", value=f)