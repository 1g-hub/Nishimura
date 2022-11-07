import random
import card
import numpy as np

class Player1:
    #コンストラクタ
    def __init__(self,enemy,name="player1"):
        #体力と最大体力と名前
        self.hp = 20
        self.maxhp = 20
        self.name = name
        #デッキ,手札,自分の盤面,墓地を配列で管理
        self.deck = []
        self.hand = []
        self.is_played = []
        self.discard = []
        #敵への参照取得
        self.enemy = enemy

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
            #print(self.name + "は" + draw_card + "をドローした")

    #ダメージ受けた時
    def damage(self,cnt):
        #cardと同じ
        self.hp -= cnt
        if self.hp < 0:
            self.hp = 0
        print(self.name + "health: " + str(self.hp)  +"/"+ str(self.maxhp))
        if self.hp <= 0:
            print("GAMEEND")

    #手札のカード表示
    def printhand(self):
        print ("")
        print  (self.name + "の手札")
        #number them
        for i in range(len(self.hand)):
            print (str(i+1) + " - " + self.hand[i])
        print ("")
    
    #場のカード表示
    def printisplayed(self):
        print("")
        print(self.name + "の場にあるカード")
        
        for i in range(len(self.is_played)):
            print(str(i+1) + " : " + self.is_played[i])
    
    #場にカード出す
    def playcard(self):
        #盤面表示
        #self.enemy.printisplayed()
        #self.printisplayed()
        #self.printhand()
        #ここではランダムに
        random.shuffle(self.hand)
        play_card = self.hand.pop()
        #print(self.name + "は" + play_card + "を場に出した")
        #自分の盤面カードリストに追加
        self.is_played.append(play_card)
        #カードをactivateさせる
        play_card.activate()
        return ""

    #場のカード使う
    def usecard(self):
        #自分の盤面に手札がなかったら
        if len(self.is_played) == 0:
            print(self.name + "は盤面にカードがありません")
        else:
            #盤面分カードをループ
            for use_card in self.is_played:
                #cardのusedがFalseなら使えない
                if use_card.is_used == False:
                    #trueにして使えるようにする
                    use_card.is_used == True
                    #target指定
                    target = self.selecttarget()
                    #ターゲットが無ければ顔殴る
                    if target == False:
                        print(self.name + "は" + self.enemy.name + "を攻撃した")
                        self.enemy.damage(use_card.attack)
                    else:
                        print("")
                        print(self.name +"の攻撃")
                        use_card.use(target)
        return ""
    
    #自分の手札からランダムに一枚選ぶ
    def selectcardplayed(self):
        chosen_card = random.choice(self.is_played)
        return chosen_card
    
    #相手のターゲットを選ぶ
    def selecttarget(self):
        #相手の盤面にカードがなかったらFalse
        if len(self.enemy.is_played) <= 0:
            return False
        #カードあったらランダムに一枚選ぶ
        else:
            enemy_attack = []
            for i in self.enemy.is_played:
                enemy_attack.append(i.attack)
            target = self.enemy.is_played[np.argmax(enemy_attack)]
            return target
            

    
    
        


    

