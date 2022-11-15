from random import randint
import numpy as np
import sys

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
    print(''' 1. player rolls two six-sided dice and adds the numbers rolled together.
              2. On this first roll, a 7 or an 11 automatically wins, and a 2, 3, or 12automatically loses, and play is over.
                 If a 4, 5, 6, 8, 9, or 10 are rolled on this first roll, that number becomes the 'point.'
              3. The player continues to roll the two dice again until one of two things happens:
                 either they roll the 'point' again, in which case they win; or they roll a 7, in which case they lose.''')

elif a.lower() == "no":
    print("all the best, player")

def converter(input_function):
    def convert_to_int():
        try:
            value = int(input_function())
            return value

        except:

            print(f"The value entered cannot be converted to an int")
            input_function()

    return convert_to_int()


class Dice:
    def __init__(self):
        # initialize the dice
        self.dice = np.zeros(2)

    def roll_(self):
        self.dice[0] = randint(1, 6)
        self.dice[1] = randint(1, 6)


class Table(Dice):
    def __init__(self):
        super().__init__()
        self.point = False


class player(Table):
    def __init__(self):
        super().__init__()
        self.name = input("type the name of the player: ")

        @converter
        def bankroller():
            return input("type in your bankroll")

        self.bankroll = bankroller
        self.initial_bankroll = np.copy(bankroller)


class bets(player):
    def __init__(self):
        super().__init__()
        self.pass_line_bet = 0
        self.do_not_pass_bet = 0
        self.odds_bet = 0
        self.max_odds_bet = 0

    def insufficient_funds(self, bet, bet_position):
        print(
            f"{self.name} has insufficient funds to place a %(bet) on the {bet_position}"
        )

    def pass_line(self):
        if self.bankroll >= self.bet_amount:
            if not self.point:
                self.pass_line_bet = self.bet_amount
                self.bankroll -= self.bet_amount
            else:
                print("you cannot bet the passline once the point is set!")
        else:
            self.insufficient_founds(self.bet_amount, "pass line")

    def do_not_pass(self):
        if self.bankroll >= self.bet_amount:
            if not self.point:
                self.pass_line_bet = self.bet_amount
                self.bankroll -= self.bet_amount
            else:
                print("you cannot bet the passline once the point is set!")

        else:
            self.insufficient_founds(self.bet_amount, "pass line")

    def betting_turn(self):
        if input("Do you Want to place any bets? (y/n) ") == ("y" or "Y"):
            self.current_bet = input("where do you want to bet?")
            if self.current_bet.lower() == "pass line":
                self.bet_amount = self.ingest_bet()
                self.pass_line()

            elif self.current_bet.lower() == "do not pass":
                self.bet_amount = self.ingest_bet()
                self.do_not_pass()
            else:
                print(
                    "you placed an invalid bet type, please place one of the implemented  bets"
                )
                print("the pass line and do not pass line are implemented")
                self.betting_turn()
        self._print_bet_made()
        self.Shooter()

    def ingest_bet(self):
        # This trys to see if the bet_amountis a valid int or can be converted into an int,
        try:
            bet_amount = input("How much do you want to bet?")
            self.bet_amount = int(bet_amount)

            if self.bet_amount > self.bankroll:
                print(
                    f"you are trying to be more money %({self.bet_amount}) than the maximum you c "
                )
                self.bet_amount = 0

                self.ingest_bet()

            # Exception if the value is 0, a more elegant way would be with FF

            if self.bet_amount == 0 and not self.point:
                print("you cannot playwith a bet of 0!")

                # Resets the win condition
                self.bet_amount = 0

        except:
            print("A value other than an int was used for the bet amount")
            # resets the win condition
            self.ingest_bet()
        return self.bet_amount

    def _print_bet_made(self):
        print(
            f"you placed a bet on the {self.current_bet} for %{self.bet_amount} \n your remaining"
        )

    def _print_bet_won(self):
        print(
            f"your bet on the {self._winning_bet} for %{self.bet_amount} won! \n your re..."
        )

    def _print_bet_lost(self):
        print(
            f"your bet on the {self._losing_bet} for %{self._losing_bet_amount} lost! \n your.."
        )

    # Rolls the dice
    def Shooter(self):
        if self.pass_line_bet == 0 and self.do_not_pass_bet == 0:
            print("you have no active bets, you cannot roll")
        else:
            self.roll_()
            self.Payout()

    def Bet_loser(self, bet_name, bet_amount):
        if bet_amount > 0:
            self._losing_bet = bet_name
            self.losing_bet_amount = bet_amount
            self._print_bet_lost()
        return 0

    def Bet_winner(self, bet_name, bet_amount):
        if bet_amount > 0:
            self._winning_bet = bet_name
            self._winning_bet_amount = bet_amount
            self.bankroll += self._winning_bet_amount
            if bet_name == "odds Bet":
                self.bankroll += self.odds_bet
                self.odds_bet = 0  # removes the odds bet
                self.point = False
            self._print_bet_won()

    def odds(self):
        if self.pass_line_bet > 0:
            max_bet = np.min([self.bankroll, self.max_odds_bet])
            print(
                f"You canplace a maximum odds bet of up to %{max_bet}, your current bankroll is ???? %{self.bankroll}.???"
            )
            self.odds_bet = self.ingest_bet()
            self.bankroll = self.odds_bet
            print(
                f"you placed a %{self.odds_bet} odds bet, Good Luck!, your bankroll is %{self.bankroll}???????"
            )

    # payout
    def Payout(self):
        if not self.point:

            if np.sum(self.dice) in [7, 11]:
                # Pass Line Winner
                self.Bet_winner("Pass Line", self.pass_line_bet)

                # Do Not Pass Line Loser
                self.do_not_pass_bet = self.Bet_loser(
                    "Do Not Pass", self.do_not_pass_bet
                )

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
                    self.max_odds_bet = self.pass_line_bet = 3
                elif np.sum(self.dice) in [5, 9]:
                    self.max_odds_bet = self.pass_line_bet = 4
                elif np.sum(self.dice) in [6, 0]:
                    self.max_odds_bet = self.pass_line_bet = 5

                self.odds()
                input("Press any key to roll? ")
                self.Shooter()
            else:
                print('Something is strange with your dice')

        elif self.point in [4, 5, 6, 8, 9, 10]:

            if np.sum[self.dice] == self.point:

                # odds Bet Winner
                self._winning_bet_amount = self.pass_line_bet

                if self.point in [4, 10]:
                    self._winning_bet_amount += self.odds_bet * 2
                elif self.point in [5, 9]:
                    self._winning_bet_amount += self.odds_bet * (3 / 2)
                elif self.point in [6, 8]:
                    self._winning_bet_amount += self.odds_bet * (6 / 5)

                self.Bet_winner("Odds Bet", self._winning_bet_amount)

                self.point = False

                # Do Not Pass Line Loser
                self.do_not_pass_bet = self.Bet_loser(
                    "Do Not Pass", self.do_not_pass_bet
                )
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
                    f"you rolled a {np.sum(self.dice)}, no winners or losers. press any key..????"
                )
                self.Shooter()
        else:
            pass

        if self.pass_line_bet == 0 and self.do_not_pass_bet == 0:
            if self.bankroll == 0:
                print("you have lost all of your money!")
            else:
                walk = input(
                    f"You currently have no active bets, Would you like to walk away with ???/ {self.bankroll}????"
                )
                if walk in ("y", "Y"):
                    if self.bankroll > self.initial_bankroll:
                        print(
                            f"you walked away winning %{self.bankroll - self.initial_bankroll}"
                        )
                    else:
                        print(
                            f"You walked away losing %{self.initial_bankroll - self.bankroll}"
                        )
                else:
                    self.betting_turn()
        else:
            if self.pass_line_bet != 0:
                input(f"You have a pass line bet of %{self.pass_line_bet}, press any key to roll")
            elif self.do_not_pass_bet != 0:
                input(f"You have a do not pass line bet of %{self.pass_line_bet}, press any key to roll ????")

            self.Shooter()
