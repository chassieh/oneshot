from django.urls import path
from . import views

app_name = 'submissions'

urlpatterns = [
    path('submit/', views.submit_song, name='submit'),
    path('<uuid:pk>/checkout/', views.checkout, name='checkout'),
    path('<uuid:pk>/stripe-pay/', views.stripe_payment, name='stripe_payment'),
    path('<uuid:pk>/stripe-success/', views.stripe_success, name='stripe_success'),
    path('<uuid:pk>/paypal-success/', views.paypal_success, name='paypal_success'),
    path('<uuid:pk>/', views.submission_detail, name='detail'),
    path('', views.submission_list, name='list'),
]
