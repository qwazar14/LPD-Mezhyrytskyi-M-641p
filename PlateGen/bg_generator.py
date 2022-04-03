import random

import numpy as np
from PIL import Image, ImageOps, ImageFilter

from PlateGen.cardplate_generator import create_plate
from Logger.logger import log


def get_rand_bool():
    return True if random.randint(0, 1) == 0 else False


def gen_rand_in_range(start, end):
    log(gen_rand_in_range.__name__, 0, 1)
    return random.randint(start, end)


def get_rand_img():
    log(get_rand_img.__name__, 0, 1)
    path = f"./assets/images/random_background/ ({gen_rand_in_range(1, 100)}).jpg"
    return Image.open(path).convert('LA')


def convert_img():
    log(convert_img.__name__, 0, 1)
    img = get_rand_img()
    img = img.resize((128, 68))
    img = ImageOps.grayscale(img)
    return img


def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

    A = np.matrix(matrix, dtype=float)
    B = np.array(pb).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)


def transform_plate(plate):
    width, height = plate.size

    if get_rand_bool():
        coeffs = find_coeffs(
            [(0, 0), (180, 0), (180, 38), (0, 38)],
            [(0, 0), (180, gen_rand_in_range(0, 3)), (180, gen_rand_in_range(35, 38)), (0, 38)])
    else:
        coeffs = find_coeffs(
            [(0, 0), (180, 0), (180, 38), (0, 38)],
            [(0, gen_rand_in_range(0, 3)), (180, 5), (180, 35), (0, gen_rand_in_range(35, 38))])
    return plate.transform((width, height), Image.PERSPECTIVE, coeffs,
                           Image.BICUBIC)


def prepare_plate():
    log(__name__, 0, 1)
    plate, plate_number = create_plate()
    width, height = plate.size
    new_height = gen_rand_in_range(9, 13)
    new_width = new_height * width / height

    plate = plate.resize((int(new_width), int(new_height)))
    plate = ImageOps.grayscale(plate)

    plate = transform_plate(plate)
    # plate.show()
    return plate, plate_number, int(new_width), int(new_height)


def bg_gen():
    log(bg_gen.__name__, 0, 1)
    bg = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    bg_noise = Image.effect_noise((128, 64), 10)
    bg_noise = bg_noise.filter(ImageFilter.GaussianBlur(1))

    plate, plate_number, plate_w, plate_h = prepare_plate()
    plate_zone = (gen_rand_in_range(0, 128 - plate_w), gen_rand_in_range(0, 64 - plate_h))
    bg.paste(convert_img())
    bg.paste(plate, plate_zone, plate)
    bg.paste(bg_noise, (0, 0), bg_noise)
    # bg.show()
    img_save_path = f"./assets/images/dataset/train/img/{plate_number}.png"
    bg.save(img_save_path)


def main():
    print('Generating', sep='', end='')
    for i in range(5):
        print('.', sep='', end='')
        bg_gen()


if __name__ == '__main__':
    main()
