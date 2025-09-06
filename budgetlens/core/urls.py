from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLogoutView

urlpatterns = [
    path("upload-receipt/", views.upload_receipt, name="upload_receipt"),
    path('dashboard/', views.dashboard, name='dashboard'),
    # Using the login template from core/templates/login.html
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page='/core/login/'), name='logout'),

    path('expense/<int:expense_id>/', views.expense, name='expense'),
    path('save_expense/<int:expense_id>/', views.save_expense, name='save_expense'),
    # Expense URLs
    path('expense/add/', views.add_expense, name='add_expense'),
    # Income URLs
    path('income/add/', views.add_income, name='add_income'),
    path('income/list/', views.income_list, name='income_list'),
    path('income/<int:income_id>/', views.income_detail, name='income_detail'),
    path('income/edit/<int:income_id>/', views.edit_income, name='edit_income'),
]
