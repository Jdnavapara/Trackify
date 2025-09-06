"""Views for the core app"""

import base64
from decimal import Decimal
import logging
import json
import os
import requests
from django.db.models import Sum, F, Value, FloatField
from django.db.models.functions import Lower, Trim, Coalesce
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
<<<<<<< HEAD
from openai import OpenAI
from .forms import ExpenseEditForm, ExpenseForm
from .models import Expense, UserProfile
=======
from .forms import ExpenseEditForm, ExpenseForm, IncomeForm, IncomeEditForm
from .models import Expense, UserProfile, Income
>>>>>>> ca617e54b6346e6a6476509de411ac9ae0620eb9


OPEN_EXCHANGE_RATES_API_KEY = os.getenv("OPEN_EXCHANGE_RATES_API_KEY")
OPEN_EXCHANGE_RATES_API_URL = "https://openexchangerates.org/api/historical/"

log = logging.getLogger(__name__)

# Initialize OpenAI client only if API key is available
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not os.getenv("OPENAI_API_KEY"):
        client = None
except (ImportError, Exception):
    client = None


def encode_image(image_path):
    """Encode the image file to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def process_receipt(image_path):
<<<<<<< HEAD
    """Process the receipt image using OpenAI API"""
    log.debug("views : process_receipt()")
    base64_image = encode_image(image_path)
    category = "Sample Category"
    expense_date = "2024-11-13"
    amount = 10.00
    currency = "EUR"

=======
    """Process the receipt image using OpenAI API if available, otherwise return default values"""
    log.debug("views : process_receipt()")
    category = "Miscellaneous"
    # Use current date as default in YYYY-MM-DD format
    import datetime
    expense_date = datetime.date.today().strftime("%Y-%m-%d")
    amount = 10.00
    currency = "EUR"

    # If OpenAI client is not available, return default values
    if client is None:
        return {
            "category": category,
            "date": expense_date,
            "amount": amount,
            "currency": currency,
        }
    
    base64_image = encode_image(image_path)
    
>>>>>>> ca617e54b6346e6a6476509de411ac9ae0620eb9
    base_categories = [
        "Housing",
        "Utilities",
        "Transportation",
        "Groceries",
        "Dining Out",
        "Healthcare",
        "Debt Payments",
        "Insurance",
        "Clothing",
        "Entertainment",
        "Education",
        "Childcare",
        "Pet Care",
        "Subscriptions",
        "Miscellaneous",
    ]

<<<<<<< HEAD
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Analyze the provided receipt and extract the following details: "
                            "1. Category: Determine the category of the expense from this list: "
                            f"{', '.join(base_categories)}. 2.Date: Identify the transaction date. "
                            "3. Amount: Extract the expense amount as a decimal number. Consider: "
                            "- A comma may serve as a thousand separator or decimal separator. "
                            "- In KRW (Korean Won), the amount is never lower than a thousand. "
                            "4. Currency: Identify the currency used in the expense starting "
                            "(three-character ISO 4217 code). Respond strictly in JSON format, "
                            "and ending with braces, without any additional markup language "
                            'or explanation. Example response: {"category": "<category>",'
                            ' "date": "<date>", "amount": <amount>,'
                            ' "currency": "<currency>"}'
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
=======
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Analyze the provided receipt and extract the following details: "
                                "1. Category: Determine the category of the expense from this list: "
                                f"{', '.join(base_categories)}. 2.Date: Identify the transaction date. "
                                "3. Amount: Extract the expense amount as a decimal number. Consider: "
                                "- A comma may serve as a thousand separator or decimal separator. "
                                "- In KRW (Korean Won), the amount is never lower than a thousand. "
                                "4. Currency: Identify the currency used in the expense starting "
                                "(three-character ISO 4217 code). Respond strictly in JSON format, "
                                "and ending with braces, without any additional markup language "
                                'or explanation. Example response: {"category": "<category>",'
                                ' "date": "<date>", "amount": <amount>,'
                                ' "currency": "<currency>"}'
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
>>>>>>> ca617e54b6346e6a6476509de411ac9ae0620eb9
                    },
                ],
            }
        ],
        temperature=0.2,
    )

<<<<<<< HEAD
    try:
=======
>>>>>>> ca617e54b6346e6a6476509de411ac9ae0620eb9
        if (
            not response
            or not response.choices
            or not response.choices[0].message.content
        ):
            raise ValueError("Empty or invalid response from OpenAI API")

        content = response.choices[0].message.content.strip()
        log.debug("Response from OpenAI")
        log.debug(content)
<<<<<<< HEAD

        if content.startswith("```json") and content.endswith("```"):
            log.debug("Content: %s", content)
            content = content[7:-3].strip()
            log.debug("Content after stripping markdown: %s", content)

        response_data = json.loads(content)

        if "/" in response_data.get("date"):
            response_data["date"] = response_data["date"].replace("/", "-")

        category = response_data.get("category", "Miscellaneous")
        if category not in base_categories:
            category = "Miscellaneous"

        expense_date = response_data.get("date")
        amount = response_data.get("amount")
        currency = response_data.get("currency").upper()

        return category, expense_date, amount, currency
    except json.JSONDecodeError as e:
        log.error("JSON decode error: %s", e)
        raise
    except ValueError as e:
        log.error("Value error: %s", e)
        raise
=======
    except Exception as e:
        log.error(f"Error processing receipt with OpenAI: {str(e)}")
        return {
            "category": category,
            "date": expense_date,
            "amount": amount,
            "currency": currency,
        }

        try:
            if content.startswith("```json") and content.endswith("```"):
                log.debug("Content: %s", content)
                content = content[7:-3].strip()
                log.debug("Content after stripping markdown: %s", content)

            response_data = json.loads(content)
            
            # Ensure amount is a valid decimal
            amount_val = response_data.get("amount")
            if amount_val is not None:
                try:
                    # Try to convert to float first to handle various formats
                    float_val = float(str(amount_val).replace(',', '.'))
                    response_data["amount"] = float_val
                except (ValueError, TypeError):
                    log.error(f"Invalid amount format from API: {amount_val}. Using default amount.")
                    response_data["amount"] = 0.00
            
            # Ensure date is in YYYY-MM-DD format
            date_str = response_data.get("date")
            if date_str:
                # Replace any separators with hyphens
                date_str = date_str.replace("/", "-").replace(".", "-")
                
                # Try to parse and standardize the date format
                try:
                    import datetime
                    # Check for various date formats
                    if len(date_str.split("-")) == 3:
                        parts = list(map(int, date_str.split("-")))
                        
                        # Determine which format we're dealing with
                        if parts[0] > 31 and parts[0] <= 9999 and parts[1] <= 12 and parts[2] <= 31:
                            # Already YYYY-MM-DD format
                            year, month, day = parts
                            date_str = f"{year:04d}-{month:02d}-{day:02d}"
                        elif parts[0] <= 31 and parts[1] <= 12 and parts[2] <= 9999:
                            # DD-MM-YYYY format
                            day, month, year = parts
                            if year < 100:
                                # Handle 2-digit year
                                current_year = datetime.date.today().year
                                century = current_year // 100
                                year = century * 100 + year
                            date_str = f"{year:04d}-{month:02d}-{day:02d}"
                        elif parts[0] <= 12 and parts[1] <= 31 and parts[2] <= 9999:
                            # MM-DD-YYYY format
                            month, day, year = parts
                            if year < 100:
                                # Handle 2-digit year
                                current_year = datetime.date.today().year
                                century = current_year // 100
                                year = century * 100 + year
                            date_str = f"{year:04d}-{month:02d}-{day:02d}"
                    
                    # Validate the final date format
                    datetime.datetime.strptime(date_str, "%Y-%m-%d")
                    response_data["date"] = date_str
                except (ValueError, IndexError):
                    # If parsing fails, use current date
                    log.error(f"Could not parse date: {date_str}. Using current date.")
                    response_data["date"] = datetime.date.today().strftime("%Y-%m-%d")

            category = response_data.get("category", "Miscellaneous")
            if category not in base_categories:
                category = "Miscellaneous"

            expense_date = response_data.get("date")
            amount = response_data.get("amount")
            currency = response_data.get("currency").upper()

            return {
                "category": category,
                "date": expense_date,
                "amount": amount,
                "currency": currency,
            }
        except json.JSONDecodeError as e:
            log.error("JSON decode error: %s", e)
            return {
                "category": category,
                "date": expense_date,
                "amount": amount,
                "currency": currency,
            }
        except ValueError as e:
             log.error("Value error: %s", e)
             return {
                 "category": category,
                 "date": expense_date,
                 "amount": amount,
                 "currency": currency,
             }
>>>>>>> ca617e54b6346e6a6476509de411ac9ae0620eb9
    except Exception as e:
        log.error("Unexpected error: %s", e)
        raise


def get_exchange_rate(date, from_currency, to_currency):
    """Get the exchange rate for the given date and currencies"""

    if from_currency == to_currency:
        return 1, 1

    log.debug("views : get_exchange_rate()")
    url = f"{OPEN_EXCHANGE_RATES_API_URL}{date}.json"
    log.debug("URL: %s", url)
    params = {"app_id": OPEN_EXCHANGE_RATES_API_KEY}
    response = requests.get(url, params=params, timeout=10)

    if response.status_code == 200:
        data = response.json()
        return data["rates"].get(from_currency), data["rates"].get(to_currency)

    log.error("Error fetching exchange rate: %s", response.text)
    return None, None


@login_required
def upload_receipt(request):
    """View to upload the receipt image and process it"""
    log.debug("views : upload_receipt()")
    if request.method == "POST":
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense_dto = form.save(commit=False)
            expense_dto.user = request.user
            expense_dto.save()

            category, expense_date, amount, currency = process_receipt(
                expense_dto.receipt_image.path
            )

            expense_dto.category = category
<<<<<<< HEAD
            expense_dto.expense_date = expense_date
            expense_dto.amount = amount
=======
            # Ensure date is in YYYY-MM-DD format
            try:
                # Check if date is already in correct format
                import datetime
                if expense_date:
                    # Try to parse the date and reformat it to ensure YYYY-MM-DD format
                    parsed_date = datetime.datetime.strptime(expense_date, "%Y-%m-%d").date()
                    expense_dto.expense_date = parsed_date
                else:
                    # Use current date if no date was extracted
                    expense_dto.expense_date = datetime.date.today()
            except ValueError:
                # If date parsing fails, use current date
                log.error(f"Invalid date format: {expense_date}. Using current date instead.")
                expense_dto.expense_date = datetime.date.today()
                
            # Ensure amount is a valid decimal
            try:
                if amount:
                    # Convert to Decimal to ensure it's a valid decimal number
                    from decimal import Decimal, InvalidOperation
                    expense_dto.amount = Decimal(str(amount))
                else:
                    # Use default amount if none was extracted
                    expense_dto.amount = Decimal('0.00')
            except (ValueError, TypeError, InvalidOperation):
                log.error(f"Invalid amount format: {amount}. Using default amount.")
                expense_dto.amount = Decimal('0.00')
                
>>>>>>> ca617e54b6346e6a6476509de411ac9ae0620eb9
            expense_dto.currency = currency

            user_profile = UserProfile.objects.get(user=request.user)
            target_currency = user_profile.target_currency

<<<<<<< HEAD
            exchange_rate_to_usd, exchange_rate_to_target = get_exchange_rate(
                expense_date, currency, target_currency
=======
            # Format the date as YYYY-MM-DD string for the API call
            date_str = expense_dto.expense_date.strftime("%Y-%m-%d") if expense_dto.expense_date else datetime.date.today().strftime("%Y-%m-%d")
            
            exchange_rate_to_usd, exchange_rate_to_target = get_exchange_rate(
                date_str, currency, target_currency
>>>>>>> ca617e54b6346e6a6476509de411ac9ae0620eb9
            )
            log.debug(
                "Exchange rates: to USD %s, to target %s",
                exchange_rate_to_usd,
                exchange_rate_to_target,
            )

            if exchange_rate_to_usd and exchange_rate_to_target:
                exchange_rate_to_usd = Decimal(str(exchange_rate_to_usd))
                exchange_rate_to_target = Decimal(str(exchange_rate_to_target))
                amount_decimal = Decimal(str(amount))

                converted_amount_to_usd = amount_decimal / exchange_rate_to_usd
                converted_amount_to_target = (
                    converted_amount_to_usd * exchange_rate_to_target
                )
                expense_dto.amount_in_target_currency = round(
                    converted_amount_to_target, 2
                )
                log.debug("Converted amount: %s", expense_dto.amount_in_target_currency)
            else:
                log.error("Could not convert amount to target currency")

            expense_dto.save()
            # Redirect to the expense page to adjust information
            return redirect("expense", expense_id=expense_dto.id)
        else:
            log.error("Form errors: %s", form.errors)
    else:
        form = ExpenseForm()
    return render(request, "upload.html", {"form": form})


@login_required
def dashboard(request):
<<<<<<< HEAD
    """View to display the user's expenses ordered by date and aggregated by category"""
    expenses = Expense.objects.filter(user=request.user).order_by("-expense_date")
=======
    """View to display the user's expenses and income ordered by date and aggregated by category"""
    expenses = Expense.objects.filter(user=request.user).order_by("-expense_date")
    incomes = Income.objects.filter(user=request.user).order_by("-income_date")
>>>>>>> ca617e54b6346e6a6476509de411ac9ae0620eb9

    expenses = expenses.annotate(category_normalized=Trim(Lower(F("category"))))
    log.debug("Normalized Category: %s", expenses.values("category_normalized"))

    category_data = (
        expenses.values("category_normalized")
        .annotate(
            total_amount=Coalesce(
                Sum("amount_in_target_currency", output_field=FloatField()),
                Value(0, output_field=FloatField()),
            )
        )
        .order_by("category_normalized")
    )

    categories = [
        (
            item["category_normalized"].capitalize()
            if item["category_normalized"]
            else "Uncategorized"
        )
        for item in category_data
    ]
    amounts = [float(item["total_amount"]) for item in category_data]

    log.debug("Aggregated Category Data: %s", categories)

<<<<<<< HEAD
=======
    # Calculate total income
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate total expenses
    total_expenses = expenses.aggregate(Sum('amount_in_target_currency'))['amount_in_target_currency__sum'] or 0

>>>>>>> ca617e54b6346e6a6476509de411ac9ae0620eb9
    return render(
        request,
        "dashboard.html",
        {
            "expenses": expenses,
<<<<<<< HEAD
            "categories": json.dumps(categories),
            "amounts": json.dumps(amounts),
=======
            "incomes": incomes,
            "categories": json.dumps(categories),
            "amounts": json.dumps(amounts),
            "total_income": total_income,
            "total_expenses": total_expenses,
>>>>>>> ca617e54b6346e6a6476509de411ac9ae0620eb9
        },
    )


@login_required
def expense(request, expense_id):
    """View to display the details of a specific expense"""
    log.debug("views : expense()")
    log.debug("Expense ID: %s", expense_id)
    expense_detail = Expense.objects.get(id=expense_id, user=request.user)
    log.debug("Expense detail: %s", expense_detail.expense_date)
    log.debug("User Currency: %s", request.user.userprofile.target_currency)
    return render(
        request, "expense.html", {"expense": expense_detail, "user": request.user}
    )


@login_required
def save_expense(request, expense_id):
    """View to save the edited expense details with currency conversion"""
    log.debug("views : save_expense()")
    expense_edit = Expense.objects.get(id=expense_id, user=request.user)

    if request.method == "POST":
        form = ExpenseEditForm(request.POST, instance=expense_edit)
        if form.is_valid():
            expense_form = form.save(commit=False)

            user_profile = UserProfile.objects.get(user=request.user)
            target_currency = user_profile.target_currency

<<<<<<< HEAD
            exchange_rate_to_usd, exchange_rate_to_target = get_exchange_rate(
                expense_form.expense_date, expense_form.currency, target_currency
=======
            # Format the date as YYYY-MM-DD string for the API call
            date_str = expense_form.expense_date.strftime("%Y-%m-%d") if expense_form.expense_date else datetime.date.today().strftime("%Y-%m-%d")
            
            exchange_rate_to_usd, exchange_rate_to_target = get_exchange_rate(
                date_str, expense_form.currency, target_currency
>>>>>>> ca617e54b6346e6a6476509de411ac9ae0620eb9
            )

            if exchange_rate_to_usd and exchange_rate_to_target:
                exchange_rate_to_usd = Decimal(str(exchange_rate_to_usd))
                exchange_rate_to_target = Decimal(str(exchange_rate_to_target))

                converted_amount_to_usd = expense_form.amount / exchange_rate_to_usd
                converted_amount_to_target = (
                    converted_amount_to_usd * exchange_rate_to_target
                )
                expense_form.amount_in_target_currency = round(
                    converted_amount_to_target, 2
                )

            expense_form.save()
            log.debug("Expense updated successfully")
            return redirect("expense", expense_id=expense_id)
        else:
            log.error("Form errors: %s", form.errors)
    else:
        form = ExpenseEditForm(instance=expense_edit)

    return render(
        request,
        "expense.html",
        {"form": form, "expense": expense_edit, "user": request.user},
    )
<<<<<<< HEAD
=======

@login_required
def add_income(request):
    """View to add a new income entry"""
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect("income_list")
        else:
            log.error("Form errors: %s", form.errors)
    else:
        form = IncomeForm()
    return render(request, "add_income.html", {"form": form})

@login_required
def income_list(request):
    """View to display all income entries"""
    incomes = Income.objects.filter(user=request.user).order_by("-income_date")
    return render(request, "income_list.html", {"incomes": incomes})

@login_required
def income_detail(request, income_id):
    """View to display the details of a specific income entry"""
    income = Income.objects.get(id=income_id, user=request.user)
    return render(request, "income_detail.html", {"income": income})

@login_required
def edit_income(request, income_id):
    """View to edit an income entry"""
    income = Income.objects.get(id=income_id, user=request.user)
    if request.method == "POST":
        form = IncomeEditForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect("income_detail", income_id=income_id)
        else:
            log.error("Form errors: %s", form.errors)
    else:
        form = IncomeEditForm(instance=income)
    return render(request, "edit_income.html", {"form": form, "income": income})
>>>>>>> ca617e54b6346e6a6476509de411ac9ae0620eb9
