import streamlit as st 
import datetime
import urllib.parse

st.header('GT Trading Co.')
st.divider()

date = st.date_input('Date', value=datetime.datetime.today(), format='DD/MM/YYYY')
vn = st.text_input('Vehicle No.')
pname = st.text_input('Party Name')
iname = st.text_input('Item Name')

def getInputs(e):
    data = []
    for x in range(1,e+1):
        col1, col2 = st.columns(2)

        z = col1.number_input('Qty.',key='q-'+str(x),step=1,value=0)
        y = col2.number_input('Rate',key='r-'+str(x), value=0)

        data.append([z,y])
    
    return data

nitems = st.number_input('No. of Entries', step=1, value=1)
items = getInputs(nitems)

comm = st.number_input('Commission', value=0)

frtcol, ftypecol = st.columns([0.8,0.2])

frt = frtcol.number_input('Freight', value=0)
ftyp = ftypecol.selectbox('Type',['Rate','Total'],key='fsel')

expcol, etypecol = st.columns([0.8,0.2])

exp = expcol.number_input('Expense', value=5)
etyp = etypecol.selectbox('Type',['Rate','Total'],key='esel')

post = st.number_input('Post', value=10)

def calculate():

    i_str = ''

    for i,item in enumerate(items):
        items[i].append(item[0]*item[1])
        i_str += str(item[0])+' @ '+str(item[1]) + ' = ' + str(item[2]) + '\n'

    total = sum([x[2] for x in items])
    total_boxes = sum([x[0] for x in items])
    f_cost = frt if ftyp == 'Total' else frt*total_boxes
    e_cost = exp if etyp == 'Total' else exp*total_boxes
    
    final_amt = total - (f_cost+e_cost+post)

    data_str = ''

    data_str += date.strftime('%d/%m/%Y') + '\n' + vn + '\n' + pname + '\n' + iname + '\n' + i_str
    data_str += '\n\n\n'
    data_str += 'Total = ' + str(total) + '\nBoxes = ' + str(total_boxes) + '\nCommision = (-) ' + str(comm) + '\nFreight = (-) '+ str(f_cost) + '\nExpense = (-) '+ str(e_cost) + '\nPost = (-) '+ str(post) + '\nFinal Amount = ' + str(final_amt) + '\n\n\nGT Trading Co.'

    return data_str

data_str = st.button('Calculate', on_click=calculate)
st.divider()

if data_str:
    data_str = calculate()
    st.empty()

    st.code(data_str)

    encoded_str = data_str.replace('@','%40')
    encoded_str = encoded_str.replace(' ','%20')
    encoded_str = encoded_str.replace('\n','%0a')
    encoded_str = encoded_str.replace('=', '%3D')
    encoded_str = encoded_str.replace('(', '%28')
    encoded_str = encoded_str.replace(')', '%29')
    encoded_str = encoded_str.replace('-', '%2D')
    encoded_str = encoded_str.replace('/', '%2F')

    st.link_button('Send on WhatsApp', url=f'whatsapp://send?text={encoded_str}')

