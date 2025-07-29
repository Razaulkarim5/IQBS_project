from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Question  # Import the Question model
import json


# login 
def signup(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use")
            return redirect("signup")

        user = User.objects.create_user(
            username=email, first_name=first_name, last_name=last_name, email=email, password=password1
        )
        user.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("signin")

    return render(request, "signup.html")

def signin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # Change to your home page
        else:
            messages.error(request, "Invalid email or password")
            return redirect("signin")

    return render(request, "signin.html")

def signout(request):
    logout(request)
    return redirect("signin")
  

# Bloom Taxonomy keywords grouped by levels
bloom_taxonomy = {
    "C1": ["define", "list", "recall", "identify", "describe", "recognize", "retrieve", "name", "state"],
    "C2": ["explain", "summarize", "paraphrase", "classify", "interpret", "compare", "discuss", "restate"],
    "C3": ["solve", "use", "implement", "demonstrate", "perform", "apply", "execute", "modify"],
    "C4": ["analyze", "differentiate", "organize", "attribute", "structure", "compare", "test", "examine"],
    "C5": ["assess", "critique", "evaluate", "judge", "recommend", "justify", "argue", "defend", "decide"],
    "C6": ["design", "construct", "develop", "build", "create", "generate", "compose", "plan", "propose"],
}

def classify_bloom_level(user_input):
    """Classify the question based on Bloom's taxonomy."""
    words = user_input.lower().split()  # Tokenize the input text into words
    for level, keywords in bloom_taxonomy.items():
        for word in words:
            if word in keywords:
                return level, word  # Return the first match
    return None, None  # If no match is found

@login_required
def create(request):
    if request.method == 'POST':
        question_id = request.POST.get('serial-number')
        subject_code = request.POST.get('subject-code')
        question_text = request.POST.get('question')

        # Classify the Bloom level and keyword (assumed you have a method for this)
        bloom_level, bloom_keyword = classify_bloom_level(question_text)

        # Save the question in the database
        question = Question(
            id=question_id,
            subject_code=subject_code,
            question_text=question_text,
            bloom_level=bloom_level if bloom_level else "Unclassified",
            bloom_keyword=bloom_keyword if bloom_keyword else "None"
        )
        question.save()

        # Add success message
        messages.success(request, "Question created successfully!")

        return redirect('create')  # Redirect back to the same page

    return render(request, 'createQuestion.html')

'''def data(request):
      
      #return JsonResponse({'message':'this is IQBS'})
      return render(request, 'index.html')'''
      
      

@login_required
def home(request):
      return render(request, 'home.html')
  
@login_required
def view(request):
    # Retrieve all questions from the database
    questions = Question.objects.all()
    
    # Pass the questions to the template
    return render(request, 'View_question.html', {'questions': questions})



# def analyze(request):
#     # Retrieve all questions from the database
#     questions = Question.objects.all()

#     # Classify questions into difficulty levels
#     difficulty_levels = {
#         "easy": [],
#         "medium": [],
#         "hard": []
#     }

#     for question in questions:
#         bloom_level = question.bloom_level
#         if bloom_level in ["C1", "C2"]:
#             difficulty_levels["easy"].append(question)
#         elif bloom_level in ["C3", "C4"]:
#             difficulty_levels["medium"].append(question)
#         elif bloom_level in ["C5", "C6"]:
#             difficulty_levels["hard"].append(question)

#     # Pass the classified questions to the template
#     return render(request, 'analyzeReport.html', {"difficulty_levels": difficulty_levels})


def analyze(request):
    # Retrieve all questions from the database
    questions = Question.objects.all()

    # Classify questions into difficulty levels
    difficulty_levels = {
        "easy": [],
        "medium": [],
        "hard": []
    }

    for question in questions:
        bloom_level = question.bloom_level
        if bloom_level in ["C1", "C2"]:
            difficulty_levels["easy"].append(question)
        elif bloom_level in ["C3", "C4"]:
            difficulty_levels["medium"].append(question)
        elif bloom_level in ["C5", "C6"]:
            difficulty_levels["hard"].append(question)

    # Calculate percentages for the bar chart
    total_questions = len(questions)
    easy_percentage = (len(difficulty_levels["easy"]) / total_questions) * 100 if total_questions else 0
    medium_percentage = (len(difficulty_levels["medium"]) / total_questions) * 100 if total_questions else 0
    hard_percentage = (len(difficulty_levels["hard"]) / total_questions) * 100 if total_questions else 0

    # Pass the classified questions and percentages to the template
    chart_data = {
        "labels": ["Easy", "Medium", "Hard"],
        "data": [easy_percentage, medium_percentage, hard_percentage]
    }

    return render(request, 'analyzeReport.html', {
        "difficulty_levels": difficulty_levels,
        "chart_data": json.dumps(chart_data)  # Pass chart data as JSON to the template
    })