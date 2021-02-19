from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

TEMPLATE_PATH = 'files/ticket_base.PNG'
FONT_PATH = 'files/Roboto-Regular.ttf'
FONT_SIZE = 35
DARK_BLUE_COLOR = (0, 32, 96, 255)
NAME_OFFSET = (550, 515)
EMAIL_OFFSET = (550, 618)


def generate_ticket(name, email):
    base = Image.open(TEMPLATE_PATH).convert("RGBA")
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    draw = ImageDraw.Draw(base)
    draw.text(NAME_OFFSET, name, font=font, fill=DARK_BLUE_COLOR)
    draw.text(EMAIL_OFFSET, email, font=font, fill=DARK_BLUE_COLOR)
    temp_file = BytesIO()
    base.save(temp_file, 'png')
    temp_file.seek(0)
    return temp_file


# from generate_ticket import generate_ticket
# generate_ticket('Василий', 'email@email.ru')
