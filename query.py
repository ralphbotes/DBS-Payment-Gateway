from datetime import datetime
from utils import dbs_timestamp
from decrypt import pgp_decrypt
from encrypt import pgp_encrypt
import requests

def query_status(a_transaction_data):
    transaction_id = a_transaction_data["transactionId"]
    reference = a_transaction_data["reference"]

    date_obj = datetime.now()
    msgId = dbs_timestamp(date_obj,2)
    timeStamp = dbs_timestamp(date_obj)

    dbs_headers = {
        "x-api-key": "api_key",
        "X-DBS-ORG_ID": "org_id",
        "Content-Type": "text/plain",
        "Accept": "text/plain"
    }

    body = {
        "header": {
            "msgId": msgId,
            "orgId": "org_id",
            "timeStamp": timeStamp
        },
        "data": [
            {
                "txnInfo": {
                    "transactionId": transaction_id,
                    "merchantReference": reference,
                    "version": "2.1"
                }
            }
        ]
    }

    url = "https://testcld-enterprise-api.dbs.com/api/sg/hpp/v4/enquiry/transactionstatus"

    # Encrypt message
    merchant_private_pgp_file_loc = f"./path/to/merchant_private.asc"
    dbs_public_pgp_file_loc = f"./path/to/dbs_public_api.asc"
    encrypted_msg = pgp_encrypt(body, merchant_private_pgp_file_loc, dbs_public_pgp_file_loc)

    if encrypted_msg:
        # Do Request
        response = requests.post(url, data=encrypted_msg, headers=dbs_headers)
        if response.text and response.text != "":
            pgp_decrypted_response = pgp_decrypt(response.text, merchant_private_pgp_file_loc)
            if pgp_decrypted_response:
                '''
                    Additional code like saving response to database
                '''
                database_response = 'OK'
                
                return pgp_decrypted_response