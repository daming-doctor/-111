from Crypto.Cipher import AES
from base64 import b64encode
import json
import requests
import csv
# 找到加密参数
# 想办法对依照网易的逻辑加密参数（params，encSecKey）
# 请求到网易，拿到歌曲评论
url="https://music.163.com/weapi/comment/resource/comments/get?csrf_token=e57d87cc4ec14747d662e9b13e7f0c3b"
# 找到参数
# 请求方式是POST
data={
"csrf_token":"e57d87cc4ec14747d662e9b13e7f0c3b",
"cursor":"-1",
"offset":"0",
"orderType":"1",
"pageNo":"1",
"pageSize":"20",
"rid":"R_SO_4_29567189",
"threadId":"R_SO_4_29567189"
}
# 处理加密过程
# 服务于window.asrsea
f="00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
g="0CoJUm6Qyw8W8jud"
e="010001"
i="3I4QkDskT3xIwl3n"
def get_encSecKey():
    return"a5c4471efcc77c7bedb168058dc97b2e14c92466b8d2f6db02ecb4f1892e4154c098d905859bce673f31b13691e34e06f79276c9518c8ed92987289c4d7aced7f3c768e457d8323fb12c616ef06ddff7e618244de2a0be721a31afb7206f321d9119bf0acd83c5f2afa1fe97a06467646e84c2f943ff1c35354a30c8da65ed0a"

def get_params(data):
    first=enc_params(data,g)
    second=enc_params(first,i)
    return second
# 转换成16的倍数，服务于下方的加密过程
def to_16(data):
    pad=16-len(data)%16
    data+=chr(pad)*pad
    return data
# 加密过程
def enc_params(data,key):
    iv="0102030405060708"
    data=to_16(data)
    aes=AES.new(key=key.encode("utf-8"),IV=iv.encode("utf-8"),mode=AES.MODE_CBC)
    bs=aes.encrypt(data.encode("utf-8"))
    return str(b64encode(bs),"utf-8")


"""
function a(a) {)
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
    function b(a, b) {
        var c = CryptoJS.enc.Utf8.parse(b)
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {
            iv: d,
            mode: CryptoJS.mode.CBC
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    function d(d, e, f, g) {d:数据,e:010001,f:很复杂，g:0CoJUm6Qyw8W8jud
        var h = {}
          , i = a(16);
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),
        h.encSecKey = c(i, e, f),
        h
    }
"""

resp=requests.post(url,data={
    "params":get_params(json.dumps(data)),
    "encSecKey":get_encSecKey()
})
comments = resp.json()["data"]["comments"]
with open("comments_content.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["content"])
    for comment in comments:
        content = comment.get("content")
        if content:  # 确保 content 不为空
            writer.writerow([content])

print("评论内容已保存为 comments_content.csv")