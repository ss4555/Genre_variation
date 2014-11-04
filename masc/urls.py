from django.conf.urls import patterns, url
from masc import views
urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^upload/$',views.read_csv,name='read_csv'),
                       url(r'^model_graph/$',views.render_model_graph,name='model_graph')
                       )