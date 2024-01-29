import streamlit as st
from multipage import MultiApp
#from pages import BSE100, nimf_baf  # import your app modules here
from pages import nimf_baf

st.set_page_config(
    page_title='Sentiment Analysis',
    layout="wide",
    initial_sidebar_state="collapsed",
)

app = MultiApp()


# Add all your application here
#app.add_app("BSE100", BSE100.main)
app.add_app("NIMF BAF", nimf_baf.main)
# app.add_app("Sentiment", sent.main)
# The main app
app.run()
