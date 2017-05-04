# coding=utf-8
import requests
import json
import os
import base64
from Crypto.Cipher import AES


def createSecretKey(size):
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]


def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext


def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(text.encode('hex'), 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def loadPage():
    url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_466122659?csrf_token='
    headers = {
        'Cookie': 'appver=1.5.0.75771;',
        'Referer': 'http://music.163.com/'
    }
    text = {'username': 'fanghao9342@gmail.com',
            'password': '1930402werfds', 'rememberLogin': 'true'}
    text = json.dumps(text)
    secKey = createSecretKey(16)
    nonce = '0CoJUm6Qyw8W8jud'
    pubKey = '010001'
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)

    data = {'params': encText, 'encSecKey': encSecKey}
    req = requests.post(url, headers=headers, data=data)
    print type(req)
    return req.json()[u'comments']


if __name__ == '__main__':
    contents = loadPage()
    print contents
    context = ''
    for content in contents:
        context += content[u'content'].encode('UTF-8') + '*****'
    with open('pinglun.txt', 'w') as file:
        file.write(context)
