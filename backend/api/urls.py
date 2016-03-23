from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include

from . import views

urlpatterns = [
    url(r'^inventaire/$', views.InventaireList.as_view()),
    url(r'^clients/$', views.ClientsList.as_view()),
    url(r'^clients/(?P<pk>[0-9]+)$', views.ClientDetail.as_view()),
    url(r'^commande/(?P<pk>[0-9]+)', views.commande)
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns +=  [
    url(r'^login', views.login),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
