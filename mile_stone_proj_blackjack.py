import random
from enum import Enum


class HandStatus(Enum):
    bust = 1
    blackJack = 2
    playable = 3
    surrender = 4


class Card(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def __str__(self):
        return self.name

        
class Deck(object):
    remainingCards = []
    
    def __init__(self, decks=1):
        self.numberOfDecks = decks
        self.shuffle()
      
    def shuffle(self):
        for x in range(self.numberOfDecks):
            for suit in ['clubs', 'diamonds', 'hearts', 'spades']:
                for value in [('Ace',1), ('Two',2), ('Three',3), ('Four',4), ('Five',5), ('Six',6), ('Seven',7), ('Eight',8), ('Nine',9), ('Ten',10), ('Jack',10), ('Queen',10), ('King',10)]:
                    self.remainingCards.append(Card('{v} of {s}'.format(v=value[0],s=suit), value[1]))
                    
        random.shuffle(self.remainingCards)
                
    def draw(self):
        if len(self.remainingCards) == 0:
            self.shuffle()
            
        toRemove = random.randint(0,len(self.remainingCards)-1)
        return self.remainingCards.pop(toRemove)
    

class Player(object):
    currentBet = 0
        
    def __init__(self,name,bankRoll):
        self.name = name
        self.bankRoll = bankRoll
        self.resetHand()
    
    def deposit(self, amount):
        self.bankRoll += amount
        
    def withdraw(self, amount):
        self.bankRoll -= amount

    def newHand(self):
        self.resetHand()
        
    def resetHand(self):
        self.handTotals = [0]
        self.hand = []
        self.handStatus = HandStatus.playable
        self.best = 0
        self.split = False
        
    def addCard(self, card):
        self.hand.append(card)
        self.handTotals = self.computeHandTotals(card, self.handTotals)
        
    def computeHandTotals(self, card, currentTotals):
        newTotals = []
        
        for value in currentTotals:
            newTotals.append(value + card.value)
            
            if card.value == 1:
                newTotals.append(value + 11)
            
        return newTotals
    
    def checkHandStatus(self):
        if self.handTotals.count(21) > 0 and len(self.hand) == 2:
            self.handStatus = HandStatus.blackJack
            return self.handStatus
        
        bust = True
        
        for value in self.handTotals:
            if value <= 21:
                bust = False
                
                if value > self.best:
                    self.best = value
                
        if bust:
            self.handStatus = HandStatus.bust
        else:
            self.handStatus = HandStatus.playable
            
        return self.handStatus
        
    def takeTurn(self):
        round = 1
           
        while True:
            if self.checkHandStatus() == HandStatus.blackJack:
                break
        
            self.printCurrentHand()
            print '1. Hit'
            print '2. Stand'
            print '3. Double down'
            
            if round == 1:
                print '4. Surrender'
                
                if self.hand[0].value == self.hand[1].value and not isinstance(self, SplitPlayer):
                    print '5. Split'
                    
            choice = raw_input('Enter your choice: ')
            
            if choice == '1':
                card = deck.draw()
                print 'Card drawn: {a}'.format(a=card.name)
                self.addCard(card)
                
                if self.checkHandStatus() == HandStatus.bust:
                    print 'Bust!!!, you\'re out'
                    break
                    
            elif choice == '2':
                break
            elif choice == '3':
                if self.canDoubleDown():
                    self.currentBet = self.currentBet * 2
                    card = deck.draw()
                    print 'Card drawn: {a}'.format(a=card.name)
                    self.addCard(card)
                
                    if self.checkHandStatus() == HandStatus.bust:
                        print 'Bust!!!, you\'re out'
                        
                    break
                else:
                    print 'Not enough in your bankroll...'
                    continue
            elif choice == '4':
                self.handStatus = HandStatus.surrender
                break
            elif choice == '5':
                if self.canDoubleDown():
                    self.split = True
                    cardLeft = self.hand[0]
                    cardRight = self.hand[1]
                    self.resetHand()
                    self.addCard(cardLeft)
                    self.addCard(deck.draw())
                    splitPlayer = SplitPlayer(self.name, self.currentBet, self, [cardRight, deck.draw()])
                    players.insert(players.index(self)+1, splitPlayer)
                else:
                    print 'Not enough in your bankroll...'
                    continue
            else:
                print 'Invalid Option'
                continue
                
            round += 1
            
            
     
    def canDoubleDown(self):
        if self.currentBet * 2 <= self.bankRoll:
            if self.split:
                if self.currentBet * 3 <= self.bankRoll:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False
     
    
    def printCurrentHand(self):
        print '\nPlayer: {a}, current hand:'.format(a=self.name)
        
        for card in self.hand:
            print card.name
        
        print ''
        

class SplitPlayer(Player):
    def __init__(self, name, bet, parentPlayer, cards):
        Player.__init__(self, '{a} *split hand*'.format(a=name), 0)
        self.parentPlayer = parentPlayer
        self.currentBet = bet
        
        for card in cards:
            self.addCard(card)
            
    def canDoubleDown(self):
        if self.currentBet * 2 + self.parentPlayer.currentBet <= self.parentPlayer.bankRoll:
            return True
        else:
            return False
        

class Dealer(Player):
    stayOn = 18
    
    def __init__(self):
        Player.__init__(self, 'Computer Dealer', 0)
        
    def takeTurn(self):
        print ''
        self.printCurrentHand()
            
        if self.checkHandStatus() == HandStatus.blackJack:
            return
        
        allPlayersBustOrSurrender = True
        
        for player in players:
            if player.handStatus != HandStatus.bust and player.handStatus != HandStatus.surrender:
                allPlayersBustOrSurrender = False
                
        if allPlayersBustOrSurrender:
            return
        
        while self.handStatus == HandStatus.playable and self.best < self.stayOn:
            card = deck.draw()
            print 'Drew card: {a}'.format(a=card.name)
            self.addCard(card)
            self.checkHandStatus()
            
            if self.handStatus == HandStatus.bust:
                print 'Dealer Busts !!!!'
                break
            
            print ''
            self.printCurrentHand()

        
class Game(object):
    def __init__(self, players, deck):
        self.players = players
        self.deck = deck
        
        for player in players:
            betStr = raw_input('{a}, enter bet amount, current bankroll is, {b} :'.format(a=player.name, b=player.bankRoll))
            bet = int(betStr)
            
            if bet > player.bankRoll:
                bet = player.bankRoll
                print 'Changing your amount to: {a}'.format(a=bet)
                
            player.currentBet = bet
            
        self.dealer = Dealer()
        self.deal()
        
        if self.dealer.handStatus == HandStatus.blackJack:
            self.gameOver()
        else:
            for player in self.players:
                player.takeTurn()

            self.dealer.takeTurn()
            self.gameOver()
        
    def deal(self):
        for i in range(2):
            for player in self.players:
                player.addCard(self.deck.draw())
                
            self.dealer.addCard(self.deck.draw())
            
        self.printInitialHands()
            
    def printInitialHands(self):
        print '\nDealt Hands:'
        
        for player in self.players:
            print 'player: {a}'.format(a=player.name)
            print player.hand[0]
            print player.hand[1]
            
            if player.checkHandStatus() == HandStatus.blackJack:
                print 'BlackJack !!!!!'
            
            print ''
            
        print 'player: {a}'.format(a=self.dealer.name)
        print 'Hole Card'
        #print self.dealer.hand[0]
        print self.dealer.hand[1]
        
        if self.dealer.checkHandStatus() == HandStatus.blackJack:
            print 'BlackJack !!!!!'
                
        print ''

    def gameOver(self):
        print '\n'
        print '**** Game Results ****'
        self.computePlayersStatus(self.dealer, False, self.dealer)
        results = []
        splitsToRemove = []
        
        for player in players:
            isSplit = False
            
            if isinstance(player, SplitPlayer):
                splitsToRemove.append(player)
                isSplit = True
                
            results.append(self.computePlayersStatus(player, isSplit, self.dealer))
            
        for result in results:
            print result
            
        print '\n\n'
        
        for split in splitsToRemove:
            players.remove(split)
                
                
    def computePlayersStatus(self, player, isSplit, dealer):
        statusLine = 'Player {a}, '.format(a=player.name)
        toReturn = ''
        
        if player.handStatus == HandStatus.blackJack:
            statusLine += 'BlackJack !!!'
            
            if dealer.handStatus != HandStatus.blackJack:
                toReturn = self.addToBankRoll(player, isSplit)
            else:
                toReturn = 'Player {a} and dealer tie, bankroll remains the same'.format(a=player.name)
                
        elif player.handStatus == HandStatus.surrender:
            statusLine += 'Surrendered'
            toReturn = self.removeFromBankRoll(player, isSplit)
        
        elif player.handStatus == HandStatus.bust:
            statusLine += 'Busted'
            toReturn = self.removeFromBankRoll(player, isSplit)
        
        else:
            statusLine += 'final hand is {a}'.format(a=player.best)
            
            if dealer.handStatus == HandStatus.bust and dealer.handStatus != HandStatus.blackJack:
                toReturn = self.addToBankRoll(player, isSplit)
                
            else:
                if dealer.handStatus == HandStatus.blackJack:
                    toReturn = self.removeFromBankRoll(player, isSplit)
                elif player.best > dealer.best:
                    toReturn = self.addToBankRoll(player, isSplit)
                elif dealer.best > player.best:
                    toReturn = self.removeFromBankRoll(player, isSplit)
                else:
                    toReturn = 'Player {a} and dealer tie, bankroll remains the same'.format(a=player.name)
               
        print statusLine
        return toReturn
                
                
    def addToBankRoll(self, player, isSplit):
        name = player.name
        
        if isSplit:
            player.parentPlayer.bankRoll = player.parentPlayer.bankRoll + player.currentBet
            name = player.parentPlayer.name
        else:
            player.bankRoll = player.bankRoll + player.currentBet
        
        #print 'Player {b} wins, wages gained {a}'.format(a=player.currentBet,b=name)
        return 'Player {b} wins, wages gained {a}'.format(a=player.currentBet,b=name)
        
    
    def removeFromBankRoll(self, player, isSplit):
        name = player.name
        
        if player.handStatus == HandStatus.surrender:
            player.currentBet = player.currentBet / 2
        
        if isSplit:
            player.parentPlayer.bankRoll = player.parentPlayer.bankRoll - player.currentBet
            name = player.parentPlayer.name
        else:
            player.bankRoll = player.bankRoll - player.currentBet
        
        #print 'Player {b} loses, wages lost {a}'.format(a=player.currentBet,b=name)
        return 'Player {b} loses, wages lost {a}'.format(a=player.currentBet,b=name)
        
        
        
###### end classes #######

###### start driver ######


players = []
deck = Deck()

print 'Enter up to 8 players...\n'

for i in range(8):
    name = raw_input('Enter name of player, or just <return> to stop entering players: ')
    
    if name == '':
        break
    else:
        players.append(Player(name, 100))
        
numberOfPlayers = len(players)
deck = Deck(numberOfPlayers/3 + 1)

while True:
    Game(players, deck)
    playersToRemove = []
    
    for player in players:
        player.newHand()
        
        if player.bankRoll <= 0:
            print 'Player {a} is out of funds, removing from game'.format(a=player.name)
            playersToRemove.append(player)
            
    for toRemove in playersToRemove:
        players.remove(toRemove)
            
    if len(players) == 0:
        break
    else:
        for player in players:
            print 'Player {a} bankroll before game is ${b}'.format(a=player.name,b=player.bankRoll)
        

