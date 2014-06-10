# Implementation of simplified version of Blackjack

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# load card images - 949x392
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("https://dl.dropboxusercontent.com/u/38413745/blackjack_cards.png")

# back image for dealers hole card
CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("https://dl.dropboxusercontent.com/u/38413745/blackjack_card_back.png")    

# global variables
in_play = False
outcome = ""
message = ""
last_game = ""
score = 0
card_deck = []
player_hand = []
dealers_hand = []

# global variable for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# hand class
class Hand:
    def __init__(self):
        self.hand_cards = []

    def __str__(self):
        s = "Hand contains"
        for card in self.hand_cards:
            s = s + " " + str(card)
        return s 

    def add_card(self, card):
        self.hand_cards.append(card)	# add a card object to a hand

    def get_value(self):
        has_ace = False
        value = 0
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        for card in self.hand_cards:
            value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                has_ace = True
        
        if has_ace:
            if value + 10 <= 21:
                value = value + 10

        return value

    def draw(self, canvas, pos):
        for card in self.hand_cards:
            card.draw(canvas, pos)
            pos[0] += 100
 
        
# deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        s = "Deck contains"
        for card in self.deck:
            s = s + " " + str(card)
        return s         # return a string representing the deck

# event handlers for buttons
def deal():
    global outcome, in_play, card_deck, player_hand, dealers_hand, message, score
    message = ""
    outcome = "Hit or Stand?"
    card_deck = Deck()
    player_hand = Hand()
    dealers_hand = Hand()
    card_deck.shuffle()
    #print card_deck  # for debugging purposes
    if in_play:         # player losses point, if player press "Deal" button in between the playing hand
        last_game = "Lost"
        score -= 1
    for i in range(2):
        player_hand.add_card(card_deck.deal_card())
        dealers_hand.add_card(card_deck.deal_card())
    #for debugging purposes
    #print "Player: ", player_hand  
    #print "Dealer: ", dealers_hand 
    #print card_deck
    in_play = True
    

def hit():
    global player_hand, in_play, score, outcome, message, last_game
    if in_play:                          # if the hand is in play, hit the player
        if player_hand.get_value() < 21:
            player_hand.add_card(card_deck.deal_card())
            outcome = "Hit or Stand?"
            #print "Player: ", player_hand
        if player_hand.get_value() > 21: # if busted, assign a message to outcome, update in_play and score
            in_play = False
            score -= 1
            message = "You have busted"  
            outcome = "New deal?" 
            last_game = "Lost"
       
def stand():
    global score, in_play, dealers_hand, player_hand, outcome, message, last_game
    dealer_stay = 17
    if not in_play:
        message = "You have busted"
    else:
        if player_hand.get_value() <17:
            dealer_stay = player_hand.get_value()
        while dealers_hand.get_value() < dealer_stay:  # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
            dealers_hand.add_card(card_deck.deal_card()) 
        if dealers_hand.get_value() > 21:  # assign a message to outcome, update in_play and score
            message = "Dealer have busted!!! You won"
            last_game = "Won"
            score += 1
        elif dealers_hand.get_value() >= player_hand.get_value():
            message = "Dealer won!!!"
            score -= 1
            last_game = "Lost"
        else:
            message = "You won"
            last_game = "Won"
            score += 1
        outcome = "New deal?"
        in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global dealers_hand, player_hand, outcome, message, in_play, last_game
    canvas.draw_text("Blackjack", (50, 50), 48, "Red")
    canvas.draw_text("Score: " + str(score), (300, 50), 48, "White")
    canvas.draw_text("Last Game: " + last_game, (300, 100), 30, "White")
    canvas.draw_text("Dealer", (50, 125), 30, "Black")
    canvas.draw_text("Player", (50, 325), 30, "Black")
    canvas.draw_text(message, (50, 500), 30, "White")
    canvas.draw_text(outcome, (300,325), 30, "White")
    dealer_pos = [50, 150]
    dealers_hand.draw(canvas, dealer_pos)
    player_hand.draw(canvas,[50, 350])
    if in_play:  # if hand is in play, it hides the dealers hole card
        canvas.draw_image(card_back,CARD_BACK_CENTER, CARD_BACK_SIZE, (50 + CARD_BACK_CENTER[0],150 + CARD_BACK_CENTER[1]), CARD_BACK_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

deal()
frame.start()
