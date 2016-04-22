from pyqrcode import create
from qrtools import QR

def qrencode(data, filename):
    create(data).png(filename, scale=2)


def qrdecode(filename):
    qr = QR()
    qr.decode(filename)
    return qr.data
