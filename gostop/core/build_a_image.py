# Importing Image class from PIL module 
from PIL import Image, ImageDraw, ImageFont
import click
import sys

def get_concat_h(im1, im2, overlap_percent):
    overlapping_width = im2.width*overlap_percent//100
    dst = Image.new('RGB', (im1.width + im2.width - overlapping_width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width - overlapping_width, 0))
    return dst

def add_number(img, num):
    draw = ImageDraw.Draw(img)

    draw.rectangle( (1, 1, 25, 30),
            fill=(205, 200, 240),
            outline=(255, 255, 255))

    # to find ttf in linux, "locate .ttf"
    font = ImageFont.truetype('tahoma.ttf',25)
    draw.text((5, 5), f"{num}", fill=(0, 0, 255), font=font)
    return img

@click.command()
@click.argument('src', nargs=-1, required=True)
@click.option('-d', '--dst')
@click.option('-o', '--overlap', default=0)
@click.option('-n', '--number', default=False)
def build_image(src, dst, overlap, number):
    """ ex) # python build_a_image.py images/11.png images/43.png images/a3.png -o 50 -d gostop.png
    """
    images = []
    for i, card in enumerate(src):
        img = Image.open(card)
        img = add_number(img, i) 
        images.append(img)
    
    dst_image = images.pop(0)
    for i in images:
        dst_image = get_concat_h(dst_image, i, overlap)

    if dst: 
        dst_image.save(dst)
    else:
        dst_image.show()

if __name__ == "__main__":
    build_image()