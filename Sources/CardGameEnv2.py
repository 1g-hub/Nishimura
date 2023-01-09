import gym
from gym import spaces
import player2
import deck
import card
import run
import numpy as np


class CardGameEnv2:
    def __init__(self):
        self.curr_step = -1
        self.previous_action = 100
        #first or second
        self.isfirstAttack = True
        #手札を自盤面に出す・・・0~8
        #手札1が敵カード12345攻撃or敵・・・9~14
        #手札2・・・15~20
        #手札3・・・21~26
        #手札4・・・27~32
        #手札5・・・33~38
        #turnend ・・・ 39
        self.action_space = spaces.Discrete(40)
        """
        self.observation_space = spaces.Dict({
            "MyHand1Attack" :
            "MyHand1HP" : 
            "MyHand2Attack" :
            "MyHand2HP" :
            "MyHand3Attack" :
            "MyHand3HP" : 
            "MyHand4Attack" :
            "MyHand4HP" : 
            "MyHand5Attack" :
            "MyHand5HP" : 
            "MyHand6Attack" :
            "MyHand6HP" :
            "MyHand7Attack" :
            "MyHand7HP" : 
            "MyHand8Attack" :
            "MyHand8HP" : 
            "MyHand9Attack" :
            "MyHand9HP" :  
            "MyCard1Attack": spaces.Discrete(5),#0~4
            "MyCard1HP" : spaces.Discrete(5),
            "MyCard2Attack": spaces.Discrete(5),
            "MyCard2HP" : spaces.Discrete(5),
            "MyCard3Attack": spaces.Discrete(5),
            "MyCard3HP" : spaces.Discrete(5),
            "MyCard4Attack": spaces.Discrete(5),
            "MyCard4HP" : spaces.Discrete(5),
            "MyCard5Attack": spaces.Discrete(5),
            "MyCard5HP" : spaces.Discrete(5),
            "EnemyCard1Attack" : spaces.Discrete(5),
            "EnemyCard1HP" : spaces.Discrete(5),
            "EnemyCard2Attack" : spaces.Discrete(5),
            "EnemyCard2HP" : spaces.Discrete(5),
            "EnemyCard3Attack" : spaces.Discrete(5),
            "EnemyCard3HP" : spaces.Discrete(5),
            "EnemyCard4Attack" : spaces.Discrete(5),
            "EnemyCard4HP" : spaces.Discrete(5),
            "EnemyCard5Attack" : spaces.Discrete(5),
            "EnemyCard5HP" : spaces.Discrete(5),
            "MyCard1CanAttack": spaces.Discrete(2),#True or False
            "MyCard2CanAttack": spaces.Discrete(2),
            "MyCard3CanAttack": spaces.Discrete(2),
            "MyCard4CanAttack": spaces.Discrete(2),
            "MyCard5CanAttack": spaces.Discrete(2),
        })
        
        #dict型むりそう；；

        """
        #これで行けなかったら終わり
        LOW = np.array([
                        #自分のHP,コスト
                        0,0,
                        #敵のHP,コスト
                        0,0,
                        #手札1~9のカードのAttackとHPとコストとeffectnum
                        0,0,0,0,
                        0,0,0,0,
                        0,0,0,0,
                        0,0,0,0,
                        0,0,0,0,
                        0,0,0,0,
                        0,0,0,0,
                        0,0,0,0,
                        0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,#自盤面1~5のAtackとHP
                        0,0,0,0,0,0,0,0,0,0,#敵盤面1~5のAtackとHP
                        0,0,0,0,0,#自盤面1~5のcanAttack
                        0,0#decknum
                        ])
        HIGH = np.array([
                        #自分のHP,コスト
                        20,5,
                        #敵のHP,コスト
                        20,5,
                        #手札1~9のカードのAttackとHPとコストとeffectnum
                        5,5,5,6,
                        5,5,5,6,
                        5,5,5,6,
                        5,5,5,6,
                        5,5,5,6,
                        5,5,5,6,
                        5,5,5,6,
                        5,5,5,6,
                        5,5,5,6,
                        5,5,5,5,5,5,5,5,5,5,#自盤面1~5のAtackとHP
                        5,5,5,5,5,5,5,5,5,5,#敵盤面1~5のAtackとHP
                        1,1,1,1,1,#自盤面1~5のcanAttack
                        30,30#decknum
                        ])
        self.observation_space = spaces.Box(low=LOW,high=HIGH)

        self.action_record = { i : 0 for i in range(self.action_space.n)}
        self.action_record_total = { i : 0 for i in range(self.action_space.n)}
        self.action_record_win = {i : 0 for i in range(self.action_space.n)}
        self.action_record_tmp = {i : 0 for i in range(self.action_space.n)}
        self.card_record_total = {i : 0 for i in range(15)}
        self.card_record_win = {i : 0 for i in range(15)}
        self.card_record_tmp = {i : 0 for i in range(15)}
        self.curr_episode = -1
        self.already_selected_actions=[]
        self.isGameEnd = False
        self.reset()

    def setup_game(self):
        self.player = player2.Player2()
        player = self.player

        run.initdecks(self.player)

        run.inithands(self.player)

        #3枚ずつ場に出しとく
        #self.player.playcard()
        #self.player.playcard()
        #self.player.playcard()
        #self.player.enemy.playcard()
        #self.player.enemy.playcard()
        #self.player.enemy.playcard()

        if not self.isfirstAttack:
            #敵1turn
            #敵をランダムに行動させる
            #player.enemy.draw()
            #player.enemy.draw()
            log = player.enemy.playcard()
            log += player.enemy.usecard()
            self.updatecost(player.enemy)
            player.draw()



        self.reset_use(self.player)
        self.reset_use(self.player.enemy)
        self.reset_see(self.player)
        self.reset_see(self.player.enemy)


    def reset(self):
        
        self.setup_game()
        self.isGameEnd = False
        player = self.player
        #action 回数記録用
        self.action_record = { i : 0 for i in range(self.action_space.n)}
        self.action_record_tmp = {i : 0 for i in range(self.action_space.n)}
        #card記録用
        self.card_record_tmp = {i : 0 for i in range(15)}
        self.action_episode_memory=[]
        self.previous_action = 100
        
        #初期状態
        '''
        s = {
            "MyHand1Attack" : player.hand[0].attack if 0 < len(player.hand) else 0,
            "MyHand1HP" : player.hand[0].hp if 0 < len(player.hand) else 0,
            "MyHand2Attack" : player.hand[1].attack if 1 < len(player.hand) else 0,
            "MyHand2HP" : player.hand[1].hp if 1 < len(player.hand) else 0,
            "MyHand3Attack" : player.hand[2].attack if 2 < len(player.hand) else 0,
            "MyHand3HP" : player.hand[2].hp if 2 < len(player.hand) else 0,
            "MyHand4Attack" : player.hand[3].attack if 3 < len(player.hand) else 0,
            "MyHand4HP" : player.hand[3].hp if 3 < len(player.hand) else 0,
            "MyHand5Attack" : player.hand[4].attack if 4 < len(player.hand) else 0,
            "MyHand5HP" : player.hand[4].hp if 4 < len(player.hand) else 0,
            "MyHand6Attack" : player.hand[5].attack if 5 < len(player.hand) else 0,
            "MyHand6HP" : player.hand[5].hp if 5 < len(player.hand) else 0,
            "MyHand7Attack" : player.hand[6].attack if 6 < len(player.hand) else 0,
            "MyHand7HP" : player.hand[6].hp if 6 < len(player.hand) else 0,
            "MyHand8Attack" : player.hand[7].attack if 7 < len(player.hand) else 0,
            "MyHand8HP" : player.hand[7].hp if 7 < len(player.hand) else 0,
            "MyHand9Attack" : player.hand[8].attack if 8 < len(player.hand) else 0,
            "MyHand9HP" : player.hand[8].hp if 8 < len(player.hand) else 0,
            "MyCard1Attack": player.is_played[0].attack if 0 < len(player.is_played) else 0,
            "MyCard1HP" : player.is_played[0].hp if 0 < len(player.is_played) else 0,
            "MyCard2Attack": player.is_played[1].attack if 1 < len(player.is_played) else 0,
            "MyCard2HP" : player.is_played[1].hp if 1 < len(player.is_played) else 0,
            "MyCard3Attack": player.is_played[2].attack if 2 < len(player.is_played) else 0,
            "MyCard3HP" : player.is_played[2].hp if 2 < len(player.is_played) else 0,
            "MyCard4Attack": player.is_played[3].attack if 3 < len(player.is_played) else 0,
            "MyCard4HP" : player.is_played[3].hp if 3 < len(player.is_played) else 0,
            "MyCard5Attack": player.is_played[4].attack if 4 < len(player.is_played) else 0,
            "MyCard5HP" : player.is_played[4].hp if 4 < len(player.is_played) else 0,
            "EnemyCard1Attack" : player.enemy.is_played[0].attack if 0 < len(player.enemy.is_played) else 0,
            "EnemyCard1HP" : player.enemy.is_played[0].hp if 0 < len(player.enemy.is_played) else 0,
            "EnemyCard2Attack" : player.enemy.is_played[1].attack if 1 < len(player.enemy.is_played) else 0,
            "EnemyCard2HP" : player.enemy.is_played[1].hp if 1 < len(player.enemy.is_played) else 0,
            "EnemyCard3Attack" : player.enemy.is_played[2].attack if 2 < len(player.enemy.is_played) else 0,
            "EnemyCard3HP" : player.enemy.is_played[2].hp if 2 < len(player.enemy.is_played) else 0,
            "EnemyCard4Attack" : player.enemy.is_played[3].attack if 3 < len(player.enemy.is_played) else 0,
            "EnemyCard4HP" : player.enemy.is_played[3].hp if 3 < len(player.enemy.is_played) else 0,
            "EnemyCard5Attack" : player.enemy.is_played[4].attack if 4 < len(player.enemy.is_played) else 0,
            "EnemyCard5HP" : player.enemy.is_played[4].hp if 4 < len(player.enemy.is_played) else 0,
            "MyCard1CanAttack": 1 if 0 < len(player.is_played) and not player.is_played[0].is_used else 0,
            "MyCard2CanAttack": 1 if 1 < len(player.is_played) and not player.is_played[1].is_used else 0,
            "MyCard3CanAttack": 1 if 2 < len(player.is_played) and not player.is_played[2].is_used else 0,
            "MyCard4CanAttack": 1 if 3 < len(player.is_played) and not player.is_played[3].is_used else 0,
            "MyCard5CanAttack": 1 if 4 < len(player.is_played) and not player.is_played[4].is_used else 0,
            "MyDeckNum": len(player.deck),
            "EnemyDeckNum" : len(player.enemy.deck)
        }
        
        '''
        s = [
            player.hp,
            player.cost,
            player.enemy.hp,
            player.enemy.cost,
            player.hand[0].attack if 0 < len(player.hand) else 0,
            player.hand[0].hp if 0 < len(player.hand) else 0,
            player.hand[0].cost if 0 < len(player.hand) else 0,
            player.hand[0].effectnum if 0 < len(player.hand) else 0,
            player.hand[1].attack if 1 < len(player.hand) else 0,
            player.hand[1].hp if 1 < len(player.hand) else 0,
            player.hand[1].cost if 1 < len(player.hand) else 0,
            player.hand[1].effectnum if 1 < len(player.hand) else 0,
            player.hand[2].attack if 2 < len(player.hand) else 0,
            player.hand[2].hp if 2 < len(player.hand) else 0,
            player.hand[2].cost if 2 < len(player.hand) else 0,
            player.hand[2].effectnum if 2 < len(player.hand) else 0,
            player.hand[3].attack if 3 < len(player.hand) else 0,
            player.hand[3].hp if 3 < len(player.hand) else 0,
            player.hand[3].cost if 3 < len(player.hand) else 0,
            player.hand[3].effectnum if 3 < len(player.hand) else 0,
            player.hand[4].attack if 4 < len(player.hand) else 0,
            player.hand[4].hp if 4 < len(player.hand) else 0,
            player.hand[4].cost if 4 < len(player.hand) else 0,
            player.hand[4].effectnum if 4 < len(player.hand) else 0,
            player.hand[5].attack if 5 < len(player.hand) else 0,
            player.hand[5].hp if 5 < len(player.hand) else 0,
            player.hand[5].cost if 5 < len(player.hand) else 0,
            player.hand[5].effectnum if 5 < len(player.hand) else 0,
            player.hand[6].attack if 6 < len(player.hand) else 0,
            player.hand[6].hp if 6 < len(player.hand) else 0,
            player.hand[6].cost if 6 < len(player.hand) else 0,
            player.hand[6].effectnum if 6 < len(player.hand) else 0,
            player.hand[7].attack if 7 < len(player.hand) else 0,
            player.hand[7].hp if 7 < len(player.hand) else 0,
            player.hand[7].cost if 7 < len(player.hand) else 0,
            player.hand[7].effectnum if 7 < len(player.hand) else 0,
            player.hand[8].attack if 8 < len(player.hand) else 0,
            player.hand[8].hp if 8 < len(player.hand) else 0,
            player.hand[8].cost if 8 < len(player.hand) else 0,
            player.hand[8].effectnum if 8 < len(player.hand) else 0,
            player.is_played[0].attack if 0 < len(player.is_played) else 0,
            player.is_played[0].hp if 0 < len(player.is_played) else 0,
            player.is_played[1].attack if 1 < len(player.is_played) else 0,
            player.is_played[1].hp if 1 < len(player.is_played) else 0,
            player.is_played[2].attack if 2 < len(player.is_played) else 0,
            player.is_played[2].hp if 2 < len(player.is_played) else 0,
            player.is_played[3].attack if 3 < len(player.is_played) else 0,
            player.is_played[3].hp if 3 < len(player.is_played) else 0,
            player.is_played[4].attack if 4 < len(player.is_played) else 0,
            player.is_played[4].hp if 4 < len(player.is_played) else 0,
            player.enemy.is_played[0].attack if 0 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[0].hp if 0 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[1].attack if 1 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[1].hp if 1 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[2].attack if 2 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[2].hp if 2 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[3].attack if 3 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[3].hp if 3 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[4].attack if 4 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[4].hp if 4 < len(player.enemy.is_played) else 0,
            1 if 0 < len(player.is_played) and not player.is_played[0].is_used else 0,
            1 if 1 < len(player.is_played) and not player.is_played[1].is_used else 0,
            1 if 2 < len(player.is_played) and not player.is_played[2].is_used else 0,
            1 if 3 < len(player.is_played) and not player.is_played[3].is_used else 0,
            1 if 4 < len(player.is_played) and not player.is_played[4].is_used else 0,
            len(player.deck),
            len(player.enemy.deck)
        ]
        self.observation = s

        #print("RESET STATE")
        #print(self.observation)
        #print("state.shape" + s.shape)

        return s
    
    def step(self,action):
        done = False
        self.reward = 0.0
        player = self.player
        
        attack_sum = 0
        for i in player.is_played:
            if i.is_used == False:
                attack_sum += i.attack
        #print("attacknum")
        #print(attack_sum)
        
        #print("action")
        #print(self.action_episode_memory)

        #reward設定用is_playedの個数の和
        is_used_sum = 0
        for i in player.is_played:
            if i.is_used == False:
                is_used_sum += 1
        
    

        #行動を行う
        if self.isGameEnd == False:
            self.take_action(action)
        
        #print("observation")
        #print(self.get_state())
                                        
        #ステップごとに終了条件満たしてるか判定
        if player.is_dead or player.is_deckend or player.enemy.is_dead or player.enemy.is_deckend:
            self.isGameEnd = True


        #print("action")
        #print(self.action_episode_memory)

        
        #print("previous_action, now_action")
        #print(self.previous_action, self.now_action)
        done = self.get_done()
        reward = self.get_reward()
        self.observation = self.get_state()

        #action record 表示
        if done:
            for i in range(self.action_space.n):
                self.action_record_total[i] += self.action_record[i]
            
            action_record_total = sorted(self.action_record_total.items(), key=lambda x:x[1], reverse=True)
            #print("action_record_total")
            #print(action_record_total)


        if done and reward == 1.0:
            for i in range(self.action_space.n):
                self.action_record_win[i] += self.action_record_tmp[i]
            action_record_win = sorted(self.action_record_win.items(), key=lambda x:x[1], reverse=True)
            #print("action_record_win")
            #print(action_record_win)
            
        #card record 表示
        if done:
            for i in range(15):
                self.card_record_total[i] += self.card_record_tmp[i]
            
            card_record_total = sorted(self.card_record_total.items(), key=lambda x:x[1], reverse=True)
            #print("card_record_total")
            #print(card_record_total)

        if done and reward == 1.0:
            for i in range(15):
                self.card_record_win[i] += self.card_record_tmp[i]
            
            card_record_win = sorted(self.card_record_win.items(), key=lambda x:x[1], reverse=True)
            #print("card_record_win")
            #print(card_record_win)


        #記録
        self.curr_step += 1
        #print("state")
        #print(self.observation)
        self.previous_action = self.now_action
        

        return self.observation,reward,done,{}

    # 場に出ているis_usedの数を数える
    def get_sum_of_isused(self):
        sum = 0
        if len(self.player.is_played) > 0:
            for i in self.player.is_played:
                if i.is_used == False:
                    sum += 1
        return sum

    # 手札のis_seeの数を数える
    def get_sum_of_issee(self):
        sum = 0
        if len(self.player.hand) > 0: 
            for i in self.player.hand:
                if i.is_see == False:
                    sum += 1
        return sum

    #カードのis_used状態をリセット（ターン処理で呼ばれる)
    def reset_use(self,player):
        for played_card in player.is_played:
                played_card.is_used = False
    
    #カードのis_see状態をリセット(ターン処理で呼ばれる)
    def reset_see(self,player):
        for see_card in player.hand:
            see_card.is_see = False
    

    #プレイヤーのコストUpdate処理 (ターン処理で呼ばれる)
    def updatecost(self,player):
        if player.turnmaxcost < player.maxcost:
            player.turnmaxcost += 1
        player.cost = player.turnmaxcost
        #print("updated cost")
        #print(player.name + ":" + str(player.cost))
    
    #報酬を返す
    def get_reward(self):

        player = self.player
        reward = self.reward


        #finishした時に報酬渡す
        if self.get_done():
            #player win
            if player.enemy.is_dead == True:
                reward = 1.0
            elif player.enemy.is_deckend == True:
                reward = 1.0
            #enemy win
            elif player.is_deckend == True:
                reward = -1.0
            elif player.is_dead == True:
                reward = -1.0
        
        self.reward = reward
        return reward

    #finish条件 
    def get_done(self):
        if self.isGameEnd == True:
            return True
        else:
            return False

    #状態を返す
    def get_state(self):

        player = self.player

        s = [
            player.hp,
            player.cost,
            player.enemy.hp,
            player.enemy.cost,
            player.hand[0].attack if 0 < len(player.hand) else 0,
            player.hand[0].hp if 0 < len(player.hand) else 0,
            player.hand[0].cost if 0 < len(player.hand) else 0,
            player.hand[0].effectnum if 0 < len(player.hand) else 0,
            player.hand[1].attack if 1 < len(player.hand) else 0,
            player.hand[1].hp if 1 < len(player.hand) else 0,
            player.hand[1].cost if 1 < len(player.hand) else 0,
            player.hand[1].effectnum if 1 < len(player.hand) else 0,
            player.hand[2].attack if 2 < len(player.hand) else 0,
            player.hand[2].hp if 2 < len(player.hand) else 0,
            player.hand[2].cost if 2 < len(player.hand) else 0,
            player.hand[2].effectnum if 2 < len(player.hand) else 0,
            player.hand[3].attack if 3 < len(player.hand) else 0,
            player.hand[3].hp if 3 < len(player.hand) else 0,
            player.hand[3].cost if 3 < len(player.hand) else 0,
            player.hand[3].effectnum if 3 < len(player.hand) else 0,
            player.hand[4].attack if 4 < len(player.hand) else 0,
            player.hand[4].hp if 4 < len(player.hand) else 0,
            player.hand[4].cost if 4 < len(player.hand) else 0,
            player.hand[4].effectnum if 4 < len(player.hand) else 0,
            player.hand[5].attack if 5 < len(player.hand) else 0,
            player.hand[5].hp if 5 < len(player.hand) else 0,
            player.hand[5].cost if 5 < len(player.hand) else 0,
            player.hand[5].effectnum if 5 < len(player.hand) else 0,
            player.hand[6].attack if 6 < len(player.hand) else 0,
            player.hand[6].hp if 6 < len(player.hand) else 0,
            player.hand[6].cost if 6 < len(player.hand) else 0,
            player.hand[6].effectnum if 6 < len(player.hand) else 0,
            player.hand[7].attack if 7 < len(player.hand) else 0,
            player.hand[7].hp if 7 < len(player.hand) else 0,
            player.hand[7].cost if 7 < len(player.hand) else 0,
            player.hand[7].effectnum if 7 < len(player.hand) else 0,
            player.hand[8].attack if 8 < len(player.hand) else 0,
            player.hand[8].hp if 8 < len(player.hand) else 0,
            player.hand[8].cost if 8 < len(player.hand) else 0,
            player.hand[8].effectnum if 8 < len(player.hand) else 0,
            player.is_played[0].attack if 0 < len(player.is_played) else 0,
            player.is_played[0].hp if 0 < len(player.is_played) else 0,
            player.is_played[1].attack if 1 < len(player.is_played) else 0,
            player.is_played[1].hp if 1 < len(player.is_played) else 0,
            player.is_played[2].attack if 2 < len(player.is_played) else 0,
            player.is_played[2].hp if 2 < len(player.is_played) else 0,
            player.is_played[3].attack if 3 < len(player.is_played) else 0,
            player.is_played[3].hp if 3 < len(player.is_played) else 0,
            player.is_played[4].attack if 4 < len(player.is_played) else 0,
            player.is_played[4].hp if 4 < len(player.is_played) else 0,
            player.enemy.is_played[0].attack if 0 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[0].hp if 0 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[1].attack if 1 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[1].hp if 1 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[2].attack if 2 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[2].hp if 2 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[3].attack if 3 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[3].hp if 3 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[4].attack if 4 < len(player.enemy.is_played) else 0,
            player.enemy.is_played[4].hp if 4 < len(player.enemy.is_played) else 0,
            1 if 0 < len(player.is_played) and not player.is_played[0].is_used else 0,
            1 if 1 < len(player.is_played) and not player.is_played[1].is_used else 0,
            1 if 2 < len(player.is_played) and not player.is_played[2].is_used else 0,
            1 if 3 < len(player.is_played) and not player.is_played[3].is_used else 0,
            1 if 4 < len(player.is_played) and not player.is_played[4].is_used else 0,
            len(player.deck),
            len(player.enemy.deck)
        ]
        return s
    
    def close(self):
        # 環境を閉じて，後処理をする
        pass

    def seed(self, seed=None):
        # ランダムシードを固定する
        pass

    def render(self, mode='human', close=False):
        # 環境を可視化する
        # human の場合はコンソールに出力．ansi の場合は StringIO を返す
        pass

    def state_to_env(self):
        state = self.observation

    def do_action(self,action):
        player = self.player
        #action 0~8 は　自手札0~8を盤面に出す操作
        if action >= 0 and action <= 8:
            draw_card_num = action
            #盤面表示
            #player.enemy.printisplayed()
            #player.printisplayed()
            #player.printhand()
            #action番目のカードをDraw
            if action+1 > len(player.hand):
                pass
                #print("出せる手札がありません")
            else:
                player.hand[draw_card_num].is_see = True
                play_card = player.hand.pop(draw_card_num)
                #decrease cost
                player.cost -= play_card.cost
                #playercost
                #print("player 残りcost" + str(player.cost))
                #自分の盤面カードリストに追加
                player.is_played.append(play_card)
                #print(player.name + "は" + play_card + "を場に出した")
                #盤面の枚数制限超えてたら最後に追加したカード削除
                if len(player.is_played) > player.is_played_maxnum:
                    eliminated_card = player.is_played.pop(-1)
                    player.discard.append(eliminated_card)
                #カードをactivateさせる
                play_card.activate(player)
                #card record 追加
                self.card_record_tmp[play_card.id] += 1
        
        #action 9~17は自手札0~8を盤面に出さない
        #elif action >= 9 and action <= 17:
        #    #rint("カード出しません")
        #    draw_card_num = action - 9
        #    #print(player.hand[draw_card_num])
        #    #print(player.hand[draw_card_num].is_see)
        #    player.hand[draw_card_num].is_see = True
        #    #print(player.hand[draw_card_num])
        #   #print(player.hand[draw_card_num].is_see)
    
        
        #action 9~14は自カード1の攻撃
        elif action >= 9 and action <= 14:
            action -= 9
            enemy_num = action
            #action = 0~4 attack enemycard
            if action != 5:
                if len(player.enemy.is_played) > enemy_num and len(player.is_played) > 0:
                    #自分カード0が敵0攻撃
                    if player.is_played[0].is_used == False:
                        player.is_played[0].use(player.enemy.is_played[enemy_num])
                    else:
                        pass
                        #print("味方のカード1はすでに行動済みです")
                else:
                    pass
            #action = 5 attack enemy
            else:
                player.enemy.damage(player.is_played[0].attack)
                player.is_played[0].is_used = True
        
        #action 15~20は自カード2の攻撃
        elif action >= 15 and action <= 20:
            action -= 15
            enemy_num = action
            #action = 0~4 attack enemycard
            if action != 5:
                if len(player.enemy.is_played) > enemy_num and len(player.is_played) > 1:
                    #自分カード1が敵0攻撃
                    if player.is_played[1].is_used == False:
                        player.is_played[1].use(player.enemy.is_played[enemy_num])
                    else:
                        pass
                        #print("味方のカード1はすでに行動済みです")
                else:
                    pass
            #action = 5 attack enemy
            else:
                player.enemy.damage(player.is_played[1].attack)
                player.is_played[1].is_used = True
            
        #action 21~26は自カード3の攻撃
        elif action >= 21 and action <= 26:
            action -= 21
            enemy_num = action
            #action = 0~4 attack enemycard
            if action != 5:
                if len(player.enemy.is_played) > enemy_num and len(player.is_played) > 2:
                    #自分カード2が敵0攻撃
                    if player.is_played[2].is_used == False:
                        player.is_played[2].use(player.enemy.is_played[enemy_num])
                    else:
                        pass
                        #print("味方のカード1はすでに行動済みです")
                else:
                    pass
            #action = 5 attack enemy
            else:
                player.enemy.damage(player.is_played[2].attack)
                player.is_played[2].is_used = True
        
        #action 27~32は自カード4の攻撃
        elif action >= 27 and action <= 32:
            action -= 27
            enemy_num = action
            #action = 0~4 attack enemycard
            if action != 5:
                if len(player.enemy.is_played) > enemy_num and len(player.is_played) > 3:
                    #自分カード3が敵0攻撃
                    if player.is_played[3].is_used == False:
                        player.is_played[3].use(player.enemy.is_played[enemy_num])
                    else:
                        pass
                        #print("味方のカード1はすでに行動済みです")
                else:
                    pass
            #action = 5 attack enemy
            else:
                player.enemy.damage(player.is_played[3].attack)
                player.is_played[3].is_used = True
            
        #action 33~38は自カード4の攻撃
        elif action >= 33 and action <= 38:
            action -= 33
            enemy_num = action
            #action = 0~4 attack enemycard
            if action != 5:
                if len(player.enemy.is_played) > enemy_num and len(player.is_played) > 4:
                    #自分カード1が敵0攻撃
                    if player.is_played[4].is_used == False:
                        player.is_played[4].use(player.enemy.is_played[enemy_num])
                    else:
                        pass
                        #print("味方のカード1はすでに行動済みです")
                else:
                    pass
            #action = 5 attack enemy
            else:
                player.enemy.damage(player.is_played[4].attack)
                player.is_played[4].is_used = True
        
        elif action == 39:
            #自分のコスト更新
            self.updatecost(self.player)
            #print("-------------------------------------------------------------------------------------------------")
            #print("Enemy Player Turn")
            #敵が死んでなければランダムに行動させる
            if not player.enemy.is_dead:
                player.enemy.draw()
                if player.enemy.is_deckend:
                    #print(player.enemy.name + "のデッキ切れです")
                    self.isGameEnd = True
                else:
                    #print("enemy draw")
                    #player.enemy.draw()
                    log = player.enemy.playcard()
                    #log = player.enemy.playcard()
                    log += player.enemy.usecard()
                if player.is_dead:
                    self.isGameEnd = True
            #敵のコスト更新
            self.updatecost(self.player.enemy)
            #カードリセット
            self.reset_use(self.player)
            self.reset_use(self.player.enemy)
            self.reset_see(self.player)
            self.reset_see(self.player.enemy)
            #print("-------------------------------------------------------------------------------------------------")
            #print("First Player Turn")
            #プレイヤーが死んでなければドロー
            #プレイヤー一枚ドロー
            if not player.is_dead:
                player.draw()
                if player.is_deckend:
                    #print(player.name + "のデッキ切れです")
                    self.isGameEnd = True

        else:
            print(action)
            print("未定義のActionです")                                        
            print(self.get_state())  

    #盤面から使える行動を選んでvalid_movesに追加、それをreturn 
    def get_valid_moves(self):
        player = self.player
        valid_moves = []
        #手札
        for i in range(len(player.hand)):
            if player.hand[i].is_see == False:
                #valid_moves.append(i+9)
                if player.hand[i].cost <= player.cost:
                    valid_moves.append(i)

        #盤面1
        if len(player.is_played) > 0 and player.is_played[0].is_used == False:
            valid_moves.append(14)
            for i in range(len(player.enemy.is_played)):
                valid_moves.append(i+9)
        
        #盤面2
        if len(player.is_played) > 1 and player.is_played[1].is_used == False:
            valid_moves.append(20)
            for i in range(len(player.enemy.is_played)):
                valid_moves.append(i+15)
        
        #盤面3
        if len(player.is_played) > 2 and player.is_played[2].is_used == False:
            valid_moves.append(26)
            for i in range(len(player.enemy.is_played)):
                valid_moves.append(i+21)
        
        #盤面4
        if len(player.is_played) > 3 and player.is_played[3].is_used == False:
            valid_moves.append(32)
            for i in range(len(player.enemy.is_played)):
                valid_moves.append(i+27)

        #盤面5
        if len(player.is_played) > 4 and player.is_played[4].is_used == False:
            valid_moves.append(38)
            for i in range(len(player.enemy.is_played)):
                valid_moves.append(i+33)

        #turn end
        valid_moves.append(39)

        #print("valid_moves")
        #print(valid_moves)
        return valid_moves

    def take_action(self,action):
        player = self.player
        valid_actions = self.get_valid_moves()
        if len(valid_actions) == 0:
            #print(self.observation)
            print("cant execute")
            pass
        #print("valid_moves")
        #print(valid_actions)
        cnt=0
        #print("already_selected_actions")
        #print(self.already_selected_actions)
        #for a in self.already_selected_actions:
        #    valid_actions.remove(a)
        while len(valid_actions)<self.action_space.n: 
            valid_actions.append(valid_actions[cnt])
            cnt=cnt+1
        self.action_episode_memory.append(valid_actions[action])
        self.now_action = valid_actions[action]
        #print("selected_action")
        #print(valid_actions[action])
        self.action_record[valid_actions[action]] += 1
        self.action_record_tmp[valid_actions[action]] += 1
        self.do_action(valid_actions[action])
        self.already_selected_actions.append(valid_actions[action])
        '''
        if self.get_sum_of_isused() == 0 and self.get_sum_of_issee() == 0:
            #自分のコスト更新
            self.updatecost(self.player)
            print("-------------------------------------------------------------------------------------------------")
            print("Enemy Player Turn")
            #敵が死んでなければランダムに行動させる
            if not player.enemy.is_dead:
                player.enemy.draw()
                if player.enemy.is_deckend:
                    #print(player.enemy.name + "のデッキ切れです")
                    self.isGameEnd = True
                else:
                    #print("enemy draw")
                    #player.enemy.draw()
                    log = player.enemy.playcard()
                    #log = player.enemy.playcard()
                    log += player.enemy.usecard()
                if player.is_dead:
                    self.isGameEnd = True
            #敵のコスト更新
            self.updatecost(self.player.enemy)
            #カードリセット
            self.reset_use(self.player)
            self.reset_use(self.player.enemy)
            self.reset_see(self.player)
            self.reset_see(self.player.enemy)
            print("-------------------------------------------------------------------------------------------------")
            print("First Player Turn")
            #プレイヤーが死んでなければドロー
            #プレイヤー一枚ドロー
            if not player.is_dead:
                player.draw()
                if player.is_deckend:
                    #print(player.name + "のデッキ切れです")
                    self.isGameEnd = True
            #print("player draw")
            #reset alreadyselectedactions
            self.already_selected_actions = []
            '''