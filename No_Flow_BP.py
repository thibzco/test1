import streamlit as st
import openai
from openai import OpenAI
import pandas as pd
from pydantic import BaseModel

###### --------- Classes
class ProblemExtraction(BaseModel):
    person2: str
    relationship: str
    issues: list[str]
    context: str
    causes: list[str]
    desired_outcomes: list[str]

class YesNoAnswer(BaseModel):
    YesNo: bool

class ActionChosen(BaseModel):
    user_chosen_action_person_to_perform: str
    user_chosen_action_action_to_perform: str

###### --------- Functions
# Initialization function
def ini():
    
    ###### --------- Global
    global suggest_prompt, propose_prompt
    
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    code_assistant_setup = st.secrets["ALL_IN_BP"] 

    ###### --------- Variables
    # Initialize flags and variables
    if "convo1" not in st.session_state:
        st.session_state["convo1"] = []

    if "i1" not in st.session_state:
        st.session_state["i1"] = 1

    if "model_user1" not in st.session_state:
        st.session_state["model_user1"]=st.secrets["MODEL_USER1"]

    try:
        if st.session_state.user_flow['Stage_bot_validation'][st.session_state.s1]:
            yesno_eval = openai.beta.chat.completions.parse(
            model=model_parsing,
            n=1, #important to keep the number of choices limited to 1
            messages= st.session_state.yesno_setup + [whole_convo[-1]],
            response_format=YesNoAnswer
            )
            user_confirms = yesno_eval.choices[0].message
            if user_confirms.parsed:
                yesno_object=yesno_eval.choices[0].message.parsed
            else:
                print("Parsing refusal:", resp_parsing.refusal)

            st.session_state.user_flow['Stage_user_validation'][st.session_state.s1]=yesno_object.YesNo
            if yesno_object.YesNo:
                resp1 = propose_prompt
            else:
                st.session_state.user_flow['Stage_bot_validation'][st.session_state.s1] = False
                st.session_state.current_action.user_chosen_action_person_to_perform =''
                st.session_state.current_action.user_chosen_action_action_to_perform =''
                st.session_state.y = len(whole_convo)
                response_foruser = openai.chat.completions.create(
                model=model_user,
                n=1, #important to keep the number of choices limited to 1
                messages=whole_convo
                )
                resp1 = response_foruser.choices[0].message.content
        else:
            response = openai.beta.chat.completions.parse(
            model=model_parsing,
            n=1, #important to keep the number of choices limited to 1
            messages=st.session_state.message_assistant2+whole_convo[st.session_state.y:], #Original
            response_format=ActionChosen
            )
            resp_parsing=response.choices[0].message
            if resp_parsing.parsed:
                st.session_state.current_action=response.choices[0].message.parsed
            else:
                print("Parsing refusal:", resp_parsing.refusal)

            if are_all_properties_populated(st.session_state.current_action):
                st.session_state.user_flow['Stage_bot_validation'][st.session_state.s1]=True
                resp1 = f"I understand that you want " + action_summary(st.session_state.current_action) + f" Is this correct?"

            else:
                response_foruser = openai.chat.completions.create(
                model=model_user,
                n=1, #important to keep the number of choices limited to 1
                messages=whole_convo
                )
                resp1 = response_foruser.choices[0].message.content
        
        whole_convo.append({'role':'assistant', 'content':resp1})

    except Exception as e:
        return f"An error occurred: {e}"
    return resp1


# Function to handle the user submission
def submit_message(prompt1):

    st.session_state.messages.append({"role": "user", "content": prompt})

    st.session_state.convo1.append({"role": "user", "content": prompt})
    GPT_response = globals()[st.session_state.user_flow['Stage_user_function'][st.session_state.s1]](st.session_state.convo1, st.session_state.model_user1, st.session_state.model_parsing1)
    st.session_state.messages.append({"role": "assistant", "content": GPT_response})
    st.session_state.i1 += 1

    if st.session_state.user_flow['Stage_bot_validation'][st.session_state.s1] and st.session_state.user_flow['Stage_user_validation'][st.session_state.s1]:
        transition_state()
    else:
        # No input from the user
        pass


    return all(value for value in vars(obj).values())

st.title("Prototype Thibz Interface")

###### --------- Main program
if "messages" not in st.session_state:
    st.session_state["messages"]=[]
    ini()

if prompt := st.chat_input("Type here"):
    submit_message(prompt)

for message in st.session_state.messages:
     with st.chat_message(message["role"]):
         st.markdown(message["content"])
