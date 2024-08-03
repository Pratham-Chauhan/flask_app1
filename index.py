from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import json
import requests as rq

app = Flask(__name__)

# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
# }

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': 'at=ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pT0dZeE9EWmtaV1V0TlRFNFpTMHhNV1ZtTFRnek1tTXRNbVV3TURCa1lqSmhaREEySWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUzTXpneU16YzRNVGtzSW1semN5STZJa2xFUlVFaWZRLjdEZlFwanlabmFQQ3FlbkxQRmFkVjRXdUpKcGk4YW1rem11SUlMdEFiU1U=; _d_id=346a79a2-3569-4aea-8836-0661fd37b56c; bm_ss=ab8e18ef4e; ak_bmsc=98E98AF7883BB6337A6CDE8B1A7C4662~000000000000000000000000000000~YAAQD20/F0qxtP6QAQAAxYwTGBgf6nDuivIUuAtFx1Dt4Vwzfi+X1D0d6S+b+/hyBM1m2BuFsk+bf2Nk1HgNklSz4GGc6SxC8GwQkCkg3nY91bIAalzJ/xTmpDem0VMNoQPH+en8+ZDFo0FPNLmtXnhYPv6IxiI++tjE9mm2s6crGGsFBmbIbU4NfoGmbGdg+2H/NEqj/wMAjgGFRoIlywyCbxdS/jBClnEsxLLTlL2g6rWpdmG/7AAxrdFPAffOVePj0Y9+gVBdM2JX5yx68/bW3p4SwNcQeliyIB59JQRNPvA6dZYKqpKt4WY8raEVA2WkRqw0vegesgYP0PqRU8zTbjSMFtlSCKzXwLS9aseV5ivjRDPEzBej6WHP2GA/9NZQTjrSic+akWd7UxVmf7NDXv0PehEZoQMulG8YWA8GiTVX; mynt-eupv=1; _abck=B8F380B4EADA5F67C56387750FBEB8D1~0~YAAQD20/F1axtP6QAQAAUZATGAxxIJ+p5Q+7qISQ5cXhIwSfu7yUd576bxIenkbjGpHEJrru1osALjGxugK6wkFdplwwqJuDy++2Cey3hUIvz9RB7xS/di1G5h8k63PAT8aCYQO9BErE+qJvp5KMxkvcsI8os4EWoOmyRCCGRycPZALYb/O9aZtPw9fyKTe3OI0PDLtS6XzTGDcfl8fHf1O5TTp+TFd8cmT9JTnhfss43kwIxDRLfvaIsrK2h3EaEDxWhuWL/m1e/vsT++S0KY4tDwgGmUMftgPwniuncLuHTu1JCizZY9AWmZwSbtQj64Cpz4MB/gtShNPQpoeSJsMqGk7uwtJgaE3xtAg/CaS9Sy8ZV/N1enf4rvNFF+xBRbC/jqTyy0EOOFBj6k6/vQ47KxGyI18=~-1~||0||~-1; _xsrf=9qr96JMWHtV4KAGnx4nHIPoHukXhw3WC; mynt-ulc-api=pincode%3A110060; mynt-loc-src=expiry%3A1722687261394%7Csource%3AIP; x-mynt-pca=CG6dcArfcBEoQX8DJmrAKYV8ZQ8iZr0XXm54uTGSdL5adEo7-2tphcjwHzjgYm7gUguBKvAF8WO7gz-pgc38em2I2tPI6IeOQHwt0xskmqZbxsENgbOhyQlEyCBcGI2dmdYtTwcjfGeTNv8SFuq2nGmI18EV8SAOjxcuG6VFiLAf2vyZMEMj_Q%3D%3D; ext_name=ojplmecpdpgccookcobabopnaifgidhf; bm_so=D6AB5DF3AD01CFCB6DD4A849216140688BF5947426284577003ACBE816AC70E5~YAAQH20/F55nXA2RAQAAxFQWGAB3r1VIh36J0RNdjchBySw5JHTcmDT+V2hZNaewVS2OPFeDn4J8MOe4X3rr3qdrIKK1Dfm2bD0a3/M6hLAxaD3FLaLA4Xp0tz1tzwlbZFNooPIRjOWH7RSgXSURhTD2pNO96cuKgJXZgR5mcXvgcQ9O4RaCdznRuOuk2sh8A+7kVVX/TDZpzp+c7iDcDRnCZh21wlBiE1oCPgwhaj8mP6bXvdXuqfuro255/k2s/9lxiZuEo69V03tUZF6qPxCgyCDeHUSNNlOM+SyN9k9Td6FmZye3GibzicfXZ6nwIOmHOgN+8n86dQUxMaD03F3H59Rx7J14Gnsy82Er4X0uCP3CgyVQtHqFP/70I0dAnEnFVqF+FlupP9tnspb527lhy3EmWBI+QrPRxlCSXqLLPgwA1ORWMPgWf/BpeJ3gJGZLtfcZcGmxuBgasLftjmWeVghU21g/s8UUpjYrGDiXAh7Zgf0fdWaa5xxolLEWqC6lllTTjyvhhEe1fRyOnLn2XPCizXZqZutYt+Qy4Y3r8E7k+b/j7yFCRj9RCnOLo6uzh171L0RA/N9ReJVJg7mrhUESsIy8q9wszoYhm5cjWy8+5ZrxyHpO; bm_sz=0C10E8C149230CEBD96E59B2B48FA65A~YAAQH20/Fz9oXA2RAQAAUnIWGBiDgSyRuCluRQ/+hnUIZbAG0/NphKmNtrgKwe1RxRZgm5opdTSloUDTnfusxph9ofC6Zjqh4lVGjDV1xhrZ6Nh3ccvYcOGGm+2qY/8Lnp2sUl4MdadQTxqaoesHwwATVn6rOOpNAdfBLl2UtxuCGOQTKKIECuR2ixnf+M0/r9Lm2P/oweGJFO6bOZsUjRF3oUswsXIGh84hdHQfn3Is2riYEkDUgg773oc/W7r1T1o6y71s74nJ7t/iPHvk3Ju+OBfsu/fBcB2fjJ2z4UlezqNbdUA26oxWH9qhf1KbdVxUZt712XAbndtQsPnk67SYEbU2z7miYKItBfkIEOrLMvfi/zCnW/gAPX10bARGCDEuT6s3IVyetqBlwvgOm8ycaEhltQ7zVk63W5m4M+DlbhqKDPOb0EcsDNEdHImMwSh+4Gpcw8vDfpmhkDNnXg==~3551792~3687746; bm_s=YAAQH20/F1ZoXA2RAQAAsHUWGAGyOfY8ihoguf1JEy53lLVHH2QRnpXnn34o20lQRgFwHfBxRW1zm72Q1ZMKNMQe3kclAxGRGjj9CMIjFjYk1huU2vXv7Pgb/a1bvjNeM0aiqsvkofPGVtehnnSlshheKEnstUp2IKFqeQe5/VuDf7xHn9ZdFQCMuNsw4M+BIRm+15y0FjhzHkDRPBtlenV48bw3MTkTMl0MTMfbCEKT87lKdbA2KZmSvFF/gFOE1xxJyu0ZnNrl8VxzaIS7dgt2fceT+6wA2v3agLhlzjk6qJtB955xjXuo5o3IXdCdEleXllxK7AxOowFeOGdRcRs=; _mxab_=config.bucket%3Dregular%3BConvenience_fee_logged_out_user%3Denabled%3Bcoupon.cart.channelAware%3DchannelAware_Enabled%3Bdesktop.pla%3Denabled; _pv=default; dp=d; utm_track_v1=%7B%22utm_source%22%3A%22direct%22%2C%22utm_medium%22%3A%22direct%22%2C%22trackstart%22%3A1722687863%2C%22trackend%22%3A1722687923%7D; lt_timeout=1; lt_session=1; bm_mi=60D668F40434D2793A99C5EC68C312BC~YAAQNG0/F1qvYgCRAQAAQ7syGBj7lVIuu3lp1a2+tae1WSxosTCc1s5p5kdcXMlWsbrcCTt+f91aCIMUbec+rwk87OLCDv5I9VaU9yBrZp+7IwJ7zC8Wi4rPnLFTWwMmeMYiHIR5Gip0LXTRaEmzS8bbelpYycshRbqnPxyuaR/y/mlS+u1IkaVXz7SHOLQwktEs//tTakrs812oKWxLNcrHUXd/CGR8qfTRI8pOHT0JtbXZ+8GTh21zTlLnMYsKPCZFhvCVSuFFQQwm3j4fk+LqRZMJle7IMjFwNO4r7RYKa/fvVQtrkzxnJN8SnfHswt0/PnCwhggY4FJk4ZMqYkBpsHbJvbA4+xVKzgomH1awag==~1; utrid=TGd%2BcGhTERsUb0pgcAVAMCMxOTI3NDI3Mzg3JDI%3D.f70fa51d7bc19fec4ef516bf26e64bda; bm_sv=8C844C201A38863C2DB321895B9E7B2C~YAAQNG0/F8qvYgCRAQAAusQyGBgE7rzziboJUtOcZYEqoZnfbKvSnIDOwDcAtG/S64zMNMNsFU0HL/6lefzoL8pTn4uF44Wvq0ah4l3df99MWD2ulFN3rzO1HDQxzKKSkeEeuJJ+kDLFAcLD0AVSYks32WzcpWtitLofEfrH2Qya6xI8V39TFJWzh4G58TWm4ay3fIv6urZutuaEANDH+sA/k002dn52AD9LRVHrnbAmCXscs6FZdvNxJ/Mlqq2tyQ==~1',
    'dnt': '1',
    'if-none-match': 'W/"506bd-dFvtKN5UVOWzVlT3DaRN/ONiB+c"',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}


def get_price(style_id):
    s = rq.Session()

    url = f'https://www.myntra.com/{style_id}'  
    res = s.get(url, headers=headers)

    print((res, style_id))
    soup = BeautifulSoup(res.text, 'html.parser')
    
    print('TEXT:', soup)
    script_text = next((s.get_text(strip=True) for s in soup.find_all("script") if 'pdpData' in s.text), None)
    if script_text:
        try:
            data = json.loads(script_text[script_text.index('{'):])
            mrp = data['pdpData']['price']['mrp']
            price = data['pdpData']['price']['discounted']
            print((mrp, price))
            return mrp, price
        except (json.JSONDecodeError, KeyError) as e:
            print('error: ', e)
            pass
    # return 'OOS'
    return None, None

@app.route('/get_prices', methods=['GET'])
def get_prices():
    style_ids = request.args.get('style_ids').split(',')
    print("style_ids", style_ids)
    data = []
    for style_id in style_ids:
        mrp, price = get_price(style_id)
        data.append({'style_id': style_id, 'mrp': mrp, 'price': price})
    return jsonify(data)

# if __name__ == '__main__':
#     app.run('0.0.0.0', port=8080)
