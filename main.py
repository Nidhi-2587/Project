import openai

with open('hidden.txt') as file:
    openai.api_key = file.read()
    
