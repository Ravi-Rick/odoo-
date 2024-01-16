# -*- coding: utf-8 -*-
# from odoo import http


# class Demomodule(http.Controller):
#     @http.route('/demomodule/demomodule', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/demomodule/demomodule/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('demomodule.listing', {
#             'root': '/demomodule/demomodule',
#             'objects': http.request.env['demomodule.demomodule'].search([]),
#         })

#     @http.route('/demomodule/demomodule/objects/<model("demomodule.demomodule"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('demomodule.object', {
#             'object': obj
#         })
from odoo import http
from odoo.http import request

from werkzeug.wrappers import Response
import json
import base64

class Demoomodule(http.Controller):
    @http.route('/demomodule/',website=True,auth='public')
    def module(self,**kw):
        return "Hello World! This is small api"   
       
    
    
# class Demomodule(http.Controller):
#     @http.route('/demo/',website=True,auth='public')
#     def module(self,**kw):
        
#         return request.render("demomodule.products",{})
    

# class Demomodule(http.Controller):
#     @http.route('/model/',website=True,auth='public')
#     def module(self,**kw):
#         user=request.env['demomodule.demomodule'].sudo().search([])
#         return request.render("demomodule.products",{'user':user})
    
# class ProductController(http.Controller):
#     @http.route('/products/',website=True,type='json',auth='public',methods=['GET'])
#     def get_products(self):
#         product=http.request.env['res.partner']
#         products=product.sudo().search_read([],'name','last_price')
#         formated_products=[{'name':product['name'],'price':product['last_price']} for product in products]
#         return JsonRequest(formated_products)





# class PartnerController(http.Controller):

   

# class PartnerController(http.Controller):

    @http.route('/get_/api/get_partner/', auth='public', type='json', methods=['POST'])
    def get_partner_data(self, **kwargs):
        # Extract criteria from the request
        search_criteria = kwargs.get('search_criteria', {})

        # Search for partners based on criteria
        Partner = http.request.env['res.partner']
        partners = Partner.sudo().search_read(
            domain=[(key, '=', value) for key, value in search_criteria.items()],
            fields=['email', 'category_id', 'image_1920']
        )

        # Convert the image field to base64
        for partner in partners:
            if 'image_1920' in partner and partner['image_1920']:
                partner['image_1920'] = base64.b64encode(partner['image_1920']).decode('utf-8')
                
        # return Response(json.dumps({'partners': partners}), content_type='application/json')
        
        response_data = {'partners': partners}
        return response_data
    
    
    @http.route('/get_/api/get_partner_names/', auth='public', type='json', methods=['POST'])
    def get_partner_names(self, **kwargs):
   
            result_list = []
            Partner = http.request.env['res.partner']
            partner_ids = Partner.sudo().search([('company_type', '=','company'),('is_company', '=', True)])
            partner_data = Partner.sudo().search_read(
            [('id', 'in', partner_ids.ids)],
            fields=['name','id']
        )
            partner_names = [data['name'] for data in partner_data] 
            result_list.append({'names': partner_names})
            response_data = {'results': result_list}
            return response_data


    @http.route('/get_/api/get_partner_names_with_company/', auth='public', type='json', methods=['POST'])
    def get_partner_names_with_company(self, **kwargs):
      
        result_list = []
        Partner = http.request.env['res.partner']
        partner_ids = Partner.sudo().search([('company_type', '=', 'company'),('is_company', '=', True)])
        partner_data = Partner.sudo().search_read(
            [('id', 'in', partner_ids.ids)],
            fields=['name', 'id']
        )
        partners_info = [{'id': data['id'], 'name': data['name']} for data in partner_data]
        result_list.append({'partners': partners_info})
        response_data = {'results': result_list}
        return response_data
    

    @http.route('/get_/api/get_partner_search_names/', auth='public', type='json', methods=['POST'])
    # def get_partner_search_names(self, **kwargs):   
    #     search_params = kwargs.get('search_params', {})     
    #     Partner = http.request.env['res.partner']    
    #     search_domain = [('company_type', '=', 'company')]
    #     for key, value in search_params.items():
    #         search_domain.append((key, '=', value))
    #     partner_data = Partner.sudo().search_read(
    #         search_domain,
    #         fields=['name', 'id']
    #     )
    #     partners_info = [{'id': data['id'], 'name': data['name']} for data in partner_data] 
    #     # response_data = {'results': [{'names': partners_info[0]['name']}]}
    #     response_data = {'results': [{'names': partner_info['name']} for partner_info in partners_info]}

    #     return response_data
    
    # @http.route('/get_/api/get_partner_search_names/', auth='public', type='json', methods=['POST'])
    # def get_partner_search_names(self, **kwargs):
    #     search_params = kwargs.get('search_params', {})
    #     Partner = http.request.env['res.partner']
    #     search_domain = [('company_type', '=', 'company')]

    #     for key, value in search_params.items():
    #         search_domain.append((key, '=', value))
            
    #     name_condition = ('name', '=', search_params.get('name', ''))
    #     search_domain.append(name_condition)
        
    #     print("Search Parameters:", search_params)
    #     print("Search Domain:", search_domain)

    #     partner_data = Partner.sudo().search_read(
    #         search_domain,
    #         fields=['name', 'id'],
            
    #     )

    #     response_data = {'results': []}

    #     for partner_info in partner_data:
    #      response_data['results'].append({'names': partner_info['name']})


    #     return response_data
    
    
    @http.route('/get_/api/get_partner_search_names/', auth='public', type='json', methods=['POST'])
    def get_partner_search_names(self, **kwargs):
        search_params = kwargs.get('search_params', {})
        Partner = http.request.env['res.partner']  
        search_domain = [('name', 'ilike', search_params.get('name', ''))]    
        # search_domain.append(('company_type', '=', 'company'))   
        print(search_domain,'-------------------------------------------------')   
        partner_ids = Partner.sudo().search(search_domain)
        print(partner_ids)
        # partner_names = Partner.sudo().browse(partner_ids).mapped('name')  
        partner_names = partner_ids.mapped('name') 
        
            
        response_data = {'results': [{'name': name} for name in partner_names]}
       
       
        return response_data
    
    
    @http.route('/get_/api/get_partner_names_with_company_chaild/', auth='public', type='json', methods=['POST'])
    def get_partner_names_with_company_chaild(self, **kwargs):
        result_list = []
        Partner = http.request.env['res.partner']
        
        # Get the company name from the request parameters
        company_name = kwargs.get('company_name', '')

        # Find the parent company ID based on the provided name
        parent_company_domain = [('name', '=', company_name), ('company_type', '=', 'company'), ('is_company', '=', True)]
        parent_company = Partner.sudo().search(parent_company_domain, limit=1)

        if parent_company:
            # Find the children of the parent company
            children_domain = [('parent_id', '=', parent_company.id)]
            children_data = Partner.sudo().search_read(children_domain, fields=['name', 'id'])
            children_info = [{'id': data['id'], 'name': data['name']} for data in children_data]
            # result_list.append({'children': children_info})
            # result_list.append({'parent': {'id': parent_company.id, 'name': parent_company.name}, 'children': children_info})
            result_list.append({'children': [{'id': parent_company.id, 'name': parent_company.name, 'type': 'parent'}] + children_info})


        else:
            result_list.append({'error': 'Parent company not found'})

        response_data = {'results': result_list}
        return response_data
    
    
    
    @http.route('/get_/api/get_partner_names_with_company_sibiling/', auth='public', type='json', methods=['POST'])
    def get_partner_names_with_company_sibiling(self, **kwargs):
        result_list = []
        Partner = http.request.env['res.partner']
        
        # Get the company name from the request parameters
        partner_name = kwargs.get('partner_name', '')

        # Find the partner based on the provided name
        partner_domain = [('name', '=', partner_name), ('company_type', '=', 'company')]
        partner = Partner.sudo().search(partner_domain, limit=1)

        if partner:
            # Find the parent of the partner
            parent_domain = [('id', '=', partner.parent_id.id)]
            parent_data = Partner.sudo().search_read(parent_domain, fields=['name', 'id'])
            parent_info = [{'id': data['id'], 'name': data['name'], 'type': 'parent'} for data in parent_data]

            # Find the siblings of the partner
            siblings_domain = [('parent_id', '=', partner.parent_id.id), ('id', '!=', partner.id)]
            siblings_data = Partner.sudo().search_read(siblings_domain, fields=['name', 'id'])
            siblings_info = [{'id': data['id'], 'name': data['name']} for data in siblings_data]
            
            siblings_info.append({'id': partner.id, 'name': partner.name})
            
            sorted_siblings_info = sorted(siblings_info, key=lambda x: x['id'])
            
            # siblings_info.insert(0,{'id':partner.id,'name':partner.name})

            # Include partner information within siblings list
            # result_list.append({'children': parent_info + siblings_info})
            result_list.append({'children': parent_info + sorted_siblings_info})

        else:
            result_list.append({'error': 'Partner not found'})

        response_data = {'results': result_list}
        print(response_data)
        return response_data
    
    
    # @http.route('/get_/api/get_individual_partners_without_parent/', auth='public', type='json', methods=['POST'])
    # def get_individual_partners_without_parent(self, **kwargs):
    #     result_list = []
    #     Partner = http.request.env['res.partner']

        # Find individual partners without a parent
        # individual_partners_without_parent_domain = [('company_type', '=', 'person'), ('parent_id', '=', False),('is_company', '=', False)]
        # individual_partners_without_parent_data = Partner.sudo().search_read(
        #     individual_partners_without_parent_domain,
        #     fields=['name', 'id']
        # )
        
    #     users_without_parent_domain = [('parent_id', '=', False)]
    #     individual_partners_without_parent_data = Partner.sudo().search_read(
    #         users_without_parent_domain,
    #         fields=['name', 'id']
    #     )
        
    #     sorted_individual_partners = sorted(
    #     individual_partners_without_parent_data,
    #     key=lambda x: x['id']
    # )

    #     users_partners_info = [{'id': data['id'], 'name': data['name']} for data in sorted_individual_partners ]

    #     result_list.append({'usrers_without_parent': users_partners_info})

    #     response_data = {'results': result_list}
    #     return response_data

    # @http.route('/get_/api/get_individual_partners_without_parent/', auth='public', type='json', methods=['POST'])
    # def get_individual_partners_without_parent(self, **kwargs):
    #     result_list = []
    #     Partner = http.request.env['res.partner']
        
    #     # Find all users without a parent
    #     users_without_parent_data = Partner.sudo().search_read(
    #         [('parent_id', '=', False)],
    #         fields=['name', 'id']
    #     )
        
    #     users_info = []
    #     for user_data in users_without_parent_data:
    #         # Fetch children for each user without a parent
    #         children_data = Partner.sudo().search_read(
    #             [('parent_id', '=', user_data['id'])],
    #             fields=['name', 'id','type']
    #         )
            
    #         # Combine the user and their children
    #         user_info = {
    #             'id': user_data['id'],
    #             'name': user_data['name'],
    #             'children': [{'id': child['id'], 'name': child['name'],'type':child['type']} for child in children_data]
    #         }
            
    #         users_info.append(user_info)

    #     result_list.append({'users_without_parent_with_children': users_info})
        
    #     response_data = {'results': result_list}
    #     return response_data

    # @http.route('/get_/api/get_individual_partners_without_parent/', auth='public', type='json', methods=['POST'])
    # def get_individual_partners_without_parent(self, **kwargs):
    #     result_list = []
    #     Partner = http.request.env['res.partner']
        
    #     # Find all users without a parent
    #     users_without_parent_data = Partner.sudo().search_read(
    #         [('parent_id', '=', False)],
    #         fields=['name', 'id']
    #     )
        
    #     users_info = []
    #     for user_data in users_without_parent_data:
    #         # Fetch children for each user without a parent
    #         children_data = Partner.sudo().search_read(
    #             [('parent_id', '=', user_data['id'])],
    #             fields=['name', 'id', 'type']
    #         )

    #         # Fetch sales for each user
    #         # sale_order_count = Partner.sudo().browse(user_data['id'])._compute_sale_order_count()
    #         user_sales = len(Partner.sudo().browse(user_data['id']).sale_order_ids)
    #         # user_sales = Partner.sudo().browse(user_data['id']).sale_order_ids


            
            
    #         # Combine the user and their children, including sales
    #         user_info = {
    #             'id': user_data['id'],
    #             'name': user_data['name'],
    #             'sale_order_count': user_sales,
    #             'children': [{'id': child['id'], 'name': child['name'], 'type': child['type']} for child in children_data]
    #         }
            
    #         users_info.append(user_info)

    #     result_list.append({'users_without_parent_with_children_and_sales': users_info})
        
    #     response_data = {'results': result_list}
    #     return response_data
    
    
    @http.route('/get_/api/get_individual_partners_without_parent/', auth='public', type='json', methods=['POST'])
    def get_individual_partners_without_parent(self, **kwargs):
            result_list = []
            Partner = http.request.env['res.partner']
            
            # Find all users without a parent
            users_without_parent_data = Partner.sudo().search_read(
                [('parent_id', '=', False)],
                fields=['name', 'id']
            )
            
            users_info = []
            for user_data in users_without_parent_data:
                # Fetch children for each user without a parent
                children_data = Partner.sudo().search_read(
                    [('parent_id', '=', user_data['id'])],
                    fields=['name', 'id', 'type']
                )

                # Fetch sales for each user
                user_sales = len(Partner.sudo().browse(user_data['id']).sale_order_ids)

                # Combine the user and their children, including sales
                user_info = {
                    'id': user_data['id'],
                    'name': user_data['name'],
                    'sale_order_count': user_sales,
                    'children': []
                }

                # Fetch sale_order_count for each child
                for child_data in children_data:
                    child_sales = len(Partner.sudo().browse(child_data['id']).sale_order_ids)
                    user_info['children'].append({
                        'id': child_data['id'],
                        'name': child_data['name'],
                        'type': child_data['type'],
                        'sale_order_count': child_sales
                    })

                users_info.append(user_info)

            result_list.append({'users_without_parent_with_children_and_sales': users_info})
            
            response_data = {'results': result_list}
            return response_data
        
        
        
        # Assuming you are creating a new module named custom_api
# Create a new Python file inside your custom_api module, for example, controllers/main.py



from odoo import http
from odoo.http import request

class CustomApiController(http.Controller):
    @http.route('/custom_api/partner_data/', auth='public', type='json', methods=['POST'])
    def get_all_partner_names(self, **post):
        # Retrieve all partner names
        partners = request.env['res.partner'].sudo().search([])

        # Return the partner names
        # partner_names = [partner.id for partner in partners]
        partner_email = [partner.email for partner in partners]
        

        return {'partner_email': partner_email}



            
        

        
        
        
    


