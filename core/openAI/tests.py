import openai

api_key = ''

user_input = 'Explain how solar energy works.'

# Вызов API ChatGPT
response = openai.Completion.create(
    engine="davinci",
    prompt=user_input,
    max_tokens=50,
    api_key=api_key
)
answer = response.choices[0].text

print(answer)