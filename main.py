from initiate import initiate
from query import query_status

def main():

    ''' ======================================================================================================
        Initiate DBS transaction request
    ====================================================================================================== '''
    
    headers = {
            "x-api-key": "api_key",
            "X-DBS-ORG_ID": "org_id",
            "Content-Type": "text/plain",
            "Accept": "text/plain"
        }
    body = {
            "header": {
                "msgId": "abc20210214150726222",
                "orgId": "orginization_id",
                "timeStamp": "2021-02-14T15:07:26.222" # Can make use of dbs_timestamp import from  utils
            },
            "data":  [
                {
                    "txnInfo": {
                        "typeOfPayment": "w02",
                        "version": "2.1",
                        "merchantInfo": {
                            "brandName": "brand_name",
                            "geoLanguage": "en_US",
                            "returnUrl": "https://mywebsite.co.za/orders",                      
                            "callbackUrl": "https://mywebsite.co.za/backend",                
                            "cancelUrl": "https://mywebsite.co.za/orders?cancelled=true",  
                            "appDeeplinkUrl": None
                        },
                        "customerInfo": {
                            "customerId": "user_123",
                            "hppExpressId": None
                        },
                        "transactionInfo": {
                            "merchantReference": "perftestmyUniqueRef",
                            "txnType": "TX01",
                            "amount": {
                                "amount": 123.23,
                                "currency": "SGD"
                            },
                            "channelType": "HC03"
                        }
                    }
                }
            ]
        }
    response = initiate(headers,body)
    # Response is retuned to your website from your API for example, or however you are handling requests.


    ''' ======================================================================================================
        Redirect to DBS:
            
            redirect_to_page(response["payload"])

            Notes:
                • Assumes initiate was successful. Error handling not supplied.
                • Redirect done in javascript.
    ====================================================================================================== '''

    
    ''' ======================================================================================================
        Additional:
            Initiate DBS transaction status request
            *Requires pre-redirect data saved to the database before initial redirect to DBS portal
    ====================================================================================================== '''
    transaction_data = {
        "transactionId": "dbsTrxID",    # Supplied by DBS when initializing transaction during first time request
        "reference": "perftestmyUniqueRef"
    }
    query_response = query_status(transaction_data)

if "__main__" == __name__:
    main()