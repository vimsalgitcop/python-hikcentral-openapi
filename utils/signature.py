import hashlib
import hmac
import base64
import time
from utils.config import Config
 
def generate_signature(method: str, api_path: str) -> tuple[str, str]:
    try:
        timestamp = str(int(time.time() * 1000))
        sign_str = f"{method}\n*/*\napplication/json\n{api_path}".encode('utf-8')
        signature = hmac.new(Config.APP_SECRET.encode('utf-8'), sign_str, hashlib.sha256).digest()
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        return signature_b64, timestamp
    except Exception as e:
        raise ValueError(f"Error generating signature: {str(e)}")