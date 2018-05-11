from django.conf.urls  import url
from axf import views


urlpatterns = [
    url(r'^home/', views.home),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^register/', views.register),
    url(r'^myself/', views.myself),
    url(r'^cart/', views.cart),
    url(r'^market/$', views.market),
    url(r'^marketinfo/(\d+)/(\d+)/(\d+)/', views.marketinfo, name='marketinfo'),
    url(r'^addgood/', views.addgood, name='addgood'),
    url(r'^subgood/', views.subgood, name='subgood'),
    url(r'^goodselect/', views.goodselect, name='goodselect'),
    url(r'^allselect/', views.allselect, name='allselect'),
    url(r'^order/', views.order, name='order'),
    url(r'^pay/(\d+)/', views.pay, name='pay'),
    url(r'^waitpay/', views.waitpay, name='waitpay'),
    url(r'^payed/', views.payed, name='payed'),
    url(r'^deleteorder/(\d+)/', views.deleteorder, name='deleteorder'),



]