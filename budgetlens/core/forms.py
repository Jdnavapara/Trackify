from django import forms
from django import forms
from .models import Expense, Income

class ExpenseForm(forms.ModelForm):
    """Form to upload an expense"""
    class Meta:
        model = Expense
        fields = ['receipt_image', 'category', 'expense_date', 'amount', 'currency']
        widgets = {
            'category': forms.TextInput(attrs={'required': False}),
            'expense_date': forms.DateInput(attrs={'required': False}),
            'amount': forms.NumberInput(attrs={'required': False}),
            'currency': forms.TextInput(attrs={'required': False}),
        }

class ExpenseEditForm(forms.ModelForm):
    """Form to edit an expense"""
    class Meta:
        model = Expense
        fields = ['category', 'expense_date', 'amount', 'currency']
        widgets = {
            'category': forms.Select(choices=Expense.CATEGORY_CHOICES),
        }

class IncomeForm(forms.ModelForm):
    """Form to add an income entry"""
    class Meta:
        model = Income
        fields = ['amount', 'currency', 'income_date', 'description', 'category']
        widgets = {
            'income_date': forms.DateInput(attrs={'type': 'date'}),
        }

class IncomeEditForm(forms.ModelForm):
    """Form to edit an income entry"""
    class Meta:
        model = Income
        fields = ['amount', 'currency', 'income_date', 'description', 'category']
        widgets = {
            'income_date': forms.DateInput(attrs={'type': 'date'}),
        }
        