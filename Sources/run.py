import player2
import deck
import card
import sys

#デッキの初期化
def initdecks(player):
    #デッキ生成
    player.deck = deck.generateDeck(player)
    #デッキのシャッフル
    player.shuffle()
    #対戦相手にも同じこと
    player.enemy.deck = deck.generateDeckEnemy(player.enemy)
    player.enemy.shuffle()

#ゲーム開始時のドロー
def inithands(player):
    #敵味方3枚ずつドロー
    player.draw()
    player.draw()
    player.draw()
    player.enemy.draw()
    player.enemy.draw()
    player.enemy.draw()
    #player.enemy.draw()
    #player.enemy.draw()


#カードのis_used状態をリセット（ターン処理で呼ばれる)
def resetuse(player):
    for played_card in player.is_played:
        if played_card.attack == 0 and played_card.is_used == card.Card.use:
            played_card.is_used = True
        else:
            played_card.is_used = False

def doTurn(player,turnsum):
    print ("")
    print ("--")
    player.printhand()
    player.enemy.printhand()
    #player1の場を表示
    player.enemy.printisplayed()
    #player2の場を表示
    player.printisplayed()
    #敵のカードドロー
    if turnsum != 0:
        player.enemy.draw()
        if player.enemy.is_deckend:
            return True
    #敵のカードプレイ
    log = player.enemy.playcard()
    log += player.enemy.usecard()
    #敵のresetuse
    resetuse(player.enemy)
    

    print ("")
    print ("--")
    #自分も同じことする
    player.printhand()
    player.enemy.printhand()
    #player1の場を表示
    player.enemy.printisplayed()
    #player2の場を表示
    player.printisplayed()
    player.draw()
     #敵の番でHP切れたらretrun
    if player.is_deckend:
        return True
    log = player.playcard()
    log += player.usecard()
    resetuse(player)
    return False

def play():
    player = player2.Player2()
    Turnsum = 0
    initdecks(player)

    inithands(player)

    #3枚ずつ場に出しとく
    #player.playcard()
    #player.playcard()
    #player.playcard()
    #player.enemy.playcard()
    #player.enemy.playcard()
    #player.enemy.playcard()

    resetuse(player)
    resetuse(player.enemy)

    while True:

        isGameEnd = doTurn(player,Turnsum)

        Turnsum += 1
        print(Turnsum)

        if isGameEnd:
              #勝利条件
            if len(player.enemy.is_played) >= len(player.is_played):
                print(player.enemy.name + "Win!!")
                return -1
            elif len(player.enemy.is_played) < len(player.is_played):
                print(player.name + "Win!!")
                return 1


if __name__ == '__main__':
    print ("")
    print ("-----------------------")
    play
    win_sum = 0
    lose_sum = 0

    for _ in range(10000):
        if play() == 1:
            win_sum += 1
        else:
            lose_sum += 1
    
    print("win_sum:"  + str(win_sum))
    print("lose_sum:" + str(lose_sum))
    print("win_rate : " + str(win_sum /10000))


