# Criando Seu Assistente de Programação Python, em Python

# Importa módulo para interagir com o sistema operacional
import os

# Importa a biblioteca Streamlit para criar a interface web interativa
import streamlit as st

# Importa a classe Groq para se conectar à API da plataforma Groq e acessar o LLM
from groq import Groq

# Configura a página do Streamlit com título, ícone, layout e estado inicial da sidebar
st.set_page_config(
    page_title="IA GuLucca 🤖",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define um prompt de sistema que descreve as regras e comportamento do assistente de IA
CUSTOM_PROMPT = """
Você é o "👨‍🎓 IA GuLucca Capolongo Lima 👨‍🎓", um assistente de IA especialista em estudos escolares.

REGRAS DE OPERAÇÃO:
1.  **Foco em Estudos**: Responda apenas a perguntas relacionadas a estudos escolares, pesquisas na internet, assuntos relacionados a estudos escolares e IA. Se o usuário perguntar sobre outro assunto, responda educadamente que seu foco é exclusivamente em auxiliar com estudos escolares.
2.  **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
    * **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático. Formate suas respostas para adolecentes de até 16 anos.
    * **Exemplo de estudos**: Forneça uma ou mais explicações sobre o assunto abordado. O assunto deve ser bem comentado para explicar as partes importantes.
    * **Detalhes da pesquisa**: Após a explicação, descreva em detalhes o que cada parte do estudo que foi solicitdo.
    * **Documentação de Referência**: Ao final, inclua uma seção chamada "📚 Documentação de Referência" com um link direto e relevante para a documentação oficial da Linguagem Python (docs.python.org) ou da biblioteca em questão.
    * **Após toda explicação questione o usuário se precisa de mais alguma coisa e dê sugestões de estudos sobre o assunto solicitado.
3.  **Clareza e Precisão**: Use uma linguagem clara. Evite jargões desnecessários. Suas respostas devem ser tecnicamente precisas.
"""

# Cria o conteúdo da barra lateral no Streamlit
with st.sidebar:
    
    # Define o título da barra lateral
    st.title("🖥️ IA GuLucca")
    
    # Mostra um texto explicativo sobre o assistente
    st.markdown("Assistente de IA focado para ajudar nos estudos.")
    
    # Campo para inserir a chave de API da Groq
    groq_api_key = st.text_input(
        "Insira sua API Key Groq", 
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys"
    )

    # Adiciona linhas divisórias e explicações extras na barra lateral
    st.markdown("---")
    st.markdown("Desenvolvido para auxiliar em suas dúvidas escolares. IA pode cometer erros. Sempre verifique as respostas.")


# Título principal do app
st.title("IA GuLucca")

# Subtítulo adicional
st.title("💻Assistente Pessoal do Gustavo e Lucca💻")

# Texto auxiliar abaixo do título
st.caption("Faça sua pergunta sobre estudos escolares e obtenha explicações e referências.")

# Inicializa o histórico de mensagens na sessão, caso ainda não exista
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe todas as mensagens anteriores armazenadas no estado da sessão
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Inicializa a variável do cliente Groq como None
client = None

# Verifica se o usuário forneceu a chave de API da Groq
if groq_api_key:
    
    try:
        
        # Cria cliente Groq com a chave de API fornecida
        client = Groq(api_key = groq_api_key)
    
    except Exception as e:
        
        # Exibe erro caso haja problema ao inicializar cliente
        st.sidebar.error(f"Erro ao inicializar o cliente Groq: {e}")
        st.stop()

# Caso não tenha chave, mas já existam mensagens, mostra aviso
elif st.session_state.messages:
     st.warning("Por favor, insira sua API Key da Groq na barra lateral para continuar.")

# Captura a entrada do usuário no chat
if prompt := st.chat_input("Qual sua dúvida sobre estudos?"):
    
    # Se não houver cliente válido, mostra aviso e para a execução
    if not client:
        st.warning("Por favor, insira sua API Key da Groq na barra lateral para começar.")
        st.stop()

    # Armazena a mensagem do usuário no estado da sessão
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Exibe a mensagem do usuário no chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepara mensagens para enviar à API, incluindo prompt de sistema
    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:
        
        messages_for_api.append(msg)

    # Cria a resposta do assistente no chat
    with st.chat_message("assistant"):
        
        with st.spinner("Analisando sua pergunta..."):
            
            try:
                
                # Chama a API da Groq para gerar a resposta do assistente
                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = "openai/gpt-oss-20b", 
                    temperature = 0.7,
                    max_tokens = 2048,
                )
                
                # Extrai a resposta gerada pela API
                dsa_ai_resposta = chat_completion.choices[0].message.content
                
                # Exibe a resposta no Streamlit
                st.markdown(dsa_ai_resposta)
                
                # Armazena resposta do assistente no estado da sessão
                st.session_state.messages.append({"role": "assistant", "content": dsa_ai_resposta})

            # Caso ocorra erro na comunicação com a API, exibe mensagem de erro
            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq: {e}")

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p>IA GuLucca</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Obrigado DSA



