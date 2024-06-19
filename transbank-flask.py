from flask import Flask, render_template, request
from flask_cors import CORS
from transbank.common.options import WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.webpay.webpay_plus.transaction import *
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys
import json

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

@app.route("/transaction", methods=["POST"])
def webpay_plus_transaction():
    buy_order = request.form.get("bo")
    session_id = request.form.get("session")
    amount = request.form.get("amount")
    return_url = request.form.get("ru")

    tx = Transaction(WebpayOptions("597055555532", "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C", IntegrationType.TEST))
    response = tx.create(buy_order, session_id, amount, return_url)
    output = response['url'] + "?token_ws=" + response['token']

    return output

@app.route("/transaction_commit", methods=["POST"])
def webpay_plus_commit():
    token = request.form.get("token_ws")

    response = (Transaction(WebpayOptions("597055555532", "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C", IntegrationType.TEST))).commit(token=token)
    
    response_dict = {
        "vci": response['vci'],
        "amount": response['amount'],
        "status": response['status'],
        "buy_order": response['buy_order'],
        "session_id": response['session_id'],
        "card_detail": response['card_detail'],
        "accounting_date": response['accounting_date'],
        "transaction_date": response['transaction_date'],
        "authorization_code": response['authorization_code'],
        "payment_type_code": response['payment_type_code'],
        "response_code": response['response_code'],
        "installments_number": response['installments_number']
    }

    response_json = json.dumps(response_dict)

    return response_json