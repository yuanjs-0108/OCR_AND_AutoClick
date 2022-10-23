from datetime import date
from paddleocr import PaddleOCR,draw_ocr
from PIL import Image
import os
import logging

logging.basicConfig(filename='log/log.log',level=logging.DEBUG)
img_path = './imgs/img_04.jpg'
image = Image.open(img_path).convert('RGB')
temp_img = 'cut.jpg'

def rec(image_name):
    ocr = PaddleOCR(use_angle_cls=True,lang='japan')
    # need a file not instance
    set = ocr.ocr(image_name,cls=True)
    result = set[0]
    # data = set[0][0][1][0]
    logging.info(date.today().strftime("%b-%d-%Y"))
    logging.info(f'[-]result: {len(result)}')
    # [logging.debug(line) for line in result]
    # boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    logging.debug(txts)
    # scores = [line[1][1] for line in result]


def cut_img(image:Image):
    box = (100,400,980,550)
    cut = image.crop(box)
    cut.save(temp_img)
    rec(temp_img)
    os.remove(temp_img)
    return cut
# dir = [{key,val} for key,val in result]

def answer_image(image:image):
    pass

cut_img(image)

# image_name = f'{data}.jpg'
# im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
# im_show = Image.fromarray(im_show)
# im_show.save(image_name)

