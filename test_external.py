import streamlit as st
import openai
from openai import OpenAI
import pandas as pd
from pydantic import BaseModel

st.write("Secrets:", st.secrets)

# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ###### --------- Classes
# class ProblemExtraction(BaseModel):
#     person2: str
#     relationship: str
#     issues: list[str]
#     context: str
#     causes: list[str]
#     desired_outcomes: list[str]

# class YesNoAnswer(BaseModel):
#     YesNo: bool

# class ActionChosen(BaseModel):
#     user_chosen_action_person_to_perform: str
#     user_chosen_action_action_to_perform: str

# ###### --------- Functions
# # Initialization function
# def ini():
    
#     ###### --------- Global
#     global user_input, model_user1, model_parsing1, user_flow, s1, i1, convo1, message_assistant, message_assistant2, yesno_setup, suggest_prompt, propose_prompt
    
#     ###### --------- ChatGPT set ups
#     model_user1=st.secrets["MODEL_USER1"]
#     model_parsing1=st.secrets["MODEL_PARSING1"]
    
#     ###### --------- Variables
#     # Initialize flags and variables
#     code_assistant_setup = st.secrets["CODE_ASSISTANT_SETUP"] 
#     message_assistant=[{"role": "system", "content": code_assistant_setup}]

#     code_assistant_setup2 = st.secrets["CODE_ASSISTANT_SETUP2"] 
#     message_assistant2=[{"role": "system", "content": code_assistant_setup2}]

#     script_yesno_setup = st.secrets["YESNO_SETUP"]
#     yesno_setup=[{"role": "system", "content": script_yesno_setup}]

#     # Initiate user_flow, s1, i1 and convo1
#     init_userflow()
 
#     opening_prompt="Hello! I am here to help you with an interpersonal problem.\n Can you please describe it?\n"
#     suggest_prompt="Thank you for confirming my understanding. Are you ok with me suggesting a few solutions?"
#     propose_prompt="Thank you for choosing this action. Do you want to go in the details of it?"

#     ###### --------- Visuals settings
#     st.title("BuildPath Interface")
#     st.session_state.messages.append({"role": "assistant", "content": opening_prompt})

# # Function used to initiate and reset User_Flow, s1, i1 and convo1.
# def init_userflow():
#     global user_flow, s1, i1, convo1

#     general_flow = {
#     'Stage_id': [1, 2, 3],
#     'Stage_name': ['Understanding', 'Suggesting solutions', 'Preparing execution'],
#     'Stage_chat': ['', '', ''],
#     'Stage_bot_validation': [False, False, False],
#     'Stage_user_validation': [False, False, False],
#     'Stage_user_function': ['understand_problem', 'suggest_solutions', 'prep_exec']
#     }
#     user_flow = pd.DataFrame(general_flow)
#     user_flow.index = pd.RangeIndex(start=1, stop=len(user_flow) + 1, step=1)
#     s1 = 1 #Step of the flow in which is the user
#     i1 = 1 #Counter of messages send by the user in one state
#     convo1 = []
#     #user_flow.loc[s1, 'Stage_chat']=str(convo1) #Assigns the chat in the user_flow for the stage 1 until it's reassigned at the next stage
#     user_flow['Stage_chat'][s1]=convo1
#     return ""

# #Function to move to another state
# def transition_state():
#     global s1, i1, convo1
#     s1+=1
#     i1=1
#     convo1 = []

# # Function for ChatGPT to paraphrase the problem
# def understand_problem(whole_convo, model_user, model_parsing):

#     global user_problem, user_flow, i1
#     if i1==1:
#        chatGPT_setup_understanding = st.secrets["UNDERSTANDING"] 
#        temp=whole_convo[-1]
#        whole_convo.pop()
#        whole_convo.append({"role": "system", "content": chatGPT_setup_understanding})
#        whole_convo.append(temp)

#     ###### --------- ChatGPTopening chat
#     try:
#         if user_flow['Stage_bot_validation'][s1]:
#             yesno_eval = openai.beta.chat.completions.parse(
#             model=model_parsing,
#             n=1, #important to keep the number of choices limited to 1
#             messages= yesno_setup + [whole_convo[-1]],
#             response_format=YesNoAnswer
#             )
#             user_confirms = yesno_eval.choices[0].message
#             if user_confirms.parsed:
#                 yesno_object=yesno_eval.choices[0].message.parsed
#             else:
#                 print("Parsing refusal:", resp_parsing.refusal)

#             user_flow['Stage_user_validation'][s1]=yesno_object.YesNo
#             if yesno_object.YesNo:
#                 resp1 = suggest_prompt
#             else:
#                 user_flow['Stage_bot_validation'][s1] = False
#                 resp1 = "Can you please specify what is incorrect in my understanding?"
#         else:
#             response = openai.beta.chat.completions.parse(
#             model=model_parsing,
#             n=1, #important to keep the number of choices limited to 1
#             messages=message_assistant+whole_convo[1:],
#             response_format=ProblemExtraction
#             )
#             resp_parsing=response.choices[0].message

#             if resp_parsing.parsed:
#                 user_problem=response.choices[0].message.parsed
#             else:
#                 print("Parsing refusal:", resp_parsing.refusal)
        
#             if are_all_properties_populated(user_problem):
#                 user_flow['Stage_bot_validation'][s1]=True
#                 resp1 = f"I understand that " + problem_summary(user_problem) + f"Is this correct?"
#             else:
#                 response_foruser = openai.chat.completions.create(
#                 model=model_user,
#                 n=1, #important to keep the number of choices limited to 1
#                 messages=whole_convo
#                 )
#                 resp1 = response_foruser.choices[0].message.content
        
#         whole_convo.append({'role':'assistant', 'content':resp1})
#         # Return the assistant's response using dot notation
#         return resp1
#     except Exception as e:
#         return f"An error occurred: {e}"

# # Function generating a summary of a problem
# def problem_summary(problem: ProblemExtraction):
#     summary = f"the problem is with {problem.person2}, who is a {problem.relationship.lower()} ."
#     issues_str = ', '.join(problem.issues)
#     summary += f" The issues are: {issues_str.lower()}."
#     summary += f" This is happening in the context of {problem.context.lower()}."
#     causes_str = ', '.join(problem.causes)
#     summary += f" The causes are: {causes_str.lower()}."
#     outcomes_str = ', '.join(problem.desired_outcomes)
#     summary += f" The desired outcomes are: {outcomes_str.lower()}."
#     return(summary)

# # Function used to suggest actions to the user
# def suggest_solutions(whole_convo, model_user, model_parsing):
    
#     global current_action, i1, y, propose_prompt

#     if i1 == 1:
#         chatGPT_setup_suggesting_solutions= st.secrets["SUGGESTING"] 
        
#         temp = whole_convo[-1]["content"]
#         whole_convo.pop()
#         whole_convo.append({"role": "system", "content": chatGPT_setup_suggesting_solutions})
#         whole_convo.append({"role": "system", "content": "The summary of the problem is " + problem_summary(user_problem)})
#         whole_convo.append({"role": "user", "content": temp + " What is your best suggestion?"})
#         y= 2 #y is used in the action chosen parsing function: init to 2, then provide the last messages after a confirmation was declined

#     try:
#         if user_flow['Stage_bot_validation'][s1]:
#             yesno_eval = openai.beta.chat.completions.parse(
#             model=model_parsing,
#             n=1, #important to keep the number of choices limited to 1
#             messages= yesno_setup + [whole_convo[-1]],
#             response_format=YesNoAnswer
#             )
#             user_confirms = yesno_eval.choices[0].message
#             if user_confirms.parsed:
#                 yesno_object=yesno_eval.choices[0].message.parsed
#             else:
#                 print("Parsing refusal:", resp_parsing.refusal)

#             user_flow['Stage_user_validation'][s1]=yesno_object.YesNo
#             if yesno_object.YesNo:
#                 resp1 = propose_prompt
#             else:
#                 user_flow['Stage_bot_validation'][s1] = False
#                 current_action.user_chosen_action_person_to_perform =''
#                 current_action.user_chosen_action_action_to_perform =''
#                 y = len(whole_convo)
#                 response_foruser = openai.chat.completions.create(
#                 model=model_user,
#                 n=1, #important to keep the number of choices limited to 1
#                 messages=whole_convo
#                 )
#                 resp1 = response_foruser.choices[0].message.content
#         else:
#             response = openai.beta.chat.completions.parse(
#             model=model_parsing,
#             n=1, #important to keep the number of choices limited to 1
#             messages=message_assistant2+whole_convo[y:], #Original
#             response_format=ActionChosen
#             )
#             resp_parsing=response.choices[0].message
#             if resp_parsing.parsed:
#                 current_action=response.choices[0].message.parsed
#             else:
#                 print("Parsing refusal:", resp_parsing.refusal)

#             if are_all_properties_populated(current_action):
#                 user_flow['Stage_bot_validation'][s1]=True
#                 resp1 = f"I understand that you want " + action_summary(current_action) + f" Is this correct?"

#             else:
#                 response_foruser = openai.chat.completions.create(
#                 model=model_user,
#                 n=1, #important to keep the number of choices limited to 1
#                 messages=whole_convo
#                 )
#                 resp1 = response_foruser.choices[0].message.content
        
#         whole_convo.append({'role':'assistant', 'content':resp1})

#     except Exception as e:
#         return f"An error occurred: {e}"
#     return resp1

# # Function summarizing the action chosen
# def action_summary(action1):
#     sum1 = action1.user_chosen_action_person_to_perform.lower() + f" to " + action1.user_chosen_action_action_to_perform.lower()
#     return sum1

# # Function used to execute the solution
# def prep_exec(whole_convo, model_user, model_parsing):

#     global current_action, i1

#     if i1 == 1:
#         temp = whole_convo[-1]["content"]
#         whole_convo.pop()

#         if current_action.user_chosen_action_person_to_perform=='me':
#             chatGPT_setup_prep_execution= st.secrets["EXECUTING1"] 
#         else:
#             chatGPT_setup_prep_execution= st.secrets["EXECUTING2"] 
        
#         whole_convo.append({"role": "system", "content": chatGPT_setup_prep_execution})
#         if current_action.user_chosen_action_person_to_perform=='me':
#             whole_convo.append({"role": "system", "content": "The problem is " + problem_summary(user_problem)})
#             whole_convo.append({"role": "user", "content": "What email are you thinking you will send?"})
#         else:
#             whole_convo.append({"role": "system", "content": "The action is " + action_summary(current_action)})
#             whole_convo.append({"role": "user", "content": temp + ". How can this be done?"})
#         try:
#             response_foruser = openai.chat.completions.create(
#                 model=model_user,
#                 n=1, #important to keep the number of choices limited to 1
#                 messages=whole_convo
#                 )
#             resp1 = response_foruser.choices[0].message.content
#         except Exception as e:
#             return f"An error occurred: {e}"
#     else:
#         yesno_eval = openai.beta.chat.completions.parse(
#             model=model_parsing,
#             n=1, #important to keep the number of choices limited to 1
#             messages= yesno_setup + [whole_convo[-1]],
#             response_format=YesNoAnswer
#             )
#         user_confirms = yesno_eval.choices[0].message
#         if user_confirms.parsed:
#             yesno_object=yesno_eval.choices[0].message.parsed
#         else:
#             print("Parsing refusal:", user_confirms.refusal)

#         user_flow['Stage_user_validation'][s1]=yesno_object.YesNo
#         if yesno_object.YesNo:
#             if current_action.user_chosen_action_person_to_perform.lower() == 'me':
#                 resp1 = "Thank you for validating the content. I let you know when I've done it"
#             else:
#                 resp1 = "Thank you for validating the content. I will wait for your follow up"
#         else:
#             try:
#                 response_foruser = openai.chat.completions.create(
#                     model=model_user,
#                     n=1, #important to keep the number of choices limited to 1
#                     messages=whole_convo
#                     )
#                 resp1 = response_foruser.choices[0].message.content
#             except Exception as e:
#                 return f"An error occurred: {e}"
#         whole_convo.append({'role':'assistant', 'content':resp1})
    
#     return resp1

# # Function to handle the user submission
# def submit_message(prompt1):

#     ###### --------- Global
#     global i1, convo1, s1
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     convo1.append({"role": "user", "content": prompt})
#     GPT_response = globals()[user_flow['Stage_user_function'][s1]](convo1, model_user1, model_parsing1)
#     st.session_state.messages.append({"role": "assistant", "content": GPT_response})
#     i1 += 1

#     if user_flow['Stage_bot_validation'][s1] and user_flow['Stage_user_validation'][s1]:
#         transition_state()
#     else:
#         # No input from the user
#         pass

# # Tests if all properties of an object are populated
# def are_all_properties_populated(obj):
#     return all(value for value in vars(obj).values())


# ###### --------- Main program
# if prompt := st.chat_input("Type here"):
    submit_message(prompt)



# from openai import OpenAI
# import streamlit as st

# st.title("ChatGPT-like clone")

# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# if prompt := st.chat_input("What is up?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):
#         stream = client.chat.completions.create(
#             model=st.session_state["openai_model"],
#             messages=[
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages
#             ],
#             stream=True,
#         )
#         response = st.write_stream(stream)
#     st.session_state.messages.append({"role": "assistant", "content": response})