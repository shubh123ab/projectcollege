from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import predict
import shutil

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("main.html",{
                                                    "request": request,
                                                    })

@app.post("/result/")
async def root(request: Request, my_file: UploadFile = File(...)):
    if request.method == 'POST':
        with open("demo.jpg", "wb") as buffer:
            shutil.copyfileobj(my_file.file, buffer)
        data = predict.predict(my_file)
        val = data['values']
    else:
        data=''
        val=''
    return templates.TemplateResponse("result.html",{
                                                    "request": request,
                                                    "data": data,
                                                    "val":val,
                                                    })