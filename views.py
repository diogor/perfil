# -*- coding: utf-8 -*-
import string, random
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect as red
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from perfil.forms import PerfilForm, LoginForm
from perfil.models import Perfil

def registro(request):
	form = PerfilForm()
	if request.POST:
		form = PerfilForm(request.POST)
		if form.is_valid():
			form.save()
			return red("/")
	return render(request, "register.html", {'form': form})

def entrar(request):
	form = LoginForm()
	msg = False
	next = request.REQUEST.get('next', '/')
	if request.POST:
		form = LoginForm(request.POST)
		if form.is_valid():
			e = form.cleaned_data['username']
			p = form.cleaned_data['password']
			ah = authenticate(username=e, password=p)
			if ah is not None:
				if ah.is_active:
					login(request, ah)
					return red(next)
				else:
					msg = "Usuário Inativo."
			else:
				msg = "Usuário ou senha errados."
	return render(request, "login.html", {'msg': msg, 'form': form, 'next': next})

def get_token(request):
	uname = request.REQUEST.get('uname', False)
	msg = False
	if uname:
		token = "".join([random.choice(string.hexdigits) for n in xrange(30)]).upper()
		u = g404(Perfil, username=uname)
		u.token = token
		u.save()
		if u.email:
			uri = settings.BASE_URL + "/perfil/esqueci-a-senha/?u="+u.username+"&t="+u.token
			u.email_user("Recuperação de senha", "Para redefinir a sua senha acesse: " + uri)
			msg = "Verifique o seu e-mail. " + "(" + u.email + ")"
		else:
			msg = "Você não possui email cadastrado. Contate o suporte."

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
						return red('/perfil/login/?next=/painel/')
			except Perfil.DoesNotExist:
				msg = "Não existe o usuário informado."
		else:
			msg = "Informe o nome de usuário e a nova senha."

	return render(request, "mudar_senha.html", {'msg': msg, 'token': token, 'uname': uname})

def sair(request):
	logout(request)
	return red("/")