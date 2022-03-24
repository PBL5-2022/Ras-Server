from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'heroes', views.HeroViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('dht11/', views.DHT11Manage.as_view()),
    path('bh1750', views.BH1750Manage.as_view()),
    path('car/', views.CarsAPIView.as_view()),
    path('led', views.LedManage.as_view()),
    path('schedule/', views.ScheduleManage.as_view()),
    path('schedule/cron', views.ScheduleManage_Cron.as_view()),
    path('api/register', views.UserRegisterView.as_view(), name='register'),
    path('api/login', views.UserLoginView.as_view(), name='login'),
]
