import json
import os #fs
import time 
import gradio as gr #快速建立介面
import requests #express
import numpy as np #處理大規模數值運算

import base64
from io import BytesIO
from PIL import Image #圖像處理 Pillow

URL = "https://kongtest2.ngrok.ibr.tw/api/prompt"
# OUTPUT_DIR = "C:\ComfyUI\NewVenv\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\output"

# 透過 API 取得最新圖片
def get_latest_image(folder):
    files = os.listdir(folder) # 列出資料夾內所有檔案
    image_files= [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))] # 過濾出圖片檔
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x))) # 依照檔案建立時間排序，此時最新的檔案會在最後面
    latest_image = os.path.join(folder, image_files[-1]) if image_files else None # 檢查image_files是否為空，不為空則取得最新圖片
    return latest_image

# 把參數發送到ComfyUI
def start_queue(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    requests.post(URL, data=data)

# 生成圖片
def generate_image(prompt_text, step_count):
    with open("text2image.json", "r") as file_json:
        prompt = json.load(file_json)
        prompt["6"]["inputs"]["text"] = f"digital artwork of a {prompt_text}"
        prompt["3"]["inputs"]["steps"] = step_count

    # image = Image.fromarray(input_image)
    # min_side = min(image.size)
    # scale_factor =  512/ min_side
    # new_size = (round(image.size[0] *scale_factor), round(image.size[1] * scale_factor))
    # resized_image = image.resize(new_size)

    # buffered = BytesIO()
    # resized_image.save(buffered, format="PNG")
    # encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    # prompt["11"]["inputs"]["image"] = encoded_image
    # resized_image.save("C:\ComfyUI\NewVenv\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\input\test_api.jpg")

    # previous_image = get_latest_image(OUTPUT_DIR)
        
    start_queue(prompt)

    # while True:
    
    #     latest_image = get_latest_image(OUTPUT_DIR)
    #     if latest_image != previous_image:
    #         return latest_image
        
        # time.sleep(1)  
    
# 伺服器
demo = gr.Interface(fn=generate_image, inputs=["text","text"], outputs=["image"])
demo.launch()
