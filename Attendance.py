import streamlit as st


#--- PAGE SETUP ---
about_page= st.Page(
    page="views/about_project.py",
    title="About Project",
    icon=":material/account_circle:",
)

project_2_page = st.Page(
    page="views/chatbot.py",
    title="Chatbot",
    icon=":material/smart_toy:",
)

project_3_page = st.Page(
    page="views/table.py",
    title="Table",
    icon=":material/bar_chart:",
)


#--- Navigation Setup [Without Sections] --
#pg = st.navigation(pages=[about_page, project_1_page, project_2_page])


# -- Navigation Setup [With Sections]
pg = st.navigation(
    {
        "info":[about_page],
        "Projects": [ project_2_page, project_3_page],
    }
)

# ---Shared on all Pages ---
st.logo("assets/Automated.png")
st.sidebar.text("Made by Muzna")

#--- Run Navigation --
pg.run()
