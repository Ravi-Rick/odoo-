import requests
from odoo import models, fields, api
from odoo import http,fields
from odoo.http import request
import base64



class SMSApi(http.Controller):
    @http.route('/api/send_sms_otp', type='json', auth='public', csrf=False, cors='*')
    def send_sms_otp(self,lang='ar_001',massage='',numbers=[],user=None,):
        app_id = request.env['ir.config_parameter'].sudo().get_param('cspl_eccomerce_api.sms_api_id')
        app_sec = request.env['ir.config_parameter'].sudo().get_param('cspl_eccomerce_api.sms_api_secret')
        app_hash = base64.b64encode(f"{app_id}:{app_sec}".encode()).decode()
        messages = {
            "messages": [
                {
                    "text": massage,
                    "numbers": numbers,
                    "sender": request.env['ir.config_parameter'].sudo().get_param('cspl_eccomerce_api.sms_api_senders')
                    # "sender": "Awalem.m-AD"
                }
            ]
        }

        url = "https://api-sms.4jawaly.com/api/v1/account/area/sms/send"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {app_hash}"
        }

        response = requests.post(url, headers=headers, json=messages)
        response_json = response.json()
        try:
            sms_values = {
                'number': numbers[0],  # Replace with the actual phone number
                'partner_id': user.id if user else None,
                'body': massage,  # Replace with the actual SMS content
                'state': 'sent' if response.status_code == 200 else 'error', # Replace with
            }
            new_sms_record = request.env['sms.sms'].sudo().create(sms_values)
        except:
            pass
        return response_json
        