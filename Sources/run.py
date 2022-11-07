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
    #どっちも3枚ドロー
    player.draw()
    player.draw()
    player.draw()
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

def doTurn(player):
    print ("")
    print ("--")
    #敵のカードドロー
    #player.enemy.draw()
    #敵のカードプレイ
    log = ""
    log += player.enemy.usecard()
    #敵のresetuse
    resetuse(player.enemy)
    
    #敵の番でHP切れたらretrun
    if(player.hp <= 0):
        return

    print ("")
    print ("--")
    #自分も同じことする
    #player.draw()
    log = ""
    log += player.usecard()
    resetuse(player)

def play():
    player = player2.Player2()

    initdecks(player)

    inithands(player)

    #3枚ずつ場に出しとく
    player.playcard()
    player.playcard()
    player.playcard()
    player.enemy.playcard()
    player.enemy.playcard()
    player.enemy.playcard()

    resetuse(player)
    resetuse(player.enemy)

    while True:
        #player1の場を表示
        player.enemy.printisplayed()

        #player2の場を表示
        player.printisplayed()

        doTurn(player)  

        #勝利条件
        if player.hp <= 0:
            print(player.enemy.name + "Win!!")
            sys.exit(player.enemy.name + "Win!!")
        elif player.enemy.hp <= 0:
            print(player.name + "Win!!")
            sys.exit(player.name + "Win!!")
        elif len(player.is_played) == 0 and len(player.enemy.is_played) == 0:
            sys.exit("DROW")


if __name__ == '__main__':
    print ("")
    print ("-----------------------")

    play()


    




