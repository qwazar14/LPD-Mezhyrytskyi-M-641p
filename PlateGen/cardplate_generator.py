import json
import random
from PIL import Image, ImageFont, ImageDraw


def gen_random_in_range(start, end):
    return random.randint(start, end)


def gen_random_first_letters():
    first_letters = ['AK', 'AB', 'AC', 'AE', 'AH', 'AM', 'AO',
                     'AP', 'AT', 'AA', 'AI', 'BA', 'BB', 'BC',
                     'BE', 'BH', 'BI', 'BK', 'CH', 'BM', 'BO',
                     'AX', 'BT', 'BX', 'CA', 'CB', 'CE']
    random_value = gen_random_in_range(0, len(first_letters) - 1)
    return first_letters[random_value]


def gen_random_last_letters():
    last_letters = ['AA', 'BA', 'CA', 'EA', 'HA', 'IA', 'KA', 'MA', 'OA', 'PA', 'TA', 'XA',
                    'AB', 'BB', 'CB', 'EB', 'HB', 'IB', 'KB', 'MB', 'OB', 'PB', 'TB', 'XB',
                    'AC', 'BC', 'CC', 'EC', 'HC', 'IC', 'KC', 'MC', 'OC', 'PC', 'TC', 'XC',
                    'AE', 'BE', 'CE', 'EE', 'HE', 'IE', 'KE', 'ME', 'OE', 'PE', 'TE', 'XE',
                    'AH', 'BH', 'CH', 'EH', 'HH', 'IH', 'KH', 'MH', 'OH', 'PH', 'TH', 'XH',
                    'AI', 'BI', 'CI', 'EI', 'HI', 'II', 'KI', 'MI', 'OI', 'PI', 'TI', 'XI',
                    'AK', 'BK', 'CK', 'EK', 'HK', 'IK', 'KK', 'MK', 'OK', 'PK', 'TK', 'XK',
                    'AM', 'BM', 'CM', 'EM', 'HM', 'IM', 'KM', 'MM', 'OM', 'PM', 'TM', 'XM',
                    'AO', 'BO', 'CO', 'EO', 'HO', 'IO', 'KO', 'MO', 'OO', 'PO', 'TO', 'XO',
                    'AP', 'BP', 'CP', 'EP', 'HP', 'IP', 'KP', 'MP', 'OP', 'PP', 'TP', 'XP',
                    'AT', 'BT', 'CT', 'ET', 'HT', 'IT', 'KT', 'MT', 'OT', 'PT', 'TT', 'XT',
                    'AX', 'BX', 'CX', 'EX', 'HX', 'IX', 'KX', 'MX', 'OX', 'PX', 'TX', 'XX']
    random_value = gen_random_in_range(0, len(last_letters) - 1)
    return last_letters[random_value]


def gen_random_4_numbers():
    numbers = ''
    for i in range(4):
        numbers += str(gen_random_in_range(0, 9))
    return numbers


def gen_plate():
    return f"{gen_random_first_letters()} {gen_random_4_numbers()} {gen_random_last_letters()}"


def parse_text(plate_number, part=0):
    if part == 0:
        return plate_number[0:2]
    if part == 1:
        return plate_number[3:7]
    if part == 2:
        return plate_number[8:10]


def get_template_image():
    template_path = './assets/images/template_new.jpg'
    return Image.open(template_path).convert('RGBA')


def draw_text_img(plate, text, font_size, pos_x=0, pos_y=0):
    font = ImageFont.truetype(
        "./assets/fonts/nomera.ttf", font_size, encoding="unic"
    )
    user_name_text_draw = ImageDraw.Draw(plate)

    user_name_text_draw.text(
        (pos_x, pos_y),  # 1st letters (32, 15), numbers (62, 15), last (130, 15)
        text,
        fill="black",
        font=font
    )


def create_plate():
    first_letters = gen_random_first_letters()
    numbers = gen_random_4_numbers()
    last_letters = gen_random_last_letters()
    plate_number = first_letters + numbers + last_letters
    plate = Image.new("L", (180, 38), 0)

    user_image = get_template_image()
    plate.paste(user_image)
    draw_text_img(plate, first_letters, font_size=47, pos_x=15)
    draw_text_img(plate, numbers, font_size=36, pos_x=60, pos_y=7)
    draw_text_img(plate, last_letters, font_size=47, pos_x=132)
    # img_save_path = f"./assets/images/dataset/train/img/{plate_number}.png"
    # json_save_path = f"./assets/images/dataset/train/ann/{plate_number}.png.json"
    # plate.show()
    # plate.save(img_save_path)
    # json_string = gen_json_data(plate_number, is_train=True)
    # with open(json_save_path, 'w') as outfile:
    #     json.dump(json_string, outfile)
    return plate, plate_number


def gen_json_data(text, is_train=False):
    if is_train:
        mode = "train"
    else:
        mode = "test"
    x = {
        "description": text,
        "tags": [
            {
                "name": mode,
                "value": None,
                "labelerLogin": None
            }
        ],
        "size": {
            "height": 38,
            "width": 180
        },
        "objects": []
    }
    return x


for i in range(10000):
    create_plate()
