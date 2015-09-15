# -*- coding: utf-8 -*-
import string, random
from django.conf import settings
from django.shortcuts import render, get_object_or_404 as g404
from django.http import HttpResponseRedirect as red
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from .forms import PerfilForm, LoginForm
from .models import Perfil
 
def registro(request):
    form = PerfilForm()
    if request.POST:
        form = PerfilForm(request.POST)
        if form.is_valid():
            u = form.save(commit=False)
            #u.is_active = False
            u.save()
            return red("/")
    return render(request, "register.html", {'form': form})

def get_token(request):
    uname = request.REQUEST.get('uname', False)
    msg = False
    if uname:
        try:
            token = "".join([random.choice(string.hexdigits) for n in xrange(30)]).upper()
            u = g404(Perfil, username=uname)
            u.token = token
            u.save()
        except:
            msg = "User not found. Contact our support."
            return render(request, "get_token.html", {'msg': msg})
        if u.email:
            uri = settings.BASE_URL + "/perfil/forgot-password/?u="+u.username+"&t="+u.token
            u.email_user("Password change", "To redefine your password, please follow: " + uri)
            msg = "Check your inbox. " + "(" + u.email + ")"
        else:
            msg = "You do not have an e-mail set in your account."
            
    return render(request, "get_token.html", {'msg': msg})

def mudar_senha(request):
    token = request.REQUEST.get('t', False)
    uname = request.REQUEST.get('u', "")
    senha = request.REQUEST.get('s', False)
    msg = False
    if token:
        if uname and senha:
            try:
                u = Perfil.objects.get(username=uname)
                if token == u.token:
                    if senha:
                        u.set_password(senha)
                        u.token = "".join([random.choice(string.hexdigits) for n in xrange(30)]).upper()
                        u.save()
                        uh = authenticate(username=uname, password=senha)
                        login(request, uh)
                        return red('/')
            except Perfil.DoesNotExist:
                msg = "The user does not exist."
        else:
            msg = "Enter the username and the new password."
        
    return render(request, "mudar_senha.html", {'msg': msg, 'token': token, 'uname': uname})

def entrar(request):
    form = LoginForm()
    msg = False
    next = request.REQUEST.get('next', '/')
    e = ""
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            e = form.cleaned_data['username']
            p = form.cleaned_data['password']
            ah = authenticate(username=e, password=p)
            if ah is not None:
                if ah.is_active:
                    login(request, ah)
                    #request.session.set_expiry(7200)
                    return red(next)
                else:
                    msg = "Inactive user"
            else:
                msg = "User or password are wrong."
    return render(request, "login.html", {'msg': msg, 'form': form, 'next': next, 'uname': e})

def sair(request):
    logout(request)
    return red("/")
