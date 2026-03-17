import streamlit as st
import requests

st.set_page_config(page_title="MedAssist AI - Prontuário Inteligente", page_icon="⚕️", layout="wide")
st.title("⚕️ MedAssist AI: Estruturação de Transcrições")
st.markdown("Cole abaixo a transcrição médica crua ditada pelo profissional (ex: dados do dataset Medical Transcriptions).")

transcription = st.text_area("Transcrição Médica", height=200, placeholder="Ex: Paciente do sexo masculino, 45 anos, apresenta dor torácica irradiando para o braço esquerdo. Histórico de hipertensão. Prescrito Aspirina e solicitado ECG...")

if st.button("Estruturar Prontuário 🧠"):
    if not transcription:
        st.warning("Por favor, insira o texto da transcrição.")
    else:
        with st.spinner('Analisando transcrição com Agentes de IA...'):
            payload = {"transcription_text": transcription}
            response = requests.post("http://localhost:8000/run", json=payload)
            
            if response.ok:
                data = response.json()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📌 Triagem e Especialidade")
                    triagem = data.get("triagem", {})
                    st.success(f"**Especialidade Sugerida:** {triagem.get('especialidade', 'N/A')}")
                    st.info(f"**Justificativa:** {triagem.get('justificativa', 'N/A')}")
                
                with col2:
                    st.subheader("🧬 Entidades Clínicas Extraídas")
                    entidades = data.get("entidades_clinicas", {})
                    st.write("**Sintomas:**", ", ".join(entidades.get("Sintomas", [])))
                    st.write("**Diagnósticos:**", ", ".join(entidades.get("Diagnósticos", [])))
                    st.write("**Medicamentos:**", ", ".join(entidades.get("Medicamentos", [])))
                    st.write("**Procedimentos:**", ", ".join(entidades.get("Procedimentos", [])))
            else:
                st.error("Erro ao conectar com os agentes médicos.")