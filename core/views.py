from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import json

def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "core/home.html")

def about(request):
    return render(request, "core/about.html")

def ask_anything(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "core/ask_anything.html")

def chatbot_api(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)
    
    if not settings.GEMINI_API_KEY:
        return JsonResponse({
            "status": "error", 
            "message": "Gemini API key not configured. Please add GEMINI_API_KEY in settings.py"
        })

    try:
        import google.generativeai as genai
        data = json.loads(request.body)
        user_message = data.get("message", "")
        
        if not user_message:
            return JsonResponse({"status": "error", "message": "Empty message"})

        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        response = model.generate_content(user_message)
        
        return JsonResponse({
            "status": "success",
            "response": response.text
        })
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
