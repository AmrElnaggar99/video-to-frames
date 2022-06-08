import aiofiles
from fastapi import FastAPI, File, UploadFile
import cv2
from fastapi.middleware.cors import CORSMiddleware
   
    
app = FastAPI()

# Just allowing CORS for local testing, you can ignore that part
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

################################################################

@app.post("/videoToFrames")
async def cut_video(file:UploadFile = File(...)):
    async with aiofiles.open("outvideo.mp4", 'wb') as out_file:
        content = await file.read()  # read video from request
        await out_file.write(content)  # write video to server
        vidcap = cv2.VideoCapture("outvideo.mp4") # give openCV a hold on the video
        # From here onwards, divide the video to frames and save them in "./frames"
        def getFrame(sec):
            vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
            hasFrames,image = vidcap.read()
            if hasFrames:
                cv2.imwrite("frames/image"+str(count)+".jpg", image)     # save frame as JPG file
            return hasFrames
        sec = 0
        frameRate = 0.5 # it will capture image in each 0.5 second
        count=1
        success = getFrame(sec)
        while success:
            count = count + 1
            sec = sec + frameRate
            sec = round(sec, 2)
            success = getFrame(sec)
        return {"Result": "OK"}