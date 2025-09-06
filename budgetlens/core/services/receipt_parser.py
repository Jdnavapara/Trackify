import re
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from datetime import datetime
from django.core.files import File
from ..models import Expense
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def parse_receipt_image(image_path):
    """Extract details from receipt using OCR with preprocessing"""
    try:
        # Preprocess the image for better OCR accuracy
        img = Image.open(image_path).convert("L")  # grayscale
        img = img.filter(ImageFilter.MedianFilter())  # reduce noise
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)  # increase contrast

        text = pytesseract.image_to_string(img)

        # Debug: print OCR text in terminal
        print("=== OCR OUTPUT START ===")
        print(text)
        print("=== OCR OUTPUT END ===")

    except Exception as e:
        print(f"Tesseract not available or error: {e}")
        return {
            "amount": None,
            "expense_date": None,
            "description": "Receipt Expense (OCR not available)",
            "category": "Miscellaneous",
            "currency": "INR",
        }

    # --- Extract Amount (₹500, 123.45, etc.) ---
    amount_match = re.search(r'(\d+[.,]?\d{0,2})', text)
    amount = float(amount_match.group(1).replace(',', '')) if amount_match else None

    # --- Extract Date (dd/mm/yyyy or yyyy-mm-dd) ---
    date_match = re.search(r'(\d{2}[/-]\d{2}[/-]\d{4}|\d{4}[/-]\d{2}[/-]\d{2})', text)
    expense_date = None
    if date_match:
        for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
            try:
                expense_date = datetime.strptime(date_match.group(1), fmt).date()
                break
            except ValueError:
                continue

    # --- Description (first line of OCR) ---
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    description = lines[0] if lines else "Receipt Expense"

    # --- Category detection ---
    category = "Miscellaneous"
    category_keywords = {
        "Groceries": ["grocery", "supermarket", "store", "mart"],
        "Dining Out": ["restaurant", "cafe", "food", "pizza", "burger"],
        "Transportation": ["uber", "ola", "taxi", "bus", "train", "metro"],
        "Entertainment": ["movie", "cinema", "netflix", "concert"],
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
        "currency": "INR",  # default
    }


def create_expense_from_receipt(user, image_path):
    """Process receipt and create Expense object"""
    data = parse_receipt_image(image_path)

    with open(image_path, 'rb') as f:
        django_file = File(f)
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
