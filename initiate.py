from decrypt import pgp_decrypt
from encrypt import pgp_encrypt
import requests

def initiate(a_headers,a_body):
    # Encrypt message
    merchant_private_pgp_file_loc = f"./path/to//merchant_private.asc"
    dbs_public_pgp_file_loc = f"./path/to//dbs_public_api.asc"
    dbs_public_pgp_hpp_file_loc = f"./path/to//dbs_public_hpp.asc"
    encrypted_msg = pgp_encrypt(a_body, merchant_private_pgp_file_loc, dbs_public_pgp_file_loc)

    # Update after initialization took place
    return_message = {
        "payload": {"message": "PGP Encryption Failed"},
        "error_code": 401
    }

    if encrypted_msg:
        # Do Request
        response = requests.post("https://testcld-enterprise-api.dbs.com/api/sg/hpp/v4/payment/transaction", data=encrypted_msg, headers=a_headers)
        if response.text and response.text != "":
            pgp_decrypted_response = pgp_decrypt(response.text, merchant_private_pgp_file_loc)
            if pgp_decrypted_response:
                
                '''
                    Additional code like saving response to database
                '''
                database_response = 'OK'

                if database_response == 'OK':
                    # Check transaction status
                    if "data" in pgp_decrypted_response and len(pgp_decrypted_response["data"]) > 0:
                        if "txnResponse" in pgp_decrypted_response["data"][0]:
                            txn_response = pgp_decrypted_response["data"][0]["txnResponse"]
                            if txn_response["txnStatus"] == "ACTC":
                                # Success

                                # Compile form request data
                                form_message = {
                                    "orgId": a_headers["X-DBS-ORG_ID"],
                                    "transactionId": txn_response["transactionId"]
                                }

                                encrypted_form_payload = pgp_encrypt(form_message, merchant_private_pgp_file_loc,
                                                                     dbs_public_pgp_hpp_file_loc)
                                if encrypted_form_payload:
                                    txn_response["form_request_payload"] = {
                                        "requestId": txn_response["requestId"],
                                        "encryptedPayload": encrypted_form_payload
                                    }

                                    return_message["payload"] = txn_response
                                    return_message["error_code"] = 0
                                else:
                                    return_message["payload"]["message"] = "Form request payload could not be created"
                            else:
                                return_message["payload"]["message"] = txn_response["txnStatusDescription"]
                        else:
                            return_message["payload"]["message"] = "No response transaction data returned"
                    else:
                        return_message["payload"]["message"] = "No response data returned"
                else:
                    return_message["payload"]["message"] = database_response

                # Check response
        else:
            return_message["payload"]["message"] = response.text
    else:
        return_message["payload"]["message"] = encrypted_msg

    return return_message