import numpy as py

def GetNextWord(content):
#get the word before next blank
    content = content.strip()
    if len(content) < 1:
        return '', content
    nextBlank = content.find(' ')
    if nextBlank == -1:
        return content.strip(), ''
    return content[0:nextBlank], content[nextBlank:].strip()

def TrimBeforeAfter(sign, content):
    content = content.strip()
    while content.find(' '+sign) > 0:
        content = content.replace(' '+sign, sign)
    while content.find(sign + ' ') > 0:
        content = content.replace(sign +' ', sign)
    return content

def RemoveSpace(content):
    if content == None:
        return None
    if len(content) == 0:
        return ''
    content = TrimBeforeAfter('=', content)
    content = TrimBeforeAfter(',', content)
    while not content.find('  ') == -1:
        content = content.replace('  ', ' ')
    result = ''
    sCount = 0
    for c in content:
        if c == '\'':
            sCount = (sCount+1) % 2
        if c == ' ' and sCount == 1:
            pass
        else:
            result = result+c
    return result
            
    

def DivideNameValue(paramValuePair):
    paramValuePair = paramValuePair.strip()
    words = paramValuePair.split('=')
    if len(words) == 2:
        return words[0].strip(), words[1].strip()
    else:
        return '', ''



    