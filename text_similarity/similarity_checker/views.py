from django.shortcuts import render

def index(request):
    text = ''  # デフォルトで空のテキスト
    count = -1  # デフォルトでカウントを-1にしておき、フォーム未送信時には表示しない
    if request.method == "POST":
        text = request.POST.get('text', '')
        count = len(text)
    return render(request, 'similarity_checker/index.html', {'text': text, 'count': count})
