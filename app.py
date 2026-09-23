import cv2
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI(title="ECG Classification API")

# Load trained model
MODEL_PATH = "model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

CLASSES = [
    'Abnormal Heartbeat',
    'History of Myocardial Infarction',
    'Myocardial Infarction',
    'Normal'
]

@app.get("/")
def health_check():
    return {"status": "ok", "message": "ECG Classification API is running on AKS"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img_bgr is None:
        return JSONResponse(status_code=400, content={"error": "Invalid image file"})

    # Preprocessing matching your notebook (240x240, RGB, / 255.0)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    resized_img = cv2.resize(img_rgb, (240, 240)) / 255.0
    input_tensor = np.expand_dims(resized_img, axis=0)

    # Model inference
    predictions = model.predict(input_tensor)
    class_idx = int(np.argmax(predictions))
    confidence = float(predictions[0][class_idx] * 100)

    return {
        "predicted_class": CLASSES[class_idx],
        "confidence_percentage": round(confidence, 2)
    }