import random
import card

class Player1:
    #コンストラクタ
    def __init__(self,name):
        #体力と最大体力と名前
        self.hp = 20
        self.maxhp = 20
        self.name = name
        #デッキ,手札,自分の盤面,墓地を配列で管理
        self.deck = []
        self.hand = []
        self.is_played = []
        self.discard = []

    #デッキシャッフル
    def shuffle(self):
        #random.shuffleを用いて配列deckの要素をシャッフル
        random.shuffle(self.deck)
    
    #カードのドロー
    def draw(self):
        if len(self.deck) <= 0:
            print(self.name + "のデッキにカードがありません")
        else:
            #デッキからカード一枚とって手札に加える
            draw_card = self.deck.pop()
            self.hand.append(draw_card)
            print(self.name + "はカードをドローした")

    #ダメージ受けた時
    def damage(self,cnt):
        #cardと同じ
        self.hp -= cnt
        print(self.name + "health: " + str(self.hp)  +"/"+ str(self.mhp))
        if self.hp <= 0:
            print("GAMEEND")
    #場のカード表示
    def printinplay(self):
        print("")
        print(self.name + "の場にあるカード")
        
        for i in range(len(self.is_played)):
            print(str(i+1) + " : " + self.is_played[i])
    
    #場にカード出す
    def playercard(self):
        #ここではランダムに
        random.shuffle(self.hand)
        play_card = self.hand.pop()
        print(self.name + "は" + play_card + "をドローしました")
        #自分の盤面カードリストに追加
        self.is_played.append(play_card)
        #場にある
        play_card.activate()
        return ""
        


    

