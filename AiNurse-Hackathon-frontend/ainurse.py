# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from email.mime import image
from flask import Flask, request, jsonify
from upload import initiate_digitise_request,check_digitise_results
from vertexcaller import generate
from format import process_data
from util import extract
from cart import search_api,emptyCart,addToCart
from flask_cors import CORS
from googletrans import Translator
from gtts import gTTS
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
CORS(app)

paths = {}


@app.route('/upload', methods=['POST'])
# ‘/’ URL is bound with hello_world() function.
def upload():
    image_path = request.get_json()['image_path']
    print(image_path)
    response = initiate_digitise_request(image_path, paths)
    print(response)
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

@app.route('/translate', methods=['POST'])
def translate():
    # Check if the request contains JSON data
    if request.is_json:
        # Retrieve the JSON data from the request
        data = request.get_json()
        
        # Extract text, src, and dest from the JSON data
        text = data.get('text')
        src_lang = data.get('src', 'en')  # Default source language is English
        dest_lang = data.get('dest', 'hi')  # Default destination language is Hindi
        
        # Translate the text
        translator = Translator()
        translated_text = translator.translate(text, src=src_lang, dest=dest_lang)
        final_translated_text = translated_text.text
        
        # Return the translated text as JSON response
        return jsonify({"translatedText": final_translated_text})
    else:
        return jsonify({'error': 'Request must contain JSON data.'}), 400

@app.route('/audio', methods=['POST'])
def audio():
    # Check if the request contains JSON data
    if request.is_json:
        # Retrieve the JSON data from the request
        data = request.get_json()
        path = '/Applications/XAMPP/xamppfiles/htdocs/AiNurse-Hackathon-frontend/'
        
        # Extract text, src, and dest from the JSON data
        text = data.get('text')
        lang = data.get('lang', 'en')  # Default source language is English
        file_name = data.get('fileName')
        
        obj= gTTS(text=text,slow = False, lang= lang)
        obj.save(path + file_name)
        
        # Return the translated text as JSON response
        return jsonify({"audioGenerated":"true","fileName": file_name})
    else:
        return jsonify({'error': 'Request must contain JSON data.'}), 400


@app.route('/hello')
# ‘/’ URL is bound with hello_world() function.
def hello_world():

    return {
        "text" : "Hi! How are you. Hope you are doing good",
        "link" : "cartPage.html"
    }


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(host='127.0.0.1', port=5000)