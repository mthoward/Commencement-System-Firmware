# import pyqrcode
# import qrtools

# def encode_qr(data):
    # qr = pyqrcode.create(data)
    # filename = data + ".png"
    # qr.png(filename, scale=2)


# def decode_qr(filename):
    # qr = qrtools.QR()
    # qr.decode(filename)
    # return qr.data

# #print decode_qr("mthoward.png")
import os

strpath = "/home/sethkara/"
strfile = "cam_test2"


print "Reading data from qrcode"
# call os command to read qr data to text file
os.system("zbarimg -q "+strpath+strfile+".png > "+strpath+strfile+".txt")

strreadtext = strpath+strfile+".txt"

if os.path.exists(strreadtext):
        strqrcode = open(strreadtext, 'r').read()
        print strqrcode
else:
        print "QR-Code text file not found"
