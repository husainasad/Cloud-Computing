from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse
import pandas as pd

csv_path = 'Resources/dataset/Classification Results on Face Dataset (1000 images).csv'

def get_lookup_dict():    
    try:
        lookup_df = pd.read_csv(csv_path)
        return dict(zip(lookup_df['Image'], lookup_df['Results']))
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="CSV file not found")

lookup_dict = get_lookup_dict()

app = FastAPI()

async def img_result(img_name):
    if img_name not in lookup_dict:
        raise HTTPException(status_code=404, detail=f"Image '{img_name}' not found in the lookup dictionary")
    return lookup_dict[img_name]

@app.post("/", response_class=PlainTextResponse)
async def get_img_result(inputFile: UploadFile):
    img_name = inputFile.filename.split('.')[0]
    result = await img_result(img_name)
    return f"{img_name}:{result}"