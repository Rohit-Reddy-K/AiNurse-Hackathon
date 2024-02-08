import os
import openai

os.environ["OPENAI_API_KEY"] = "478f5b6559c04f069639ab6f7dbcaea8"
openai.api_type = "azure"
openai.api_base = "https://fkh-hackathon-instance.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

def process_data(vertex_response):
    messages=[
        {
            "role": "system",
            "content": "You will be provided with unstructured data, and your task is to parse and only return in csv format, product name as 'product' along with dosage as 'dosage' in string and quantities as 'quantities' in integer."
        },
        {
            "role": "user",
            "content":  vertex_response
        }
    ]
    completion = openai.ChatCompletion.create(
        engine="fkh-hackathon-35-turbo",
        messages = messages,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    print(completion)
    return str(completion['choices'][0]['message']['content'])

