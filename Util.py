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

def TrimAtEuqalSign(content):
    content = content.strip()
    while content.find(' =') > 0:
        content = content.replace(' =', '=')
    while content.find('= ') > 0:
        content = content.replace('= ', '=')
    return content

def DivideNameValue(paramValuePair):
    paramValuePair = paramValuePair.strip()
    words = paramValuePair.split('=')
    if len(words) == 2:
        return words[0].strip(), words[1].strip()
    else:
        return None, None

    