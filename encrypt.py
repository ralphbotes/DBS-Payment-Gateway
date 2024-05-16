import orjson
import pgpy

def pgp_encrypt(a_message, a_merchant_private_pgp, a_dbs_public_pgp):
    l_message = orjson.dumps(a_message).decode('utf-8')

    # Load private key
    merchant_key, _ = pgpy.PGPKey.from_file(a_merchant_private_pgp)

    # Load public key
    bank_key, _ = pgpy.PGPKey.from_file(a_dbs_public_pgp)

    # Create a PGPMessage object
    message = pgpy.PGPMessage.new(l_message)

    # Sign message
    signature = merchant_key.sign(message)

    # Create a PGPMessage object for the signed message
    signed_message = pgpy.PGPMessage.new(l_message)

    # Add signature to the signed message
    signed_message |= signature

    # Encrypt signed message
    encrypted_message = bank_key.encrypt(signed_message)

    # Return signed and encrypted message
    return str(encrypted_message)