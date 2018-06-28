from django.conf.urls import url
from django.contrib import admin
from boards import views
## from django.urls import path     # for django 2.0 


urlpatterns = [
    url(r'^$', views.home, name='home'),   # path('', views.home, name='home'),for django 2.0
    url(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    url(r'^admin/', admin.site.urls),
]
