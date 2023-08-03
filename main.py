from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import qrcode
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image

app = FastAPI()




origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Mount the "static" folder to serve static files (HTML, CSS, JS, etc.)
# app.mount("/static", StaticFiles(directory="static"), name="static")



@app.post("/generate-qr-code/{text}")
async def generate_qr_code(text: str):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image to a BytesIO object as PNG
    qr_image_bytes = BytesIO()
    qr_image.save(qr_image_bytes, format='PNG')
    qr_image_bytes.seek(0)

    # Create a PIL Image from the BytesIO object
    pil_image = Image.open(qr_image_bytes)

    # Save the PIL Image to another BytesIO object as PNG
    image_bytes = BytesIO()
    pil_image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    return StreamingResponse(image_bytes, media_type="image/png")