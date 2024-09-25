import base64
import hashlib
import json
import time

def create_jwt(payload, secret_key, algorithm='HS256'):
	header = {"alg": algorithm, "typ": "JWT"}
	encoded_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode()

	encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()

	message = f"{encoded_header}.{encoded_payload}"
	signature = base64.urlsafe_b64encode(hashlib.sha256((message + secret_key).encode('utf-8')).digest()).decode('utf-8')
	return (f"{message}.{signature}")

def decode_jwt(jwt_token, secret_key, algorithm='HS256'):

    try:
        header_encoded, payload_encoded, signature_encoded = jwt_token.split('.')

        header = json.loads(base64.urlsafe_b64decode(header_encoded + '==').decode('utf-8'))
        payload = json.loads(base64.urlsafe_b64decode(payload_encoded + '==').decode('utf-8'))

        message = header_encoded + '.' + payload_encoded
        signature = base64.urlsafe_b64encode(hashlib.sha256((message + secret_key).encode('utf-8')).digest()).decode('utf-8')

        if signature_encoded == signature:
            return payload
        else:
            return None

    except Exception as e:
        print(f"Erro ao decodificar o token: {e}")
        return None

