from datetime import date
import re
from paddleocr import PaddleOCR,draw_ocr
from PIL import Image
import os
import logging
from pykakasi import Kakasi
import translators as trans

# logging.basicConfig(filename='log/log.log',level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
img_path = './imgs/img_08.jpg'
image = Image.open(img_path).convert('RGB')
ocr_jp = PaddleOCR(use_angle_cls=True,lang='japan')
ocr_zh = PaddleOCR(use_angle_cls=True,lang='ch')

def rec_jp(image_name):
    # need a file not instance
    set = ocr_jp.ocr(image_name,cls=True)
    result = set[0]
    # data = set[0][0][1][0]
    logging.info(date.today().strftime("%b-%d-%Y"))
    logging.info(f'[-]result: {len(result)}')
    # [logging.debug(line) for line in result]
    # boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    # logging.debug(txts)
    return txts
    # scores = [line[1][1] for line in result]

def get_kana(txt):
    result = Kakasi.convert(txt)
    return (result['kana'],'')[len(result)]

def jp_2_zh(txts):
    if len(txts) == 0:
        logging.error(f"NON Result")
    jp_to_zh = trans.baidu(txts[0],from_language='jp',to_language='zh')
    return jp_to_zh

def zh_2_jp(txts):
    if len(txts) == 0:
        logging.error(f"NON Result")
    zh_to_jp = trans.baidu(txts[0],from_language='zh',to_language='jp')
    return zh_to_jp

def rec_zh(image_name):
    set = ocr_zh.ocr(image_name,cls=True)
    result = set[0]
    # data = set[0][0][1][0]
    logging.info(date.today().strftime("%b-%d-%Y"))
    logging.info(f'[-]result: {len(result)}')
    # [logging.debug(line) for line in result]
    # boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    # logging.debug(txts)
    return txts

def qus_img(image:Image):
    temp_img = 'cut.jpg'
    # box = (100,400,980,550)
    width,hight= image.size
    # logging.debug(f'({width},{hight})')
    box = (width * 0.1,hight * 0.13,width * 0.9,hight * 0.25)
    cut = image.crop(box)
    # cut.show()
    cut.save(temp_img)
    qustion = rec_jp(temp_img)
    result = jp_2_zh(qustion)
    logging.debug(f'{temp_img}:{qustion} to {result}')
    os.remove(temp_img)
    return qustion

def answer_image(image:image):
    width,hight= image.size
    # logging.debug(f'({width},{hight})')
    for setp in range(1,5):
        box = (width * 0.1,hight * (0.32+(setp + setp * 0.1)/10), width * 0.9,hight * (0.45+(setp + setp * 0.1)/10))
        cut = image.crop(box)
        txt = f'temp-{setp}.jpg'
        cut.save(txt)
        context =  rec_jp(txt)
        result = jp_2_zh(context)
        logging.debug(f'{txt}:{context} trans to {result}')
        os.remove(txt)
        # cut.show()
    # cut.save('temp.jpg')
    # txt = rec_zh('temp.jpg')
    # logging.debug(f'{txt}')
    # os.remove('temp.jpg')
    # rec_zh(image)

qus_img(image)
answer_image(image)
# org_txt = cut_img(image)
# result = jp_2_zh(org_txt)
# logging.debug(f"{org_txt} to {result}")
# logging.debug(image.size)

# image_name = f'{data}.jpg'
# im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
# im_show = Image.fromarray(im_show)
# im_show.save(image_name)

