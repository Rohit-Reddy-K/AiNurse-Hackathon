from itertools import product
from statistics import quantiles
import requests
import json

def search_api(data):
    processed_data = []
    try:
        print(data)
        for item in data:
            url = "http://sspl-search.fkh.prv/search_list?device=5&page=1&size=40&app_type=M&token=l59i759i7589o5966589l589958954t&wh=1&pincode=700156&q=" + item["product"] + "%" + item["dosage"] + "&userType=NEW_USER&userGroup=CUSTOMER"
            # params = {
            #     "device": "5",
            #     "page": "1",
            #     "size": "40",
            #     "app_type": "M",
            #     "token": "l59i759i7589o5966589l589958954t",
            #     "wh": "1",
            #     "pincode": "700156",
            #     "q": item["product"] + "%" + item["dosage"],
            #     "userType": "NEW_USER",
            #     "userGroup": "CUSTOMER"
            # }
            payload = {}
            headers = {
                'X-EXPERIMENT-MPAB': 'true',
                'X-EXPERIMENT-MPBP': 'true'
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            length = len(response.json()["products"])
            if(length > 0):
                product_details = {"id": response.json()['products'][0][23], "name": response.json()['products'][0][0], "strength": response.json()['products'][0][30]}
                processed_data.append(product_details)
        return processed_data
    except Exception as e:
        return processed_data

def addToCart(data):
    processed_data = []
    try:
        for item in data:
            id = item['id']
            name = item['name']
            url = "http://preprod-fkhp-cart-service.fkh.prv/api/v1/cart/addProduct"
            payload = json.dumps({
                "sessionId": None,
                "customerId": "44002583",
                "createdBy": "44002583",
                "products": [
                    {
                        "productType": "PHYSICAL",
                        "productId": id,
                        "quantity": 1
                    }
                ]
            })
            headers = {
                'deviceid': '48981aa718f8bb45dcfc7ef908105018',
                'apptype': 'M',
                'userid': '44002583',
                'Content-Type': 'application/json',
                'x-experiment-mpab': 'true'
            }
            print("yes")
            response = requests.request("PUT", url, headers=headers, data=payload)
            print(response.json())
            if(response.json()['status'] == 'SUCCESS'):
                product_details = {"id": id, "name": name}
                processed_data.append(product_details)
        return processed_data
    except Exception as e:
        return processed_data


def emptyCart():
    try:
        url = "http://preprod-fkhp-cart-service.fkh.prv/api/v1/cart/delete"
        payload = json.dumps({
            "sessionId": None,
            "customerId": "44002583",
            "createdBy": "44002583"
        })
        headers = {
            'deviceid': '48981aa718f8bb45dcfc7ef908105018',
            'apptype': 'M',
            'userid': '44002583',
            'Content-Type': 'application/json',
            'x-experiment-mpab': 'true'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if(response.json()['status'] == 'SUCCESS'):
            return 'SUCCESS'
        return 'FAILED'
    except Exception as e:
        return 'FAILED'

def catalog_api(data):
    processed_data = []
    try:
        for product_id in data:
            url = "https://catalog.preprod.fkhealthplus.com/product/getProductDetail"
            payload = json.dumps({
                "productId": product_id,
                "pincode": "411002",
                "userId": "44002583",
                "userGroup": "CUSTOMER",
                "userCohort": "REPEAT_USER",
                "warehouseId": "10"
            })
            payload = {}
            headers = {
                'token': '76i786i456i776i766i646iii64l584',
                'Content-Type': 'application/json',
                'x-experiment-mpab': 'true'
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            #response["product"][0]["details"][]
            processed_data.append(response.json()['products'][0][24])
        return processed_data
    except Exception as e:
        return processed_data


# request = [
#     {
#         "product": "Dolo",
#         "dosage": "650 mg",
#         "quantities": 4
#     }]
# product_details = search_api(request)
# print(product_details)
# response = emptyCart()
# print(response)
# cart_products = addToCart(product_details)
# print(cart_products)
