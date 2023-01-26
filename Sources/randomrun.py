import randomplayer2
import deck
import card
import math
import sys

#デッキの初期化
def initdecks(player,card_arr, is_all_changed):
    #デッキ生成
    if is_all_changed:
        player.deck = deck.generateDeck(player,card_arr)
    else:
        player.deck = deck.generatePartialDeck(player,card_arr)
    #player.showDeck()
    #デッキのシャッフル
    player.shuffle()
    #対戦相手にも同じこと
    #デッキ生成
    if is_all_changed:
        player.enemy.deck = deck.generateDeckEnemy(player.enemy, card_arr)
    else:
        player.enemy.deck = deck.generatePartialDeck(player.enemy, card_arr)
    player.enemy.shuffle()

#ゲーム開始時のドロー
def inithands(player):
    #敵味方3枚ずつドロー
    for i in range(player.init_draw_count):
        player.draw()
    for i in range(player.enemy.init_draw_count):
        player.enemy.draw()

#カードのis_used状態をリセット（ターン処理で呼ばれる)
def resetuse(player):
    for played_card in player.is_played:
        if played_card.attack == 0 and played_card.is_used == card.Card.use:
            played_card.is_used = True
        else:
            played_card.is_used = False


def doTurn(player,isFirst,turnnum):
    #print ("'RandomPlayer 1 '")
    #print ("-----------------------------------------------------------------------------------------------")

    #敵のカードドロー
    if isFirst == True or turnnum != 0:
         player.enemy.draw()
    #敵がデッキ切れ起こしたらreturn
    if player.enemy.is_deckend:
        return
    
    while 1:
        if player.is_dead:
            break
        if player.enemy.take_action() == 39:
            resetuse(player.enemy)
            break
    
    #敵の番でHP切れたらretrun
    if player.is_dead:
        return

    #print ("'Random Player 2'")
    #print ("-----------------------------------------------------------------------------------------------")
    #自分も同じことする
    player.draw()
    #自分がデッキ切れ起こしたらreturn 
    if player.is_deckend:
        return
    
    while 1:
        if player.enemy.is_dead:
            break
        if player.take_action() == 39:
            resetuse(player)
            break
    
    if player.enemy.is_dead:
        return

def play(isFirst,card_arr,is_all_change):
    player = randomplayer2.RandomPlayer2()

    initdecks(player,card_arr,is_all_change)
    #player.showDeck()
    player.generate_dict()
    player.generate_dict_draw()
    player.generate_dict_action()

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
            while 1:
                if player.take_action() == 39:
                    resetuse(player)
                    break

        doTurn(player,isFirst,turnnum)  
        turnnum += 1

        #勝利条件
        #敵の勝利条件
        if player.is_dead == True or player.is_deckend == True:
            #print(player.enemy.name + "Win!!")
            record = player.get_record()
            draw_record = player.get_draw_record()
            card_action_record = player.get_action_record()
            #sys.exit(player.enemy.name + "Win!!")
            return [-1, record, draw_record, card_action_record]
        #自分の勝利条件
        elif player.enemy.is_dead == True or player.enemy.is_deckend == True:
            #print(player.name + "Win!!")
            
            record = player.get_record()
            draw_record = player.get_draw_record()
            card_action_record = player.get_action_record()
            #sys.exit(player.name + "Win!!")
            return [1, record,draw_record, card_action_record]

if __name__ == '__main__':
    '''
    #NEW
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
    #NEW (PARTAIL)
    '''
    card_values = [
        4,4,1,#0
        2,3,5 #14
    ]
    '''
    card_values = [
        1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 3, 4, 5, 4, 5, 2, 2, 2, 2, 3, 1, 1, 1, 1, 1, 3, 1, 2, 1, 2, 3, 1, 3, 1, 4, 2, 2, 3, 3, 1, 1, 1, 2, 1, 2
    ]

    '''
    #old
    card_values = [
        1,1,0,#0
        2,1,1,#1
        3,2,2,#2
        4,3,3,#3
        5,4,4,#4
        2,2,2,#5
        2,3,3,#6
        1,1,1,#7
        1,3,2,#8
        2,1,2,#9
        3,1,3,#10
        1,2,2,#11
        2,3,3,#12
        1,1,1,#13
        2,1,3 #14
    ]
    '''
    #print ("")
    #print ("-----------------------")
    #後攻の勝率が５５％超えるまでループしていろいろいじる
    #while(1):
    win_rate_list = []
    play_count_total = { i : 0 for i in range(15)}
    play_count_win = { i : 0 for i in range(15)}
    draw_count_total = { i : 0 for i in range(15)}
    draw_count_win = {i : 0 for i in range(15)}
    card_action_count_total = { i : 0 for i in range(15)}
    card_action_count_win = { i : 0 for i in range(15)}
    total_win_count = 0
    for _ in range(5):
        win_sum = 0
        lose_sum = 0
        playsum_whenwin = { i : 0 for i in range(15)}
        playsum_total = { i : 0 for i in range(15)}
        for i in range(10000):
            res = play(isFirst = False, card_arr = card_values, is_all_change=True)
            #print("DrawRecord")
            #print(res[2])
            for t in res[1]:
                playsum_total[t[0]] += t[1]
                play_count_total[t[0]] += t[1]
            for t in res[2]:
                draw_count_total[t[0]] += t[1]
            for t in res[3]:
                card_action_count_total[t[0]] += t[1]

            
            # if win
            if res[0] == 1:
                record = res[1]
                for t in record:
                    playsum_whenwin[t[0]] += t[1]
                    play_count_win[t[0]] += t[1]
                draw_record = res[2]
                for t in draw_record:
                    draw_count_win[t[0]] += t[1]
                card_action_record = res[3]
                for t in card_action_record:
                    card_action_count_win[t[0]] += t[1]
                #print(record)
                win_sum += 1
            #if lose
            elif res[0] == -1:
                lose_sum += 1
            #if lose_sum >= 5500:
            #    break
            #else:
            #    pass
                #ここに後攻のパラメータいじる処理
        total_win_count += win_sum
        #print("playsum_total")
        for i in range(15):
            playsum_total[i] /= 10000
        #print(playsum_total)
        #print("playsum_whenwin")
        for i in range(15):
            playsum_whenwin[i] /= win_sum
        #print(playsum_whenwin)
        #print("win_sum " + str(win_sum))
        #print("lose_sum " + str(lose_sum))
        #print("win_rate " + str(win_sum / 10000))
        win_rate_list.append(win_sum / 10000)
    print("play_count_total")
    print(play_count_total)
    print("play_count_win")
    print(play_count_win)
    print("playした時の勝率 sorted")
    win_per_card = { i : 0 for i in range(15)}
    for i in range(15):
        win_per_card[i] = play_count_win[i] / play_count_total[i]
    sorted_win_per_card = sorted(win_per_card.items(), key=lambda x:x[1], reverse=True)
    print(sorted_win_per_card)
    print("draw_count_total")
    print(draw_count_total)
    print("draw_count_win")
    print(draw_count_win)
    print("draw したときの勝率 sorted")
    win_rate_when_draw = { i : 0 for i in range(15)}
    for i in range(15):
        win_rate_when_draw[i] = draw_count_win[i] / draw_count_total[i]
    sorted_wrd = sorted(win_rate_when_draw.items(), key=lambda x:x[1], reverse=True)
    print(sorted_wrd)
    print("card_action_total")
    print(card_action_count_total)
    print("card_action_win")
    print(card_action_count_win)
    print("カードがなんかaction したときの勝率 sorted")
    #win_rate_when_action = { i : 0 for i in range(15)}
    #for i in range(15):
    #    win_rate_when_action[i] = card_action_count_win[i] / card_action_count_total[i]
    #sorted_wra  = sorted(win_rate_when_action.items(), key=lambda x:x[1], reverse=True)
    #print(sorted_wra)
    print("win_rate")
    print(win_rate_list)
    sum = 0
    for i in range(5):
        sum += win_rate_list[i]
    ave = sum / 5.0
    print("ave" + str(ave))
    tmp = 0
    for i in range(5):
        tmp += (win_rate_list[i] - ave) * (win_rate_list[i] - ave)
    e = math.sqrt(tmp/5.0)
    print(e)