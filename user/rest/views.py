from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from drf_yasg.utils import swagger_auto_schema
import secrets

@method_decorator(csrf_exempt, name='dispatch')
class AuthNonceView(View):
    @swagger_auto_schema()
    def get(self, request, wallet_address):
        print(wallet_address)
        nonce = secrets.token_hex(32)
        request.session[f'auth_nonce_{wallet_address.lower()}'] = nonce
        return JsonResponse({'nonce': nonce})

@method_decorator(csrf_exempt, name='dispatch')
class AuthVerifyView(View):
    @swagger_auto_schema()
    def post(self, request):
        wallet_address = request.POST.get('wallet_address')
        signature = request.POST.get('signature')
        nonce = request.session.get(f'auth_nonce_{wallet_address.lower()}')

        if not nonce:
            return JsonResponse({'error': 'Nonce not found'}, status=400)

        user = authenticate(
            request,
            wallet_address=wallet_address,
            signature=signature,
            nonce=nonce
        )

        if user is not None:
            login(request, user)
            del request.session[f'auth_nonce_{wallet_address.lower()}']
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Invalid signature'}, status=401)
