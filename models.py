# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Perfil(AbstractUser):
    telefone = models.CharField("Phone number", max_length=100, blank=True)
    papel = models.ForeignKey('Papel', null=True, verbose_name="Role", blank=True)
    token = models.CharField(max_length=30, blank=True)
    
    class Meta:
        ordering = ['first_name']

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

class Papel(models.Model): ## User role
    nome = models.CharField("Role name", max_length=300)
    atividades = models.TextField("Assignments")

    def __unicode__(self):
        return self.nome