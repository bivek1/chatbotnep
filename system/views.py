from io import BytesIO
import re
from urllib.parse import urlparse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .preprocess import  get_answer




def train(request, id):
   
    return render(request, "customer/train.html", {'chatbot_id': id})


def get_answerView(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        question = request.GET.get('question', None)
        chatbot_id = request.GET.get('chatbot_id', None)
        if question and chatbot_id:
            # Try to find the most relevant answer from FAQ
            answers = FAQ.objects.filter(chatbot_id=chatbot_id)
            ques_ans = []

            for answer in answers:
                ques_ans.append({
                    "question": answer.question,
                    "answer": answer.answer
                })

            print(ques_ans)
            
            ans = get_answer( question, ques_ans)
            print(ans)
            if ans:
                response = {'answer': ans}
            else:
                response = {'answer': "Sorry, I couldn't find an answer to your question."}
        else:
            response = {'answer': "Please ask a question."}
        return JsonResponse(response)
    return JsonResponse({'error': 'Invalid request'}, status=400)



def LoginView(request):
    if request.method == 'POST':
        username = request.POST['email_user']
        password = request.POST['password']

        log= authenticate(request, username = username, password = password)

        if log != None:
            login(request, log)
            return HttpResponseRedirect(reverse('system:dashboard'))
        else:
            messages.error(request, "Failed to authenticate user")

    
    return render(request, "login.html")


def signUpView(request):
    if request.method == 'POST':
        username = request.POST['email_user']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        User.objects.create_user(username=username, password=password, first_name =first_name, last_name=last_name, email= username)
        messages.success(request,"Successfully created an account. Please login")
        return HttpResponseRedirect(reverse('system:login'))
    else:
        return render(request, "signup.html")

@login_required
def Dashboard(request):
    

    dist = {
        'chatbot':ChatBot.objects.filter(of_user= request.user).order_by('-id')
    }
    if request.method == 'POST':
        chatbot = request.POST['chatbot']

        ChatBot.objects.create(name = chatbot, of_user = request.user)
        return HttpResponseRedirect(reverse('system:dashboard'))
    return render(request, "customer/dashboard.html", dist)

@login_required
def chatbotView(request, id):
    chatbot = ChatBot.objects.get(id =id)
    faq = FAQ.objects.filter(chatbot = id)
    dist = {
        'chatbot':chatbot,
        'faq':faq
    }

    if request.method == 'POST':
        questions = request.POST.getlist('questions[]')
        answers = request.POST.getlist('answers[]')
       
        if not questions or not answers or len(questions) != len(answers):
            messages.success(request,"Error on adding data")

        chatbot = ChatBot.objects.get(id=id)  # Get the chatbot instance

        for question, answer in zip(questions, answers):
            FAQ.objects.create(chatbot=chatbot, question=question, answer=answer)
        messages.success(request,"Successfully added all data")
       

    return render(request, "customer/chatbot.html", dist)

def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('system:login'))