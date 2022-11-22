import gym
from gym import spaces
import player2
import deck
import card
import run
import numpy as np


class CardGameEnv:
    def __init__(self):
        self.curr_step = -1
        self.previous_action = 100
        #手札を自盤面に出す・・・0~8
        #手札1が敵カード12345攻撃・・・9~13
        #手札2・・・14~18
        #手札3・・・19~23
        #手札4・・・24~28
        #手札5・・・29~33
        #ターンエンド・・・34
        self.action_space = spaces.Discrete(35)
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
        LOW = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,#手札1~9のカードのAttackとHP
                        0,0,0,0,0,0,0,0,0,0,#自盤面1~5のAtackとHP
                        0,0,0,0,0,0,0,0,0,0,#敵盤面1~5のAtackとHP
                        0,0,0,0,0#自盤面1~5のcanAttack
                        ])
        HIGH = np.array([20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,#手札1~9のカードのAttackとHP
                        20,20,20,20,20,20,20,20,20,20,#自盤面1~5のAtackとHP
                        20,20,20,20,20,20,20,20,20,20,#敵盤面1~5のAtackとHP
                        1,1,1,1,1#自盤面1~5のcanAttack
                        ])
        self.observation_space = spaces.Box(low=LOW,high=HIGH)


        self.curr_episode = -1
        self.already_selected_actions=[]
        self.reset()

    def setup_game(self):
        self.player = player2.Player2()

        run.initdecks(self.player)

        run.inithands(self.player)

        #3枚ずつ場に出しとく
        #self.player.playcard()
        #self.player.playcard()
        #self.player.playcard()
        #self.player.enemy.playcard()
        #self.player.enemy.playcard()
        #self.player.enemy.playcard()


        run.resetuse(self.player)
        run.resetuse(self.player.enemy)


    def reset(self):
        
        self.setup_game()

        player = self.player
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
            
        }
        
        '''
        s = [
            player.hand[0].attack if 0 < len(player.hand) else 0,
            player.hand[0].hp if 0 < len(player.hand) else 0,
            player.hand[1].attack if 1 < len(player.hand) else 0,
            player.hand[1].hp if 1 < len(player.hand) else 0,
            player.hand[2].attack if 2 < len(player.hand) else 0,
            player.hand[2].hp if 2 < len(player.hand) else 0,
            player.hand[3].attack if 3 < len(player.hand) else 0,
            player.hand[3].hp if 3 < len(player.hand) else 0,
            player.hand[4].attack if 4 < len(player.hand) else 0,
            player.hand[4].hp if 4 < len(player.hand) else 0,
            player.hand[5].attack if 5 < len(player.hand) else 0,
            player.hand[5].hp if 5 < len(player.hand) else 0,
            player.hand[6].attack if 6 < len(player.hand) else 0,
            player.hand[6].hp if 6 < len(player.hand) else 0,
            player.hand[7].attack if 7 < len(player.hand) else 0,
            player.hand[7].hp if 7 < len(player.hand) else 0,
            player.hand[8].attack if 8 < len(player.hand) else 0,
            player.hand[8].hp if 8 < len(player.hand) else 0,
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
        ]
        self.observation = s

        print("RESET STATE")
        print(self.observation)
        #print("state.shape" + s.shape)

        return s
    
    def step(self,action):
        self.play_card = False
        self.use_card = False
        self.turn_end = False
        done = False
        self.reward = 0.0
        player = self.player
        

        #OTK可能であるのに逃したら-30
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

        #reward設定用事前のenemyHP
        #before_enemyHP = player.enemy.hp

        #行動を行う
        self.take_action(action)
                                        
        #print("action")
        #print(self.action_episode_memory)

        after_is_used_sum = 0
        for i in player.is_played:
            if i.is_used == False:
                after_is_used_sum += 1

        #print("is_used_sum")
        #print(is_used_sum)
        #print("after_used_sum")
        #print(after_is_used_sum)
        
        print("previous_action, now_action")
        print(self.previous_action, self.now_action)
        reward = self.get_reward()
        done = self.get_done()
        self.observation = self.get_state()

        #記録
        self.curr_step += 1
        print("state")
        print(self.observation)
        self.previous_action = self.now_action
        

        return self.observation,reward,done,{}

    # now getused means turnend , and should fix it by using flag  
    def getused(self):
        flag = True
        if len(self.player.is_played):
            for i in self.player.is_played:
                if i.is_used == False:
                    flag = False
            return flag
        else:
            return True
    #報酬を返す
    def get_reward(self):

        player = self.player
        reward = self.reward

        if self.turn_end == True:

            if self.previous_action == 34 and self.now_action == 34:
                reward = -30
            else:
                #print("Turn end reward ")
                if len(player.is_played) > len(player.enemy.is_played):
                    reward = 1.0
                    #print("First Player WIN")
                elif len(player.is_played) < len(player.enemy.is_played):
                    reward = -1.0
                    #print("Second Player WIN")
                else:
                    first_sum = 0
                    second_sum = 0
                    for i in player.is_played:
                        first_sum += i.attack
                        first_sum += i.hp
                    for i in player.enemy.is_played:
                        second_sum += i.attack
                        second_sum += i.hp
                    if first_sum >= second_sum:
                        reward = 1.0
                        #print("First Player WIN")
                    else:
                        reward = -1.0
                        #print("Second Player WIN")

        #finish条件
        if len(player.hand) == 0 and len(player.enemy.hand) == 0 and self.turn_end == True:
            
            if self.previous_action == 34 and self.now_action == 34:
                reward = -30
            else:
                #done = True
                if len(player.is_played) > len(player.enemy.is_played):
                    reward = 10.0
                    print("First Player WIN")
                elif len(player.is_played) < len(player.enemy.is_played):
                    reward = -10.0
                    print("Second Player WIN")
                else:
                    first_sum = 0
                    second_sum = 0
                    for i in player.is_played:
                        first_sum += i.attack
                        first_sum += i.hp
                    for i in player.enemy.is_played:
                        second_sum += i.attack
                        second_sum += i.hp
                    if first_sum >= second_sum:
                        reward = 10.0
                        print("First Player WIN")
                    else:
                        reward = -10.0
                        print("Second Player WIN")

        
        self.reward = reward
        return reward
        
    def get_done(self):
        player = self.player
        #finish条件
        if len(player.hand) == 0 and len(player.enemy.hand) == 0 and self.turn_end == True:
            return True
        return False

    #状態を返す
    def get_state(self):

        player = self.player

        s = [
            player.hand[0].attack if 0 < len(player.hand) else 0,
            player.hand[0].hp if 0 < len(player.hand) else 0,
            player.hand[1].attack if 1 < len(player.hand) else 0,
            player.hand[1].hp if 1 < len(player.hand) else 0,
            player.hand[2].attack if 2 < len(player.hand) else 0,
            player.hand[2].hp if 2 < len(player.hand) else 0,
            player.hand[3].attack if 3 < len(player.hand) else 0,
            player.hand[3].hp if 3 < len(player.hand) else 0,
            player.hand[4].attack if 4 < len(player.hand) else 0,
            player.hand[4].hp if 4 < len(player.hand) else 0,
            player.hand[5].attack if 5 < len(player.hand) else 0,
            player.hand[5].hp if 5 < len(player.hand) else 0,
            player.hand[6].attack if 6 < len(player.hand) else 0,
            player.hand[6].hp if 6 < len(player.hand) else 0,
            player.hand[7].attack if 7 < len(player.hand) else 0,
            player.hand[7].hp if 7 < len(player.hand) else 0,
            player.hand[8].attack if 8 < len(player.hand) else 0,
            player.hand[8].hp if 8 < len(player.hand) else 0,
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

    '''
    #終了条件判定
    def is_done(self):
        
        player = self.player

        #プレイヤーの手札で１つでもuseしてないカードがあればplayer_flag = False
        player_flag = True
        for i in player.is_played:
            if i.is_used == False:
                player_flag = False
        
        if player_flag:
            return True
        else:
            return False
    '''
    def calculate_reward(self):
        player = self.player
        reward = 0
        #プレイヤーの残り体力
        reward += player.hp*3.0
        #print("reward")
        #print(reward)
        #味方カードの評価値
        if len(player.is_played) > 0:
            for i in player.is_played:
                #print("attack,hp")
                #print(i.attack)
                #print(i.hp)
                reward += (i.attack + i.hp)*1.0
                #print(reward)
        #敵カードの評価
        if len(player.enemy.is_played) > 0:
            for i in player.enemy.is_played:
                #print("attack,hp")
                #print(i.attack)
                #print(i.hp)
                tmp = (i.attack + i.hp)*1.5
                #print("tmp")
                #print(tmp)
                reward = reward - tmp
                #print("reward")
                #print(reward)

        #敵の残り体力
        reward -= player.enemy.hp*0.5

        #print("reward")
        #print(reward)

        #報酬のCliping
        #if reward > 0:
        #   reward = 1
        #elif reward < 0:
        #   reward = -1
        
        print("reward")
        print(reward)
        
        return reward

    def state_to_env(self):
        state = self.observation

    def do_action(self,action):
        player = self.player
        #action 0~8 は　自手札0~8を盤面に出す操作
        if action >= 0 and action <= 8:
            self.play_card = True
            #
            draw_card_num = action
            #盤面表示
            #player.enemy.printisplayed()
            #player.printisplayed()
            #player.printhand()
            #action番目のカードをDraw
            if action+1 > len(player.hand):
                print("出せる手札がありません")
            else:
                play_card = player.hand.pop(draw_card_num)
                #自分の盤面カードリストに追加
                player.is_played.append(play_card)
                #print(player.name + "は" + play_card + "を場に出した")
                #盤面の枚数制限超えてたら最後に追加したカード削除
                if len(player.is_played) > player.is_played_maxnum:
                    eliminated_card = player.is_played.pop(-1)
                    player.discard.append(eliminated_card)
                #カードをactivateさせる
                play_card.activate()
        
        #action 9~13は自カード1の攻撃
        elif action >= 9 and action <= 13:
            self.play_card = True
            action -= 9
            enemy_num = action
            if len(player.enemy.is_played) > enemy_num and len(player.is_played) > 0:
                #自分カード0が敵0攻撃
                if player.is_played[0].is_used == False:
                    player.is_played[0].use(player.enemy.is_played[enemy_num])
                else:
                    pass
                    #print("味方のカード1はすでに行動済みです")
            else:
                pass
        
        #action 14~18 は自カード2の攻撃
        elif action >= 14 and action <= 18:
            self.play_card = True
            action -= 14
            enemy_num = action
            if len(player.enemy.is_played) > enemy_num and len(player.is_played) > 1:
                #自分カード1が敵0攻撃
                if player.is_played[1].is_used == False:
                    player.is_played[1].use(player.enemy.is_played[enemy_num])
                else:
                    pass
                    #print("味方のカード1はすでに行動済みです")
            else:
                pass
        
        #action 19~23 は自カード3の攻撃
        elif action >= 19 and action <= 23:
            self.play_card = True
            action -= 19
            enemy_num = action
            if len(player.enemy.is_played) > enemy_num and len(player.is_played) > 2:
                #自分カード2が敵0攻撃
                if player.is_played[2].is_used == False:
                    player.is_played[2].use(player.enemy.is_played[enemy_num])
                else:
                    pass
                    #print("味方のカード1はすでに行動済みです")
            else:
                pass
        
        #action 24~28 は自カード4の攻撃
        elif action >= 24 and action <= 28:
            self.play_card = True
            action -= 24
            enemy_num = action
            if len(player.enemy.is_played) > enemy_num and len(player.is_played) > 3:
                #自分カード3が敵0攻撃
                if player.is_played[3].is_used == False:
                    player.is_played[3].use(player.enemy.is_played[enemy_num])
                else:
                    pass
                    #print("味方のカード1はすでに行動済みです")
            else:
                pass

        #action 29~33 は自カード5の攻撃
        elif action >= 29 and action <= 33:
            self.play_card = True
            action -= 29
            enemy_num = action
            if len(player.enemy.is_played) > enemy_num and len(player.is_played) > 4:
                #自分カード4が敵0攻撃
                if player.is_played[4].is_used == False:
                    player.is_played[4].use(player.enemy.is_played[enemy_num])
                else:
                    pass
                    #print("味方のカード1はすでに行動済みです")
            else:
                pass
        
        elif action == 34:
            self.turn_end = True

        else:
            print(action)
            print("未定義のActionです")                                        
            print(self.get_state())  

    def get_valid_moves(self):
        player = self.player
        valid_moves = []
        #手札play
        for i in range(len(player.hand)):
            valid_moves.append(i)

        #盤面1
        if len(player.is_played) > 0 and player.is_played[0].is_used == False:
            for i in range(len(player.enemy.is_played)):
                valid_moves.append(i+9)
        
        #盤面2
        if len(player.is_played) > 1 and player.is_played[1].is_used == False:
            for i in range(len(player.enemy.is_played)):
                valid_moves.append(i+14)
        
        #盤面3
        if len(player.is_played) > 2 and player.is_played[2].is_used == False:
            for i in range(len(player.enemy.is_played)):
                valid_moves.append(i+19)
        
        #盤面4
        if len(player.is_played) > 3 and player.is_played[3].is_used == False:
            for i in range(len(player.enemy.is_played)):
                valid_moves.append(i+24)

        #盤面5
        if len(player.is_played) > 4 and player.is_played[4].is_used == False:
            for i in range(len(player.enemy.is_played)):
                valid_moves.append(i+29)
        
        valid_moves.append(34)

        return valid_moves

    def take_action(self,action):
        player = self.player
        valid_actions = self.get_valid_moves()
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
        print("action")
        print(self.action_episode_memory)
        #print("selected_action")
        #print(valid_actions[action])
        #if turn end ...
        if valid_actions[action] == 34:
            #print("-------------------------------------------------------------------------------------------------")
            #print("Second Player Turn")
            #敵をランダムに行動させる
            player.enemy.draw()
            #player.enemy.draw()
            log = player.enemy.playcard()
            #log = player.enemy.playcard()
            log += player.enemy.usecard()
            #カードリセット
            run.resetuse(player)
            run.resetuse(player.enemy)
            #print("-------------------------------------------------------------------------------------------------")
            #print("First Player Turn")
            #プレイヤー一枚ドロー
            player.draw()
            #reset alreadyselectedactions
            self.already_selected_actions = []
            #true turn_end
            self.turn_end = True
        else:
            self.do_action(valid_actions[action])
            self.already_selected_actions.append(valid_actions[action])
