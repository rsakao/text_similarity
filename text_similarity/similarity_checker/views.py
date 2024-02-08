from django.shortcuts import render
from openai import OpenAI

def index(request):
    text = ''
    count = ''
    if request.method == "POST":
        text = request.POST.get('text', '')
        client = OpenAI()
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant who counts the number of characters in a given text. Please return only the number of characters."},
                {"role": "user", "content": text}
            ]
        )
        
        response = completion.choices[0].message.content
        print(response)
        count = response  # APIからの応答をそのまま使用

    return render(request, 'similarity_checker/index.html', {'text': text, 'count': count})
