import numpy as py
from GlobalVar import globalModelNames, globalParamNames, globalParamValues, SPICEUNIT


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
    elif len(words) == 1:
        return words[0].strip(), ''
    else:
        return '', ''

def IsValidGlobalParam(parName):
    if parName == None:
        return False
    return parName in globalParamNames

def IsValidGlobalModel(modelName):
    if modelName == None:
        return False
    return modelName in globalModelNames

def EvaluateValue(value):
    #expression must start and end with \'
    #only + - * / ( ) operators are support
    if value == None:
        return 0.
    value = str(value).upper()
    if IsNumber(value):
        return eval(value)
    if len(value) < 2:
        return 0.
    if value[0] == '\'' and value[-1] == '\'':
        value = ExpandExpression(value[1:-1])
    #replace the parameters
    for param in globalParamNames:        
        if ' ' + param + ' ' in value:
            value = value.replace(param, globalParamValues[globalParamNames.index(param)])
    #handle the U, M, K
    for key in SPICEUNIT.keys():
        if key in value:
            value = value.replace(key, '*'+SPICEUNIT[key])  
    ret = 0.
    try:
        ret = eval(value)
    except:
        ret = 0.
    return ret         
def ExpandExpression(value):
    #add into blank before and after each operator
    if value == None:
        return ''
    if len(value) == 0:
        return ''
    #remove the first character is it is '+'
    if value[0] == '+':
        if len(value) >= 2:
            value = value[1:]
        else:
            return ''
    retVal = ''
    index = 0
    lastIsLeftBracket = False
    for ch in value:
        if ch == '+' or ch == '*' or ch == '/' or ch == ')':
            retVal += ' ' + ch + ' '
            lastIsLeftBracket = False
        elif ch == '-':
            if index == 0 or lastIsLeftBracket:
                retVal += ch
            else:
                retVal += ' ' + ch + ' '
            lastIsLeftBracket = False
        elif ch == '(':            
            lastIsLeftBracket = True    
            retVal += ' ' + ch + ' ' 
        else:
            retVal += ch                  

        index += 1
    return retVal


def IsNumber(str):
    try:        
        if str=='NaN':
            return False
        float(str)
        return True
    except ValueError:
        return False