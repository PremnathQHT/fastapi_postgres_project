import pyotp

def generate_otp(secret_key):

    totp = pyotp.TOTP(secret_key, interval=60)
    otp = totp.now()
    return otp

def verify_otp(secret_key, user_input_otp):

    totp = pyotp.TOTP(secret_key, interval=60)
    return totp.verify(user_input_otp)

# Example usage:# Assuming this is the user's stored secret key retrieved from the database
secret_key = "user's_stored_secret_key"# Generate OTP
generated_otp = generate_otp(secret_key)
print(f"Generated OTP: {generated_otp}")

# Simulate user input for OTP verification
user_input_otp = input("Enter OTP: ")

# Verify the OTP
if verify_otp(secret_key, user_input_otp):
    print("OTP is valid!")
else:
    print("OTP is invalid or expired.")

