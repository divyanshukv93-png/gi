import cv2, numpy as np

def analyze(data: bytes) -> dict:
    """Demo mode: image quality checks only. A trained model plugs in here (see model_weights/). No disease result is ever fabricated."""
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Not a readable image")
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sharp, bright = float(cv2.Laplacian(gray, cv2.CV_64F).var()), float(gray.mean())
    return {"mode": "demo", "prediction": None, "confidence": None,
            "image_checks": {"width": w, "height": h, "sharpness": round(sharp, 1), "brightness": round(bright, 1),
                             "usable": w >= 224 and h >= 224 and sharp > 50 and 40 < bright < 220},
            "message": "No trained model is loaded, so no disease or defect result was produced."}
