# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from email.mime import image
from flask import Flask, request
from upload import initiate_digitise_request,check_digitise_results
from vertexcaller import generate
from format import process_data
from util import extract
from cart import search_api,emptyCart,addToCart
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

paths = {}

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/upload/', methods=['POST'])
# ‘/’ URL is bound with hello_world() function.
def upload():
    image_path = request.get_json()['image_path']
    response = initiate_digitise_request(image_path, paths)
    return response

@app.route('/cart/<request_id>', methods=['POST'])
def cart(request_id):
    # process
    rx_process_response = check_digitise_results(request_id)
    print("rx_process_response:", rx_process_response)

    image_data = paths[request_id]["rxImages"][0]["imageBytes"]
    print("image_data:", image_data)

    vertex_response = generate(image_data, rx_process_response.text)
    print("vertex_response:", vertex_response)

    format_str = process_data(vertex_response)
    print("format_str:", format_str)

    product_list = extract(format_str)
    print("product_list:", product_list)

    product_details = search_api(product_list)
    print("product_details:", product_details)

    response = emptyCart()
    print("response:", response)

    cart_products = addToCart(product_details)
    print("cart_products:", cart_products)

    response = {"cart_products":cart_products , "cart_url":"https://healthplus.flipkart.com/cart/details" , "vertex_response": vertex_response}
    return response


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()