from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel
from typing import List, Optional #optional for example if a student doesnt have an email he can skip that field and list is used to store the data 
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import PydanticOutputParser

# Load model
model = ChatMistralAI(model="mistral-small-2506")

class Movie(BaseModel): #creating a form called schema 
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str

parser = PydanticOutputParser(pydantic_object=Movie) #creating an instance of the parser and passing the schema to it

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ('system', """ 
    Extract movie information from the paragraph 
    {format_instructions}
    """),
    ('human', " {paragraph} ")
]
)

# User Input
para = input("Enter your paragraph: ")

# Create final prompt
final_prompt = prompt.invoke({
    "paragraph": para,
    'format_instructions':parser.get_format_instructions()
})

# Generate response
response = model.invoke(final_prompt)

# Print output
print(response.content)