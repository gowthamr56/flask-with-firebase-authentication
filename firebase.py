import pyrebase
import json
from pprint import pprint

config = json.load(open("firebase_config.json"))

pb = pyrebase.initialize_app(config)
auth = pb.auth()

def signup(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        auth.send_email_verification(user["idToken"])
    except Exception as e:
        if "EMAIL_EXISTS" in e.strerror:
            return "E-mail already exists", "error"
        elif "WEAK_PASSWORD" in e.strerror:
            return "Password should be atleast 6 characters", "error"
        else:
            return e.strerror, "error"
    else:
        return "Successfully signed up", "success"

def signin(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        isVerified = auth.get_account_info(user["idToken"])["users"][0]["emailVerified"]
        
        if isVerified:
            return "Successfully logged in", "success"
        else:
            auth.send_email_verification(user["idToken"])
            return "email not verified", "success"
    
    except Exception as e:
        if "INVALID_PASSWORD" in e.strerror:
            return "Incorrect password", "error"
        elif "EMAIL_NOT_FOUND" in e.strerror:
            return "Incorrect e-mail", "error"

# signup = signup("gowtham180502@gmail.com", "123456")
# print(signup)

# login = login("gowtham180502@gmail.com", "123456")
# print(login)

