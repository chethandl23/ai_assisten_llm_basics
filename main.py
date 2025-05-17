import streamlit as st
import json
import ollama
from datetime import datetime
import time 
Task_file = "tasks.json"

def load_data():
    try:
        with open(Task_file,'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_tasks(tasks):
    with open(Task_file,'w') as file :
        json.dump(tasks,file,indent = 4)

def ask_question(question):
    response = ollama.chat(
        model = 'mistral',messages = [{"role":"user","content":question}]
    )
    return response["message"]["content"]

st.set_page_config(page_title = "AI assistant ",layout="centered")
st.title("AI assistant ")

st.subheader("your tasks are:")
tasks = load_data()
for i,task in enumerate(tasks):
    st.write(f"{i+1}.{task['task']} (at:{task['time']})")

st.subheader("Add Tasks")

new_task = st.text_input("enter your new task:")
if st.button("ADD TASKS") and new_task:
    tasks.append({"task":new_task,"time":str(datetime.now())})
    save_tasks(tasks)
    st.success("Task added")
    time.sleep(1)

st.subheader("DELETE THE TASKS")
dropdown_option = [f"{i+1}. {task['task']} (at: {task['time']})" for i, task in enumerate(tasks)]
selected_task = st.selectbox("select a task to be deleted",options=dropdown_option)
index_to_delete = dropdown_option.index(selected_task)
if st.button("delete a task"):
    del tasks[index_to_delete]
    save_tasks(tasks)
    st.success("Task deleted successfully!")
    st.experimental_rerun() 

    

st.subheader("Ask Your AI")

question = st.text_input("ask anything about productivity")
if st.button("ask"):
    if question:
        reply = ask_question(question)
        st.markdown(f"assistant {reply}")
    else:
        st.warning("please enter your question")