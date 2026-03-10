import base64

_SHIFT = 7

def encrypt_password(plain: str) -> str:
    shifted = "".join(chr((ord(c) + _SHIFT) % 256) for c in plain)
    encoded = base64.b64encode(shifted.encode("latin-1")).decode("utf-8")
    return encoded

def decrypt_password(cipher: str) -> str:
    decoded_bytes = base64.b64decode(cipher.encode("utf-8"))
    decoded_str = decoded_bytes.decode("latin-1")
    plain = "".join(chr((ord(c) - _SHIFT) % 256) for c in decoded_str)
    return plain


