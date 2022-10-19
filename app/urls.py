# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf.urls import url
from django.urls import path, re_path, include
# from myFinance import views as f_views
from rest_framework.routers import DefaultRouter

from app import views
from app.views import TransactionViewSet, UserTagViewSet, CredentialViewSet, UserTagGoalView
from myFinance.admin import admin_site

adminurlpatterns = [
    url(r'^myadmin/', admin_site.urls),
]
urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    # re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    # re_path(r'tag.html.*$', views.by_tag, name="tag"),
    # re_path(r'transaction.html.*$', views.by_name, name="transaction"),
    # re_path(r'tables.html.*$', views.tabels, name="load_statements"),
    # re_path(r'profile.html.*$', views.pages, name="profile"),
    re_path(r'add_tag.*$', views.add_tag, name="add_tag"),
    # re_path(r'planing.*$', views.planing, name="planing"),
    re_path(r'summery_widgets.*$', views.SummeryWidgetsView.as_view(), name="summery_widgets"),
    re_path(r'total_month_expenses.*$', views.TotalMonthExpensesView.as_view(), name="summery_widgets"),
    re_path(r'month_category.*$', views.MonthCategoryView.as_view(), name="month_category"),
    re_path(r'bank_info.*$', views.BankInfo.as_view(), name="month_category"),
    # path('', views.index, name='home'),
    path('create/', views.TransactionCreateView.as_view(), name='create_transaction'),
    path('api/month-tracking', views.MonthTrackingView.as_view(), name='create_transaction'),
    path('api/user_credentials/', views.CredentialTypes.as_view()),
    path('api/user_goals/', views.UserTagGoalView.as_view()),
]

urlpatterns += adminurlpatterns

router = DefaultRouter()
router.register(r'user_transactions', TransactionViewSet, basename='user_transactions')
router.register(r'user_accounts', CredentialViewSet, basename='user_accounts')
router.register(r'user_tags', UserTagViewSet, basename='user_tags')
urlpatterns += router.urls

dj_login_patterns = [path('dj-rest-auth/', include('dj_rest_auth.urls')),
                     path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))]
urlpatterns += dj_login_patterns
