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
    player.enemy.deck = deck.generateDeck(player.enemy)
    player.enemy.shuffle()

#ゲーム開始時のドロー
def inithands(player):
    #どっちも2枚ドロー
    player.draw()
    player.draw()
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
    player.enemy.draw()
    #敵のカードプレイ
    log = player.enemy.playcard()
    log += player.enemy.usecard()
    #敵のresetuse
    resetuse(player.enemy)
    
    #敵の番でHP切れたらretrun
    if(player.hp <= 0):
        return

    print ("")
    print ("--")
    #自分も同じことする
    player.draw()
    log = player.playcard()
    log += player.usecard()
    resetuse(player)

def play():
    player = player2.Player2()

    initdecks(player)

    inithands(player)

    while True:
        doTurn(player)

        #勝利条件
        if player.hp <= 0:
            print(player.enemy.name + "Win!!")
            sys.exit(player.enemy.name + "Win!!")
        elif player.enemy.hp <= 0:
            print(player.name + "Win!!")
            sys.exit(player.name + "Win!!")
        elif len(player.deck) <= 0 and len(player.enemy.deck) <= 0:
            print("引き分け")
            sys.exit("引き分け")


if __name__ == '__main__':
    print ("")
    print ("-----------------------")

    play()


    




