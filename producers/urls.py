from django.urls import path
from . import views

app_name = 'producers'

urlpatterns = [
    path('dashboard/', views.producer_dashboard, name='dashboard'),
    path('review/<uuid:pk>/', views.review_submission, name='review'),
    path('reviewed/', views.reviewed_submissions, name='reviewed'),
]
