"""helplife URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from helplifeapi.views import register_user, login_user
from helplifeapi.views import CareTipView, PlantView, PlantCareTipView, PlantTypeView, UserPlantPlantTypeView
from helplifeapi.views import HelpLifeUserView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Help Life Find a Way API",
        default_version='v1',
        description="API for creating Plants and claiming up available plants.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@HelpLife.local"),
        license=openapi.License(name="BSD License"),
    ),

    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'careTips', CareTipView, 'careTip')
router.register(r'plants', PlantView, 'plant')
router.register(r'plantCareTips', PlantCareTipView, 'plantCareTip')
router.register(r'plantTypes', PlantTypeView, 'plantType')
router.register(r'userPlantPlantTypes', UserPlantPlantTypeView, 'userPlantPlantType')
router.register(r'helplifeusers', HelpLifeUserView, 'helplifeuser')


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
