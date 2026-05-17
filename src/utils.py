import base64
import hashlib

API = "http://www.boomlings.com/database/"
SECRET = "Wmfd2893gb7"
HEADERS = { "User-Agent": "" }

def xor(text: str, key: str) -> str:
    res = []
    for i in range(len(text)):
        c = ord(text[i])
        xkey = ord(key[i % len(key)])
        res.append(chr(c ^ xkey))
    return "".join(res)

def generateChk(values: list[int | str], key: str, salt: str) -> str:
    salted = [*values, salt]
    string = "".join(map(str, salted))

    hashed = hashlib.sha1(string.encode()).hexdigest()
    xored = xor(hashed, key)
    return base64.urlsafe_b64encode(xored.encode()).decode()

def commentChk(username: str, comment: str, levelID: int, percentage: int) -> str:
    salted = [username, comment, levelID, percentage, "0xPT6iUrtws0J"]
    string = "".join(map(str, salted))

    hashed = hashlib.sha1(string.encode()).hexdigest()
    xored = xor(hashed, "29481")
    return base64.urlsafe_b64encode(xored.encode()).decode()

def gjp2(password: str) -> str:
    string = password + "mI29fmAnxgTs"
    return hashlib.sha1(string.encode()).hexdigest()

def parseTempBan(res: str) -> dict[str, str]:
    pieces = res.split("_")
    return {
        "duration": simplifySeconds(int(pieces[1])),
        "reason": pieces[2]
    }

def simplifySeconds(seconds: int) -> str:
    return str(round(seconds / 86400))

def parseKeyValStr(keyval: str) -> dict[str, str]:
    pieces = keyval.split(":")
    res = {}
    for i in range(0, len(pieces) - 1, 2):
        key = pieces[i]
        val = pieces[i + 1]
        res[key] = val
    return res