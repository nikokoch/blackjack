# BlackJack game

# all cards
import random

suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


# Card class
class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit


five_hearts = Card(suits[0], ranks[3])
ace_hearts = Card(suits[0], ranks[12])
ace_spades = Card(suits[2], ranks[12])
queen_hearts = Card(suits[0], ranks[10])
seven_hearts = Card(suits[0], ranks[5])


# One standard deck with all 52 unique cards
class StDeck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    # shuffles the deck
    def shuffle_deck(self):
        random.shuffle(self.deck)

    # gives the topmost card
    def deal_one(self):
        return self.deck.pop()


# Dealer as a class
class Dealer:

    def __init__(self):
        self.dealer_deck = []
        self.d_hand = []
        self.graveyard = []
        self.bank = 0
        st_deck = StDeck()

        # adds 6 shuffled standard decks to the dealer deck
        for x in range(6):
            st_deck.shuffle_deck()
            self.dealer_deck.extend(st_deck.deck)

    # the dealer deals one card
    def deal_card(self):
        dealed_card = self.dealer_deck.pop()
        self.graveyard.append(dealed_card)
        return dealed_card

    # the dealer hand
    def dhand_add(self, new_card):
        self.d_hand.append(new_card)

    # clearing the dealers hand
    def dhand_clear(self):
        self.graveyard.extend(self.graveyard)
        self.d_hand = []

    # refresh everthing for a new game
    def refresh_dealer(self):
        self.dealer_deck.extend(self.graveyard)
        random.shuffle(self.dealer_deck)

    # counts the value of the dealers hand
    def dhand_value(self):
        val = 0
        for x in range(len(self.d_hand)):
            val += self.d_hand[x].value

        return val


# Class of a player
class Player:

    def __init__(self, pname, pbalance):
        self.name = pname
        self.balance = pbalance
        self.hand = []
        self.splithand = []

    # prints players hand
    def show_hand(self):
        for x in range(len(self.hand)):
            print(self.hand[x])

    # adds a card to the players hand
    def add_hand(self, new_card):
        self.hand.append(new_card)

    # adds a card to the players hand
    def add_splithand(self, new_card):
        self.splithand.append(new_card)

    # calculates the value of the players hand as with ace=11 and ace =1 and returns the higher value hand
    def value_hand(self):
        value11 = 0
        value1 = 0
        for x in range(len(self.hand)):
            value11 += self.hand[x].value
            if self.hand[x].value == 11:
                value1 += 1
            else:
                value1 += self.hand[x].value

        # if the value is over 21, return with ace=1
        if value11 > 21:
            return value1
        else:
            return value11

    def clear_hand(self):
        self.hand = []


sam = Player('Sam', 50)


# tests for the functions above
# sam.add_hand(five_hearts)
# sam.show_hand()
# sam.add_hand(ace_hearts)
# sam.show_hand()
# print(sam.value_hand())
# sam.add_hand(queen_hearts)
# print(sam.value_hand())

# calculates int inputs so I don't have to have a thousand while-tries in my main program
def money_stuff():
    switch = True

    while switch:
        try:
            amount = int(input(''))
            return amount
        except:
            print('Versuchen Sie es erneut:')


# calculates blackjack reward based on plaer and dealer points and hand cards
def blackjack_reward(p, d, amount, phand):
    # blackjack == 21 points with the first two cards, while the dealer doesn't have blackjack
    if p == 21 and d != 21 and len(phand) == 2:
        amount *= 1.5

    # otherwise its 1:1
    else:
        amount *= 2
    return amount


print("")
print('GAME START - Player vs Dealer')

playing = True
rounds = 0

bot = Dealer()

# gets players name and balance
name = input('Wie ist Ihr Name? ')
print('')

print('Wilkommen {}. Wie viel möchten Sie auf Ihr Konto einzahlen? '.format(name))
balance = money_stuff()
print('Vielen Dank.')

player = Player(name, int(balance))

print('')

while playing and rounds < 6:

    rounds += 1

    enough_money = False

    while enough_money == False:  # FIXME

        # Start of the game: Player bets money
        print('Wieviel Geld wollen sie setzen?')
        bet = money_stuff()

        if player.balance >= bet:
            player.balance -= bet
            bot.bank += bet
            print('Ihr Kontostand beträgt nun {}€.'.format(player.balance))
            enough_money = True

        else:
            print('Ihr Kontostand ist zu niedrig, versuchen Sie es erneut.')

    print('')

    # round without betting
    play_round = True
    player.clear_hand()
    bot.dhand_clear()

    # Player and dealer get dealed a card
    bcard = bot.deal_card()
    player.add_hand(bcard)
    bot.dhand_add(bot.deal_card())

    print('Ihre Hand:')
    player.show_hand()
    print('')
    print('Sie zogen {} und Ihr Kartenwert beträgt nun {}.'.format(bcard, player.value_hand()))
    print('Die Karte des Dealers ist {}.'.format(bot.d_hand[0]))
    print('')

    # playing a round
    while play_round:

        # Players hand value is > 21
        if player.value_hand() > 21:
            print('Der Kartenwert Ihrer Hand ist größer als 21. Sie haben verloren')
            break

        # Players decision
        print('Wollen sie eine weitere Karte ziehen (hit), die Runde beenden (stand) oder aufgeben (surrender)?')
        print('Sie können Ihren Einsatz verdoppeln (double down) oder Ihre Hand aufteilen (split)')
        decision = input('Bei Aufgeben verlieren Sie nur ihren halben Einsatz.                                    '
                         '                         ')
        print('')

        # special double down choice only on the third turn
        dd = False

        # on a surrender, half of the bet is returned
        if decision == 'surrender':
            half = bet / 2
            player.balance += half
            bot.bank -= half

        # on a stand the dealer begins to draw
        elif dd or decision == 'stand':  # FIXME hit geht noch durch
            n_card = bot.deal_card()
            bot.dhand_add(n_card)
            print('Der Dealer zog {} und is somit bei {} Punkten.'.format(n_card, bot.dhand_value()))
            dd = False

            # if the dealer is under 16 points he has to draw again
            while bot.dhand_value() <= 16:
                print('Der Dealer zieht erneut.')
                a_card = bot.deal_card()
                bot.dhand_add(a_card)
                print('Der Dealer zog {} und is somit bei {} Punkten.'.format(a_card, bot.dhand_value()))

            # on 17+ points the dealer stand too
            # comparison of values to determine winner
            if bot.dhand_value() >= 17:

                # bot loses because he is over 21 points
                if bot.dhand_value() > 21:
                    win = blackjack_reward(player.value_hand(), bot.dhand_value(), bet, player.hand)
                    print('')
                    print('Ihr Kartenwert beträgt {}. '.format(player.value_hand()))
                    print('Der Kartenwert des Dealer beträgt {}.'.format(bot.dhand_value()))
                    print('Congratulations! You won! You earned {}€.')
                    bot.bank -= win
                    player.balance += win
                    play_round = False  # ends round

                # comparison, player wins
                elif bot.dhand_value() < player.value_hand():
                    win = blackjack_reward(player.value_hand(), bot.dhand_value(), bet, player.hand)
                    print('')
                    print('Ihr Kartenwert beträgt {}. '.format(player.value_hand()))
                    print('Der Kartenwert des Dealer beträgt {}.'.format(bot.dhand_value()))
                    print('Congratulations! You won! You earned {}€.'.format(win))
                    bot.bank -= win
                    player.balance += win
                    play_round = False  # ends round

                # comparison, dealer wins
                elif bot.dhand_value() > player.value_hand():
                    print('')
                    print('Ihr Kartenwert beträgt {}. '.format(player.value_hand()))
                    print('Der Kartenwert des Dealer beträgt {}.'.format(bot.dhand_value()))
                    print('Sie haben leider verloren! Sie verloren {}€.'.format(bet))
                    bot.bank += bet
                    player.balance -= bet
                    play_round = False  # ends round

                # draw, nothing happens
                elif bot.dhand_value() == player.value_hand():
                    print('')
                    print('Ihr Kartenwert beträgt {}. '.format(player.value_hand()))
                    print('Der Kartenwert des Dealer beträgt {}.'.format(bot.dhand_value()))
                    print('Unentschieden! Ihr Einsatz wird zurückgezahlt.')
                    bot.bank -= bet
                    player.balance += bet
                    play_round = False  # ends round
                print('')
                print('Runde: {}'.format(rounds))
                print('')

        # on a hit the player draws again
        elif decision == 'hit':
            a_card = bot.deal_card()
            player.add_hand(a_card)
            print('Ihre Hand:')
            player.show_hand()
            print('')
            print('Sie zogen {} und Ihr Kartenwert beträgt nun {}.'.format(a_card, player.value_hand()))
            print('')

            # if points are over 21, the player looses
            if player.value_hand() > 21:
                print('')
                print('Ihr Kartenwert beträgt {}. '.format(player.value_hand()))
                print('Der Kartenwert des Dealer beträgt {}.'.format(bot.dhand_value()))
                print('Sie haben leider verloren! Sie verloren {}€.'.format(bet))
                bot.bank += bet
                player.balance -= bet
                play_round = False  # ends round

        # only on the third round, doubles bet and player only gets one more card (dd)
        elif decision == 'double down' and len(player.hand) == 2:
            bet *= 2
            c_card = bot.deal_card()
            player.add_hand(c_card)
            print('Ihre Hand:')
            player.show_hand()
            print('')
            print('Sie zogen {} und Ihr Kartenwert beträgt nun {}. '
                  'Der Einsatz wurde verdoppelt.'.format(c_card, player.value_hand()))
            print('')
            dd = True

        else:
            print('Das war leider keine der möglichen Optionen "hit", "stand" oder "surrender"')

    print('')
    print('')

print('')
print('ERGEBNIS')
print('Vielen Dank, dass Sie uns heute beehrt haben. Ihr neuer Kontostand beträgt {}€'.format(player.balance))
