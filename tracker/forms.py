from django import forms
from tracker.models import Transaction


class Transaction_Form(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = (
            "title",
            "transaction_date",
            "transaction_type",
            "amount",
            "category",
            "description",
        )
        labels = {
            "transaction_date": "Transaction Date",
            "transaction_type": "Transaction Type",
            "description": "Description (Optional)",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input form-title"}),
            "transaction_date": forms.DateInput(
                attrs={"class": "form-input form-date", "type": "date"},
            ),
            "transaction_type": forms.RadioSelect(
                attrs={"class": "transaction-type-options"}
            ),
            "amount": forms.NumberInput(attrs={"class": "form-input form-amount"}),
            "category": forms.Select(attrs={"class": "form-input form-category"}),
            "description": forms.Textarea(
                attrs={"class": "form-input form-description", "rows": 3}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["transaction_type"].choices = (
            Transaction.Transaction_Choices.choices
        )

        if not self.instance.pk and not self.is_bound:
            self.fields["transaction_type"].initial = (
                Transaction.Transaction_Choices.INCOME
            )
