from django.urls import path
from .views import *

urlpatterns = [
    path("", index),

    # =============== URL USER =====================
    path("register", UserView.register),
    path("login", UserView.login),
    path("list-user", UserView.list_user),
    path("list-manage", UserView.list_user_manage),
    path("list-customer", UserView.list_user_customer),
    path("logout", UserView.logout),
    path("search-user", UserView.search_user),
    path("update-user/<pk>", UserView.update_user),
    path("delete-user/<pk>", UserView.delete_user),
    # ===============================================

    # =============== URL SUPPLIER ===================
    path("create-supplier", SupplierView.create_supplier),
    path("list-supplier", SupplierView.list_supplier),
    path("search-supplier", SupplierView.search_supplier),
    path("update-supplier/<pk>", SupplierView.update_supplier),
    path("delete-supplier/<pk>", SupplierView.delete_supplier),
    # ================================================

    # =============== URL CATEGORY ===================
    path("create-category", CategoryView.create_category),
    path("list-category", CategoryView.list_category),
    path("search-category", CategoryView.search_category),
    path("get-category/<pk>", CategoryView.get_category_by_id),
    path("update-category/<pk>", CategoryView.update_category),
    path("delete-category/<pk", CategoryView.delete_category),
    # ================================================

    # ============== URL BRANCH ======================
    path("create-branch", BranchView.create_branch),
    path("list-branch", BranchView.list_branch),
    path("update-branch/<pk>", BranchView.update_branch),
    path("delete-branch/<pk>", BranchView.delete_branch),
    # ================================================
]