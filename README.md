Write at the top

The files map.json and adventure.py are for the basic functionality and have been submitted for testing in gradescope

The files map_extension.json and adventure_extension.py are the complete adventure story, with minor changes to the items on the map for the final win/lose conditions, which I have detailed in the README.md file
----------------------------------------------------------------------------------------------
▶ your name and Stevens login

Wenkai Xiao wxiao7@stevens.edu
----------------------------------------------------------------------------------------------
▶ the URL of your public GitHub repo

----------------------------------------------------------------------------------------------
▶ an estimate of how many hours you spent on the project

I spent about two hours on the basic map and basic verb section, where I first mapped out the basic game logic and then wrote the code based on the SAMPLES given by the professor.

I spent more than 70 hours on the expansion section, where I had big trouble with the win-lose condition section, abandoning the initial solution and then changing it to another, so it took more time.

I spent about an hour on testing and writing the README part, so I spent about 73 hours in total to complete the first project
----------------------------------------------------------------------------------------------
▶ a description of how you tested your code

I used two methods to test my code

The first one is simpler, I input the full spelling and abbreviation of each verb and check if the output of the full spelling and abbreviation are consistent and if the input follows the logic diagram I drew.

If they are consistent, there is no problem, if not, there is a bug in the code.

For the second method I used doctests, and the following is an example of the doctests process for the verb Inventory:

**The code for the doctest of the match() function of the Verb_Inventory class is：**

```python
>>> game = Game('map.json')
>>> verb_inventory = Verb_Inventory(game)
>>> game.player.items = ['book', 'key', 'potion']
>>> verb_inventory.match("", [])
'Inventory:\n\tbook\n\tkey\n\tpotion'
>>> game.player.items = []
>>> verb_inventory.match("", [])
"You're not carring anything."
```

The logic of this test is that we first create a Game object and a Verb_Inventory object. Then we set the player.items property of the Game object to simulate that the player has three items. We run the Verb_Inventory object's match() method and compare it to the expected string.
Next, we set the player.items property of the Game object to an empty list to simulate that the player has no items. We run the match() method of the Verb_Inventory object again and compare it to the expected string.

**The code for the test results is：**


```python
Trying:
    g=Game("example.json")
Expecting nothing
ok
Trying:
    g.verbs[3].match("", [])
Expecting:
    "You're not carring anything."
ok
Trying:
    g.verbs[3].match("", ["inventory"])
Expecting:
    "You're not carring anything."
ok
Trying:
    g.player.items = ["sword"]
Expecting nothing
ok
Trying:
    g.verbs[3].match("", ["inventory"])
Expecting:
    'Inventory:\n\tsword'
ok
Trying:
    g.player.items = ["sword", "shield"]
Expecting nothing
ok
Trying:
    g.verbs[3].match("", ["inventory"])
Expecting:
    'Inventory:\n\tsword\n\tshield'
ok
1 items had no tests:
    __main__
2 items passed all tests:
   1 tests in __main__.Game.__init__
   5 tests in __main__.Verb_Inventory.match
5 tests in 3 items.
5 passed and 0 failed.
Test passed.
```
----------------------------------------------------------------------------------------------
▶ any bugs or issues you could not resolve

I encountered an unresolvable problem in terms of win-lose conditions. At first I set the win-lose condition: within the 10 seconds countdown, I attack the dragon, and when the dragon's HP is less than or equal to 0, output I win, and when the dragon's HP is greater than or equal to 0, I lose. I found that in order to attack while still counting down the 10 seconds, my code had to be multi-threaded.

But in the process of writing the code, I found that the input() function blocks the main thread until I type and press Enter, then it returns the input to the program. However, in a multi-threaded case, if one thread is waiting for input(), other threads may run and call print() or other IO operations in the meantime.

With my level of coding and learning, I had no idea how to solve this problem, and the program kept reporting errors showing more than 5 bugs, so I finally had to abandon this setting and change the win-lose condition to a simple turn-based attack
----------------------------------------------------------------------------------------------
▶ an example of a difficult issue or bug and how you resolved

In addition to the above I gave up an unsolvable problem, I also encountered a bug, the key verb matching appears to be unable to correctly match the bug, after a long period of research, I found that the bug may appear in the go command implementation part

At first, the keyword is determined by in to determine whether the keyword exists

Later I changed to regular matching to solve the bug
----------------------------------------------------------------------------------------------
▶ a list of the three extensions you’ve chosen to implement, with appropriate detail on them for the CAs to evaluate them (i.e., what are the new verbs/features, how do you exercise them, where are they in the map)

**1.The first extension is the help verb**

My understanding is that help is a guide to the game, so it can be output by the player at any time from the beginning to the end of the game through the command help or abbreviation

When the player types help or the abbreviation h, he can see all the command verbs of the game and the corresponding abbreviated forms at the same time

This is the code for this function：

```python
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
```
According to the professor, to get all the credits, help should not be a static text, but should be generated from the verb I defined

So in the constructor of the Game class, I initialize a list self.verbs containing all the verbs that are instances of the Verb class, and each Verb class has a __repr__ method that returns the name and shortcut of that verb. In the Verb_Help class, the match method returns a string containing the names and shortcut keys of all verbs, so the help display is dynamically generated rather than static text.

**2.The second extension is that the direction becomes a verb**

In my game, using go west as an example, players can output go west whether they type go west, or abbreviate g w, or just type w

I implement this extension with the following code：

```python
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
```
This code implements a verb class (Verb) and a concrete verb class (Verb_Go). The verb class is the parent of other concrete verb classes and contains some general properties and methods. The concrete verb class inherits the automatic verb class and implements specific actions.

In this concrete verb class (Verb_Go), it inherits some properties and methods from the verb class and overrides the match method and __repr__ method to implement specific actions. match method is used to match the commands entered by the user and return the result of action execution. In this specific verb class, the match method implements the functionality to move the game character based on the input command. The __repr__ method returns a short description of the action, which is used to help the user understand the available actions.

In addition, this concrete verb class (Verb_Go) contains an exits method that generates a dictionary based on the exits of the current room, with the key being the direction and the value being the id of the next room. this method takes into account the abbreviation of the direction, for example north can be abbreviated to n, and takes into account the case where multiple exits share the same prefix. The generated result of this method will be used in the match method to match the direction entered by the user.

**The third extension is the win-lose condition**

In the base map, the player gets the ring and sword, I think if a game to be full of fun and reasoning, so the HP and attack values of the player and the boss are set so that if the player attacks directly, it will show failure

I want the player to think, what is the use of the previously obtained items? Press the help command to see the verb summon, so does the ring previously obtained in the room play a role? If you can't win by attacking the boss with just the longsword, is it possible to summon a companion to get a boost in HP and attack value?

So in room 0, if you attack the dragon directly, it will show that the game is lost, if you use the ring to summon a companion to get a numerical boost by summoning a verb to defeat the dragon, it will show that the game is won
class Verb_Summon(Verb):

   ```python
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

   ```
About the abbreviation of the two verbs summon and attack, I added a little association. In the movie Avengers, Dr. Strange summons a companion by drawing a circle, and the Japanese pronunciation of attack is tatakai, so they are abbreviated as o and t. These two abbreviations are not meant to avoid repeating other verbs.

Even if the player does not know Japanese and has not seen the superhero movie, he can win the game just as well by using the verb help.

In terms of the conditions for triggering the boss, I set it so that the boss will appear only if the player has passed all three rooms, and then the player will enter the win-lose condition determination

I did this by using the following code：

```python
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
                    print("You've been defeated by the dragon, you've failed.")
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
```
This code is the main loop function of a game, which includes a Boss function. In the main loop, the user can enter commands to play the game, and the Boss function is triggered if three items are collected and the current room is at 0. When the Boss function starts, the user will face a dragon with a life value of 2500, and the goal of the game is to defeat the dragon. If the player's life value drops below 0, the game is lost, and if the dragon's life value drops below 0, the game is won. In the Boss function, each time the user enters a command, the dragon will attack the player and the player's life value will be reduced accordingly. When the game ends, the program will exit.

----------------------------------------------------------------------------------------------