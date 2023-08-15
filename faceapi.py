from deepface import DeepFace

backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'retinaface', 
  'mediapipe',
  'yolov8',
  'yunet',
]

class FaceModules:
    
    def preprocess_result(results):
        preprocessed_results = [] 
        
        for result in results:
            preprocessed_result = {
                "facial_area": result.get("facial_area", {}),
                "confidence": result.get("confidence", 0.0),
            }
            preprocessed_results.append(preprocessed_result)
        
        return preprocessed_results
    
    
    def face_detection(image, backend):
        face = DeepFace.extract_faces(img_path = image,
                                            # target_size = (224, 224), 
                                            detector_backend = backends[backend],
                                            enforce_detection=False
                                        )
        
        processed_result = FaceModules.preprocess_result(face)
        
        if processed_result:
            return processed_result
        else:
            raise ValueError(f"No faces detected in {image.filename}")
    
    
    def face_detection_bundle(image):
        
        if image is not None:
            face = FaceModules.face_detection(image, 1)
            
        for i in range(len(face)):
            if face[i]['confidence'] <= 0.5:
                enforced_face = FaceModules.face_detection(image, 3)
                return enforced_face
            else:
                return face
            
            
    def face_extraction(image, backend):
        face_objs = DeepFace.extract_faces(img_path = image, 
                target_size = (224, 224), 
                detector_backend = backends[backend]
        )
        
        processed_result = FaceModules.preprocess_result(face_objs)
        
        if processed_result:
            return processed_result
        else:
            raise ValueError(f"No faces detected in {image.filename}")
        
        
    def face_extraction_bundle(image):
        
        if image is not None:
            face = FaceModules.face_extraction(image, 1)
            
            for i in range(len(face)):
                if face[i]['confidence'] <= 0.5:
                    enforced_face = FaceModules.face_extraction(image, 3)
                    return enforced_face
                else:
                    return face
            
        
    def face_analyzer(image, backend):
        # imaages = '/Users/parasgupta/bn7754vgq0-1691579596.jpeg'
        demographies = DeepFace.analyze(
                                            img_path = image,
                                            detector_backend = backends[backend],
                                            enforce_detection=False
                                        )
        return demographies
    
    
    def face_analyzer_bundle(image):
        
        face = FaceModules.face_analyzer(image, 1)
        
        return [{ 
                    "dominant_emotion": face[0]['dominant_emotion'],
                    "facial_area": face[0]['region'],
                    "age": face[0]['age'],
                    "dominant_gender": face[0]['dominant_gender'],
                    "dominant_race": face[0]['dominant_race'],
                }]
        
        
    def face_verification(image1, image2, backend):
        obj = DeepFace.verify(img1_path = image1, 
                                img2_path = image2, 
                                detector_backend = backends[backend],
                                enforce_detection=False
                            )
        
        return obj
    
    def face_verification_bundle(image1, image2):
        
        if image1 and image2 is not None:
            face = FaceModules.face_verification(image1, image2, 1)
            
            return {"verified": face['verified'], "facial_areas": face['facial_areas']}
        
            # {'verified': True, 'distance': 3.3306690738754696e-16, 'threshold': 0.4, 'model': 'VGG-Face', 'detector_backend': 'ssd', 'similarity_metric': 'cosine', 'facial_areas': {'img1': {'x': 119, 'y': 141, 'w': 165, 'h': 258}, 'img2': {'x': 119, 'y': 141, 'w': 165, 'h': 258}}, 'time': 1.01}
            
            # for i in range(len(face)):
            #     if face[i]['confidence'] <= 0.5:
            #         enforced_face = FaceModules.face_verification(image1, image2, 3)
            #         return enforced_face
            #     else:
            #         return face
            

#face recognition
# dfs = DeepFace.find(img_path = "img.jpg", 
#         db_path = "my_db", 
#         detector_backend = backends[1]
# )

#embeddings
# embedding_objs = DeepFace.represent(img_path = "img.jpg", 
#         detector_backend = backends[2]
# )

#facial analysis
# demographies = DeepFace.analyze(img_path = "img4.jpg", 
#         detector_backend = backends[3]
# )

#face detection and alignment
# face_objs = DeepFace.extract_faces(img_path = "img.jpg", 
#         target_size = (224, 224), 
#         detector_backend = backends[4]
# )