"""
URL configuration for my_library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from loans import views
from loans.views import welcome_view

urlpatterns = [
    path('', views.welcome_view, name='index'),   # <-- new: serve welcome at root
    path('welcome/', views.welcome_view, name='welcome'),
    path('book/<int:book_id>/<int:foo>/<int:bar>', views.get_book, name='get_book'),
    path('admin/', admin.site.urls),
]
