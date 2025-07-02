from django.urls import path
from .views import XAPIStatementView, XAPIStatementGetView

urlpatterns = [
    path('statements/', XAPIStatementView.as_view(), name='xapi-statements'),
    path('statements/<uuid:statement_id>/', XAPIStatementGetView.as_view(), name='xapi-statement-detail'),
]