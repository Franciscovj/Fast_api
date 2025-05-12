# generate_key.py
import secrets

if __name__ == "__main__":
    print(secrets.token_urlsafe(32))
