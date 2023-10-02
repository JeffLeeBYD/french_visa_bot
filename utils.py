import ddddocr
from PIL import Image
from io import BytesIO
import requests

'''
# Load the SVG image
svg_image = open('Captcha.svg', 'rb').read()  # Replace with your SVG file name


png_image_io = BytesIO(png_image)
captcha_image = Image.open(png_image_io)

# Perform OCR using ddddocr
ocr = ddddocr.DdddOcr()
result = ocr.classification(captcha_image)
'''
# return the ocr
def anti_captcha(raw_in: bytes) -> str:

    # Convert PNG bytes to PIL Imagec
    png_image_io = BytesIO(raw_in)
    captcha_image = Image.open(png_image_io)

    # Perform OCR using ddddocr
    ocr = ddddocr.DdddOcr(old=True, show_ad=False)
    return ocr.classification(captcha_image)


def send_message(img_buffer, time):
    files = {'photo': img_buffer}
    #TG_ID = "1668897101"
    TG_ID = "-1001983787722"
    base_url = 'https://api.telegram.org/bot[your telegram bot token]/sendPhoto?chat_id={0}&caption={1}'.format(TG_ID, time)
    requests.post(base_url, files=files)

def send_x_y_info(img_buffer, x, y):
    files = {'photo': img_buffer}
    TG_ID = "1668897101"
    x_y_info = "location of the validate button: (x: {0}, y: {1})".format(x, y)
    base_url = 'https://api.telegram.org/bot[your telegram bot token]/sendPhoto?chat_id={0}&caption={1}'.format(TG_ID, x_y_info)
    requests.post(base_url, files=files)

if __name__ == '__main__':
    send_message()