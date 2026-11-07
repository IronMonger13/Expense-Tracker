from django.db import models
from django.utils import timezone

# Create your models here.


class Transaction(models.Model):
    class Transaction_Choices(models.TextChoices):
        INCOME = "Income", "Income"
        EXPENSE = "Expense", "Expense"

    class Category_Choices(models.TextChoices):
        Salary_Income = "salary_income", "Salary & Income"
        Bonus_Commissions = "bonus_commissions", "Bonus & Commissions"
        Gifts = "gifts", "Gifts"
        Investments = "investments", "Investments"
        Cashback_Rewards = "cashback_rewards", "Cashback & Rewards"
        Refunds = "refunds", "Refunds"
        Housing_Utilities = "housing_utilities", "Housing & Utilities"
        Food = "food", "Food"
        Groceries = "groceries", "Groceries"
        Transport_Travel = "transport_travel", "Transport & Travel"
        Shopping = "shopping", "Shopping"
        Education = "education", "Education"
        Health_Wellbeing = "health_wellbeing", "Health & Wellbeing"
        Entertainment = "entertainment"
        Financial_Debt_Payment = "financial_debt_payment", "Financial & Debt Payment"
        Others = "others", "Others"

    title = models.CharField(max_length=20)
    transaction_date = models.DateField(default=timezone.localdate)
    created_on = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(
        max_length=7, choices=Transaction_Choices.choices
    )
    category = models.CharField(max_length=30, choices=Category_Choices.choices)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title
