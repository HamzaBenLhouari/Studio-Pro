import os, requests, base64, playsound


def get_script():
    print("getting text script")
    script=""
    with open("./tiktok_tts/script.txt") as f:
        script = f.read()
    if script == "" :
        print("script is empty")
    else : print("text script done")
    return script
def get_sessionid():
    print("getting session id")
    sessionid = ""
    with open("./tiktok_tts/session_id.txt") as f:
        sessionid = f.read()
    if sessionid == "":
        print("session id not found")
    else :
        print("session id done")
    return sessionid
def get_voice_type():
    print("getting voice type")
    voice = ""
    with open("./tiktok_tts/voice_model.txt") as f:
        voice = f.read()
    if voice == "":
        print("voice not found")
    else :
        print("voice id done")
    return voice

def tts(session_id: str, text_speaker: str = "en_us_002", req_text: str = "TikTok Text To Speech", filename: str = 'voice.mp3', play: bool = False):

    req_text = req_text.replace("+", "plus")
    req_text = req_text.replace(" ", "+")
    req_text = req_text.replace("&", "and")

    headers = {
        'User-Agent': 'com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)',
        'Cookie': f'sessionid={session_id}'
    }
    url = f"https://api22-normal-c-useast1a.tiktokv.com/media/api/text/speech/invoke/?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0&aid=1233"
    r = requests.post(url, headers = headers)

    if r.json()["message"] == "Couldn't load speech. Try again.":
        output_data = {"status": "Session ID is invalid", "status_code": 5}
        print(output_data)
        return output_data

    vstr = [r.json()["data"]["v_str"]][0]
    msg = [r.json()["message"]][0]
    scode = [r.json()["status_code"]][0]
    log = [r.json()["extra"]["log_id"]][0]
    
    dur = [r.json()["data"]["duration"]][0]
    spkr = [r.json()["data"]["speaker"]][0]

    b64d = base64.b64decode(vstr)

    with open(filename, "wb") as out:
        out.write(b64d)

    output_data = {
        "status": msg.capitalize(),
        "status_code": scode,
        "duration": dur,
        "speaker": spkr,
        "log": log
    }

    print(output_data)

    if play is True:
        playsound.playsound(filename)
        os.remove(filename)

    return output_data