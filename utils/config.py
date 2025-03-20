import os
from dotenv import load_dotenv
 
load_dotenv()
 
class Config:
    HIKCENTRAL_IP = os.getenv("HIKCENTRAL_IP")
    APP_KEY = os.getenv("APP_KEY")
    APP_SECRET = os.getenv("APP_SECRET")
 
    @staticmethod
    def validate_config():
        missing_vars = [var for var in ['HIKCENTRAL_IP', 'APP_KEY', 'APP_SECRET'] if not getattr(Config, var)]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {', '.join(missing_vars)}")
 
Config.validate_config()