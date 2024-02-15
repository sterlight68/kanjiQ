import random
import re
import time
import requests
from bs4 import BeautifulSoup

#htmlをstr型にして、漢字と読みのlistを作る
def oi_kenta(us, sp):
    pattern = r'[a-zA-Z0-9<>"/▲△=〈〉\[\]\) －\n]'
    us = str(us)
    us = re.sub(pattern, '', us)
    for i in range(len(us)):
        c = us[i]
        if ord('ァ') <= ord(c) & ord(c) <= ord('ン'):
            us = us.replace(c, chr(ord(c) + ord('あ') - ord('ア')))
    us = us.split(sp)
    for i in range(len(us)):
        us[i] = us[i].split('(')
    return us

#問題を作成できるか判定
def judge(us, w):
    gomi = 0
    for c in us:
        gomi += int((len(c[0]) <= w) or (c[0].find('・') != -1))
    return len(us) - gomi >= w + 1

#読み問題と書き問題の生成と正誤判定
def yomikaki(choice, ue, shita):
    all = ue + shita
    flag = True
    quiz = []
    while flag:
        quiz = all[random.randint(0, len(all) - 1)]
        flag = (len(quiz[0]) <= 0) or (quiz[0].find('・') != -1)
    
    if choice:
        print("答えはひらがなで入力してね。送り仮名がある場合はそれも入力してね。")

    if quiz[choice] == input(quiz[not choice]):
        print("せいかーい")
    else :
        print("ざんねーん  答えは「" + quiz[choice] + "」")

#和同開珎の生成と正誤判定
def wado(ue, shita):
    print("aa")

def main():
    
    #create url 
    url = "https://www.kanjipedia.jp/sakuin/honbun/"
    pages = [6,12,4,12,7,44,39,6,24,39,19,79,6,26,20,18,17,2,16,22,2,2,2,1,20,17,13,9,19,5,2,2,3,4,3,7,9,6,15,2,8,9,3]
    kata = ['ア','イ','ウ','エ','オ','カ','キ','ク','ケ','コ','サ','シ','ス','セ','ソ','タ','チ','ツ','テ','ト','ナ','ニ','ネ','ノ','ハ','ヒ','フ','ヘ','ホ','マ','ミ','ム','メ','モ','ヤ','ユ','ヨ','ラ','リ','ル','レ','ロ','ワ']
    kana = random.randint(0,42)
    pagenum = random.randint(1,pages[kana])
    url += kata[kana] + '/' + str(pagenum)

    #get html and next url
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    elems = soup.find_all(href = re.compile("/kanji/"))
    ansnum = random.randint(0, len(elems) - 1)
    anskan = elems[ansnum].contents[0]
    ansurl = elems[ansnum].attrs['href']
    print("問題にする漢字を選択しています")
    time.sleep(1)

    print("参考：https://www.kanjipedia.jp" + ansurl)
        
    #get jukugos
    res2 = requests.get("https://www.kanjipedia.jp" + ansurl)
    soup2 = BeautifulSoup(res2.text, "html.parser")
    shita = ""
    shit = soup2.find_all(True, alt = "下つき")
    if len(shit) != 0:
        for i in shit[0].parent.next_siblings:
            shita += str(i)
    if shita.find("img") != -1:
        print("むずすぎて漢字を表示できません")
        print("参考：https://www.kanjipedia.jp" + ansurl)
        return
    ue = soup2.find_all(href = re.compile("kotoba"))
    ue = oi_kenta(ue, ',')
    shita = oi_kenta(shita, '・')

    #make quiz
    #choice = -1
    choice = 2
    if judge(ue, 1) & judge(shita, 1):
        while not (1 <= choice <= 3):
            choice = int(input("1,書き 2,読み 3,和同開珎  :"))
    elif judge(ue, 0) | judge(shita, 0):
        while not (1 <= choice <= 2):
            choice = int(input("1,書き 2,読み  :"))
    else :
        print("漢字むずすぎて問題作れなかったのでやり直します")
        print("因みに漢字は「" + anskan + "」")
        print("参考：https://www.kanjipedia.jp" + ansurl)
        return

    if 1 <= choice <= 2:
        yomikaki(choice - 1, ue, shita)
    else :
        wado(ue, shita)

    print("参考：https://www.kanjipedia.jp" + ansurl)
    


if __name__ == "__main__":
    for i in range(10):
        main()