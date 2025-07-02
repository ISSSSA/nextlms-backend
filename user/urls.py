from django.urls import path
from user.rest.views import AuthNonceView, AuthVerifyView

urlpatterns = [
    path('user/nonce/<str:wallet_address>/', AuthNonceView.as_view(), name='auth_nonce'),
    path('user/verify/', AuthVerifyView.as_view(), name='auth_verify'),
]
