import openai

openai.api_key = "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"

while True :
    prompt = input("prompt: ")
    if prompt == 'exit':
        break
    response = openai.ChatCompletion.create(model = "gpt-3.5-turbo",
                                            messages = [{"role":"user","content": prompt}])
 
    print(response.choices[0].message.content)

