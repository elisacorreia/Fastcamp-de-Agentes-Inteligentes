import streamlit as st
import requests

# 1. Configuração da página 
st.set_page_config(page_title="Consultor de Beleza IA", page_icon="💄")
st.title("💄 Seu Consultor de Maquiagem IA")

# 2. Coletando os dados do usuário
skin_type = st.selectbox("Qual o seu tipo de pele?", ["Normal", "Seca", "Oleosa", "Mista", "Sensível"])
occasion = st.text_input("Qual é a ocasião?", placeholder="Ex: Casamento, Dia a dia, Balada, Trabalho")
style = st.text_input("Qual o estilo desejado?", placeholder="Ex: Natural, Glam, Clean Girl, Marcante")


if st.button("Criar meu Look ✨"):
    # Verifica se a pessoa preencheu os campos de texto
    if not occasion or not style:
        st.warning("Por favor, preencha a ocasião e o estilo.")
    else:
        # 4. O Pacote de Dados 
        payload = {
            "skin_type": skin_type,
            "occasion": occasion,
            "style": style
        }
        
        
        with st.spinner('Consultando os especialistas...'):
            
            # Envia o pedido para o (host_agent) que está na porta 8000
            response = requests.post("http://localhost:8000/run", json=payload)
            
            # 5. Mostrando o resultado na tela
            if response.ok:
                data = response.json()
                
                st.subheader("🧴 Preparação da Pele (Skincare)")
                st.write(data.get("skincare", "Nenhuma dica de skincare retornada."))
                
                st.subheader("👩‍🎨 Pele (Base e Contorno)")
                st.write(data.get("base_makeup", "Nenhuma dica de base retornada."))
                
                st.subheader("👁️ Detalhes (Olhos e Boca)")
                st.write(data.get("details", "Nenhuma dica de detalhes retornada."))
            else:
                st.error("Falha ao criar a rotina de maquiagem. Verifique se os agentes estão rodando!")