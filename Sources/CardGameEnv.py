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
        #手札1が敵カード123攻撃・・・1,2,3
        #手札2・・・4~7
        #手札3・・・8~11
        #ターンエンド・・・12
        self.action_space = spaces.Discrete(12)
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
            "MyCard1CanAttack": spaces.Discrete(2),#True or False
            "MyCard2CanAttack": spaces.Discrete(2),
            "MyCard3CanAttack": spaces.Discrete(2),
        })
        
        #dict型むりそう；；
        self.observation_space = spaces.Dict(
            dict(
                MyHP = spaces.Box(low=0,high=20),
                EnemyHP = spaces.Box(low=0,high=20),
                MyCard1Attack = spaces.Box(low=0, high=5),
                MyCard1HP = spaces.Box(low=0, high=5),
                MyCard2Attack = spaces.Box(low=0, high=5),
                MyCard2HP = spaces.Box(low=0, high=5),
                MyCard3Attack = spaces.Box(low=0, high=5),
                MyCard3HP = spaces.Box(low=0, high=5),
                EnemyCard1Attack = spaces.Box(low=0, high=5),
                EnemyCard1HP = spaces.Box(low=0, high=5),
                EnemyCard2Attack = spaces.Box(low=0, high=5),
                EnemyCard2HP = spaces.Box(low=0, high=5),
                EnemyCard3Attack = spaces.Box(low=0, high=5),
                EnemyCard3HP = spaces.Box(low=0, high=5),
                MyCard1CanAttack = spaces.Box(low=0,high=1),
                MyCard2CanAttack = spaces.Box(low=0,high=1),
                MyCard3CanAttack = spaces.Box(low=0,high=1)
            )
        )
        """
        #これで行けなかったら終わり
        LOW = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        HIGH = np.array([20,20,5,5,5,5,5,5,5,5,5,5,5,5,1,1,1])
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
            "MyCard1CanAttack": 1 if 0 < len(player.is_played) and not player.is_played[0].is_used else 0,
            "MyCard2CanAttack": 1 if 1 < len(player.is_played) and not player.is_played[1].is_used else 0,
            "MyCard3CanAttack": 1 if 2 < len(player.is_played) and not player.is_played[2].is_used else 0,
        }
        
        s = dict(
            MyHP = player.maxhp,
            EnemyHP = player.enemy.maxhp,
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
            1 if 0 < len(player.is_played) and not player.is_played[0].is_used else 0,
            1 if 1 < len(player.is_played) and not player.is_played[1].is_used else 0,
            1 if 2 < len(player.is_played) and not player.is_played[2].is_used else 0,
        ]

        print("RESET STATE")
        print(s)
        #print("state.shape" + s.shape)

        return s
    
    def step(self,action):
        done = False
        reward = 0.01
        player = self.player
        
        
        #actionによって処理書く(ここ変えないとまずい)
        if action == 0:
            #自分カード0が敵本体攻撃
            if player.is_played[0].is_used == False:
                player.enemy.damage(player.is_played[0].attack)
                player.is_played[0].is_used = True
            else:
                print("味方のカード1はすでに行動済みです")

        elif action == 1:
            if len(player.enemy.is_played) > 0:
                #自分カード0が敵0攻撃
                if player.is_played[0].is_used == False:
                    player.enemy.is_played[0].damage(player.is_played[0].attack)
                    player.is_played[0].is_used = True
                else:
                    print("味方のカード1はすでに行動済みです")
            else:
                print("敵カードがありません")

        elif action == 2:
            if len(player.enemy.is_played) > 1:
                #自分0が敵1攻撃
                if player.is_played[0].is_used == False:
                    player.enemy.is_played[1].damage(player.is_played[0].attack)
                    player.is_played[0].is_used = True
                else:
                    print("味方のカード1はすでに行動済みです")
            else:
                print("敵カードがありません")

        elif action == 3:
            if len(player.enemy.is_played) > 2:
                #自分0が敵2攻撃
                if player.is_played[0].is_used == False:
                    player.enemy.is_played[2].damage(player.is_played[0].attack)
                    player.is_played[0].is_used = True
                else:
                    print("味方のカード1はすでに行動済みです")
            else:
                print("敵カードがありません")

        elif action == 4:
            #自分1が敵本体攻撃
            if player.is_played[1].is_used == False:
                player.enemy.damage(player.is_played[1].attack)
                player.is_played[1].is_used = True
            else:
                print("味方のカード2はすでに行動済みです")

        elif action == 5:
            if len(player.enemy.is_played) > 0:
                #自分1が敵0攻撃
                if player.is_played[1].is_used == False:
                    player.enemy.is_played[0].damage(player.is_played[1].attack)
                    player.is_played[1].is_used = True
                else:
                    print("味方のカード2はすでに行動済みです")
            else:
                print("敵カードがありません")

        elif action == 6:
            if len(player.enemy.is_played) > 1:
                #自分1が敵1攻撃
                if player.is_played[1].is_used == False:
                    player.enemy.is_played[1].damage(player.is_played[1].attack)
                    player.is_played[1].is_used = True
                else:
                    print("味方のカード2はすでに行動済みです")
            else:
                print("敵カードがありません")

        elif action == 7:
            if len(player.enemy.is_played) > 2:
                #自分1が敵2攻撃
                if player.is_played[1].is_used == False:
                    player.enemy.is_played[2].damage(player.is_played[1].attack)
                    player.is_played[1].is_used = True
                else:
                    print("味方のカード2はすでに行動済みです")
            else:
                print("敵カードがありません")

        elif action == 8:
            #自分2が敵本体を攻撃
            if player.is_played[2].is_used == False:
                player.enemy.damage(player.is_played[2].attack)
                player.is_played[2].is_used = True
            else:
                print("味方のカード3はすでに行動済みです")

        elif action == 9:
            if len(player.enemy.is_played) > 0:
                #自分2が敵0攻撃
                if player.is_played[2].is_used == False:
                    player.enemy.is_played[0].damage(player.is_played[2].attack)
                    player.is_played[2].is_used = True
                else:
                    print("味方のカード3はすでに行動済みです")
            else:
                print("敵カードがありません")

        elif action == 10:
            if len(player.enemy.is_played) > 1:
                #自分2が敵1攻撃
                if player.is_played[2].is_used == False:
                    player.enemy.is_played[1].damage(player.is_played[2].attack)
                    player.is_played[2].is_used = True
                else:
                    print("味方のカード3はすでに行動済みです")
            else:
                print("敵カードがありません")

        elif action == 11:
            if len(player.enemy.is_played) > 2:
                #自分2が敵2攻撃
                if player.is_played[2].is_used == False:
                    player.enemy.is_played[2].damage(player.is_played[2].attack)
                    player.is_played[2].is_used = True
                else:
                    print("味方のカード3はすでに行動済みです")
            else:
                print("敵カードがありません")

        else:
            print(action)
            print("未定義のActionです")
            print(self.get_state())
        
        if not action in self.action_episode_memory:
            reward = 0
        if action in self.action_episode_memory:
            reward = -1
        
        
        #自分のターンが終了したら
        if self.getused():
            #敵をランダムに行動させる
            log = ""
            log += player.enemy.usecard()
            #報酬を渡す(TODO盤面評価関数作る)
            reward = self.calculate_reward()
            #doneをTrueにする
            done = True
            #表示
            #print("reward")
            #print(reward)
            #print("self.curr_step")
            #print(self.curr_step)
            #print("self.action_episode_memory")
            #print(self.action_episode_memory)
        
        #if not action in self.action_episode_memory:
        #    reward = 0
        #if action in self.action_episode_memory:
        #    reward = -1
        observation = self.get_state()

        #記録
        self.curr_step += 1
        self.action_episode_memory.append(action)
        print("action")
        print(self.action_episode_memory)
        print("state")
        print(observation)
        

        return observation,reward,done,{}

        
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
        #敵削った体力
        reward = (player.enemy.maxhp - player.enemy.hp)*2.0
        #print("reward")
        #print(reward)
        reward = 0
        #味方カードの評価値
        if len(player.is_played) > 0:
            for i in player.is_played:
                #print("attack,hp")
                #print(i.attack)
                #print(i.hp)
                reward += (i.attack + i.hp)*1.5
                #print(reward)
        #敵カードの評価
        if len(player.enemy.is_played) > 0:
            for i in player.enemy.is_played:
                #print("attack,hp")
                #print(i.attack)
                #print(i.hp)
                tmp = (i.attack + i.hp)
                #print("tmp")
                #print(tmp)
                reward = reward - tmp
                #print("reward")
                #print(reward)

        #自分削られた体力
        reward -= (player.maxhp - player.hp)*5

        print("reward")
        print(reward)

        #報酬のCliping
        if reward > 0:
           reward = 1
        elif reward < 0:
           reward = -1
        else:
           reward = 1
        
        print("reward")
        print(reward)
        
        return reward
         