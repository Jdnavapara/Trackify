from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('upload/', views.upload_receipt, name='upload'),
    path('dashboard/', views.dashboard, name='dashboard'),
<<<<<<< HEAD
=======
    # Using the login template from core/templates/login.html
>>>>>>> ca617e54b6346e6a6476509de411ac9ae0620eb9
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('expense/<int:expense_id>/', views.expense, name='expense'),
    path('save_expense/<int:expense_id>/', views.save_expense, name='save_expense'),
<<<<<<< HEAD
=======
    # Income URLs
    path('income/add/', views.add_income, name='add_income'),
    path('income/list/', views.income_list, name='income_list'),
    path('income/<int:income_id>/', views.income_detail, name='income_detail'),
    path('income/edit/<int:income_id>/', views.edit_income, name='edit_income'),
>>>>>>> ca617e54b6346e6a6476509de411ac9ae0620eb9
]
