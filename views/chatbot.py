import random
import time
import streamlit as st

# Response generator function with more structured responses
def response_generator(prompt):
    if "attendance" in prompt.lower():
        return "The Automated Attendance System uses facial recognition to track attendance. It's automated, scalable, and can be integrated into classrooms or office settings."
    elif "who made this" in prompt.lower():
        return "This project was developed by Muzna, a sophomore from the Electrical Engineering department at FAST NUCES."
    elif "technologies" in prompt.lower():
        return "The system uses machine learning for facial recognition, OpenCV for image processing, and a Python-based interface to manage attendance."
    elif "classroom" or "scalable" in prompt.lower():
        return "Yes, the system is fully adaptable to a classroom or any event setting. It tracks students using facial recognition."
    elif "project" in prompt.lower():
        return "The Automated Attendance System is a real-world application designed to automate the process of tracking attendance using facial recognition technology."
    elif "functionalities" in prompt.lower():
        return "The core functionality of this website include:\n1)Multiple Pages \n2)Form powerd by pabbly \n3)a Chat bot\n 4)A functional ML model made with openCV"
    elif "made" in prompt.lower():
        return "It was made by using streamlit and OpenCV primarily. For further detail contact the developer through about project page!"
    elif "hi" or "hello" in prompt.lower():
        return "Hey! How can I help with Automated Attendance System"
    else:
        # Default response if no match
        return random.choice(
            [
                "Hey there! Need help with the Automated Attendance System? Let me know how I can assist you.",
                "Hi! What's up? Got questions about the project? Feel free to ask, I'm here to help!",
                "Hello! Need assistance with the attendance app? I'm happy to guide you through it.",
                "Hey! Got a question about the Automated Attendance System? Ask away, I'm here to help!",
                "Hi there! How can I help with the app? Feel free to drop your questions!"
            ]
        )

# Streamed response emulator
def streamed_response(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

st.title("Automated Attendance System Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get the assistant's response
    assistant_response = response_generator(prompt)

    # Display assistant response in chat message container (streaming)
    with st.chat_message("assistant"):
        response_stream = st.write_stream(streamed_response(assistant_response))
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    #rag