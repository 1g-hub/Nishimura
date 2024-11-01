import player2
import randomplayer2
import deck
import card
import sys
from tqdm import tqdm
import math
import csv

#デッキの初期化
def initdecks(player,card_arr,is_elimenated, elim_num_pla,elim_num_ene):
    #デッキ生成
    player.deck = deck.generateDeck(player, card_arr)
    #デッキのシャッフル
    player.shuffle()
    #特定 ID カード取り除く
    if is_elimenated and elim_num_pla != -1:
        index_list = []
        for i in range(len(player.deck)):
            #print(player.deck[i].id) 
            if player.deck[i].id == elim_num_pla:
                index_list.append(i)
        index_list[1] -= 1
        #print(index_list)
        for i in index_list:
            player.deck.pop(i)
        #print("deck")
        #for i in range(len(player.deck)):
        #    print(player.deck[i].id) 

    
            
    #対戦相手にも同じこと
    player.enemy.deck = deck.generateDeckEnemy(player.enemy, card_arr)
    player.enemy.shuffle()
    #特定 ID カード取り除く
    if is_elimenated and elim_num_ene != -1:
        index_list_enemy = []
        for i in range(len(player.enemy.deck)):
            #print(player.deck[i].id) 
            if player.enemy.deck[i].id == elim_num_ene:
                index_list_enemy.append(i)
        index_list_enemy[1] -= 1
        #print(index_list)
        for i in index_list_enemy:
            player.enemy.deck.pop(i)
        #print("enemydeck")
        #for i in range(len(player.enemy.deck)):
        #    print(player.enemy.deck[i].id) 

#ゲーム開始時のドロー
def inithands(player):
    #敵味方5枚ずつドロー
    player.draw()
    player.draw()
    player.draw()
    player.draw()
    player.draw()
    player.enemy.draw()
    player.enemy.draw()
    player.enemy.draw()
    player.enemy.draw()
    player.enemy.draw()

#カードのis_used状態をリセット（ターン処理で呼ばれる)
def resetuse(player):
    for played_card in player.is_played:
        if played_card.attack == 0 and played_card.is_used == card.Card.use:
            played_card.is_used = True
        else:
            played_card.is_used = False

#プレイヤーのコストUpdate処理 (ターン処理で呼ばれる)
def updatecost(player):
    if player.turnmaxcost < player.maxcost:
        player.turnmaxcost += 1
    player.cost = player.turnmaxcost
    #print("updated cost")
    #print(player.name + ":" + str(player.cost))

def doTurn(player,isFirst,turnnum):
    #print ("")
    #print ("-----------------------------------------------------------------------------------------------")

    #敵のカードドロー
    if isFirst == True or turnnum != 0:
         player.enemy.draw()
    #敵がデッキ切れ起こしたらreturn
    if player.enemy.is_deckend:
        return
    #敵のカードプレイ
    log = player.enemy.playcard()
    log += player.enemy.usecard()
    #敵のresetuse
    resetuse(player.enemy)
    #敵のupdatecost
    updatecost(player.enemy)
    
    #敵の番でHP切れたらretrun
    if player.is_dead:
        return

    #print ("")
    #print ("-----------------------------------------------------------------------------------------------")
    #自分も同じことする
    player.draw()
    #自分がデッキ切れ起こしたらreturn 
    if player.is_deckend:
        return
    log = player.playcard()
    log += player.usecard()
    resetuse(player)
    updatecost(player)

def play(isFirst, card_values, p1policy, p2policy,is_elim, elim_num_player, elim_num_enemy, issamedeck):
    player = player2.Player2()
    player.policydecision = p2policy
    player.enemy.policydecision = p1policy
    

    initdecks(player,card_arr=card_values,is_elimenated=is_elim,  elim_num_pla=elim_num_player, elim_num_ene=elim_num_enemy)
    
    if not issamedeck:
        if p1policy > 0.5:
            #aguro用デッキ
            card_aguro = [1, 1, 3, 1, 1, 5, 3, 2, 4, 2, 2, 4, 1, 2, 5, 1, 2, 4, 1, 2, 4, 1, 1, 4, 2, 5, 1, 4, 4, 1, 1, 1, 4, 1, 2, 3, 1, 3, 5, 1, 4, 1, 1, 2, 3]
            #デッキ生成
            player.enemy.deck = deck.generateDeck(player.enemy, card_aguro)
            #デッキのシャッフル
            player.enemy.shuffle()
        else:
            #コントロール用デッキ
            card_controll = [1, 2, 2, 1, 3, 2, 1, 2, 2, 2, 2, 4, 1, 4, 2, 1, 1, 2, 1, 1, 3, 1, 2, 2, 1, 3, 3, 5, 5, 1, 1, 1, 2, 1, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2]
            #デッキ生成
            player.enemy.deck = deck.generateDeck(player.enemy, card_controll)
            #デッキのシャッフル
            player.enemy.shuffle()
    
    #player.showDeck()
    #player.enemy.showDeck()
    
    player.generate_dict_draw()

    inithands(player)

    resetuse(player)
    resetuse(player.enemy)

    turnnum = 0

    while True:
        #player.enemy.printhand()
        #player.printhand()
        #player1の場を表示
        #player.enemy.printisplayed()

        #player2の場を表示
        #player.printisplayed()
        if isFirst == True and turnnum == 0:
            log = player.playcard()
            log += player.usecard()
            resetuse(player)
            updatecost(player)

        doTurn(player,isFirst,turnnum)  
        turnnum += 1

        #勝利条件
        #敵の勝利条件
        if player.is_dead == True or player.is_deckend == True:
            #print(player.enemy.name + "Win!!")
            #sys.exit(player.enemy.name + "Win!!")
            return -1
        #自分の勝利条件
        elif player.enemy.is_dead == True or player.enemy.is_deckend == True:
            #print(player.name + "Win!!")
            #sys.exit(player.name + "Win!!")
            return 1

# カードのパラメータを変更してミラーで勝率を計算する
# NOTE:カードが15枚である前提
def CalculateWinRateChangeCardParam(changeCardNum):

    print(changeCardNum)
    #csv 出力用のデータ
    data_list = []

    for attack in tqdm(range(5)):
        for hp in range(5):
            for cost in range(5):
                original_deck = [
                    4,4,1,#0
                    2,2,2,#1
                    3,3,3,#2
                    4,3,4,#3
                    5,4,5,#4
                    2,2,2,#5
                    2,3,3,#6
                    1,1,1,#7
                    1,3,2,#8
                    2,1,2,#9
                    3,1,3,#10
                    1,2,2,#11
                    2,3,3,#12
                    1,1,1,#13
                    1,1,5 #14
                ]
                # csv 各列のデータ格納用リスト
                data = []

                #各数値は０〜４のため1足す
                original_deck[changeCardNum*3] = attack+1
                original_deck[changeCardNum*3+1] = hp+1
                original_deck[changeCardNum*3+2] = cost+1

                print(original_deck)
                data.append(attack+1)
                data.append(hp + 1)
                data.append(cost+1)

                print("(attack , hp, cost) = (" + str(attack+1) + " , " + str(hp+1) + " , " + str(cost+1) + ")")

                TEST_COUNT = 10000
                win_sum = 0
                for _ in range(TEST_COUNT):
                        #res = randomrun.play(isFirst=False, card_arr=self.genom)
                        # if res[0] == 1:
                    if play(isFirst=True, card_values=original_deck, p1policy=1.0, p2policy=1.0, is_elim=False, elim_num_player=14, elim_num_enemy=-1, issamedeck=True) == 1:
                        win_sum += 1
                win_rate = win_sum / TEST_COUNT
                print(win_rate)
                data.append(win_rate)

                print(data)

                #dataList に data追加
                data_list.append(data)
    
    with open(str(changeCardNum)+".csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data_list)

        


if __name__ == '__main__':
    #print ("")
    #print ("-----------------------")
    for i in range(15):
        CalculateWinRateChangeCardParam(i)

    '''
    card_values = [
            1,1,1,#0
            1,2,2,#1
            2,2,3,#2
            4,2,4,#3
            3,4,5,#4
            1,1,2,#5
            1,2,3,#6
            2,1,1,#7
            2,3,2,#8
            1,2,1,#9
            2,1,3,#10
            1,1,1,#11
            2,4,3,#12
            1,1,2,#13
            1,2,3 #14
        ]
        '''
    '''
    card_values = [
            4,4,1,#0
            2,2,2,#1
            3,3,3,#2
            4,3,4,#3
            5,4,5,#4
            2,2,2,#5
            2,3,3,#6
            1,1,1,#7
            1,3,2,#8
            2,1,2,#9
            3,1,3,#10
            1,2,2,#11
            2,3,3,#12
            1,1,1,#13
            1,1,5 #14
        ]
    '''
    '''
    x = [
            4,4,1,#0
            2,2,2,#1
            3,3,3,#2
            4,3,4,#3
            5,4,5,#4
            2,2,2,#5
            2,3,3,#6
            1,1,1,#7
            1,3,2,#8
            2,1,2,#9
            3,1,3,#10
            1,2,2,#11
            2,3,3,#12
            1,1,1,#13
            1,1,5 #14
        ]
    '''
    #print(x)
    '''
    win_sum = 0
    lose_sum = 0
    for _ in range(10000):
        if play(isFirst = False, card_values=card_values, p1policy= 0.0, p2policy= 1.0, is_elim = False, elim_num_player= 0, elim_num_enemy=0, issamedeck= False) == 1:
            win_sum += 1
        else:
            lose_sum += 1
    print("win_sum " + str(win_sum))
    print("lose_sum " + str(lose_sum))
    print("win_rate " + str(win_sum / 10000))
    '''
    '''
    TEST_COUNT = 10000
    DESIRE_WIN_RATE = 0.50
    total_fitness = 0
    win_sum = 0
    for _ in range(TEST_COUNT):
            #res = randomrun.play(isFirst=False, card_arr=self.genom)
            # if res[0] == 1:
        if play(isFirst=True, card_values=x, p1policy=1.0, p2policy=1.0, is_elim=False, elim_num_player=14, elim_num_enemy=-1, issamedeck=True) == 1:
            win_sum += 1
    win_rate = win_sum / TEST_COUNT
    print(win_rate)
    #total_fitness += math.sqrt((DESIRE_WIN_RATE - win_rate)
    #                               * (DESIRE_WIN_RATE - win_rate))
'''
    '''
    win_sum = 0
    for _ in range(TEST_COUNT):
            #res = randomrun.play(isFirst=False, card_arr=self.genom)
            # if res[0] == 1:
        if play(isFirst=False, card_values=x, p1policy=1.0, p2policy=1.0, is_elim=False, elim_num_player=0, elim_num_enemy=0, issamedeck=False) == 1:
            win_sum += 1
    win_rate = win_sum / TEST_COUNT
    print(win_rate)
    total_fitness += math.sqrt((DESIRE_WIN_RATE - win_rate)
                                   * (DESIRE_WIN_RATE - win_rate))

    win_sum = 0
    for _ in range(TEST_COUNT):
            #res = randomrun.play(isFirst=False, card_arr=self.genom)
            # if res[0] == 1:
        if play(isFirst=True, card_values=x, p1policy=1.0, p2policy=1.0, is_elim=False, elim_num_player=0, elim_num_enemy=0, issamedeck=False) == 1:
            win_sum += 1
    win_rate = win_sum / TEST_COUNT
    print(win_rate)
    total_fitness += math.sqrt((DESIRE_WIN_RATE - win_rate)
                                   * (DESIRE_WIN_RATE - win_rate))

    win_sum = 0
    for _ in range(TEST_COUNT):
            #res = randomrun.play(isFirst=False, card_arr=self.genom)
            # if res[0] == 1:
        if play(isFirst=False, card_values=x, p1policy=0.0, p2policy=1.0, is_elim=False, elim_num_player=0, elim_num_enemy=0, issamedeck=False) == 1:
            win_sum += 1
    win_rate = win_sum / TEST_COUNT
    print(win_rate)
    total_fitness += math.sqrt((DESIRE_WIN_RATE - win_rate)
                                   * (DESIRE_WIN_RATE - win_rate))

    win_sum = 0
    for _ in range(TEST_COUNT):
            #res = randomrun.play(isFirst=False, card_arr=self.genom)
            # if res[0] == 1:
        if play(isFirst=True, card_values=x, p1policy=0.0, p2policy=1.0, is_elim=False, elim_num_player=0, elim_num_enemy=0, issamedeck=False) == 1:
           win_sum += 1
    win_rate = win_sum / TEST_COUNT
    print(win_rate)
    total_fitness += math.sqrt((DESIRE_WIN_RATE - win_rate)
                                   * (DESIRE_WIN_RATE - win_rate))

    print(total_fitness)
    '''
    '''
    win_sum = 0
    lose_sum = 0
    win_rate = []
    for i in tqdm(range(1)):
        win_rate = []
        for j in range(1):
            win_sum = 0
            lose_sum = 0
            for _ in range(10000):
                if play(isFirst = True, card_values=card_values, p1policy=0.0, p2policy= 1.0, is_elim = False, elim_num_player= i, elim_num_enemy=j) == 1:
                    win_sum += 1
                else:
                    lose_sum += 1
            #print("win_sum " + str(win_sum))
            #print("lose_sum " + str(lose_sum))
            #print("win_rate " + str(win_sum / 10000))
            win_rate.append(win_sum / 10000)
        print(str(i) + " : ")
        print(win_rate)
    '''
    
    


    

