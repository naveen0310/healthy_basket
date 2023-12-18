from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns...
    path('process-payment/', views.process_payment, name='process_payment'),
]
