with open('./test/text2.txt','w',encoding='utf-8') as g:
    g.write('你好吗,my dog')
    g.close()
with open('./text.txt','r',encoding='utf-8') as f:
    print(f.read())
    print(f.seek(1,0))
    print(f.tell())
    print(f.readline)
    f.close()