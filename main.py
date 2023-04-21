import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    Below is an email that may be poorly worded.
    Your goal is to:
    - Properly format the email  
    - Convert the input text to a specified language

    Here are some examples of words in different languages:
    - English: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - Hindi: हम सप्ताहांत के लिए बार्सिलोना गए। हमें आपको बताने के लिए बहुत सी बातें हैं।
    - Punjabi: ਅਸੀਂ ਵੀਕਐਂਡ ਲਈ ਬਾਰਸੀਲੋਨਾ ਗਏ ਸੀ। ਸਾਡੇ ਕੋਲ ਤੁਹਾਨੂੰ ਦੱਸਣ ਲਈ ਬਹੁਤ ਸਾਰੀਆਂ ਚੀਜ਼ਾਂ ਹਨ।
    
    Below is the email, and language:
    LANGUAGE: {language}
    EMAIL: {email}
    
    YOUR {language} RESPONSE:
"""

prompt = PromptTemplate(
    input_variables=["language", "email"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Globalize Email", page_icon=":robot:")
st.header("Globalize Text")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Often professionals would like to improve their emails, but don't have the skills to do so. \n\n This tool \
                will help you improve your email skills by converting your emails into a more professional format.")

with col2:
    st.image(image='test.png', width=500, caption='Powered by langchain, openai')

st.markdown("## Enter Your Email To Convert")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()


option_language = st.selectbox('Which language would you like to convert?',
        ('English', 'Hindi', 'Punjabi'))

def get_text():
    input_text = st.text_area(label="Email Input", label_visibility='collapsed', placeholder="Your Email...", key="email_input")
    return input_text

email_input = get_text()

if len(email_input.split(" ")) > 700:
    st.write("Please enter a shorter email. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.email_input = "Sally I am starts work at yours monday from dave"

st.button("*See An Example*", type='secondary', help="Click to see an example of the email you will be converting.", on_click=update_text_with_example)

st.markdown("### Your Converted Email:")

if email_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_email = prompt.format(language=option_language, email=email_input)

    formatted_email = llm(prompt_with_email)

    st.write(formatted_email)