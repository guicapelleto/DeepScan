#coding: utf-8

def find_all_lines(padrao, texto, sensitive = False):
    padrao = str(padrao)
    texto = str(texto).replace('\\r','')
    original = texto
    if not sensitive:
        padrao = padrao.lower()
        texto = texto.lower()
    if '.*' in padrao:
        padrao = padrao.split('.*')
    else:
        padrao = [padrao]
    original = original.split('\\n')#.splitlines()
    texto = texto.split('\\n')#splitlines()
    line_index = 0
    found_lines = []
    for line in texto:
        for word in padrao:
            if word in line:
                line = line.split(word)[1]
                check = True
            else:
                check=False
                break
        if check == True:
            found_lines.append(original[line_index])
        line_index += 1
    return found_lines


#l = open('/Users/gui/Documents/Untitled.txt','r').read()
#p = 'linha'

#print (len(find_all_lines(p, l)))
#for word in find_all_lines(p,l): print(word)