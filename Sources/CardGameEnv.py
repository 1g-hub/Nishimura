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
        #手札1が敵本体攻撃・・・0
        #手札1が敵カード12345攻撃・・・1,2,3,4,5
        #手札2・・・6~10
        #手札3・・・12~17
        self.action_space = spaces.Discrete(18)
        """
        self.observation_space = spaces.Dict({
            "MyHP": spaces.Discrete(21),#0~20
            "EnemyHP": spaces.Discrete(21),
            "MyCard1Attack": spaces.Discrete(5),#0~4
            "MyCard1HP" : spaces.Discrete(5),
            "MyCard2Attack": spaces.Discrete(5),
            "MyCard2HP" : spaces.Discrete(5),
            "MyCard3Attack": spaces.Discrete(5),
            "MyCard3HP" : spaces.Discrete(5),
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
        })
        
        #dict型むりそう；；

        """
        #これで行けなかったら終わり
        LOW = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        HIGH = np.array([20,20,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,1,1,1])
        self.observation_space = spaces.Box(low=LOW,high=HIGH)


        self.curr_episode = -1

        self.reset()

    def setup_game(self):
        self.player = player2.Player2()

        run.initdecks(self.player)

        run.inithands(self.player)

        #3枚ずつ場に出しとく
        self.player.playcard()
        self.player.playcard()
        self.player.playcard()
        self.player.enemy.playcard()
        self.player.enemy.playcard()
        self.player.enemy.playcard()
        self.player.enemy.playcard()
        self.player.enemy.playcard()


        run.resetuse(self.player)
        run.resetuse(self.player.enemy)


    def reset(self):
        
        self.setup_game()

        player = self.player
        self.action_episode_memory=[]
        
        #初期状態
        '''
        s = {
            "MyHP": player.maxhp,
            "EnemyHP": player.enemy.maxhp,
            "MyCard1Attack": player.is_played[0].attack if 0 < len(player.is_played) else 0,
            "MyCard1HP" : player.is_played[0].hp if 0 < len(player.is_played) else 0,
            "MyCard2Attack": player.is_played[1].attack if 1 < len(player.is_played) else 0,
            "MyCard2HP" : player.is_played[1].hp if 1 < len(player.is_played) else 0,
            "MyCard3Attack": player.is_played[2].attack if 2 < len(player.is_played) else 0,
            "MyCard3HP" : player.is_played[2].hp if 2 < len(player.is_played) else 0,
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
        }
        
        '''
        s = [
            player.maxhp,
            player.enemy.maxhp,
            player.is_played[0].attack if 0 < len(player.is_played) else 0,
            player.is_played[0].hp if 0 < len(player.is_played) else 0,
            player.is_played[1].attack if 1 < len(player.is_played) else 0,
            player.is_played[1].hp if 1 < len(player.is_played) else 0,
            player.is_played[2].attack if 2 < len(player.is_played) else 0,
            player.is_played[2].hp if 2 < len(player.is_played) else 0,
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
        ]
        self.observation = s

        print("RESET STATE")
        print(self.observation)
        #print("state.shape" + s.shape)

        return s
    
    def step(self,action):
        done = False
        reward = 0.01
        player = self.player

        #OTK可能であるのに逃したら-30
        attack_sum = 0
        for i in player.is_played:
            if i.is_used == False:
                attack_sum += i.attack
        print("attacknum")
        print(attack_sum)
        
        self.action_episode_memory.append(action)
        print("action")
        print(self.action_episode_memory)

        #reward設定用is_playedの個数の和
        is_used_sum = 0
        for i in player.is_played:
            if i.is_used == False:
                is_used_sum += 1

        #reward設定用事前のenemyHP
        before_enemyHP = player.enemy.hp
        
        #actionによって処理書く(ここ変えないとまずい)
        if action == 0:
            if len(player.is_played) > 0:
                #自分カード0が敵本体攻撃
                if player.is_played[0].is_used == False:
                    player.enemy.damage(player.is_played[0].attack)
                    player.is_played[0].is_used = True
                else:
                    pass
                    #print("味方のカード1はすでに行動済みです")
            else:
                pass
                #print("敵カードがありません or 味方カードがありません")

        elif action == 1:
            if len(player.enemy.is_played) > 0 and len(player.is_played) > 0:
                #自分カード0が敵0攻撃
                if player.is_played[0].is_used == False:
                    player.is_played[0].use(player.enemy.is_played[0])
                else:
                    pass
                    #print("味方のカード1はすでに行動済みです")
            else:
                pass
                #print("敵カードがありません or 味方カードがありません")

        elif action == 2:
            if len(player.enemy.is_played) > 1 and len(player.is_played) > 0:
                #自分0が敵1攻撃
                if player.is_played[0].is_used == False:
                    player.is_played[0].use(player.enemy.is_played[1])
                else:
                    pass
                    #print("味方のカード1はすでに行動済みです")
            else:
                pass
                #print("敵カードがありません or 味方カードがありません")

        elif action == 3:
            if len(player.enemy.is_played) > 2 and len(player.is_played) > 0:
                #自分0が敵2攻撃
                if player.is_played[0].is_used == False:
                    player.is_played[0].use(player.enemy.is_played[2])
                else:
                    pass
                    #print("味方のカード1はすでに行動済みです")
            else:
                pass
                #print("敵カードがありません or 味方カードがありません")

        elif action == 4:
            if len(player.enemy.is_played) > 3 and len(player.is_played) > 0:
                #自分0が敵3攻撃
                if player.is_played[0].is_used == False:
                    player.is_played[0].use(player.enemy.is_played[3])
                else:
                    pass
                    #print("味方のカード1はすでに行動済みです")
            else:
                pass
                #print("敵カードがありません or 味方カードがありません")

        elif action == 5:
            if len(player.enemy.is_played) > 4 and len(player.is_played) > 0:
                #自分0が敵4攻撃
                if player.is_played[0].is_used == False:
                    player.is_played[0].use(player.enemy.is_played[4])
                else:
                    pass
                    #print("味方のカード1はすでに行動済みです")
            else:
                pass
                #print("敵カードがありません or 味方カードがありません")

        elif action == 6:
            if len(player.is_played) > 1:
                #自分1が敵本体攻撃
                if player.is_played[1].is_used == False:
                    player.enemy.damage(player.is_played[1].attack)
                    player.is_played[1].is_used = True
                else:
                    pass
                    #print("味方のカード2はすでに行動済みです")
            else:
                pass
                #print("味方カードがありません")

        elif action == 7:
            if len(player.enemy.is_played) > 0 and len(player.is_played) > 1:
                #自分1が敵0攻撃
                if player.is_played[1].is_used == False:
                    player.is_played[1].use(player.enemy.is_played[0])
                else:
                    pass
                    #print("味方のカード2はすでに行動済みです")
            else:
                pass
                #print("敵カードがありません or 味方カードがありません")

        elif action == 8:
            if len(player.enemy.is_played) > 1 and len(player.is_played) > 1:
                #自分1が敵1攻撃
                if player.is_played[1].is_used == False:
                    player.is_played[1].use(player.enemy.is_played[1])
                else:
                    pass
                    #print("味方のカード2はすでに行動済みです")
            else:
                pass
                #print("敵カードがありません or 味方カードがありません")

        elif action == 9:
            if len(player.enemy.is_played) > 2 and len(player.is_played) > 1:
                #自分1が敵2攻撃
                if player.is_played[1].is_used == False:
                    player.is_played[1].use(player.enemy.is_played[2])
                else:
                    pass
                    #print("味方のカード2はすでに行動済みです")
            else:
                pass
                #print("敵カードがありません or 味方カードがありません")
        
        elif action == 10:
            if len(player.enemy.is_played) > 3 and len(player.is_played) > 1:
                #自分1が敵3攻撃
                if player.is_played[1].is_used == False:
                    player.is_played[1].use(player.enemy.is_played[3])
                else:
                    pass
                    #print("味方のカード2はすでに行動済みです")
            else:
                pass
                #print("敵カードがありません or 味方カードがありません")
        
        elif action == 11:
            if len(player.enemy.is_played) > 4 and len(player.is_played) > 1:
                #自分1が敵4攻撃
                if player.is_played[1].is_used == False:
                    player.is_played[1].use(player.enemy.is_played[4])
                else:
                    pass
                    #print("味方のカード2はすでに行動済みです")
            else:
                pass
                #print("敵カードがありません or 味方カードがありません")

        elif action == 12:
            if len(player.is_played) > 2:
                #自分2が敵本体を攻撃
                if player.is_played[2].is_used == False:
                    player.enemy.damage(player.is_played[2].attack)
                    player.is_played[2].is_used = True
                else:
                    pass
                    #print("味方のカード3はすでに行動済みです")
            else:
                pass
                #print("味方カードがありません")

        elif action == 13:
            if len(player.enemy.is_played) > 0 and len(player.is_played) > 2:
                #自分2が敵0攻撃
                if player.is_played[2].is_used == False:
                    player.is_played[2].use(player.enemy.is_played[0])
                else:
                    pass
                    #print("味方のカード3はすでに行動済みです")
            else:
                pass
                #print("敵カードがありません or 味方カードがありません")

        elif action == 14:
            if len(player.enemy.is_played) > 1 and len(player.is_played) > 2:
                #自分2が敵1攻撃
                if player.is_played[2].is_used == False:
                    player.is_played[2].use(player.enemy.is_played[1])
                else:
                    pass
                    #print("味方のカード3はすでに行動済みです")
            else:
                pass
                #print("敵カードがありません or 味方カードがありません")


        elif action == 15:
            if len(player.enemy.is_played) > 2 and len(player.is_played) > 2:
                #自分2が敵2攻撃
                if player.is_played[2].is_used == False:
                    player.is_played[2].use(player.enemy.is_played[2])
                else:
                    pass
                    #print("味方のカード3はすでに行動済みです")
            else:
                pass
                #print("敵カードがありません or 味方カードがありません")

        elif action == 16:
            if len(player.enemy.is_played) > 3 and len(player.is_played) > 2:
                #自分2が敵3攻撃
                if player.is_played[2].is_used == False:
                    player.is_played[2].use(player.enemy.is_played[3])
                else:
                    pass
                    #print("味方のカード3はすでに行動済みです")
            else:
                pass
                #print("敵カードがありません or 味方カードがありません")
        
        elif action == 17:
            if len(player.enemy.is_played) > 4 and len(player.is_played) > 2:
                #自分2が敵4攻撃
                if player.is_played[2].is_used == False:
                    player.is_played[2].use(player.enemy.is_played[4])
                else:
                    pass
                    #print("味方のカード3はすでに行動済みです")
            else:
                pass
                #print("敵カードがありません or 味方カードがありません")

        else:
            print(action)
            print("未定義のActionです")                                        
            print(self.get_state())                                  

        after_is_used_sum = 0
        for i in player.is_played:
            if i.is_used == False:
                after_is_used_sum += 1

        #print("is_used_sum")
        #print(is_used_sum)
        #print("after_used_sum")
        #print(after_is_used_sum)

            

        #使われたカードもう一回使うとペナルティ（無駄な行動なので)
        if after_is_used_sum >= is_used_sum:
            reward = -3.0 
        #OTK可能で敵に攻撃してないなら-
        elif attack_sum >= before_enemyHP and before_enemyHP == player.enemy.hp:
            reward = -50.0
        else :
            #print("reward計算")
            #報酬を渡す(TODO盤面評価関数作る)
            reward = 0.0
        
        if player.hp <= 0:
            print(player.name +"の体力が0になりました GG!!")
            #doneをTrueにする
            done = True
            #報酬渡す
            reward = -50
        elif player.enemy.hp <= 0:
            print(player.enemy.name +"の体力が0になりました GG!!")
            #doneをTrueにする
            done = True
            #報酬渡す
            reward = 50
        
        #自分のターンが終了or どちらかの体力が0になったら
        if self.getused():
            if player.enemy.hp <= 0:
                print(player.enemy.name +"の体力が0になりました GG!!")
                #doneをTrueにする
                done = True
                #報酬渡す
                reward = 50
            else:
                #敵をランダムに行動させる
                log = ""
                log += player.enemy.usecard()
                #doneをTrueにする
                done = True
                #報酬を渡す(TODO盤面評価関数作る)
            
                if player.hp <= 0:
                    print(player.name +"の体力が0になりました GG!!")
                    #doneをTrueにする
                    done = True
                    #報酬渡す
                    reward = -50
                else:
                    if attack_sum >= player.enemy.hp:
                        reward = -30
                    else:
                        #盤面評価計算して渡す
                        reward = self.calculate_reward()

        self.observation = self.get_state()

        #記録
        self.curr_step += 1
        print("state")
        print(self.observation)
        

        return self.observation,reward,done,{}

        
    def getused(self):
        flag = True
        if len(self.player.is_played):
            for i in self.player.is_played:
                if i.is_used == False:
                    flag = False
            return flag
        else:
            return True
    
    #状態を返す
    def get_state(self):

        player = self.player
        '''
        s = dict(
            MyHP = player.hp,
            EnemyHP = player.enemy.hp,
            MyCard1Attack = player.is_played[0].attack if 0 < len(player.is_played) else 0,
            MyCard1HP = player.is_played[0].hp if 0 < len(player.is_played) else 0,
            MyCard2Attack = player.is_played[1].attack if 1 < len(player.is_played) else 0,
            MyCard2HP = player.is_played[1].hp if 1 < len(player.is_played) else 0,
            MyCard3Attack = player.is_played[2].attack if 2 < len(player.is_played) else 0,
            MyCard3HP = player.is_played[2].hp if 2 < len(player.is_played) else 0,
            EnemyCard1Attack = player.enemy.is_played[0].attack if 0 < len(player.enemy.is_played) else 0,
            EnemyCard1HP = player.enemy.is_played[0].hp if 0 < len(player.enemy.is_played) else 0,
            EnemyCard2Attack = player.enemy.is_played[1].attack if 1 < len(player.enemy.is_played) else 0,
            EnemyCard2HP = player.enemy.is_played[1].hp if 1 < len(player.enemy.is_played) else 0,
            EnemyCard3Attack = player.enemy.is_played[2].attack if 2 < len(player.enemy.is_played) else 0,
            EnemyCard3HP = player.enemy.is_played[2].hp if 2 < len(player.enemy.is_played) else 0,
            MyCard1CanAttack = 1 if 0 < len(player.is_played) and not player.is_played[0].is_used else 0,
            MyCard2CanAttack = 1 if 1 < len(player.is_played) and not player.is_played[1].is_used else 0,
            MyCard3CanAttack = 1 if 2 < len(player.is_played) and not player.is_played[2].is_used else 0,
        )
        '''
        s = [
            player.hp,
            player.enemy.hp,
            player.is_played[0].attack if 0 < len(player.is_played) else 0,
            player.is_played[0].hp if 0 < len(player.is_played) else 0,
            player.is_played[1].attack if 1 < len(player.is_played) else 0,
            player.is_played[1].hp if 1 < len(player.is_played) else 0,
            player.is_played[2].attack if 2 < len(player.is_played) else 0,
            player.is_played[2].hp if 2 < len(player.is_played) else 0,
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
        
        