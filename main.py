import json
import gradio as gr
from PIL import Image
import io
import base64
import requests
import websocket

URL = 'https://kongtest2.ngrok.ibr.tw/api/prompt'

def compression_image(image):
    image = Image.fromarray(image)
    min_side = min(image.size)
    scale_factor = 512 / min_side
    new_size = (round(image.size[0] * scale_factor), round(image.size[1] * scale_factor))
    resized_image = image.resize(new_size)
    return resized_image

def encode_image_to_base64(image):
    newImage = compression_image(image)
    buffered = io.BytesIO()
    newImage.save(buffered,format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def start_queue(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    print("data:" + data.decode('utf-8'))
    requests.post(URL, data=data)

def get_image(prompt_id): 
    ws = websocket.WebSocket() 
    
    try:
        ws.connect(f"ws://{URL}/ws") 
        print(f"Waiting for image data for prompt ID: {prompt_id}") 

        while True: 
            message = ws.recv() 
            print(f"Received message: {message}")  # 打印消息内容
            
            if isinstance(message, str): 
                data = json.loads(message) 
                print(f"Received message: {data}") 
                if data["type"] == "executing": 
                    if data["data"]["node"] is None and data["data"]["prompt_id"] == prompt_id: 
                        print("Execution completed") 
                        break 
            elif isinstance(message, bytes): 
                print("Received binary data (likely image)") 
                image = Image.open(io.BytesIO(message[8:])) 
                ws.close() 
                return image 
            
    except websocket.WebSocketException as e:
        print(f"WebSocket error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    finally:
        ws.close()
    return None

def generate_image(input_image):
    with open("image2image.json","r") as file_json:
        prompt = json.load(file_json)
        encoded_image = encode_image_to_base64(input_image)
        prompt["15"]["inputs"]["image"] = encoded_image

    start_queue(prompt)

demo = gr.Interface(fn=generate_image, inputs=["image"], outputs=["image"])
demo.launch()