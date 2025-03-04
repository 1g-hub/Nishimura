import random;
import cardeffect;

#カードの基底クラス
class Card:

    #コンストラクタ
    def __init__(self,player):
        #is_played 場にでているかどうか
        self.is_played = False
        #is_used ターン中に動いたかどうか(プレイしたターンに動かないように初期値はTRUE)
        self.is_used = True
        #playerへの参照
        self.player = player
        #name 名前
        self.name = "name"
        #issee 手札カードaction管理用 ターン中確認したかどうか
        self.is_see = False

    #strのオーバーライド
    def __str__(self):
        return self.name
    
    #addのオーバーライド
    def __add__(self, other):
        return str(self) + other
    
    def __radd__(self, other):
        return other + str(self)
    
    #activate 場に出た時呼ばれる関数
    def activate(self,player):
        self.is_played = True
        return False
    
    #use 何か対象に作用する時呼ばれる関数(Unitのみの時は特になし) 
    def use(self,target):
        return False
    
    #discord 場から消える時に呼ばれる関数
    def discard(self):
        self.is_played = False
        #print(self.name + "は破壊された...")
        return False

##########################################################################

#HPと攻撃力を持ってるカード,Cardクラスを継承している
class Unit(Card):

    #コンストラクタ
    def __init__(self,name,id,player,attack,hp,cost,activate=0,use=Card.use,discard=Card.discard):
        #親クラスのコンストラクタ呼び出し
        super().__init__(player)
        #name:名前　attack:攻撃力 hp:体力 cost:コスト
        self.name = name
        self.id = id
        self.attack = attack
        self.hp = hp
        self.cost = cost
        #effectlist(0 ~ 7)
        self.effectlist = [Card.activate,cardeffect.SpawnUnit,cardeffect.PlayerDraw,cardeffect.CanAttack,cardeffect.EnemyDamage2,cardeffect.PlayerHeal2, cardeffect.DestroyAll, cardeffect.Blocking]
        #後述のオーバーライド用に変数化
        self.effectnum = activate
        self.act = self.effectlist[self.effectnum]
        self.u = use
        self.dis = discard
        #blocking用に追加
        self.isBlocking = False
        
    #strオーバーライド
    def __str__(self):
        s = "{"+ self.name + ": " + str(self.attack) + "," + str(self.hp) + "," + str(self.cost) + "," + str(self.effectnum) + "}"
        return s
    
    #ダメージ受けた時呼ばれる関数
    def damage(self, cnt):
        #cntはダメージ量
        #ダメージ受けたのでhpからcnt引く
        self.hp -= cnt
        #死んでるか確認
        if self.hp < 0:
            self.hp = 0
        if self.hp == 0:
            #print(self.player.name + "の" + self + "は破壊された")
            try:
                self.player.is_played.remove(self)
            except:
                pass
            #墓地に追加
            self.player.discard.append(self)
            #カード破壊
            self.discard()
    
    #activateのオーバーライド
    def activate(self,player):
        #print("")
        self.act(self,player)
    
    #useのオーバーライド
    def use(self,target):
        if not self.u(self,target):
            #print(self + "は" + target + "を攻撃した")
            #is_used有効化
            self.is_used = True
            target.damage(self.attack)
            if target.hp < 0:
                target.hp = 0
            #攻撃相手からもダメージ食らう
            self.damage(target.attack)
            if self.hp < 0:
                self.hp = 0
        return self.u(self,target)
    
    #discardのオーバーライド
    def discard(self):
        self.dis(self)

########################################################################

#spellカード実装はここにclass Spell(Card): で