import openai

api_key = ''

prompt = ''

# Вызов API ChatGPT
response = openai.Completion.create(
    engine="davinci",
    prompt=prompt,
    max_tokens=50,
    api_key=api_key
)
answer = response.choices[0].text

print(answer)