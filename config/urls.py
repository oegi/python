"""measurement_system5125 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView

from appcore import views
from appcore.views import admin_medida
from appcore.views import binnacle
from appcore.views import download
from appcore.views import register

urlpatterns = [
    path('', views.IndexView.as_view(), name='path_home'),
    path('registro/', register.IndexView.as_view(), name='path_register'),
    path('reportes/', views.ReportsView.as_view(), name='path_reports'),
    path('registro/exportar/', register.ExportView.as_view(), name='path_register_exp'),
    path('bitacora/exportar/', binnacle.ExportView.as_view(), name='path_binnacle_exp'),
    path('bitacora/', binnacle.BinnacleView.as_view(), name='path_binnacle'),
    path('bitacora/modificar/', views.BinnacleModifyView.as_view(), name='path_binnacle_modify'),
    path('bitacora/motivos/', views.BinnacleGroundsView.as_view(), name='path_binnacle_grounds'),
    path('recolector/', views.CollectorMeasureView.as_view(), name='path_collector'),
    path('recolector/manual/', views.CollectorManualView.as_view(), name='path_collector_manual'),
    path('medidas/', admin_medida.AdminMedidaView.as_view(), name='path_admin_measure'),
    path('api/', include('appcore.api.urls')),
    path('admin/', admin.site.urls),
    path('download/', download.ExportView.as_view()),

    # EMAIL MOCKUP
    # path('test/email/', TemplateView.as_view(template_name='email/binnacle/pending.html')),
]
