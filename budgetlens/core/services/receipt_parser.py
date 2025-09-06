import re
import pytesseract
from PIL import Image
from datetime import datetime
from django.core.files import File
from ..models import Expense


def parse_receipt_image(image_path):
    """Extract details from receipt using OCR"""
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
    except Exception as e:
        # Fallback when Tesseract is not available
        print(f"Tesseract not available: {e}")
        return {
            "amount": None,
            "expense_date": None,
            "description": "Receipt Expense (OCR not available)",
            "category": "Miscellaneous",
            "currency": "INR",
        }

    # Extract amount (e.g., 123.45 or ₹500)
    amount_match = re.search(r'(\d+[.,]\d{2})', text)
    amount = float(amount_match.group(1).replace(',', '')) if amount_match else None

    # Extract date (very naive regex, adjust for your receipts)
    date_match = re.search(r'(\d{2}[/-]\d{2}[/-]\d{4})', text)
    expense_date = None
    if date_match:
        try:
            expense_date = datetime.strptime(date_match.group(1), "%d/%m/%Y").date()
        except ValueError:
            try:
                expense_date = datetime.strptime(date_match.group(1), "%d-%m-%Y").date()
            except ValueError:
                pass

    # Simple description (first line of receipt text)
    description = text.split("\n")[0] if text else "Receipt Expense"

    # Very basic category detection
    category = "Miscellaneous"
    category_keywords = {
        "Groceries": ["grocery", "supermarket", "store"],
        "Dining Out": ["restaurant", "cafe", "food"],
        "Transportation": ["uber", "ola", "taxi", "bus", "train"],
        "Entertainment": ["movie", "cinema", "netflix"],
    }
    for cat, keywords in category_keywords.items():
        if any(word.lower() in text.lower() for word in keywords):
            category = cat
            break

    return {
        "amount": amount,
        "expense_date": expense_date,
        "description": description,
        "category": category,
        "currency": "INR",  # default, can extend with detection
    }


def create_expense_from_receipt(user, image_path):
    """Process receipt and create Expense object"""
    data = parse_receipt_image(image_path)

    # Open the file for Django's ImageField
    with open(image_path, 'rb') as f:
        django_file = File(f)
        # Set the file name from the path
        import os
        django_file.name = os.path.basename(image_path)
        expense = Expense.objects.create(
            user=user,
            receipt_image=django_file,
            amount=data["amount"],
            expense_date=data["expense_date"],
            description=data["description"],
            category=data["category"],
            currency=data["currency"],
        )
    return expense
