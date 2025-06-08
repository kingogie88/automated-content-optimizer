import secrets
import base64

def generate_secret_key():
    """Generate a secure secret key."""
    return base64.b64encode(secrets.token_bytes(32)).decode('utf-8')

if __name__ == "__main__":
    print("Generating secure keys for your application...")
    print("\nAPP_SECRET_KEY:")
    print(generate_secret_key())
    print("\nJWT_SECRET_KEY:")
    print(generate_secret_key())
    print("\nStore these keys in your .env file and never share them!")
