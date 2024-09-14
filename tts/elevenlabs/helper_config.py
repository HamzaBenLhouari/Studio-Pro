def get_text():
    print("getting text script")
    script=""
    with open("./eleven_labs_tts/script.txt") as f:
        script = f.read()
    if script == "" :
        print("script is empty")
    else : print("text script done")
    return script

def get_api_key():
    print("getting api key")
    api_key=""
    with open("./eleven_labs_tts/api_key.txt") as f:
        api_key = f.read()
    if api_key == "" :
        print("api key is empty")
    else : print("api key done")
    return api_key

def get_voice_model():
    print("getting voice model")
    voice_model=""
    with open("./eleven_labs_tts/voice_model.txt") as f:
        voice_model = f.read()
    if voice_model == "" :
        print("voice model is empty")
    else : print("voice model done")
    return voice_model