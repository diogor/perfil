from django.conf.urls import patterns, include, url

urlpatterns = patterns('perfil.views',
	url(r'^registrar/$', 'registro', name='home'),
	url(r'^esqueci-a-senha/$', 'mudar_senha', name='mudar_senha'),
	url(r'^get-token/$', 'get_token', name='get_token'),
)

urlpatterns += patterns('',
	url(r'^login/$', 'perfil.views.entrar', name='login'),
	url(r'^logout/$', 'perfil.views.sair', name='logout'),
)