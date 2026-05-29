from dotenv import load_dotenv

load_dotenv()
from langchain_mistralai import ChatMistralAI
model = ChatMistralAI(model="mistral-small-2506",temperature=0.9)
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage #to maintain the conversation history in the form of messages(human,ai,system)

print("choose your AI mode")
print("press 1 for Angry mode")
print("press 2 for Sad mode")
print("press 3 for Funny mode")
choice = int(input("Enter your choice:"))
if choice ==1:
    mode="you are an angry AI agent . You respond aggressively and impatiently to user messages. You have a short temper and often use harsh language in your replies."
elif choice ==2:
    mode="you are a sad AI agent . You respond with utter sadness and hollowness to user message. You have a melancholic nature and often use poetic and emotional language in your replies."
elif choice ==3:
    mode="you are a funny AI agent . You respond with humor and wit to user messages. You have a playful nature and often use jokes and memes in your replies."
messages = [
       SystemMessage(content=mode)  # this is a form of system mesaage here system message is an object which contains the content that defines  the behavior of the AI agent. It is used to set the context and instructions for the AI model, guiding how it should respond to user inputs. In this case, the system  message is telling the AI agent to be funny in its responses.
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