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
def yomikaki(choice, ue, shita, ansurl):
    all = ue + shita
    flag = True
    quiz = []
    while flag:
        quiz = all[random.randint(0, len(all) - 1)]
        flag = (len(quiz[0]) <= 0) or (quiz[0].find('・') != -1)
    
    if choice:
        print("答えはひらがなで入力してね。送り仮名がある場合はそれも入力してね。")

    if quiz[choice] == input(quiz[not choice]):
        print("常識だね！")
        print("参考：" + ansurl)
        return point()
    else :
        print("記憶喪失...？「" + quiz[choice] + "」に決まってるじゃん")
        print("参考：" + ansurl)
        return -point()

#和同開珎の生成と正誤判定
def wado(ue, shita, anskan, ansurl):
    quiz = ["" for _ in range(4)]

    flag = True
    while flag:
        quiz[0] = ue[random.randint(0, len(ue) - 1)][0]
        flag = (len(quiz[0]) <= 1) or (quiz[0].find('・') != -1)

    flag = True
    while flag:
        quiz[1] = ue[random.randint(0, len(ue) - 1)][0]
        flag = (len(quiz[1]) <= 1) or (quiz[1].find('・') != -1) or (quiz[1] == quiz[0])

    flag = True
    while flag:
        quiz[2] = shita[random.randint(0, len(shita) - 1)][0]
        flag = (len(quiz[2]) <= 1) or (quiz[2].find('・') != -1)

    flag = True
    while flag:
        quiz[3] = shita[random.randint(0, len(shita) - 1)][0]
        flag = (len(quiz[3]) <= 1) or (quiz[3].find('・') != -1) or (quiz[3] == quiz[2])

    for i in range(len(quiz[2]) - 1):
        print((len(quiz[3]) - 1) * '　' + quiz[2][i])

    print(quiz[3][0:-1] + '？' + quiz[1][1:])

    for i in range(len(quiz[0]) - 1):
        print((len(quiz[3]) - 1) * '　' + quiz[0][i + 1])

    if anskan == input("？に入るのは："):
        print("てんさい！")
        print("参考：" + ansurl)
        return point()
    else :
        print("あほ？「" + anskan + "」じゃん幼稚園児でもわかるぞ")
        print("参考：" + ansurl)
        return -point()

def point():
    po = [114, 514, 1919, 810, 114514, 334, 264, 0.721, 1145141919810, 69, 4545, 1107, 1919810]
    return po[random.randint(0, len(po) - 2)]

def game(now):
    print("第" + str(now) + "問！")

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
    ansurl = "https://www.kanjipedia.jp" + elems[ansnum].attrs['href']
    time.sleep(1)
        
    #get jukugos
    res2 = requests.get(ansurl)
    soup2 = BeautifulSoup(res2.text, "html.parser")
    shita = ""
    shit = soup2.find_all(True, alt = "下つき")
    if len(shit) != 0:
        for i in shit[0].parent.next_siblings:
            shita += str(i)
    if shita.find("img") != -1:
        print("むずすぎて漢字を表示できません")
        print("参考：" + ansurl)
        return 0
    ue = soup2.find_all(href = re.compile("kotoba"))
    ue = oi_kenta(ue, ',')
    shita = oi_kenta(shita, '・')

    #make quiz
    choice = -1
    if judge(ue, 1) & judge(shita, 1):
        while not (1 <= choice <= 3):
            choice = int(input("1,書き 2,読み 3,和同開珎  :"))
    elif judge(ue, 0) | judge(shita, 0):
        while not (1 <= choice <= 2):
            choice = int(input("1,書き 2,読み  :"))
    else :
        print("漢字むずすぎて問題作れなかったのでやり直します")
        print("参考：" + ansurl)
        return 0

    if 1 <= choice <= 2:
        return yomikaki(choice - 1, ue, shita, ansurl)
    else :
        return wado(ue, shita, anskan, ansurl)
    

def main():
    mondaisu = int(input("何問やるー？："))
    score = 0

    for i in range(mondaisu):
        res = 0
        while res == 0:
            res = game(i + 1)
            if res > 0:
                score += res
                print(res, "点ゲット！")
            elif res == 0:
                pass
            else :
                print("こんな問題を間違えるなんて", -res, "点減点じゃ！！")
                score += res

    print("今回のあなたの得点は", score, "点でした！！精進したまえよ。")


if __name__ == "__main__":
    main()