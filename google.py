import gtts
def save(text,fileName,language):
    s=gtts.gTTS(text,lang=language)
    s.save(fileName)