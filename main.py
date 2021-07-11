from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import predict
import shutil
import uvicorn
import math

from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("main.html",{
                                                    "request": request,
                                                    })

@app.get("/about")
async def root(request: Request):
    return templates.TemplateResponse("about.html",{
                                                    "request": request,
                                                    })

@app.post("/result/")
async def root(request: Request, my_file: UploadFile = File(...)):
    if request.method == 'POST':
        with open("static/demo.jpg", "wb") as buffer:
            shutil.copyfileobj(my_file.file, buffer)
        data = predict.predict(my_file)
        val = data['values']
        if(data['health_condition']=='covid'):
            accuracy=math.ceil(val['covid']*100)
        elif(data['health_condition']=='normal'):
            accuracy=math.ceil(val['normal']*100)
        else:
            accuracy=math.ceil(val['pneumonia']*100)
    else:
        data=''
        val=''
        accuracy=''
    return templates.TemplateResponse("result.html",{
                                                    "request": request,
                                                    "data": data,
                                                    "val":val,
                                                    "accuracy":accuracy,
                                                    })

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level="info", reload=True)