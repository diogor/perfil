# django-perfil
Django app to manage users

## Install
 - add 'django-perfil' to yous installed apps.
 - add to your settings.py:
  - AUTH_USER_MODEL = "perfil.Perfil"
  - LOGIN_URL = "/perfil/login/"
 - add to your main urls.py:
  - url(r'^perfil/', include('perfil.urls')),
