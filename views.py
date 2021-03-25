from random import choices
from flask import make_response, request
from settings import JWT_SECRET
from captcha.image import ImageCaptcha
import datetime
import jwt

CHARACTERS = 'abcdefghijklmnopqrstuvwxyzçABCDEFGHIJKLMNOPQRSTUVWXYZÇ0123456789'


def get_status_message(status: int):
    codes = {
        20: 'success',
        30: 'mismatch word',
        40: 'expired',
        50: 'invalid token'
    }
    return codes[status]


def get_word(char_count: int):
    return ''.join(choices(CHARACTERS, k=char_count))


def verify_token(token: str, word: str):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=('HS256',), options={
            'verify_exp': True
        })
    except jwt.ExpiredSignatureError:
        return 40
    except jwt.InvalidTokenError:
        return 50
    return 20 if decoded.get('word') == word else 30


def generate_captcha(word: str):
    image = ImageCaptcha(fonts=['fonts/cairo.ttf', 'fonts/ptmono.ttf'])
    image_bytes = image.generate(word, format='png')
    return [image_bytes, word]


def get_word_from_token(token: str):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=('HS256',), options={
            'require_exp': False,
            'verify_exp': False
        })
    except:
        return None
    return decoded.get('word')


def generate_token(word: str):
    expiration_date = datetime.datetime.now() + datetime.timedelta(days=2)
    return jwt.encode({
        'word': word,
        'exp': expiration_date
    }, JWT_SECRET, algorithm='HS256')


class Views:
    @staticmethod
    def verify(token: str):
        body = request.json
        word = body.get('word')
        status = verify_token(token, word)
        return {
            "word": word,
            "code": status,
            "status": get_status_message(status)
        }

    @staticmethod
    def captcha(token: str):
        word = get_word_from_token(token)
        captcha = generate_captcha(word)
        response = make_response(captcha[0].read())
        response.headers.set('Content-Type', 'image/png')
        return response

    @staticmethod
    def generate():
        word = get_word(5)
        token = generate_token(word)
        return {
            'token': token,
        }
