"""
Private License (toolsmgt)

This script is privately licensed and confidential. It is not intended for
public distribution or use without explicit permission from the owner.

All rights reserved (c) 2024.
"""

__author__ = "Premnath Palanichamy"
__copyright__ = "Copyright 2024, toolsmgt"
__license__ = "Refer Terms and Conditions"
__version__ = "1.0"
__maintainer__ = "Premnath"
__email__ = "premnath@quehive.com"
__status__ = "Development"
__desc__ = "Main Program of toolsmgt applications"


from passlib.context import CryptContext

# Initialize CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encrypt_password(password: str) -> str:
    """Encrypt a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

# # Test with a known password
# test_password = "my_secret_password"
# hashed_password = encrypt_password(test_password)

# print("Hashed Password:", hashed_password)
# print("Verification:", verify_password(test_password, hashed_password))

