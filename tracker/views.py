from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum
from django.contrib import messages
from tracker.forms import Transaction_Form
from tracker.models import Transaction


# Create your views here.
def dashboard(request):
    # try:
    all_transactions = Transaction.objects.all()
    no_of_transactions = len(all_transactions)
    total_balance = 0
    total_income = 0
    total_expense = 0

    for transaction in all_transactions:
        if transaction.transaction_type == "Income":
            total_balance += transaction.amount
            total_income += transaction.amount
        else:
            total_balance -= transaction.amount
            total_expense += transaction.amount

    category_expenses = (
        Transaction.objects.filter(transaction_type="Expense")
        .values("category")
        .annotate(total_amount=Sum("amount"))
        .order_by("-total_amount")
    )
    category_labels = dict(Transaction.Category_Choices.choices)

    for item in category_expenses:
        item["category_label"] = category_labels[item["category"]]
        item["category_percent"] = round(
            (item["total_amount"] / total_expense) * 100, 1
        )
    if total_income != 0:
        net_saving_percent = round(
            ((total_income - total_expense) / total_income) * 100, 1
        )
    else:
        net_saving_percent = 0
    if total_expense != 0:
        net_expenditure_percent = round(
            ((total_expense - total_income) / total_expense) * 100, 1
        )
    else:
        net_expenditure_percent = 0

    total_balance = f"{round(total_balance, 1):,}"
    total_income = f"{round(total_income, 1):,}"
    total_expense = f"{round(total_expense, 1):,}"

    recent_five_transactions = Transaction.objects.all().order_by("-transaction_date")
    recent_five_transactions = recent_five_transactions[:5]

    return render(
        request,
        "tracker/dashboard.html",
        {
            "total_balance": total_balance,
            "total_income": total_income,
            "total_expense": total_expense,
            "net_saving_percent": net_saving_percent,
            "net_expenditure_percent": net_expenditure_percent,
            "no_of_transactions": no_of_transactions,
            "category_expenses": category_expenses,
            "recent_five_transactions": recent_five_transactions,
        },
    )
    # except:
    #     return render(request, "404.html")


def transactions(request):
    all_transactions = Transaction.objects.all().order_by("-transaction_date")
    count_of_transactions = len(all_transactions)
    return render(
        request,
        "tracker/transactions.html",
        {
            "all_transactions": all_transactions,
            "count_of_transactions": count_of_transactions,
        },
    )


def view_transaction(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        transaction_form = Transaction_Form(instance=transaction)

        for field in transaction_form.fields.values():
            field.disabled = True

        return render(
            request,
            "tracker/view_transaction.html",
            {"transaction_form": transaction_form, "transaction_id": transaction.id},
        )

    except:
        return render(request, "404.html")


def add_transaction(request):
    if request.method == "POST":
        new_transaction = Transaction_Form(request.POST)
        if new_transaction.is_valid():
            new_transaction.save()
            messages.success(request, "Transaction Added Successfully!")
            return HttpResponseRedirect(reverse("transactions"))
        return render(
            request,
            "tracker/add_transactions.html",
            {"transaction_form": new_transaction},
        )

    return render(
        request, "tracker/add_transactions.html", {"transaction_form": Transaction_Form}
    )


def edit_transaction(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id)

        if request.method == "POST":
            transaction_form = Transaction_Form(request.POST, instance=transaction)
            if transaction_form.is_valid():
                transaction_form.save()
                messages.success(request, "Transaction Edited Successfully!")
                return HttpResponseRedirect(
                    reverse("view_transaction", args=[transaction_id])
                )
            return render(
                request,
                "tracker/edit_transaction.html",
                {
                    "transaction_form": transaction_form,
                    "transaction_id": transaction.id,
                },
            )
        else:
            transaction_form = Transaction_Form(instance=transaction)
            return render(
                request,
                "tracker/edit_transaction.html",
                {
                    "transaction_form": transaction_form,
                    "transaction_id": transaction.id,
                },
            )

    except:
        return render(request, "404.html")


def delete_transaction(request, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        if request.method == "POST":
            transaction.delete()
            messages.success(request, "Transaction Deleted Successfully!")
            return HttpResponseRedirect(reverse("transactions"))

        transaction_form = Transaction_Form(instance=transaction)
        for field in transaction_form.fields.values():
            field.disabled = True

        return render(
            request,
            "tracker/delete_transaction.html",
            {"transaction_form": transaction_form, "transaction_id": transaction_id},
        )

    except:
        return render(request, "404.html")


def settings(request):
    return render(request, "tracker/settings.html")


def delete_all_transactions(request):
    if request.method == "POST":
        Transaction.objects.all().delete()
        messages.success(request, "All transactions have been deleted")
        return HttpResponseRedirect(reverse("dashboard"))
    return HttpResponseRedirect(reverse("settings"))
