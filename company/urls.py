from django.urls import path
from .views import CreateCompanyView, CompanyListAPIView

urlpatterns = [
    path('create', CreateCompanyView.as_view(), name='create company'),
    path('list', CompanyListAPIView.as_view(), name='list company'),
]