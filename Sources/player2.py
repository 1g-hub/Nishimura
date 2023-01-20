import random
import player1
import card

class Player2:
    #コンストラクタ
    def __init__(self,name="Learning Player"):
        #体力と最大体力と名前
        self.hp = 20
        self.maxhp = 20
        self.name = name
        #ターン中コストとターン中最大コストと最大コスト
        self.cost = 1
        self.turnmaxcost = 1
        self.maxcost = 5
        #デッキ,手札,自分の盤面,墓地を配列で管理
        self.deck = []
        self.hand = []
        self.is_played = []
        self.discard = []
        #手札枚数制限,盤面制限
        self.hand_maxnum = 9
        self.is_played_maxnum = 5
        #敵への参照取得
        self.enemy = player1.Player1(self)
        #デッキ切れに気づいたフラグ
        self.is_deckend = False
        #HPが0以下になったフラグ
        self.is_dead = False

        #デッキシャッフル
    def shuffle(self):
        #random.shuffleを用いて配列deckの要素をシャッフル
        random.shuffle(self.deck)
    
    #カードのドロー
    def draw(self):
        if len(self.deck) <= 0:
            #ここでデッキ切れに気づく
            self.is_deckend = True
            #print("GAMEEND : DECKEND")
            #print(self.name + "のデッキにカードがありません")
        else:
            #デッキからカード一枚とって手札に加える
            draw_card = self.deck.pop()
            self.hand.append(draw_card)
            if self.draw_count_dict[draw_card.id] == 0:
                self.draw_count_dict[draw_card.id] += 1
            #print(self.name + "は" + draw_card + "をドローした")
            #手札の枚数制限を超えたら最後にドローしたカード排除して墓地に入れる
            if len(self.hand) > self.hand_maxnum:
                eliminated_card = self.hand.pop(-1)
                self.discard.append(eliminated_card)

    #ダメージ受けた時
    def damage(self,cnt):
       #cardと同じ
        self.hp -= cnt
        if self.hp < 0:
            self.hp = 0
        #print(self.name + "health: " + str(self.hp)  +"/"+ str(self.maxhp))
        if self.hp <= 0:
            self.is_dead = True
            #print("GAMEEND : DEAD")
    
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
        self.enemy.printisplayed()
        self.printisplayed()
        self.printhand()
        #ここではランダムに
        #random.shuffle(self.hand)
        #出す順番固定
        if len(self.hand) <= 0:
            return ""
        
        #手札カード先頭から探索して出せるカードから出していく
        while(1):
            for play_card in self.hand:
                if play_card.cost <= self.cost:
                    #手札からpop
                    play_card = self.hand.pop(self.hand.index(play_card))
                    #自分の盤面カードリストに追加
                    self.is_played.append(play_card)
                    #コスト減少
                    self.cost -= play_card.cost
                    #print(self.name + "は" + play_card + "を場に出した")
                    #盤面の枚数制限超えてたら最後に追加したカード削除
                    if len(self.is_played) > self.is_played_maxnum:
                        eliminated_card = self.is_played.pop(-1)
                        self.discard.append(eliminated_card)
                    else:
                        #カードをactivateさせる
                        play_card.activate(self)
            #出せるカード無くなったらbreak
            sum = 0
            for play_card in self.hand:
                if play_card.cost <= self.cost:
                    sum += 1
            if sum == 0:
                break
        return ""

     #場のカード使う
    def usecard(self):
        #自分の盤面に手札がなかったら
        if len(self.is_played) == 0:
            pass
            #print(self.name + "は盤面にカードがありません")
        else:
            while(1):
                #盤面分カードをループ
                for use_card in self.is_played:
                    #cardのusedがFalseなら使えない
                    if use_card.is_used == False:
                        #trueにして使えるようにする
                        use_card.is_used == True
                        #target指定
                        target = self.selecttarget(use_card)
                        #ターゲットが無ければ顔殴る
                        if target == False:
                            #print(self.name + "は" + use_card + "で" +  self.enemy.name + "を攻撃した")
                            self.enemy.damage(use_card.attack)
                            use_card.is_used = True

                        else:
                            #print("")
                            #print(self.name +"の攻撃")
                            use_card.use(target)
                #盤面全滅したか
                if len(self.is_played) <= 0:
                    break
                #全部Trueになってたらbreak
                sum = 0
                for i in self.is_played:
                    if i.is_used:
                        sum += 1
                if sum == len(self.is_played):
                    break
        return ""
    
    #自分の手札からランダムに一枚選ぶ
    def selectcardplayed(self):
        chosen_card = random.choice(self.is_played)
        return chosen_card
    
    #相手のターゲットを選ぶ
    def selecttarget(self,use_card):
         #相手の盤面にカードがなかったらFalse
                if len(self.enemy.is_played) <= 0:
                    return False
                #Blocking あればそいつしか殴れない
               #倒せるカードがあればそいつ倒して無ければ敵を殴る
                else:
                    for enemy in self.enemy.is_played:
                        if enemy.isBlocking:
                            return enemy
                    #Blocking 無ければ倒せる敵探す
                    for enemy in self.enemy.is_played:
                        if enemy.hp <= use_card.attack:
                            return enemy
                    #倒せる敵無くても敵の盤面の攻撃力総和が自分の hp より大きかったら敵盤面の最大攻撃力カードを殴る
                    sum = 0
                    attack_list = []
                    for enemy in self.enemy.is_played:
                        sum += enemy.attack
                        attack_list.append(enemy.attack)
                    #HP 判断
                    if sum >= self.hp:
                        max_attack_index = attack_list.index(max(attack_list))
                        return self.enemy.is_played[max_attack_index]
                    else:
                        return False
                return False
    def showDeck(self):
        for deckcard in self.deck:
            print(deckcard)
    
    def generate_dict_draw(self):
        self.draw_count_dict = {card.id: 0 for card in self.deck}

    def get_draw_record(self):
        self.draw_count_dict = sorted(self.draw_count_dict.items())
        return self.draw_count_dict