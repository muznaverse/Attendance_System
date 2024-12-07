import streamlit as st
from forms import contact

@st.dialog("Contact Me")
def show_contact_form():
    contact.contact_form()
    
col1, col2 = st.columns(2,gap="small", vertical_alignment="center")

with col1:
    st.image("./assets/Automated.png")

with col2:
    st.title("Description", anchor=False)
    st.write(
    """ This project is designed to simplify and streamline the attendance tracking process using modern technology.
        It leverages machine learning for facial recognition and integrates seamlessly with existing educational or
        organizational frameworks to ensure accurate and efficient attendance management. By minimizing manual 
        intervention, this system reduces human error and saves time for administrators and attendees alike. 
        Additionally, its scalability and adaptability make it suitable for various environments, such as 
        classrooms, offices, or events. The project reflects a practical implementation of concepts like 
        image processing, database integration, and user interface design, showcasing the potential of 
        technology in solving everyday challenges.
    """
    )
    if st.button ("Contact Developer"):
        show_contact_form()
