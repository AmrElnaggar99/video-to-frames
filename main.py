import os
import aiofiles
from fastapi import FastAPI, File, UploadFile
import cv2
from fastapi.middleware.cors import CORSMiddleware
   
    
app = FastAPI()

origins = [
    "https://localhost:3000",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
path = os.path.join(os.curdir,"frames")
@app.post("/videoToFrames")
async def cut_video(file:UploadFile = File(...)):
    async with aiofiles.open("outvideo.mp4", 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write
        vidcap = cv2.VideoCapture("outvideo.mp4")
        print(path)
        def getFrame(sec):
            vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
            hasFrames,image = vidcap.read()
            print(path)
            if hasFrames:
                cv2.imwrite("frames/image"+str(count)+".jpg", image)     # save frame as JPG file
            return hasFrames
        sec = 0
        frameRate = 0.5 #//it will capture image in each 0.5 second
        count=1
        success = getFrame(sec)
        while success:
            count = count + 1
            sec = sec + frameRate
            sec = round(sec, 2)
            success = getFrame(sec)
        return {"Result": "OK"}