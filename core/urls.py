from django.urls import path
from .views import home, about, chatbot_api, ask_anything

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("ask-anything/", ask_anything, name="ask_anything"),
    path("api/chat/", chatbot_api, name="chatbot_api"),
]
