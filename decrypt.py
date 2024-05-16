import orjson
import pgpy
from urllib.parse import unquote

def clean_pgp_message(encoded_message):
    # Split the message into headers and body
    header_end_index = encoded_message.find("\n\n")  # Find the end of headers
    headers = encoded_message[:header_end_index]
    body = encoded_message[header_end_index:]

    # Replace '+' characters in the headers
    cleaned_headers = headers.replace("+", " ")

    # Concatenate the cleaned headers and the body
    cleaned_message = cleaned_headers + body
    
    return unquote(cleaned_message)

def pgp_decrypt(a_message:str, a_merchant_private_pgp:str, a_dbs_public_pgp:str = ""):
    try:
        # Load private key
        merchant_key, _ = pgpy.PGPKey.from_file(a_merchant_private_pgp)

        # Webhook message
        if a_dbs_public_pgp != "":
            a_message = clean_pgp_message(a_message)

        pgp_message = pgpy.PGPMessage.from_blob(a_message)

        # Decrypt message
        decrypted_message = merchant_key.decrypt(pgp_message)

        message = orjson.loads(decrypted_message.message)

        # Return decrypted message content
        return message

    except Exception as e:
        # Print the exception for debugging purposes
        print(str(e))
        return "Error occurred during decryption."