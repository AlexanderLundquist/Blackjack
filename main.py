




#Game Class
class Player(object):
    # A player for a game
    def __init__(self,name,score = 0):
        self.name = name
        self.score = score
    
    def __str__(self):
        rep = self.name + ":\t" + str(self.score)
        return rep
    
    def ask_yes_no(question):
        #Ask a yes or no question
        response = None
        while response not in ("y","n"):
            response = input(question).lower()
        return response
    
    def ask_number(question,low,high):
        #Ask for a number within a range
        response = None
        while response not in range(low,high):
            response = int(input(question))
        return response














#Card class
class Card(object):
    # A playing card
    RANKS = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    SUITS = ["c","d","h","s"]

    def __init__(self,rank,suit,face_up = True):
        self.rank = rank
        self.suit = suit
        self.is_face_up = face_up
    
    def __str__(self):
        if self.is_face_up:
            rep = self.rank + self.suit
        else:
            rep = "XX"
        return rep
    
    def flip(self):
        self.is_face_up = not self.is_face_up

class Hand(object):
    # A hand of playing cards
    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:
            rep = ""
            for card in self.cards:
                rep += str(card) + "\t"
        else:
            rep = "<empty>"
        return rep

    def clear(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def give(self,card,other_hand):
        self.cards.remove(card)
        other_hand.add(card)



class Deck(Hand):

    def populate(self):
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.add(Card(rank,suit))

    def shuffle(self):
        import random
        random.shuffle(self.cards)
    
    def deal(self,hands, per_hand = 1):
        for rounds in range(per_hand):
            for hand in hands:
                if self.cards:
                    top_card = self.cards[0]
                    self.give(top_card,hand)
                else:
                    print("Cant continue to deal, Out of cards!")



class BJ_Card(Card):
    #A Blackjack Card
    ACE_VALUE = 1
    
    def get_value(self):
        if self.is_face_up:
            value = BJ_Card.RANKS.index(self.rank) + 1

            if value > 10:
                value = 10
            else:
                value = None
            return value
    value = property(get_value)


class BJ_Deck(Deck):
    # A blackjack deck
    def populate(self):
        for suit in BJ_Card.SUITS:
            for rank in BJ_Card.RANKS:
                self.cards.append(BJ_Card(rank,suit))
    
class BJ_Hand(Hand):
    # A blackjack hand
    def __init__(self,name):
        super(BJ_Hand).__init__()
        self.name = name
    
    def __str__(self):
        rep = self.name + ":\t" + super(BJ_Hand, self).__str__()
        if self.total:
            rep += "(" +str(self.total)+")"
        return rep
    
    def get_total(self):
        #if a card in the hand has value of None, then total is None
        for card in self.cards:
            if not card.value:
                return None
        
        #add up card values, treat each Ace as 1
        total = 0
        for card in self.cards:
            total += card.value
        
        #determine if hand contains an Ace
        contains_ace = False
        for card in self.cards:
            if card.value == BJ_Card.ACE_VALUE:
                contains_ace = True
        
        # if hand contains Ace and total is low enough, treat Ace as 11
        if contains_ace and total <= 11:
            # add only 10 since we have already added 1 for the Ace
            total += 10
        return total
    total = property(get_total)
    
    def is_busted(self):
        return self.total > 21
    


class BJ_Player(BJ_Hand):
    # A Blackjack player
    def is_hitting(self):
        response = Player.ask_yes_no("\n"+self.name + ", do you want to hit? (Y/N): ")
        return response =="y"
    
    def bust(self):
        print(self.name,"Busts.")
        self.lose()
    
    def lose(self):
        print(self.name,"Lose...")

    def win(self):
        print(self.name,"Wins!")

    def push(self):
        print(self.name,"Pushes")


class BJ_Dealer(BJ_Hand):
    #A Blackjack dealer
    def is_hitting(self):
        return self.total < 17
    
    def bust(self):
        print(self.name,"Busts.")
    
    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()

class BJ_Game(object):
    # A Blackjack game
    def __init__(self,names):
        self.players = []
        for name in names:
            player = BJ_Player(name)
            self.players.append(player)

        self.dealer = BJ_Dealer("Dealer")
        self.deck = BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()

    def get_still_playing(self):
        remaining = []
        
        for player in self.players:
            if not player.is_busted():
                remaining.append(player)
        return remaining
    still_playing = property(get_still_playing)

    def additional_cards(self,player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()

    def play(self):
        """
        The function plays the game by dealing two cards to each player and the dealer, then dealing
        additional cards to the players, then dealing additional cards to the dealer, and then comparing
        the players' hands to the dealer's hand.
        """
        # deal initial 2 card to everyone
        self.deck.deal(self.players + [self.dealer], per_hand = 2)
        self.dealer.flip_first_card() # Hide first card for dealer
        for player in self.players:
            print(player)
        print(self.dealer)

        #deal additional cards to players
        for player in self.players:
            self.additional_cards(player)
    
        self.dealer.flip_first_card() # reveal dealers first card

        if not self.still_playing:
            #since all players have busted, just show the dealers hand
            print(self.dealer)
        else:
            #deal additional cards to dealer
            print(self.dealer)
            self.additional_cards(self.dealer)

        if self.dealer.is_busted():
            #Everyone still playing wins
            for player in self.still_playing:
                player.win()
        else:
            #compare each player still playing to dealer
            for player in self.still_playing:
                if player.total > self.dealer.total:
                    player.win()
                elif player.total < self.dealer.total:
                    player.lose()
                else:
                    player.push()
    
        for player in self.player:
            player.clear()
        self.dealer.clear()





def main():
    print("\t\tWelcome to Blackjack\n")

    names = []
    number = input("How man player? (1-7): ")

    for i in range(int(number)):
        name = input("Enter player name: ")
        names.append(name)

    # print("\nWe have the following people entering the table...")
    # for i in range(int(names)):
    #     print(i + "\n")
    
    game = BJ_Game(names)

    again = None
    while again != "n":
        game.play()
        again = Player.ask_yes_no("\nDo you want to play again?: ")


if __name__ == "__main__":
    main()
    









