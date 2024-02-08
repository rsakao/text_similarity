from django.shortcuts import render
from django.conf import settings
import os
import json
from openai import OpenAI

def index(request):
    text = ''
    response_json = {}
    if request.method == "POST":
        text = request.POST.get('text', '')
        client = OpenAI()

        system_prompt_prompt_file_path = os.path.join(settings.BASE_DIR, 'similarity_checker', 'prompt', 'system')
        with open(system_prompt_prompt_file_path, 'r') as file:
            system_prompt = file.read().strip()

        print("request start")
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ]
        )
        
        response = completion.choices[0].message.content
        print(response)
        print(type(response))
        response_json = json.loads(response)
        print(response_json)
        print(type(response_json))

    return render(request, 'similarity_checker/index.html', {'text': text, 'response_data': response_json})

