# Ali-Bagherzadeh Midterm-MEM680
#Fall 2022

from random import randint
import numpy as np
import sys

def converter(input_function):
    def convert_to_int():
        try:
            value = int(input_function())
            return value

        except:

            print(f"The input cannot be converted to an int")
            input_function()

    return convert_to_int()


class Dice:
    def __init__(self):
        # for initializing the dice
        self.dice = np.zeros(2)   # to define dice with matrix

    def roll_dice(self):
        self.dice[0] = randint(1, 6)  # Use random.randint() to simulate dice-rolling events dice number 1
        self.dice[1] = randint(1, 6)  # Use random.randint() to simulate dice-rolling events dice number 2


class Table(Dice):                    # define class table while inheriting the dice
    def __init__(self):
        super().__init__()
        self.point = False            # to determine the point is set or not


class player(Table):                  # define class for player
    def __init__(self):
        super().__init__()
        self.player_name = input("Please type your name: ")
        print(f"all the best, dear {self.player_name}!")        # saving player name and welcome!

        @converter
        def bankroller():
            return input("type money amount you want in your bankroll: ")  # to ask player money on the table

        self.bankroll = bankroller
        self.initial_bankroll = np.copy(bankroller)             # initial player money amount


class bets(player):
    def __init__(self):
        super().__init__()
        self.pass_line_bet = 0        # define class bets which are not given by input!
        self.do_not_pass_bet = 0
        self.max_odds_bet = 0
        self.odds_bet = 0


    def betting_turn(self):
        if input("Do you Want to place any bets? (please type y or n) ") == ("y" or "Y"):       # asking player bet amount and position
            self.current_bet = input("you want to bet on pass line or do not pass line? ")
            if self.current_bet.lower() == ("pass line"):
                self.bet_amount = self.ingest_bet()         # call ingest_ bet function to ask bet amount
                self.pass_line()                            # call pass_line function after having bet amount to check

            elif self.current_bet.lower() == ("do not pass line"):
                self.bet_amount = self.ingest_bet()         # call ingest_ bet function to ask bet amount
                self.do_not_pass()                          # call do_not_pass function after having bet amount to check
            else:
                print(
                    "you placed an invalid bet type, please place one of the implemented  bets"  # avoid player typo!
                )
                print("the 'pass line' and 'do not pass line'  are implemented")
                self.betting_turn()
        else:
            print("bye! You currently have no active bets!")     # exit when player do not place bet!
            sys.exit()

        self._print_bet_made()                             # call function to clear bet amount and position for player
        self.Shooter()

    def pass_line(self):
        if self.bankroll >= self.bet_amount:               # check bankroll-amount
            if self.point == False:
                self.pass_line_bet = self.bet_amount
                self.bankroll -= self.bet_amount
            else:
                print("you cannot bet the pass-line once the point is set!")
        else:
            self.insufficient_funds(self.bet_amount, "pass line")

    def do_not_pass(self):
        if self.bankroll >= self.bet_amount:
            if self.point == False:
                self.pass_line_bet = self.bet_amount
                self.bankroll -= self.bet_amount
            else:
                print("you cannot bet the pass line once the point is set!")

        else:
            self.insufficient_funds(self.bet_amount, "pass line")

    def insufficient_funds(self, bet, bet_position):
        print(
            f"{self.player_name} you have insufficient funds to place a ${bet} on the {bet_position}"
        )
        
    def ingest_bet(self):
        # This trys to see if the bet_amount is a valid int or can be converted into an int,
        try:
            bet_amount = input("How much do you want to bet?")
            self.bet_amount = int(bet_amount)

            if self.bet_amount > self.bankroll:
                print(
                    f" ${self.bet_amount} is more than the maximum you can bet,please try again!! "
                )
                self.bet_amount = 0

                self.ingest_bet()


            if self.bet_amount == 0 and not self.point:      # Exception if the value is 0 !
                print("you cannot play with a bet of $ 0!")

                # Resets the win condition
                self.bet_amount = 0
        except:
            print("please type an integer for the bet amount!, please try again!")
            # resets the win condition
            self.ingest_bet()
        return self.bet_amount

    def _print_bet_made(self):
        print(
            f"you placed a bet on the {self.current_bet} for ${self.bet_amount} \n your remaining is ${self.initial_bankroll - self.bet_amount} "
        )

    def _print_bet_won(self):
        print(
            f"your bet on the {self._winning_bet} for ${self.bet_amount} won! \n your remaining is ${self.bankroll}"
        )

    def _print_bet_lost(self):
        print(
            f"your bet on the {self.losing_bet} for ${self.losing_bet_amount} lost! \n your remaining is ${self.bankroll}"
        )

    # Rolls the dice by shooter command
    def Shooter(self):
        if self.pass_line_bet == 0 and self.do_not_pass_bet == 0:
            print("you have no active bets, you cannot roll")
        else:
            self.roll_dice()
            self.Payout()

    def Bet_loser(self, bet_name, bet_amount):
        if bet_amount > 0:
            self.losing_bet = bet_name
            self.losing_bet_amount = bet_amount
            self._print_bet_lost()
        return 0

    def Bet_winner(self, bet_name, bet_amount):
        if bet_amount > 0:
            self._winning_bet = bet_name
            self._winning_bet_amount = bet_amount
            self.bankroll = self.bankroll + self._winning_bet_amount
            if bet_name == "odds Bet":
                self.bankroll += self.odds_bet
                self.odds_bet = 0  # removes the odds bet
                self.point = False
            self._print_bet_won()

    def odds(self):
        if self.pass_line_bet > 0:
            max_bet = np.min([self.bankroll, self.max_odds_bet])
            print(
                f"You can place a maximum odds bet of up to ${max_bet}, your current bankroll is ${self.bankroll}"
            )
            self.odds_bet = self.ingest_bet()
            self.bankroll -= self.odds_bet
            print(
                f"you placed a ${self.odds_bet} odds bet, Good Luck!, your bankroll is ${self.bankroll}"
            )

    # payout function
    def Payout(self):
        if self.point == False:

            if np.sum(self.dice) in [7, 11]:
                # Pass Line Winner when sum dice is 7, 11
                self.Bet_winner("Pass Line", self.pass_line_bet)

                # Do Not Pass Line Loser
                self.do_not_pass_bet = self.Bet_loser("Do Not Pass", self.do_not_pass_bet)

            elif np.sum(self.dice) in [2, 3]:
                # Do Not Pass Winner
                self.Bet_winner("Do Not Pass", self.do_not_pass_bet)

                # Pass Line Loser
                self.pass_line_bet = self.Bet_loser("Pass Line", self.pass_line_bet)

            elif np.sum(self.dice) in [12]:
                # Pass line loser
                self.pass_line_bet = self.Bet_loser("pass Line", self.pass_line_bet)

            elif np.sum(self.dice) in [4, 5, 6, 0, 9, 10]:
                self.point = np.sum(self.dice)
                print(f"A point of {self.point} has been set!")

                if np.sum(self.dice) in [4, 10]:
                    self.max_odds_bet = self.pass_line_bet * 3
                elif np.sum(self.dice) in [5, 9]:
                    self.max_odds_bet = self.pass_line_bet * 4
                elif np.sum(self.dice) in [6, 8]:
                    self.max_odds_bet = self.pass_line_bet * 5

                self.odds()
                input("Press any key to roll")
                self.Shooter()

            else:
                print('Something is strange with your dice')

        elif self.point in [4, 5, 6, 8, 9, 10]:

            if np.sum(self.dice) == self.point:


                self._winning_bet_amount = self.pass_line_bet  # odds Bet Winner

                if self.point in [4, 10]:
                    self._winning_bet_amount += self.odds_bet * 2
                elif self.point in [5, 9]:
                    self._winning_bet_amount += self.odds_bet * (3 / 2)
                elif self.point in [6, 8]:
                    self._winning_bet_amount += self.odds_bet * (6 / 5)

                self.Bet_winner("Odds Bet", self._winning_bet_amount)

                self.point = False

                # Do Not Pass Line Loser
                self.do_not_pass_bet = self.Bet_loser("Do Not Pass", self.do_not_pass_bet)
                self.Shooter()

            elif np.sum(self.dice) == 7:
                self.point = False

                # Pass Line Loser
                self.pass_line_bet = self.Bet_loser("Pass Line", self.pass_line_bet)

                # Pass Line Loser
                self.odds_bet = self.Bet_loser("odds Bet", self.odds_bet)

                # Do Not Pass Winner
                self.Bet_winner("Do Not Pass", self.do_not_pass_bet)

            else:
                roll_again = input(
                    f"you rolled a {np.sum(self.dice)}, no winners or losers. press any key to roll again"
                )
                self.Shooter()
        else:
            pass

        if self.pass_line_bet == 0 and self.do_not_pass_bet == 0:
            if self.bankroll == 0:
                print("you have lost all of your money!")
            else:
                walk = input(
                    f"You currently have no active bets, Would you like to walk away with {self.bankroll} or play "
                    f"more, please type 'y' or 'n'? "
                )
                if walk in ("y", "Y"):
                    if self.bankroll > self.initial_bankroll:
                        print(
                            f"you walked away winning ${self.bankroll - self.initial_bankroll}"
                        )
                        sys.exit()
                    else:
                        print(
                            f"You walked away losing ${self.initial_bankroll - self.bankroll}"
                        )
                        sys.exit()
                else:
                    self.betting_turn()
        else:
            if self.pass_line_bet != 0:
                input(f"You have a pass line bet of ${self.pass_line_bet}, press any key to roll!")
                self.Shooter()
            elif self.do_not_pass_bet != 0:
                input(f"You have a do not pass line bet of ${self.pass_line_bet}, press any key to roll!")
                self.Shooter()


# stat the game
a = input("TO START THE GAME TYPE 'yes' and TO QUIT TYPE 'no'\n")
if a.lower() == "no":
    sys.exit()
else:
    print("LET'S START THE GAME")

# those who need instructions can ask for it,
# others can start the game directly.
a = input(
    "welcome to the game of chance,are you ready to test your fortune ,\ndo you need instructions type (yes) or (no) \n")

if a.lower() == "yes":
    print(''' 
              1. player rolls two six-sided dice and adds the numbers rolled together.
              2. On this first roll, a 7 or an 11 automatically wins, and a 2, 3, or 12automatically loses, and play is over.
                 If a 4, 5, 6, 8, 9, or 10 are rolled on this first roll, that number becomes the 'point.'
              3. The player continues to roll the two dice again until one of two things happens:
                 either they roll the 'point' again, in which case they win; or they roll a 7, in which case they lose.''')

elif a.lower() == "no":
    print("Ok, lets Go!")

player = bets()
player.betting_turn()
