import random;

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

    #strのオーバーライド
    def __str__(self):
        return self.name
    
    #addのオーバーライド
    def __add__(self, other):
        return str(self) + other
    
    def __radd__(self, other):
        return other + str(self)
    
    #activate 場に出た時呼ばれる関数
    def activate(self):
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
    def __init__(self,name,player,attack,hp,activate=Card.activate,use=Card.use,discard=Card.discard):
        #親クラスのコンストラクタ呼び出し
        super().__init__(player)
        #name:名前　attack:攻撃力 hp:体力
        self.name = name
        self.attack = attack
        self.hp = hp
        #後述のオーバーライド用に変数化
        self.act = activate
        self.u = use
        self.dis = discard
        
    #strオーバーライド
    def __str__(self):
        s = "{"+ self.name + ": " + str(self.attack) + "," + str(self.hp) + "}"
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
            print(self.player.name + "の" + self + "は破壊された")
            try:
                self.player.is_played.remove(self)
            except:
                pass
            #墓地に追加
            self.player.discard.append(self)
            #カード破壊
            self.discard()
    
    #activateのオーバーライド
    def activate(self):
        print("")
        self.act(self)
    
    #useのオーバーライド
    def use(self,target):
        if not self.u(self,target):
            print(self + "attacks" + target)
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
