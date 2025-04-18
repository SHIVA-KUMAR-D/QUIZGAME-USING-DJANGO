from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from decouple import config
import google.generativeai as genai
import re

# Configure Gemini API using .env
genai.configure(api_key=config("GEMINI_API_KEY"))

# ---------- Views ----------

def home(request):
    return render(request, 'index.html')

def topics(request):
    return render(request, 'topics.html')

def quiz(request):
    lang = request.GET.get('lang', 'Python')
    topic = request.GET.get('topic', 'Basics')

    questions = generate_questions(lang, topic)

    return render(request, 'quiz.html', {
        'lang': lang,
        'topic': topic,
        'questions': questions
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# ---------- Gemini Integration ----------

def generate_questions(language, topic):
    try:
        prompt = (
            f"Generate 10 beginner-level multiple-choice questions about {topic} in {language}. "
            "Each question should include four options labeled A, B, C, and D, and indicate the correct answer. "
            "Format each question like this:\n"
            "Q1: What is X?\nA. Option 1\nB. Option 2\nC. Option 3\nD. Option 4\nAnswer: B"
        )

        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)

        return parse_questions(response.text)
    except Exception as e:
        print(f"Error generating questions: {e}")
        return []

# ---------- Parser ----------

def parse_questions(response_text):
    questions = []
    blocks = response_text.strip().split("Q")[1:]  # Skip any empty first part

    for block in blocks:
        lines = block.strip().split("\n")
        question_line = lines[0].strip()
        options = [line[2:].strip() for line in lines[1:5] if line[1] == '.']
        answer_line = [line for line in lines if line.lower().startswith("answer")]
        answer = answer_line[0].split(":")[1].strip() if answer_line else ""

        question_text = question_line[3:].strip() if question_line.startswith(str(len(questions)+1)) else question_line

        questions.append({
            "question": question_text,
            "options": options,
            "answer": options[ord(answer.upper()) - 65] if answer in ['A', 'B', 'C', 'D'] else ""
        })

    return questions
