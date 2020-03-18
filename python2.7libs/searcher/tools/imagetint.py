from PIL import Image
from PIL.ImageColor import getcolor, getrgb
from PIL.ImageOps import grayscale
import os
import PIL.Image
import PIL.ImageOps

script_path = os.path.dirname(os.path.realpath(__file__))


def image_tint(src, tint='#ffffff'):
    if Image.isStringType(src):  # file path?
        src = Image.open(src)
    if src.mode not in ['RGB', 'RGBA']:
        raise TypeError('Unsupported source image mode: {}'.format(src.mode))
    src.load()

    tr, tg, tb = getrgb(tint)
    tl = getcolor(tint, "L")  # tint color's overall luminosity
    if not tl: tl = 1  # avoid division by zero
    tl = float(tl)  # compute luminosity preserving tint factors
    sr, sg, sb = map(lambda tv: tv/tl, (tr, tg, tb))  # per component adjustments

    # create look-up tables to map luminosity to adjusted tint
    # (using floating-point math only to compute table)
    luts = (map(lambda lr: int(lr*sr + 0.5), range(256)) +
            map(lambda lg: int(lg*sg + 0.5), range(256)) +
            map(lambda lb: int(lb*sb + 0.5), range(256)))
    l = grayscale(src)  # 8-bit luminosity version of whole image
    if Image.getmodebands(src.mode) < 4:
        merge_args = (src.mode, (l, l, l))  # for RGB verion of grayscale
    else:  # include copy of src image's alpha layer
        a = Image.new("L", src.size)
        a.putdata(src.getdata(3))
        merge_args = (src.mode, (l, l, l, a))  # for RGBA verion of grayscale
        luts += range(256)  # for 1:1 mapping of copied alpha values

    return Image.merge(*merge_args).point(luts)

def tint_image(src, color="#FFFFFF"):
    if Image.isStringType(src):  # file path?
        src = Image.open(src)
    if src.mode not in ['RGB', 'RGBA']:
        raise TypeError('Unsupported source image mode: {}'.format(src.mode))
    src.load()
    r, g, b, alpha = src.split()
    gray = ImageOps.grayscale(src)
    result = ImageOps.colorize(gray, (0, 0, 0, 0), color) 
    result.putalpha(alpha)
    return result

if __name__ == '__main__':

    PATH = os.path.abspath(os.path.join(script_path, "..", "images"))
    p = PATH.replace("\\", "/")
    input_image_path = ['branch-vline.png', 'branch-more.png', 'branch-end.png', 'opened.png', 'collapsed.svg']
    for i in range(len(input_image_path)):
        input_image = os.path.join(p, input_image_path[i])
        print 'tinting "{}"'.format(input_image)

        root, ext = os.path.splitext(input_image)
        result_image_path = root+'_result'+ext

        print 'creating "{}"'.format(result_image_path)
        result = image_tint(input_image, '#686868')
        if os.path.exists(result_image_path):  # delete any previous result file
            os.remove(result_image_path)
        result.save(result_image_path)  # file name's extension determines format

        print 'done'