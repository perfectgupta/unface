import json
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from faceapi import FaceModules as FM
import tempfile

app = FastAPI(
    docs_url='/docs/protected',
)


origins = [
    "http://localhost:4200",
    "http://localhost:4401/",
    'https://unstop.com',
    'https://datastory.web.app',
    'https://dev2.dare2compete.com',
    'https://beta.dare2compete.com',
]

methods = [
    "GET",
    "POST",
    "DELETE",
    "OPTIONS",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_origins=["*"],
    allow_credentials=True,
    # allow_methods=["*"],
    allow_methods=methods,
    allow_headers=['*'],
)

@app.get("/main")
def main_api():
    return {"message": 'Hello, It is working!'}

@app.post("/face/analyse")
async def face_analyzer(image: UploadFile):
    contents = await image.read()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(contents)
        temp_file_path = temp_file.name
        
    face = FM.face_analyzer_bundle(image=temp_file_path)
    return face

@app.post("/face/detect")
async def face_detecter(image: UploadFile):
    # print(image)
    if image is not None:
        contents = await image.read()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(contents)
            temp_file_path = temp_file.name
            
        result = FM.face_detection_bundle(image=temp_file_path)
        
        total_faces = 0
        
        for i in range(len(result)):
            
            if result[i]["confidence"] >= 0.7:
                result[i]["face_detected"] = True
                total_faces += 1
            else:
                result[i]["face_detected"] = False

        result.append({"faces_detected": total_faces})
        
        return result
    else:
        return "Image was not found!"
    
    
@app.post("/face/verify")
async def face_verification_bundle(main: UploadFile, verifier: UploadFile):
    if main and verifier is not None:
        contents1 = await main.read()
        contents2 = await verifier.read()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(contents1)
            temp_file_path1 = temp_file.name
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(contents2)
            temp_file_path2 = temp_file.name
            
        result = FM.face_verification_bundle(temp_file_path1, temp_file_path2)
        result['verified'] = bool(result['verified'])
        
        return result
    else:
        return "Image was not found!"
    
    
@app.post("/face/extract")
async def face_extractor(image: UploadFile):
    # print(image)
    if image is not None:
        contents = await image.read()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(contents)
            temp_file_path = temp_file.name
            
        result = FM.face_extraction_bundle(image=temp_file_path)
        
        total_faces = 0
        
        for i in range(len(result)):
            
            if result[i]["confidence"] >= 0.7:
                result[i]["face_detected"] = True
                total_faces += 1
            else:
                result[i]["face_detected"] = False
                
        result.append({"faces_detected": total_faces})

        return result
    else:
        return "Image was not found!"



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)