import card

def SpawnUnit(self,player):
    #(1,1)のカード生成
    minion_card = card.Unit("minion",player,1,1,0)
    #盤面に追加
    player.is_played.append(minion_card)
    #盤面の枚数制限超えてたら削除
    if len(player.is_played) > player.is_played_maxnum:
        eliminated_card = player.is_played.pop(-1)
        player.discard.append(eliminated_card)
    minion_card.activate(player)

def PlayerHeal2(self,player):
    player.hp += 2
    if player.hp > player.maxhp:
        player.hp = player.maxhp
    #print("PlayerHP:" + str(player.hp))

def PlayerDraw(self,player):
    player.draw()
    #player.printhand()

def EnemyDamage2(self,player):
    player.enemy.damage(2)
    #print("EnemyHP:" + str(player.enemy.hp))

def CanAttack(self,player):
    self.is_used = False
    #player.printisplayed()