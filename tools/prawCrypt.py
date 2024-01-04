from cryptography.fernet import Fernet , InvalidToken
import hashlib
import base64

def generate_key_from_string(input_string):
    hashed_string = hashlib.sha256(input_string.encode()).digest()
    key = base64.urlsafe_b64encode(hashed_string)
    return key


def encrypt(message, password):
    key = generate_key_from_string(password)
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt(encrypted_message, password):
    try:
        key = generate_key_from_string(password)
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message).decode()
        return decrypted_message
    except InvalidToken:
        print("Invalid token")
        pass


# encrypted_client_ID = encrypt(reddit_client_ID, password)
# encrypted_secret_token = encrypt(reddit_secret_token, password)
# encrypted_usernName = encrypt(reddit_usernName, password)
# encrypted_password = encrypt(reddit_password, password)

# encrypted_values = {
#     'reddit_client_ID': encrypted_client_ID,
#     'reddit_secret_token': encrypted_secret_token,
#     'reddit_usernName': encrypted_usernName,
#     'reddit_password': encrypted_password
# }
# import pickle
# with open('encrypted_values.pkl', 'wb') as file:
#     pickle.dump(encrypted_values, file)


