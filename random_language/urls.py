"""random_language URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include

from django.conf.urls import url, include
from django.contrib.auth.models import User
from randLang.models import User_Created
from randLang.models import Dict_Words
from rest_framework import routers, serializers, viewsets
from django.urls import re_path

class UserCreatedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User_Created
        fields = ['language','user_word', 'definition']
class EnglishWordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dict_Words
        fields = ['word']
# ViewSets define the view behavior.
class UserCreatedSet(viewsets.ModelViewSet):
    queryset = User_Created.objects.all()
    serializer_class = UserCreatedSerializer
class EnglishWords(viewsets.ModelViewSet):
    queryset = Dict_Words.objects.all()
    serializer_class = EnglishWordSerializer
# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'user_created', UserCreatedSet)
router.register(r'dict_words',EnglishWords)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.



urlpatterns = [
    path('adminlang/', admin.site.urls),
    url(r'^', include(router.urls)),
    path('randLang/',include('randLang.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
    re_path('api/', include('randLang.urls')),
]
