from django.shortcuts import render


def homework(request):
    return render(request, "unfinish.html")


def question_bank(request):
    return render(request, "unfinish.html")
