from django.urls import path

from appcore.api import (
    admin_medida,
    binnacle,
    reason,
    table,
    tree
)
from appcore.api import collector
from appcore.api import filter_general

urlpatterns = [
    # FILTERS GENERAL APP
    path('filter/substation/', filter_general.SubstationView.as_view()),
    path('filter/level-tension/', filter_general.LevelTensionsView.as_view()),
    path('filter/measurement-point/', filter_general.MeasurementPointsView.as_view()),
    path('filter/measurement-socket/', filter_general.MeasurementSocketView.as_view()),

    # MEASUREMENT
    path('admin/measurement/', admin_medida.MeasurementView.as_view()),

    # BINNACLE
    path('binnacle/firstlist/', binnacle.InfoView.as_view()),
    path('binnacle/consult/', binnacle.ConsultView.as_view()),

    # COLLECTOR
    path('collector/', collector.CollectorView.as_view()),
    path('collector/mail/', collector.MailView.as_view()),

    # GROUNDS
    path('reason/', reason.IndexView.as_view()),
    path('reason/create/', reason.CreateView.as_view()),

    # TREE
    path('tree/', tree.IndexView.as_view()),

    # DATATABLES
    path('table/collector-manual/', table.CollectorManualView.as_view()),
]
