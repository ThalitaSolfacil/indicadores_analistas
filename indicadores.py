import pandas as pd
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import plotly.express as px




# Lendo as bases
indic_parcial = pd.read_csv('indicadores_parcialmente_tratados.csv', encoding='utf-8-sig', sep=';')
indic_total = pd.read_csv('indicadores_totalmente_tratados.csv', encoding='utf-8-sig', sep=';')
indic_sem = pd.read_excel('indicadores.xlsx', sheet_name='Planilha1')

indic_total['Motivo'] = indic_total['Motivo'].fillna('')
indic_parcial['Motivo'] = indic_parcial['Motivo'].fillna('')


# Iniciando a página
st.set_page_config(page_title = "Indicadores", page_icon = ":bar_chart:", layout = 'wide')

# Cabeçalho da página
r, l = st.columns([6, 3])
r.title('Indicadores de Análise')

solfacil_image = requests.get('https://s3.sa-east-1.amazonaws.com/cdn.solfacil.com.br/assets/icons/logo-solfacil-color.png')    
image = Image.open(BytesIO(solfacil_image.content))
l.subheader('Made by Thalita at')
l.image(image, output_format = "PNG", width = 250)

st.markdown('---')






st.header(':bar_chart: Pré-Cockpit')


st.subheader('Base de indicadores - Tratada')
st.dataframe(indic_total)
with st.expander('Descrição da análise'):
    st.markdown("- 1º: Desconsiderar IDs que não possuem analistas;")
    st.markdown("- 2º: Retirar IDs duplicados (quanto tem o mesmo motivo de reprova), mantendos sempre a primeira ocorrência;")
    st.markdown("- 3º: Retirar IDs reprovados sem motivo.")

st.markdown('---')


#Base dos analistas
prop_rep_apr = pd.DataFrame([], columns = ['Analista', 'Qtd Reprova', 'Qtd Aprova', 'Qtd Total'])

for analista in indic_total['Analista'].unique():
    rows_analista = indic_total[indic_total['Analista'] == analista]
    rows_analista = pd.DataFrame({'Analista': analista,  'Qtd Reprova': rows_analista[rows_analista['Status']=='reprovado'].shape[0], 'Qtd Aprova': rows_analista[rows_analista['Status']=='aprovado'].shape[0], 'Qtd Total': rows_analista.shape[0]}, index=[0])
    prop_rep_apr = pd.concat([prop_rep_apr, rows_analista], ignore_index=True)
prop_rep_apr = prop_rep_apr.sort_values(by='Qtd Reprova', ascending= False)



fig = px.bar((indic_total[indic_total['Status'] == 'reprovado']), title= 'Proporção dos Motivos de Reprova', x = 'Documento')
fig.update_yaxes(title= "Quantidade")
st.plotly_chart(fig, use_container_width = True)







qtd_per_doc = pd.DataFrame([], columns=['Documento', 'Quantidade Reprovações'])
for i in indic_total['Documento'].unique(): qtd_per_doc = pd.concat([qtd_per_doc, pd.DataFrame({'Documento': i, 'Quantidade Reprovações': indic_total[indic_total['Documento']==i].shape[0]}, index=[0])], ignore_index=True)
qtd_per_doc = qtd_per_doc.sort_values(by='Quantidade Reprovações', ascending= False)


l3, r3 = st.columns(2)

for j in range(1, 7):
    
    doc = qtd_per_doc['Documento'].unique()[j - 1]
    gp_doc =  px.pie(indic_total[(indic_total['Documento'] == doc) & (indic_total['Status'] == 'reprovado')], names='Motivo', title = f'Proporção do documento {doc}')
    
    if j%2 != 0: l3.plotly_chart(gp_doc, use_container_width=True)
    else: r3.plotly_chart(gp_doc, use_container_width=True)


st.dataframe(qtd_per_doc)


st.markdown('---')
fig1 = px.histogram(indic_total, x='Analista', color = 'Status', color_discrete_map={'reprovado': '#999999', 'aprovado': '#FBB600'})#, color_discrete_map={'reprovado': '', 'aprovado': ''}
fig1.update_yaxes(title= "Quantidade")
st.plotly_chart(fig1, use_container_width = True)


l2, r2 = st.columns(2)
for i in range(1, 7):
    analista = prop_rep_apr['Analista'].unique()[i - 1]
    gp_analista =  px.pie(indic_total[(indic_total['Analista'] == analista) & (indic_total['Status'] == 'reprovado')], names='Documento', title = f'Proporção do analista {analista}')

    if i%2 != 0: l2.plotly_chart(gp_analista, use_container_width=True)
    else: r2.plotly_chart(gp_analista, use_container_width=True)



st.dataframe(prop_rep_apr)







st.markdown('---')
st.subheader('Base de indicadores - Sem tratamento')
st.dataframe(indic_sem)
