from django.urls import path
import tracker.views as views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("transactions", views.transactions, name="transactions"),
    path(
        "transactions/<int:transaction_id>",
        views.view_transaction,
        name="view_transaction",
    ),
    path(
        "transactions/<int:transaction_id>/edit",
        views.edit_transaction,
        name="edit_transaction",
    ),
    path(
        "transactions/<int:transaction_id>/delete",
        views.delete_transaction,
        name="delete_transaction",
    ),
    path("add_transaction", views.add_transaction, name="add_transaction"),
    path("settings", views.settings, name="settings"),
    path(
        "settings/delete_all_transactions",
        views.delete_all_transactions,
        name="delete_all_transactions",
    ),
]
