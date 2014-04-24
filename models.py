# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Perfil(AbstractUser):
	telefone = models.CharField(max_length=100, blank=True)
	papel = models.ForeignKey('Papel', null=True, blank=True)
	token = models.CharField(max_length=30, blank=True)
	AbstractUser._meta.get_field('email')._unique = True
	AbstractUser._meta.get_field('email').blank = False
	AbstractUser._meta.get_field('email').null = False
	
	def __unicode__(self):
		if self.first_name:
			return self.get_full_name()
		else:
			return self.username
	
	def __str__(self):
		if self.first_name:
			return self.get_full_name()
		else:
			return self.username

class Papel(models.Model):
	nome = models.CharField(max_length=300)
	atividades = models.TextField()
	
	def __unicode__(self):
		return self.nome