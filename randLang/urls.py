from django.urls import path
from randLang import views

app_name = 'randLang'
urlpatterns = [

  # redirects all urls the url in the webapp "randLang"

  path('', views.show_letters, name="show_letters"),
  path('show_letters', views.show_letters, name="show_letters"),
  path('show_lang', views.show_lang, name="show_lang"),
  path('show_letters_warning', views.show_letters, name="show_letters"),
  path('generate_pdf', views.generate_pdf, name="generate_pdf"),
]
