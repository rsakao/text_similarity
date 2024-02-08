from django.shortcuts import render
from django.conf import settings
import os
from pprint import pprint
import json
import requests
from openai import OpenAI

def index(request):
    text = ''
    limit_results = {}
    response_json = {}
    if request.method == "POST":
        print("request start")
        text = request.POST.get('text', '')

        # bing search
        subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
        endpoint = os.environ['BING_SEARCH_V7_ENDPOINT'] + "/v7.0/search"
        
        # 検索パラメータ
        mkt = 'ja-JP'
        params = {'q': text, 'mkt': mkt}
        headers = {'Ocp-Apim-Subscription-Key': subscription_key}

        print("search start")
        try:
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            
            # 検索結果を変数に格納
            search_results = response.json()
            limit_results = [{'name': item['name'], 'snippet': item['snippet'], 'url': item['url']} for item in search_results["webPages"]["value"]]
            pprint(limit_results)
        except Exception as ex:
            print(ex)

        # OpneAI API
        client = OpenAI()

        system_prompt_prompt_file_path = os.path.join(settings.BASE_DIR, 'similarity_checker', 'prompt', 'system')
        with open(system_prompt_prompt_file_path, 'r') as file:
            system_prompt = file.read().strip()

        print("gpt start")
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Sentence to be examined: ```{text}``` Sentences on the Internet: ```{limit_results}```"}
            ]
        )
        
        response = completion.choices[0].message.content
        response_json = json.loads(response)
        print(response_json)

    return render(request, 'similarity_checker/index.html', {'text': text, 'search_results': limit_results, 'response_data': response_json})

