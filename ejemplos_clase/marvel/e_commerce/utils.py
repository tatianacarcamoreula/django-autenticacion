import hashlib


PUBLIC_KEY = '58ee40376f7c10e99f440f5e3abd2caa'
PRIVATE_KEY = '2c0373e00d85edb4560f68ddc2094014e8694f90'
TS = "1"
TO_HASH = TS + PRIVATE_KEY + PUBLIC_KEY
HASHED = hashlib.md5(TO_HASH.encode())

MARVEL_DICT = {
    "PUBLIC_KEY": PUBLIC_KEY,
    "PRIVATE_KEY": PRIVATE_KEY,
    "TS": TS,
    "TO_HASH": TO_HASH,
    "HASHED": hashlib.md5(TO_HASH.encode()),
    "URL": "http://gateway.marvel.com/v1/public/" + "comics",
}


def get_marvel_params():
    return {
        "ts": MARVEL_DICT['TS'],
        "apikey": MARVEL_DICT['PUBLIC_KEY'],
        "hash": MARVEL_DICT['HASHED'].hexdigest(),
        "limit": "50",
        "offset": "0"
    }
