
import nacl.encoding
import nacl.signing
import base58

from eth_account.messages import defunct_hash_message
from eth_account import Account
from solders.pubkey import Pubkey
# from ethereum.utils import checksum_encode

# def is_valid_ethereum_address(address):
#     try:
#         checksum_encode(bytes.fromhex(address.lower()))
#         return True
#     except:
#         return False


def is_valid_solana_address(address):
    # Implement your Solana address validation logic here
    try:
        Pubkey.from_string(address)
        return True
    except Exception:
        return False


def verify_signature(nonce, signature, public_key, wallet_type):
    try:
        verified = False
        if wallet_type == "solana":
            signature_bytes = base58.b58decode(signature)
            message_bytes = nonce.encode('utf-8')
            public_key_bytes = base58.b58decode(public_key)
            verify_key = nacl.signing.VerifyKey(
                public_key_bytes, encoder=nacl.encoding.RawEncoder)
            verify_key.verify(message_bytes, signature_bytes)
            verified = True
        else:
            message_hash = defunct_hash_message(text=nonce)
            retrieved_address = Account.recover_message(
                message_hash, signature=signature)
            verified = retrieved_address.lower() == public_key.lower()
        return verified
    except Exception as e:
        print(e)  # Handle or log the exception appropriately
        return False
