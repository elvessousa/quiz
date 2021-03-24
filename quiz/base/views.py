from django.shortcuts import render
from quiz.base.models import Question

def home(request):
    return render(request, 'base/home.html')

def questions(request, index):
    question = Question.objects.filter(available=True).order_by('id')[index - 1]
    context = {'index': index, 'question': question}
    return render(request, 'base/questions.html', context=context)

def ranking(request):
    return render(request, 'base/ranking.html')
