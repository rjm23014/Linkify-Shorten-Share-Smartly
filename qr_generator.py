import qrcode
import os

def generate_qr(data):
    img = qrcode.make(data)
    path = f'static/qr_{hash(data)}.png'
    img.save(path)
    return path
