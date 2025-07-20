import qrcode
import os

def generate_qr(data):
    img = qrcode.make(data)
    filename = f'qr_{hash(data)}.png'
    path = os.path.join('static', filename)
    img.save(path)
    return f'static/{filename}'
