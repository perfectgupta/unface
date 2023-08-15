from fastapi import FastAPI, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import psutil
from faceapi import FaceModules as FM
import tempfile
import asyncio

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
    
    
html = """
<!DOCTYPE html>
<html>
<head>
    <title>UnFace Current CPU Util</title>
    <style>
        .green {
            color: green;
        }
        .yellow {
            color: yellow;
        }
        .red {
            color: red;
        }
    </style>
</head>
<body>
    <h1>UnFace Current CPU Util</h1>
    <button onclick="startWebSocket()">Start</button>
    <button onclick="stopWebSocket()">Stop</button>
    <div id="responseArea"></div>
    <script>
        var ws = null;

        function startWebSocket() {
            if (ws !== null) {
                ws.close();
            }
            ws = new WebSocket("ws://localhost:8086/ws");
            ws.onmessage = function(event) {
                var responseArea = document.getElementById('responseArea');
                var message = document.createElement('p');
                var content = document.createTextNode(event.data);
                message.appendChild(content);

                var cpuUtilization = parseFloat(event.data.match(/CPU Utilization: (\d+\.\d+)%/)[1]);

                if (cpuUtilization < 45) {
                    message.classList.add('green');
                } else if (cpuUtilization >= 45 && cpuUtilization <= 70) {
                    message.classList.add('yellow');
                } else {
                    message.classList.add('red');
                }

                responseArea.appendChild(message);
            };
        }

        function stopWebSocket() {
            if (ws !== null) {
                ws.close();
                ws = null;
            }
        }
    </script>
</body>
</html>

"""

@app.get("/face/monitor")
async def get():
    return HTMLResponse(html)

async def send_cpu_utilization(websocket: WebSocket):
    while True:
        try:
            # Get CPU utilization using psutil
            cpu_usage = psutil.cpu_percent(interval=1)
            
            await websocket.send_text(f"CPU Utilization: {cpu_usage}%")
        except Exception as e:
            await websocket.send_text(f"Error: {str(e)}")
        await asyncio.sleep(0.2)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await send_cpu_utilization(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8086)
    
# uvicorn unface:app --port 8086  --reload