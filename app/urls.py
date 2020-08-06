# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from django.conf.urls import url
from django.urls import path, re_path, include

# from myFinance import views as f_views
from app import views

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
    re_path(r'tag.html.*$', views.by_tag, name="tag"),
    re_path(r'transaction.html.*$', views.by_name, name="transaction"),
    re_path(r'tables.html.*$', views.tabels, name="load_statements"),
    re_path(r'profile.html.*$', views.pages, name="profile"),
    re_path(r'add_tag.*$', views.add_tag, name="add_tag"),
    path('', views.index, name='home'),
    path('create/', views.TransactionCreateView.as_view(), name='create_transaction'),
]

urlpatterns += adminurlpatterns
