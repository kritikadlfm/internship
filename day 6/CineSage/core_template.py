from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

# Load model
model = ChatMistralAI(model="mistral-small-2506")

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are an AI movie information extractor.

Extract the following details from the movie review paragraph:

1. Movie Name
2. Genre
3. Director
4. Main Themes
5. Lead Actor
6. Positive Aspects
7. Emotional Core
8. Music Composer
9. Overall Sentiment

Movie Review:
{paragraph}

Provide the output in a clear structured format.
""")
])

# User Input
para = input("Enter your paragraph: ")

# Create final prompt
final_prompt = prompt.invoke({
    "paragraph": para
})

# Generate response
response = model.invoke(final_prompt)

# Print output
print(response.content)