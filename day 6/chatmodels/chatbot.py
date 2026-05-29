from dotenv import load_dotenv

load_dotenv()
from langchain_mistralai import ChatMistralAI
model = ChatMistralAI(model="mistral-small-2506",temperature=0.9)
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage #to maintain the conversation history in the form of messages(human,ai,system)
messages = [
       SystemMessage(content="You are a funny Ai agent")  # this is a form of system mesaage here system message is an object which contains the content that defines  the behavior of the AI agent. It is used to set the context and instructions for the AI model, guiding how it should respond to user inputs. In this case, the system  message is telling the AI agent to be funny in its responses.
]

print("____________Welcome Type 0 to exit the application____________")
while True:
    prompt=input("you: ")
    messages.append(HumanMessage(content=prompt)) #human message object is created with the content of the user input and added to the messages list to maintain the conversation history.
    if prompt=="0" :
        print("Bot: ","Bbye, See you soon!")
        break
    response = model.invoke(messages)
    messages.append(AIMessage(content=response.content)) #ai message object is created with the content of the AI response and added to the messages list to maintain the conversation history.
    print("Bot: ",response.content)

print(messages)