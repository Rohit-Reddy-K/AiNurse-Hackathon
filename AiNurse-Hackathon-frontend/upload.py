import requests
import base64
import uuid
import time

BASE_API_URL = 'http://prod-erxhub.fkh.prv'
DIGITISE_RX_URL = f'{BASE_API_URL}/digitise_rx'

def generate_request_id():
    return str(uuid.uuid4())

def initiate_digitise_request(image_path, paths):
    try:
        # Read and encode the image
        print("test")
        # image_path = "/Applications/XAMPP/xamppfiles/htdocs/AiNurse-Hackathon-frontend/Clean 2.jpeg"
        with open(image_path, "rb") as f:
            img_ = f.read()
        img_bytes_encoded = base64.b64encode(img_).decode('utf-8')
        rx_image_data = [{
            "imageBytes": img_bytes_encoded,
            "imageName": image_path.split('/')[-1]
        }]

        # Create the request data for the /digitise_rx endpoint
        request_id = generate_request_id()
        
        request_data = {
            "requestId": request_id,
            "rxImages": rx_image_data
        }
        paths[request_id] = request_data
        # Post the request to the /digitise_rx endpoint
        digitise_response = requests.post(DIGITISE_RX_URL, json=request_data, headers={'Content-Type': 'application/json'})
        # Return the status of the initiation

        print("test2")
        if digitise_response.status_code == 200 and digitise_response.json().get('success', False):
            print("test3")
            response = {"status": True, "request_id": request_id}
        else:
            print("Failed to post request or process was not successful.")
            # print("test4")
            response = {"status": False}
        # print("test 5 : ", response)
        return response
    except Exception as e:
        print(e)
        return e

# path = "/Users/rohit.komatireddi/Downloads/download-_17_.jpg"
# mypath = "/Users/v.surajkumar/Desktop/Hackathon/dhms_degree.jpg"
# result = initiate_digitise_request(mypath)
# print(result)

def check_digitise_results(request_id):
    # Construct the results URL using the BASE_API_URL constant
    result_url = f'{BASE_API_URL}/results/{request_id}'

    recheck_data = {'requiredPolling': True, 'content': []}
    res= requests.get(result_url)
    continue_polling = True


    while continue_polling :
        res= requests.get(result_url)
        if res == recheck_data:
            continue_polling = True
            time.sleep(5)

        else:
            continue_polling = False
    # result_response = res
    #pprint(result_response.json())
    return res
