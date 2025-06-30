from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from web3 import Web3
from web3.middleware import geth_poa_middleware

User = get_user_model()


class Web3Backend(BaseBackend):
    def __init__(self):
        self.w3 = Web3()
    def authenticate(self, request, wallet_address=None, signature=None, nonce=None):
        if not all([wallet_address, signature, nonce]):
            return None

        if not self._verify_signature(wallet_address, signature, nonce):
            return None

        try:
            user = User.objects.get(wallet_number__iexact=wallet_address)
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=wallet_address,
                wallet_number=wallet_address
            )

        return user

    def _verify_signature(self, wallet_address, signature, nonce):
        message = f"Auth login: {nonce}"
        try:
            recovered_address = self.w3.eth.account.recover_message(
                self.w3.eth.account.messages.encode_defunct(text=message),
                signature=signature
            )
            return recovered_address.lower() == wallet_address.lower()
        except:
            return False

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None