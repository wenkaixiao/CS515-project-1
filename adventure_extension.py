import json
import sys
import signal
import re
import copy
def signal_handler(signal,frame):
    print("\nUse 'quit' to exit")

signal.signal(signal.SIGINT,signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
class Room:
    def __init__(self,name,desc,exits,items=[]):
        self.items=items
        self.exits=exits
        self.desc=desc
        self.name=name
        self.show_items=False

class Player:
    def __init__(self):
        self.items=[]
        self.hp=1000
        self.attack=10
        self.summon=False
class Verb:
    def __init__(self,game:"Game"):
        self.game = game
        self.hasMsg=True
        self.keyword=""
    def match(self,cmd:str,s):
        return ""
    def __repr__(self):
        return "Verb"
class Verb_Go(Verb):
    def __init__(self,game):
        super(Verb_Go, self).__init__(game)
        self.keyword="go"
        self.direct=["north","south","east","west"]
    def __repr__(self):
        return "{:<15} {:<3}        {}".format("go","...","g")
    def match(self,cmd:str,s):
        if len(s)>1:
            if s[1] in self.game.room.exits:
                self.game.current_room=self.game.room.exits[s[1]]
                self.game.show=True
                return "You go "+s[1]+"."
            e=self.exits()
            kk=""
            for k,v in e.items():
                if re.match(s[1],k):
                    if kk=="":
                        kk=k
                    elif len(kk)<len(k):
                        kk=k
            if kk:
                vk = {v: k for k, v in self.game.room.exits.items()}
                vk.update(e)
                d=vk[e[kk]]
                self.game.current_room = e[kk]
                self.game.show = True
                return "You go " + d + "."
            else:
                return "There's no way to go "+s[1]+'.'
        else:
            if s[0]=="_g":
                return ""
            return "Sorry, you need to 'go' somewhere."
        return ""
    def exits(self):
        k = {}
        for i in self.game.room.exits:
            for d in self.direct:
                if d == i[:len(d)] and len(d)!=len(i):
                    k[i[0] + i[len(d)]] = self.game.room.exits[i]
        for i in self.game.room.exits:
            n = 0
            for j in self.game.room.exits:
                if i != j:
                    for n in range(n, min(len(i), len(j))):
                        if i[n] != j[n]:
                            break
            k[i[:n + 1]] = self.game.room.exits[i]
        ks=copy.deepcopy(self.game.room.exits)
        ks.update(k)
        return ks
class Verb_Look(Verb):
    def __init__(self,game):
        super(Verb_Look, self).__init__(game)
        self.hasMsg=False
        self.keyword="look"
    def match(self,cmd,s):
        self.game.show=True
        self.game.room.show_items=True
        return cmd
    def __repr__(self):
        return "{:<15} {:<3}        {}".format("look","...","l")

class Verb_Get(Verb):
    def __init__(self,game):
        super(Verb_Get, self).__init__(game)
        self.keyword='get'
    def match(self,cmd:str,s):
        if len(s)>1:
            if s[1] in self.game.room.items:
                i=self.game.room.items.index(s[1])
                self.game.room.items.pop(i)
                self.game.player.items.append(s[1])
                return "You get the "+s[1]+'.'
            else:
                return "There's no "+s[1]+" anywhere."
        return "Sorry, you need to 'get' something."
    def __repr__(self):
        return "{:<15} {:<3}        {}".format("get","","ge")

class Verb_Inventory(Verb):
    def __init__(self,game):
        super(Verb_Inventory, self).__init__(game)
        self.keyword="inventory"
    def match(self,cmd:str,s):
        if self.game.player.items==[]:
            return "You're not carring anything."
        o="Inventory:\n"
        for i in self.game.player.items:
            o+="\t"+i+"\n"
        return o[:-1]
    def __repr__(self):
        return "{:<15} {:<3}        {}".format("inventory","","i")

class Verb_Quit(Verb):
    def __init__(self,game):
        super(Verb_Quit, self).__init__(game)
        self.keyword="quit"
    def match(self, cmd: str,s):
        print("Goodbye!")
        sys.exit()
    def __repr__(self):
        return "quit"

class Verb_Drop(Verb):
    def __init__(self,game):
        super(Verb_Drop, self).__init__(game)
        self.keyword="drop"
    def match(self,cmd:str,s):
        if len(s)>1:
            if s[1] in self.game.player.items:
                self.game.player.items.pop(self.game.player.items.index(s[1]))
                self.game.room.items.append(s[1])
                return "You drop the "+s[1]+"."
            else:
                return "You don't have the "+s[1]+"."
        else:
            return "Sorry, you need to 'drop' something."
    def __repr__(self):
        return "{:<15} {:<3}        {}".format("drop","...","d")

class Verb_Help(Verb):
    def __init__(self,game):
        super(Verb_Help, self).__init__(game)
        self.keyword="help"
    def match(self,cmd:str,s):
        o="You can run the following commands:\n"
        for i in self.game.verbs:
            o+="\t"+str(i)+"\n"
        return o[:-1]
    def __repr__(self):
        return "{:<15} {:<3}        {}".format("help","","h")

class Verb_Attack(Verb):
    def __init__(self,game):
        super(Verb_Attack, self).__init__(game)
        self.keyword="attack"
    def match(self,cmd:str,s):
        if self.game.incombat:
            self.game.dragon_hp-=self.game.player.attack
            return f"Deals {self.game.player.attack} damage to the dragon."
        return "No attack target found."
    def __repr__(self):
        return "{:<15} {:<3}        {}".format("attack","","t")

class Verb_Summon(Verb):
    def __init__(self,game):
        super(Verb_Summon, self).__init__(game)
        self.keyword="summon"
    def match(self,cmd:str,s):
        if self.game.incombat:
            if not self.game.player.summon:
                self.game.player.attack+=990+500
                return "You summoned companions, unity fills you with power."
            return "A partner has been summoned."
        return "Cannot summon when not in combat."
    def __repr__(self):
        return "{:<15} {:<3}        {}".format("summon","","o")

class Game:
    def __init__(self,map):
        self.rooms = {}
        self.player=Player()
        self.current_room=0
        self.verbs=[
            Verb_Go(self),
            Verb_Look(self),
            Verb_Get(self),
            Verb_Inventory(self),
            Verb_Quit(self),
            Verb_Drop(self),
            Verb_Help(self),
            Verb_Attack(self),
            Verb_Summon(self)
        ]
        self.keywords={}
        self.map()
        self.load_map(map)
        self.show=True
        self.incombat=False
        self.dragon_hp=2500
        self.talk=False

    @property
    def room(self):
        return self.rooms[self.current_room]
    def load_map(self,map):
        with open(map) as file:
            data=json.load(file)
            for index,i in enumerate(data):
                room=Room(i['name'],i['desc'],i['exits'],i.get("items",[]))
                self.rooms[index]=room
    def map(self):
        self.keywords={i.keyword:i for i in self.verbs}
        k={}
        for i in self.keywords:
            n=0
            for j in self.keywords:
                if i!=j:
                    for n in range(n,min(len(i),len(j))):
                        if i[n] != j[n]:
                            break
            k[i[:n+1]]=self.keywords[i]
        self.keywords.update(k)
        self.keywords['t']=self.verbs[-2]
        self.keywords['o']=self.verbs[-1]

    def match(self,cmd):
        cmd=cmd.lower()
        s=self.spllt_cmd(cmd)
        k=""
        for i in self.keywords:
            if re.match(f"{s[0]}+",i):
                if k=="":
                    k=i
                elif len(k)>len(i):
                    k=i
        if k:
            message = self.keywords[k].match(cmd,s)
            if message and self.keywords[k].hasMsg:
                print(message)
                print()
                return
        else:
            message = self.verbs[0].match("_g "+s[0],["_g",s[0]])
            if message and self.verbs[0].hasMsg:
                print(message)
                print()
                return

    def spllt_cmd(self,cmd):
        s=cmd.split(" ")
        while "" in s:
            s.pop(s.index(""))
        return s
    def loop(self):
        cmd=""
        print("Welcome to the dark jungle, ")
        print("Where there are the most vicious beasts")
        print("But also the most sincere friends")
        print("Hope you can pursue the most precious things here.\n")
        while True:
            if self.show:
                self.show_room()
                self.show=False
            try:
                cmd=input("What would you like to do? ")
            except EOFError:
                cmd=""
            if cmd:
                self.match(cmd)
            if len(self.player.items)==3 and self.current_room==0:
                self.Boss()
    def Boss(self):
        self.incombat=True
        print("The dragon appears\n")
        a=250
        while True:
            print(f"Player HP:{self.player.hp} Attack:{self.player.attack}")
            print(f"Dragon HP:{self.dragon_hp} Attack:{a}\n")
            if self.player.hp <= 0:
                if not self.talk:
                    print("You lose the game.\n")
                    input("You still have a chance. Do you want to challenge again?")
                    self.player.hp=1000
                    self.dragon_hp=2500
                    self.talk=True
                else:
                    print("You haven't played a dragon before, you've failed.")
                    exit()
            if self.dragon_hp <= 0:
                print("Game victory, you defeated the dragon.")
                exit()
            try:
                cmd=input("What would you like to do? ")
            except EOFError:
                cmd=""
            if cmd:
                self.match(cmd)

            self.player.hp-=a
            print(f"The dragon dealt {a} damage to you\n")




    def show_room(self):
        print(">"+self.room.name)
        print(self.room.desc)
        if self.room.items and self.room.show_items:
            print("Items :", *self.room.items)

        print("Exits : ",end="")
        print(*self.room.exits,sep=", ",end=".\n")
        print()

if __name__ == '__main__':

    Game(sys.argv[1]).loop()