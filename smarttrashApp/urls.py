from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^token$', views.token, name='token'),
    url(r'^$', views.setup_wifi, name='index'),
    url(r'^setup_acc$', views.setup_acc, name='setup_wifi'),
    url(r'^setup_list$', views.setup_list, name='setup_list'),
    url(r'^setup_configuration$', views.setup_configuration, name='setup_configuration'),
    url(r'^create_list$', views.create_list, name='create_list'),
    url(r'^test$', views.test, name='test'),
]
