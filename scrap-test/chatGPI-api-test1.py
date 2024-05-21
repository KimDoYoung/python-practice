import os
import time
import openai


chatgpt_key = os.getenv("CHATGPT_KEY")

if not chatgpt_key:
    # Use the value of the environment variable
    print("CHATGPT_KEY is not set.")
    exit(0)

openai.api_key = chatgpt_key

def call_openai_api(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# 사용 예제
prompt = "Tell me a joke."
response = call_openai_api(prompt)
print(response)

# query = "What is the capital of the United States?"

# messages = [
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": query}
# ]
# model = "gpt-3.5-turbo"
# response = openai.chat.completions.create(model=model, messages=messages)
# print(response)
