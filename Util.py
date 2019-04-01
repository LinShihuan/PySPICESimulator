import numpy as py

def GetWord(content):
#get the word before next blank
    content = content.strip()
    if len(content) < 1:
        return '', content
    nextBlank = content.find(' ')
    if nextBlank == -1:
        return content.strip(), ''
    return content[0:nextBlank], content[nextBlank:].strip()
    