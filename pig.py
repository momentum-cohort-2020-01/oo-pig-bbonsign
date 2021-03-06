import random as rand
from time import sleep
from game_stats import update_stats, print_stats, clear_stats

OPPONENTS = ['Bot', 'Bot15', 'Bot20', 'Bot25', 'Bot30', 'Bot35']
OPENING_TEXT = """
- Bot
- Bot15
- Bot20
- Bot25
- Bot30
- Bot35
Name your opponent: """


# For formatting some of the print statements
def center(value):
    return str(value).center(15)


class Game:
    def __init__(self, die_size):
        self.die_size = die_size
        self.player1 = Player('Human')
        # self.player2 = Bot()
        self.die = Die(die_size)
        self.stop = False
        self.winner = 0
        self.start_game()

    last_winner = None

    def __str__(self):
        return "A game of Pig"

    def start_game(self):
        """
        Choose a random player to start with,
        otherwise the previous loser starts
        """
        if Game.last_winner is None:
            opponent = input(OPENING_TEXT)
            while opponent not in OPPONENTS:
                opponent = input(OPENING_TEXT)
            if opponent == 'Bot':
                self.player2 = Bot()
            else:
                self.player2 = Robot(opponent)

            if rand.choice([0, 1]) == 1:
                self.player1, self.player2 = self.player2, self.player1
        elif Game.last_winner == 'Human':
            opponent = input(OPENING_TEXT)
            while opponent not in OPPONENTS:
                opponent = input(OPENING_TEXT)
            risk = opponent.split('Bot')[1]
            if risk == '':
                self.player2 = Bot()
            else:
                self.player2 = Robot(str(risk))
            self.player1, self.player2 = self.player2, self.player1
        else:
            self.player2 = Robot(Game.last_winner)

        self.update()

    def print_turn(self, player):
        player_announce = f"{player.name} player's turn"
        print(f"{' '*20}{player_announce}")
        print(f"{' '*20}{'='*len(player_announce)}\n")

    def print_state(self):
        player1 = self.player1
        player2 = self.player2

        print(f"{'_'*60}\n")
        print(f"{' '*11}{' '*14}{'Totals:'}")
        print(f"{' '*11}{'='*34}")
        print(f"{' '*11}|{center(player1.name)}||{center(player2.name)}|")
        print(f"{' '*11}|{center(player1.score)}||{center(player2.score)}|")
        print(f"{' '*11}{'='*34}")


    def end_game(self):
        sleep(1)
        print(f"{'*'*60}\n{'*'*60}")
        print(f"{' '*11}The {self.winner} player is the winner!!!")
        print(f"{'*'*60}\n{'*'*60}")

        update_stats(self.winner.name)
        Game.last_winner = self.winner.name
        print_stats()
        sleep(.7)
        newgame = input("Play again? (y) or (n): ")
        while not(newgame == 'y' or newgame == 'n'):
            newgame = input("Play again? (y) or (n): ")
        if newgame == 'n':
            return
        elif newgame == 'y':
            Game(self.die_size)

    def update(self):
        die = self.die
        while not self.stop:
            self.print_turn(self.player1)
            self.player1.turn(die)
            self.print_state()
            if self.player1.score >= 100:
                self.winner = self.player1
                self.stop = True
                break
            self.print_turn(self.player2)
            self.player2.turn(die)
            self.print_state()
            if self.player2.score >= 100:
                self.winner = self.player2
                self.stop = True
                break
        self.end_game()


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hold = 0
        self.action = 'roll'

    def __str__(self):
        return self.name

    def roll(self, die):
        value = die.roll()
        if value == 1:
            self.hold = 0
            self.action = 'hold'
            self.update_score()
        else:
            self.hold += value
        return value

    def update_score(self):
        self.score += self.hold
        self.hold = 0

    def turn(self, die):
        while self.action == 'roll':
            value = self.roll(die)
            if value == 1:
                print(f"  {self.name} player rolled a pig. Now its the other player's turn\n")
                sleep(1.3)
                break
            print(f"  {self.name} player rolled {value}. The running total is {self.hold}\n")
            inp = input('  roll or hold?: ')
            while not(inp == 'roll' or inp == 'hold'):
                inp = input('  roll or hold?: ')
            if inp == 'hold':
                self.action = 'hold'
                self.update_score()
            elif inp == 'roll':
                continue
        self.action = 'roll'  # reset action so the next turn works the same


class Bot(Player):
    def __init__(self):
        super().__init__('Bot')

    def turn(self, die):
        while self.action == 'roll':
            sleep(1)
            value = self.roll(die)
            if value == 1:
                print(f"  {self.name} player rolled a pig. Now its the other player's turn\n")
                break
            print(f"  {self.name} player rolled {value}. The running total is {self.hold}\n")

            threshold = rand.randint(15, 30)
            if self.score+self.hold >= 100:
                self.action = 'hold'
                self.update_score()
            elif self.hold >= threshold:
                self.action = 'hold'
                self.update_score()
            else:
                continue
        self.action = 'roll'  # reset action so the next turn works the same


class Robot(Player):
    '''
    Possible names of the form: Bot##
    '''
    def __init__(self, name):
        super().__init__(name)
        self.threshold = int(self.name.split('Bot')[1])

    def turn(self, die):
        while self.action == 'roll':
            sleep(1)
            value = self.roll(die)
            if value == 1:
                print(f"  {self.name} player rolled a pig. Now its the other player's turn\n")
                break
            print(f"  {self.name} player rolled {value}. The running total is {self.hold}\n")

            if self.score + self.hold >= 100:
                self.action = 'hold'
                self.update_score()
            elif self.hold >= self.threshold:
                self.action = 'hold'
                self.update_score()
            else:
                continue
        self.action = 'roll'  # reset action so the next turn works the same


class Die:
    def __init__(self, sides):

        self.values = [i for i in range(1, sides+1)]

    def __str__(self):
        return f"{len(self.values)}-sided die"

    def roll(self):
        return rand.choice(self.values)


# if __name__ == '__main__':
#     print_stats()
#     Game(88)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Game of pig against a bot. Keeps tracks of wins',
                                     epilog='Oink! Oink!')
    parser.add_argument('mode', type=str, action='store', nargs='?',
                        default="play",
                        help="Defaults to 'play' to play a game of Pig against a bot, or 'stats' to view game statistics")
    parser.add_argument('-r', '--reset', action='store_true', help='Reset game statistics')
    args = parser.parse_args()

    if args.reset:
        clear_stats()

    if args.mode == 'play':
        Game(6)
    elif args.mode == 'stats':
        print_stats()
    else:
        print("Invalid arguments")
        exit(1)
