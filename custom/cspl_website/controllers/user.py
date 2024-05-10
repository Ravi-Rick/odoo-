from datetime import datetime
from odoo import http
from odoo.http import request
from odoo import http
# from .sms import SMSApi
import random
import string



class User(http.Controller):
    def update_user_last_update(self, user):
        user.sudo().write({"__last_update":datetime.now()})  

    def user_info(self, user):
        return {
            'user_info': {
                'name': user.name,
                'image': f"/web/image?model=res.partner&id={user.id}&field=avatar_512",
                'email': user.email,
                'phone': user.phone,
                'user_exists': user.is_published
            },
            'login_info': {
                'id': user.id,
                'auth_token': user.auth_token
            }
        }


    @http.route('/api/send_opt', type='json', auth='public', csrf=False, cors='*')
    def send_opt(self,customer_id=None):
        user = request.env['res.partner'].sudo().browse(customer_id)
        print(user.company_id.email)
        otp=random.randint(100000, 999999)
        user.sudo().write({'otp':otp})
        template=request.env.ref("cspl_website.mail_template_user_login")
        # companyData = self.get_company_context()
        template.sudo().with_context().send_mail(user.id,force_send=True)
        print(user.phone)
        # sms = SMSApi().send_sms_otp(massage=f'OTP for login is {otp}',numbers=[user.phone],user=user)
        return otp
    
    
      
        
    @http.route('/api/login', type='json', auth='public', csrf=False, cors='*')
    def login(self,phone=None):
        User = request.env['res.partner']
        if User.sudo().search(['&',("is_published","=",True),'|',('phone','=',phone),('email','=',phone)]):
            user = User.sudo().search(['&',("is_published","=",True),'|',('phone','=',phone),('email','=',phone)], limit=1)
            if user.company_type == "person":
                self.send_opt(user.id)
                return {'message': 'Login successfully', 'customer_id': user.id,"code": "1"}
            elif user.company_type == "company":
                return {'error': 'credentials in use by B2B user',"code": "3"}
            else:
                return {'error': "Invalid credentials", "code": "0"}
        else:
            user = User.sudo().search(['|', ('phone', '=', phone), ('email', '=', phone)], limit=1)
            if user.company_type == "company" and user.is_published:
                return {'error': 'credentials in use by B2B user', "code": "3"}
            elif user.company_type == "company" and not user.is_published:
                return {'error': 'credentials in use by B2B user',"code": "3"}
            return {'error': "Invalid credentials", "code": "0"}
        
    
    # @http.route('/api/registerUsers', type='json', auth='public', csrf=False, cors='*')
    # def registerUsers(self,fname,phone,email=None,redirect_url='https://www.letsunify.in:3003/login',city='', **kw):
    #     try:
    #         User = request.env['res.partner']
    #         # url=str(http.request.httprequest).split("'")[1].split("'")[0].replace("registerUsers","registeConfirm")
    #         if User.sudo().search(['&',("is_published","=",True),'|',('phone','=',phone),('email','=',email)]):
    #             user = User.sudo().search(['&',("is_published","=",True),'|',('phone','=',phone),('email','=',phone)], limit=1)
               
    #             if email and  User.sudo().search(['&',("is_published","=",True),('email','=',email)]):
    #                 userData = request.env['res.partner'].sudo().search([("is_published", "=", True), ('email', '=', email)],limit = 1)
    #                 if userData.company_type == "person":
    #                     return {'error': 'email in use by B2C user', "code": "3"}
    #                 return {'error': 'email in use ', "code": "3"}
                
    #             if User.sudo().search(['&',("is_published","=",True),('phone','=',phone)]):
    #                 userData = request.env['res.partner'].sudo().search([("is_published", "=", True), ('phone', '=', phone)],limit = 1)
    #                 if userData.company_type == "person":
    #                     return {'error': 'phone in use by B2C user', "code": "3"}
    #                 return {'error': 'phone in use ', "code": "3"}

    #         user = User.sudo().create({
    #             'name': f"{fname}",
    #             "email": email,
    #             "phone": phone,
    #             "is_public": True,
    #             "active": True,
    #             "is_published":True,
    #             "city": city,
    #         })
    #         user.sudo().write({"auth_token":f"{user.id}{''.join(random.choice(string.ascii_letters) for i in range(17))}"})
    #         self.send_opt(user.id)
    #         # template=request.env.ref("cspl_eccomerce_api.mail_template_user_activate")
    #         # template.sudo().with_context({"url":url,"redirect_url":redirect_url}).send_mail(user.id,force_send=True)
    #         massage={**{'message': 'user created', 'customer_id': user.id}
    #                 #  ,**self.user_info(user)
    #                  }
    #         return massage
    #     except KeyError as e:
    #         return {'error': f'Missing key: {e}'}
        

    # @http.route('/api/loginConfirm', type='json', auth='public', csrf=False, cors='*')
    # def loginConfirm(self, customer_id=None, otp=None):
    #     user = request.env['res.partner'].sudo().browse(customer_id)

    #     # self.update_user_last_update(user)   / These three line are commented /
    #     # if user.auth_token:
    #     #     user.sudo().write({"auth_token":f"{user.id}{''.join(random.choice(string.ascii_letters) for i in range(16))}"})
        
    #     if user.otp==otp:
    #         user.sudo().write({
    #             "is_public": True,
    #             "active": True,
    #             "is_published":True,
    #             "auth_token":f"{user.id}{''.join(random.choice(string.ascii_letters) for i in range(16))}"
    #         })

    #         return {
    #             'message': 'Login successfully',
    #             'user_details': self.user_info(user)
    #         }
        
    #     else:
    #         return {'error': "Invalid OTP"}
    
    
    @http.route('/api/registerUsers', type='json', auth='public', csrf=False, cors='*')
    def signup(self, fname, phone, email=None, city='', **kw):
        try:
            User = request.env['res.partner']
            if User.sudo().search(['&', ("is_published", "=", True), '|', ('phone', '=', phone), ('email', '=', email)]):
                return {'error': 'User already exists', 'code': '2'}

            user = User.sudo().create({
                'name': f"{fname}",
                "email": email,
                "phone": phone,
                "is_public": False,  # Set user as not public until confirmation
                "active": False,  # Set user as inactive until confirmation
                "is_published": False,  # Set user as not published until confirmation
                "city": city,
            })
            user.sudo().write({"auth_token": f"{user.id}{''.join(random.choice(string.ascii_letters) for i in range(17))}"})
            self.send_opt(user.id)
            
            return {'message': 'Signup successful', 'customer_id': user.id}
        except KeyError as e:
            return {'error': f'Missing key: {e}'}
        
        
    
    @http.route('/api/loginConfirm', type='json', auth='public', csrf=False, cors='*')
    def loginConfirm(self, customer_id=None, otp=None):
        User = request.env['res.partner']
        user = User.sudo().browse(customer_id)

        if user.otp == otp:
            user.sudo().write({
                "is_public": True,
                "active": True,
                "is_published": True,
                "auth_token": f"{user.id}{''.join(random.choice(string.ascii_letters) for i in range(16))}"
            })

            return {
                'message': 'Login successful',
                'user_details': self.user_info(user)
            }
        else:
            return {'error': "Invalid OTP"}
        
        
    
    
    
    @http.route('/api/updateUser', type='json', auth='public', csrf=False, cors='*')
    def update_user(self, user_id, name=None, phone=None, email=None, city=None, zip=None,
                    mobile=None, vat=None, website=None, function=None, auth_token=None, **kw):
        try:
            User = request.env['res.partner']
            user = User.sudo().browse(user_id)
            
            if not user:
                return {'error': 'User not found', 'code': '404'}
            
            updates = {}
            if name:
                updates['name'] = name
            if phone:
                updates['phone'] = phone
            if email:
                updates['email'] = email
            if city:
                updates['city'] = city
            if zip:
                updates['zip'] = zip
            if mobile:
                updates['mobile'] = mobile
            if vat:
                updates['vat'] = vat
            if website:
                updates['website'] = website
            if function:
                updates['function'] = function
            if auth_token:
                updates['auth_token'] = auth_token
            
            user.sudo().write(updates)
            
            return {'message': 'User updated successfully', 'customer_id': user_id}
        except Exception as e:
            return {'error': str(e)}


 
    
    
    


    
        
   
    
   

 
