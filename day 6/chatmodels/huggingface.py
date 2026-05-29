from dotenv import load_dotenv
load_dotenv()
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
llm= HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
)
model = ChatHuggingFace(llm=llm)
response = model.invoke("Write a poem about AI")
print(response.content)