import pyqrcode
import qrtools

def encode_qr(data):
    qr = pyqrcode.create(data)
    filename = data + ".png"
    qr.png(filename, scale=2)


def decode_qr(filename):
    qr = qrtools.QR()
    qr.decode(filename)
    return qr.data

encode_qr("mthoward")
print decode_qr("mthoward.png")
