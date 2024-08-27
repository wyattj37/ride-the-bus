from collections import deque
import matplotlib.pyplot as plt
import seaborn as sns
import statistics
import random

#memory must be >= 2
memory = 2
total_simulations = 100000

# Card % 4 = 0 : heart
# Card % 4 = 1 : spade
# Card % 4 = 2 : diamond
# Card % 4 = 3 : club

# Card // 4 = 0 : ace
# Card // 4 = 1 : 2
# ...

suits = ['h', 's', 'd', 'c']
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

deck_dict = {}

#in order to be able to read the cards as letters and not integers
for rank_idx, rank in enumerate(ranks):
    for suit_idx, suit in enumerate(suits):
        card_num = suit_idx + rank_idx * len(suits)
        card_name = rank + suit
        deck_dict[card_num] = card_name

def red_black(deck, card_queue):
    red = 0
    black = 0
    
    #if deck is empty, reshuffle
    if (len(deck) == 0):
        new_deck = list(range(52))
        random.shuffle(new_deck)
        deck.extend(new_deck)
        carryover = card_queue.pop()
        deck.remove(carryover)
        card_queue.clear()
        card_queue.append(carryover)
    
    card_list = list(card_queue)
    card_strings = [deck_dict[card] for card in card_list]
    
    #getting a count of red and black
    for i in card_list:
        if (i % 2 == 0):
            red += 1
        else:
            black += 1

    next_card = deck.pop(0)
    card_queue.append(next_card)
    
    #returning of the guess was right or wrong
    if (red <= black):
        return (next_card % 2 == 0)
    else:
        return (next_card % 2 == 1)
    

def up_down(deck, card_queue):
    #if deck is empty, reshuffle
    if (len(deck) == 0):
        new_deck = list(range(52))
        random.shuffle(new_deck)
        deck.extend(new_deck)
        carryover = card_queue.pop()
        deck.remove(carryover)
        card_queue.clear()
        card_queue.append(carryover)
    
    card_list = list(card_queue)
    top = card_list[-1]
    card_strings = [deck_dict[card] for card in card_list]
    
    #getting a count of how many cards are above/below current card
    below = (top // 4) * 4
    above = ((51 - top) // 4) * 4

    for i in card_list:
        if (i // 4 < top // 4):
            below -= 1
        elif (i // 4 > top // 4):
            above -= 1

    next_card = deck.pop(0)
    card_queue.append(next_card)
    
    #returning if the guess was right or wrong
    if (below >= above):
        return (next_card // 4 < top // 4)
    else:
        return (next_card // 4 > top // 4)

def in_out(deck, card_queue):
    #if deck is empty, reshuffle
    #all but the most recent cards
    if (len(deck) == 0):
        new_deck = list(range(52))
        random.shuffle(new_deck)
        deck.extend(new_deck)
        carryover1 = card_queue.pop()
        carryover2 = card_queue.pop()
        deck.remove(carryover1)
        deck.remove(carryover2)
        card_queue.clear()
        card_queue.append(carryover1)
        card_queue.append(carryover2)
        
    card_list = list(card_queue)
    lower = min(card_list[-1], card_list[-2])
    upper = max(card_list[-1], card_list[-2])
    
    #getting count of how many cards are inside or outside
    inside = (upper//4 - lower//4 + 1)*4
    outside = (lower//4)*4 + ((51 - upper)//4 + 1)*4

    card_strings = [deck_dict[card] for card in card_list]

    next_card = deck.pop(0)
    card_queue.append(next_card)

    #return is guess was right or wrong
    if (inside >= outside):
        return (next_card//4 >= lower//4 and upper//4 >= next_card//4)
    else:
        return (next_card//4 < lower//4 or next_card//4 > upper//4)

def suit(deck, card_queue):
    #if deck is empty, shuffle
    if (len(deck) == 0):
        new_deck = list(range(52))
        random.shuffle(new_deck)
        deck.extend(new_deck)
        carryover = card_queue.pop()
        deck.remove(carryover)
        card_queue.clear()
        card_queue.append(carryover)
    
    hearts = 0
    spades = 0
    diamonds = 0
    clubs = 0

    card_list = list(card_queue)
    card_strings = [deck_dict[card] for card in card_list]
    
    #get count of each suit
    for i in card_list:
        if (i % 4 == 0):
            hearts += 1
        elif (i % 4 == 1):
            spades += 1
        elif (i % 4 == 2):
            diamonds += 1
        else:
            clubs += 1

    counts = {
        'hearts': hearts,
        'spades': spades,
        'diamonds': diamonds,
        'clubs': clubs
    }

    min_suit = min(counts, key=counts.get)
    
    next_card = deck.pop(0)
    card_queue.append(next_card)

    #choose suit with lowest count, return
    if (min_suit == 'hearts'):
        return (next_card % 4 == 0)
    elif (min_suit == 'spades'):
        return (next_card % 4 == 1)
    elif (min_suit == 'diamonds'):
        return (next_card % 4 == 2)
    elif (min_suit == 'clubs'):
        return (next_card % 4 == 3)

#simulate the actual course of the gameplay
def ride_bus():
    deck = list(range(52))
    random.shuffle(deck)
    card_queue = deque(maxlen = memory)
    
    drinks = 0
    on_the_bus = True
    
    while (on_the_bus):
        if (red_black(deck, card_queue)):
            if (up_down(deck, card_queue)):
                if (in_out(deck, card_queue)):
                    if (suit(deck, card_queue)):
                        on_the_bus = False
                        continue
                    else:
                        drinks += 1
                        continue
                else:
                    drinks += 1
                    continue
            else:
                drinks += 1
                continue
        else:
            drinks += 1
            continue

    return drinks

#obtaining avg number of drinks
def get_avg():
    drink_count = 0
    for i in range(total_simulations):
        drink_count += ride_bus()
    return drink_count / total_simulations

outputs = [ride_bus() for i in range(total_simulations)]
outputs_condensed = [value for value in outputs if value <= 100]

# Create a histogram using seaborn
sns.histplot(outputs_condensed, bins=20, stat='probability')   # Set kde=True for the density plot overlay

# Labeling and title
plt.xlabel('Number of Drinks')
plt.xticks(range(0, 105, 5))
plt.title('Bus Riding Distribution')


plt.show()

print(get_avg())
