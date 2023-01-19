import random
import card
import numpy as np
import randomplayer1
import player1

class RandomPlayer2:
    #コンストラクタ
    def __init__(self,name="Random 2"):
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
        self.enemy = randomplayer1.RandomPlayer1(self)
        #デッキ切れに気づいたフラグ
        self.is_deckend = False
        #HPが0以下になったフラグ
        self.is_dead = False
        #プレイヤー初期ドロー枚数
        self.init_draw_count = 3

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
    
    def selectdraw(self, select_num):
        for i in range(len(self.deck)):
            if self.deck[i].id == select_num:
                draw_card = self.deck.pop(i)
                self.hand.append(draw_card)
                break
        print(self.name + "は" + draw_card + "をドローした")

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
    
    #プレイヤーのコストUpdate処理 (ターン処理で呼ばれる)
    def updatecost(self):
        if self.turnmaxcost < self.maxcost:
            self.turnmaxcost += 1
        self.cost = self.turnmaxcost
        #print("updated cost")
        #print(self.name + ":" + str(self.cost))

    #盤面から使える行動を選んでvalid_movesに追加、それをreturn 
    def get_valid_moves(self):
        player = self
        valid_moves = []
        #手札
        for i in range(len(self.hand)):
            if self.hand[i].is_see == False:
                #valid_moves.append(i+9)
                if self.hand[i].cost <= self.cost:
                    valid_moves.append(i)

        #盤面1
        if len(player.is_played) > 0 and player.is_played[0].is_used == False:
            #Blocking の数数えてあればそいつだけ追加, なければ敵盤面あるカード全部と敵
            blocking_sum = 0
            for i in range(len(player.enemy.is_played)):
                #print(player.enemy.is_played[i])
                if player.enemy.is_played[i].isBlocking:
                    #print("Blockingあるぞ")
                    blocking_sum += 1
            #print("blocking_sum")
            #print(blocking_sum)
            if blocking_sum > 0:
                for i in range(len(player.enemy.is_played)):
                    if player.enemy.is_played[i].isBlocking:
                        valid_moves.append(i+9)
            else:
                valid_moves.append(14)
                for i in range(len(player.enemy.is_played)):
                    valid_moves.append(i+9)
        
        #盤面2
        if len(player.is_played) > 1 and player.is_played[1].is_used == False:
            #Blocking の数数えてあればそいつだけ追加, なければ敵盤面あるカード全部と敵
            blocking_sum = 0
            for i in range(len(player.enemy.is_played)):
                #print(player.enemy.is_played[i])
                if player.enemy.is_played[i].isBlocking:
                    #print("Blockingあるぞ")
                    blocking_sum += 1
            #print("blocking_sum")
            #print(blocking_sum)
            if blocking_sum > 0:
                for i in range(len(player.enemy.is_played)):
                    if player.enemy.is_played[i].isBlocking:
                        valid_moves.append(i+15)
            else:
                valid_moves.append(20)
                for i in range(len(player.enemy.is_played)):
                    valid_moves.append(i+15)
        
        #盤面3
        if len(player.is_played) > 2 and player.is_played[2].is_used == False:
            #Blocking の数数えてあればそいつだけ追加, なければ敵盤面あるカード全部と敵
            blocking_sum = 0
            for i in range(len(player.enemy.is_played)):
                #print(player.enemy.is_played[i])
                if player.enemy.is_played[i].isBlocking:
                    #print("Blockingあるぞ")
                    blocking_sum += 1
            #print("blocking_sum")
            #print(blocking_sum)
            if blocking_sum > 0:
                for i in range(len(player.enemy.is_played)):
                    if player.enemy.is_played[i].isBlocking:
                        valid_moves.append(i+21)
            else:
                valid_moves.append(26)
                for i in range(len(player.enemy.is_played)):
                    valid_moves.append(i+21)
        
        #盤面4
        if len(player.is_played) > 3 and player.is_played[3].is_used == False:
            #Blocking の数数えてあればそいつだけ追加, なければ敵盤面あるカード全部と敵
            blocking_sum = 0
            for i in range(len(player.enemy.is_played)):
                #print(player.enemy.is_played[i])
                if player.enemy.is_played[i].isBlocking:
                    #print("Blockingあるぞ")
                    blocking_sum += 1
            #print("blocking_sum")
            #print(blocking_sum)
            if blocking_sum > 0:
                for i in range(len(player.enemy.is_played)):
                    if player.enemy.is_played[i].isBlocking:
                        valid_moves.append(i+27)
            else:
                valid_moves.append(32)
                for i in range(len(player.enemy.is_played)):
                    valid_moves.append(i+27)

        #盤面5
        if len(player.is_played) > 4 and player.is_played[4].is_used == False:
            #Blocking の数数えてあればそいつだけ追加, なければ敵盤面あるカード全部と敵
            blocking_sum = 0
            for i in range(len(player.enemy.is_played)):
                #print(player.enemy.is_played[i])
                if player.enemy.is_played[i].isBlocking:
                    #print("Blockingあるぞ")
                    blocking_sum += 1
            #print("blocking_sum")
            #print(blocking_sum)
            if blocking_sum > 0:
                for i in range(len(player.enemy.is_played)):
                    if player.enemy.is_played[i].isBlocking:
                        valid_moves.append(i+33)
            else:
                valid_moves.append(38)
                for i in range(len(player.enemy.is_played)):
                    valid_moves.append(i+33)

        #turn end
        valid_moves.append(39)

        #print("valid_moves")
        #print(valid_moves)
        return valid_moves


    def do_action(self,action):
        #action 0~8 は　自手札0~8を盤面に出す操作
        if action >= 0 and action <= 8:
            draw_card_num = action
            #action番目のカードをDraw
            if action+1 > len(self.hand):
                pass
                #print("出せる手札がありません")
            else:
                self.hand[draw_card_num].is_see = True
                play_card = self.hand.pop(draw_card_num)
                #decrease cost
                self.cost -= play_card.cost
                #record dict
                if self.play_count_dict[play_card.id] == 0:
                    self.play_count_dict[play_card.id] += 1
                #playercost
                #print(self.name + "残りcost" + str(self.cost))
                #自分の盤面カードリストに追加
                self.is_played.append(play_card)
                #print(self.name + "は" + play_card + "を場に出した")
                #盤面の枚数制限超えてたら最後に追加したカード削除
                if len(self.is_played) > self.is_played_maxnum:
                    eliminated_card = self.is_played.pop(-1)
                    self.discard.append(eliminated_card)
                #カードをactivateさせる
                play_card.activate(self)
        
        
        #action 9~14は自カード1の攻撃
        elif action >= 9 and action <= 14:
            action -= 9
            enemy_num = action
            #action = 0~4 attack enemycard
            if action != 5:
                if len(self.enemy.is_played) > enemy_num and len(self.is_played) > 0:
                    #自分カード0が敵0攻撃
                    if self.is_played[0].is_used == False:
                        self.is_played[0].use(self.enemy.is_played[enemy_num])
                    else:
                        pass
                        #print("味方のカード1はすでに行動済みです")
                else:
                    pass
            #action = 5 attack enemy
            else:
                self.enemy.damage(self.is_played[0].attack)
                self.is_played[0].is_used = True
        
        #action 15~20は自カード2の攻撃
        elif action >= 15 and action <= 20:
            action -= 15
            enemy_num = action
            #action = 0~4 attack enemycard
            if action != 5:
                if len(self.enemy.is_played) > enemy_num and len(self.is_played) > 1:
                    #自分カード1が敵0攻撃
                    if self.is_played[1].is_used == False:
                        self.is_played[1].use(self.enemy.is_played[enemy_num])
                    else:
                        pass
                        #print("味方のカード1はすでに行動済みです")
                else:
                    pass
            #action = 5 attack enemy
            else:
                self.enemy.damage(self.is_played[1].attack)
                self.is_played[1].is_used = True
            
        #action 21~26は自カード3の攻撃
        elif action >= 21 and action <= 26:
            action -= 21
            enemy_num = action
            #action = 0~4 attack enemycard
            if action != 5:
                if len(self.enemy.is_played) > enemy_num and len(self.is_played) > 2:
                    #自分カード2が敵0攻撃
                    if self.is_played[2].is_used == False:
                        self.is_played[2].use(self.enemy.is_played[enemy_num])
                    else:
                        pass
                        #print("味方のカード1はすでに行動済みです")
                else:
                    pass
            #action = 5 attack enemy
            else:
                self.enemy.damage(self.is_played[2].attack)
                self.is_played[2].is_used = True
        
        #action 27~32は自カード4の攻撃
        elif action >= 27 and action <= 32:
            action -= 27
            enemy_num = action
            #action = 0~4 attack enemycard
            if action != 5:
                if len(self.enemy.is_played) > enemy_num and len(self.is_played) > 3:
                    #自分カード3が敵0攻撃
                    if self.is_played[3].is_used == False:
                        self.is_played[3].use(self.enemy.is_played[enemy_num])
                    else:
                        pass
                        #print("味方のカード1はすでに行動済みです")
                else:
                    pass
            #action = 5 attack enemy
            else:
                self.enemy.damage(self.is_played[3].attack)
                self.is_played[3].is_used = True
            
        #action 33~38は自カード4の攻撃
        elif action >= 33 and action <= 38:
            action -= 33
            enemy_num = action
            #action = 0~4 attack enemycard
            if action != 5:
                if len(self.enemy.is_played) > enemy_num and len(self.is_played) > 4:
                    #自分カード1が敵0攻撃
                    if self.is_played[4].is_used == False:
                        self.is_played[4].use(self.enemy.is_played[enemy_num])
                    else:
                        pass
                        #print("味方のカード1はすでに行動済みです")
                else:
                    pass
            #action = 5 attack enemy
            else:
                self.enemy.damage(self.is_played[4].attack)
                self.is_played[4].is_used = True
        
        elif action == 39:
            #自分のコスト更新
            self.updatecost()
    
    def take_action(self):
        valid_actions = self.get_valid_moves()
        if len(valid_actions) == 0:
            #print(self.observation)
            print("cant execute")
            pass
        #print("valid_moves")
        #print(valid_actions)
        action = random.randint(0, len(valid_actions) - 1)
        #print("selected_action")
        #print(valid_actions[action])
        self.do_action(valid_actions[action])
        return valid_actions[action]

    def generate_dict(self):
        self.play_count_dict = {card.id : 0 for card in self.deck}
        #print(self.play_count_dict)
    
    def get_record(self):
        self.play_count_dict = sorted(self.play_count_dict.items())
        return self.play_count_dict
    
    def generate_dict_draw(self):
        self.draw_count_dict = {card.id : 0 for card in self.deck}
    
    def get_draw_record(self):
        self.draw_count_dict = sorted(self.draw_count_dict.items())
        return self.draw_count_dict
        

    def showDeck(self):
        for deckcard in self.deck:
            print(deckcard)