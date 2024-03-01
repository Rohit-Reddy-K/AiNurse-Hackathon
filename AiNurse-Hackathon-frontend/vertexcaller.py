# import vertexai
# from vertexai.preview.generative_models import GenerativeModel, Part
# from vertexai.generative_models._generative_models import HarmCategory, HarmBlockThreshold, ResponseBlockedError
# import base64
#
#
# vertexai.init(project="fkh-prod-datasci-prj-svc-fb83", location="asia-southeast1")
#
# # def generate_content():
# #     config = {
# #         "max_output_tokens": 2048,
# #         "temperature": 0.4,
# #         "top_p": 0.46,
# #         "top_k": 15
# #     }
# #
# #     safety_settings = {
# #         HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
# #         HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
# #         HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
# #         HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
# #     }
# #
# #     gemini_pro_vision_model = GenerativeModel("gemini-pro-vision")
# #     image = Part.from_uri("https://ibb.co/mJkFfQZ", mime_type="image/jpeg")
# #     model_response = gemini_pro_vision_model.generate_content(["what is this image?", image])
# #     print(model_response)
# #     #chat = model.start_chat()
# #     #print(chat.send_message("Convert image to text - https://ibb.co/mJkFfQZ", generation_config=config, safety_settings=safety_settings))
# #
# # generate_content()
# #
# #
# # fkh-prod-datasci-prj-svc-fb83
#
#
# def generate_content(image_data):
#     config = {
#         "max_output_tokens": 2048,
#         "temperature": 0.4,
#         "top_p": 0.46,
#         "top_k": 15
#     }
#
#     safety_settings = {
#         HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
#         HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
#     }
#
#     gemini_pro_vision_model = GenerativeModel("gemini-pro-vision")
#     image = Part.from_data(image_data, mime_type="image/jpeg")
#     model_response = gemini_pro_vision_model.generate_content(["Please explain this prescription?", image])
#     print(model_response)
#
# # Read the image file from your desktop and encode it in base64
# image_path = "/path/to/your/image.jpg"
# with open(image_path, "rb") as f:
#     image_data = base64.b64encode(f.read()).decode('utf-8')
#
# # Call the generate_content function with the image data
# generate_content(image_data)


import base64
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models

vertexai.init(project="fkh-prod-datasci-prj-svc-fb83", location="asia-southeast1")

def generate(image_data, prompt):

    model = GenerativeModel("gemini-pro-vision")

    # with open(image_path, "rb") as f:
    #     image_data = base64.b64encode(f.read()).decode('utf-8')

    image1 = Part.from_data(data=image_data, mime_type="image/jpeg")

    prompt = """Please explain this prescription to a person who does not understand medical terms. 
Clearly tell for each mecidine, the daily number of times the patient needs to take the medicine,  whether its morning or afternoon or evening and how many days the patients needs to continue the course. Also check for any special instruction like before food etc.
Give the response in a paragraph format without special characters.
The Metadata for this prescription is """ + prompt

    responses = model.generate_content(
        [image1, prompt],

        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32
        },
        safety_settings={
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        stream=True,
    )

    vertex_response = ""
    for response in responses:
        vertex_response = vertex_response+ response.text

    return str(vertex_response)

    image_data = ""
    #image_path = "/Users/rohit.komatireddi/Downloads/1000089007.jpg"


#generate("/Users/rohit.komatireddi/Downloads/1000089007.jpg")