from django.urls import include
from django.contrib import admin
from django.urls import path

from .views import FetchWords, GetRecommendation, TestResult, TestView
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('user_scores', TestResult, basename='user_scores')

urlpatterns = [
    path('fetch_words/', FetchWords.as_view()),
    path('fetch_words/<str:mode>/<int:length>', FetchWords.as_view()),
    path('test/', TestView.as_view()),
    path('user_scores/', TestResult.as_view()),
    path('get_recommendation/<int:user_id>', GetRecommendation.as_view())
    # path('', include(router.urls))
]
