""" QR CODE USING PYTHON """
import pyqrcode
from pyqrcode import QRCode
s="https://www.linkedin.com/in/ruquiya-anjum-4544431bb/"
url=pyqrcode.create(s)
url.svg("my linkedin.svg",scale=8)
