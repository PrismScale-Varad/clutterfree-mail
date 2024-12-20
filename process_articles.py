from huggingface_hub import InferenceClient
import secret

client = InferenceClient(api_key=secret.api_key)

def summarize(body):
    messages = [
        { "role": "system", "content": "You are an AI that summarizes Newsletters. You will be given a newsletter by the User and you must iterate over each article, summarize it and mention link to the article if the user wishes to view it. Do not be conversational, just summarize given content as if it was written by you." },
        { "role": "user", "content": body}
    ]

    completion = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.3", 
        messages=messages, 
        temperature=0.5,
        max_tokens=2048,
        top_p=0.7
    )
    return completion.choices[0].message["content"]
