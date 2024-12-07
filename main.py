import random
import sys
import time
import tkinter
import pygame

RESOLUTION = (1920, 1080)

dealer_value_rect = (958, 364, 40, 40)
dealer_position = 860, 50

dealer_value_background = ()

chip_locations = {
    0: (940, 680),
    1: (540, 680),
    2: (1340, 680),
    3: (140, 680),
    4: (1740, 680),
}

player_positions = {  # card placement positions (for images)
    0: (860, 780),  # Tuple for player_pos_value1
    1: (460, 780),  # Tuple for player_pos_value2
    2: (1260, 780),
    3: (60, 780),
    4: (1660, 780),
}

player_value_rects = {  # position recs for player value positions (for text inside)
    0: (968, 1020, 40, 40),  # Tuple for player_pos_value1
    1: (570, 1020, 40, 40),  # Tuple for player_pos_value2
    2: (1380, 1020, 40, 40),  # Tuple for player_pos_value3
    3: (173, 1020, 40, 40),
    4: (1780, 1020, 40, 40),
}

second_card_player_positions = {  # locations for second cards (for images)
    0: (910, 770),  # Tuple for player_pos_value1
    1: (510, 770),  # Tuple for player_pos_value2
    2: (1310, 770),  # Tuple for player_pos_value3
    3: (110, 770),
    4: (1710, 770),
}

card_delete_locations_rects = {
    0: (860, 770, 250, 301),  # Tuple for player_pos_value1
    1: (460, 770, 250, 301),  # Tuple for player_pos_value2
    2: (1260, 770, 250, 301),  # Tuple for player_pos_value3
    3: (60, 770, 250, 301),
    4: (1660, 770, 250, 301),
}

player_card_background = {  # surface  behind second card
    0: (),
    1: (),
    2: (),
    3: (),
    4: (),
}

player_value_background = {  # surface behind player value
    0: (),  # Tuple for player_pos_value1
    1: (),  # Tuple for player_pos_value2
    2: (),  # Tuple for player_pos_value3
    3: (),
    4: (),
}

slot_in_play = 0


def background_saver(win, background):
    global dealer_value_background

    win.blit(background, (0, 0))  # setting background

    for i in player_positions:
        saved_background = win.subsurface(
            card_delete_locations_rects[i]).copy()  # saving background for players value spot
        player_card_background[i] = saved_background

    card_pic = pygame.image.load("pictures/cards/hearts_2.png")  # default card

    for i in player_positions:  # printing first cards in players' slot
        win.blit(card_pic, player_positions[i])

    for i in second_card_player_positions:  # printing second card
        win.blit(card_pic, second_card_player_positions[i])

    win.blit(card_pic, dealer_position)
    change_dealer_values()  # printing dealer cards
    win.blit(card_pic, dealer_position)

    for i in player_value_background:
        saved_background = win.subsurface(player_value_rects[i]).copy()  # saving background for players value spot
        player_value_background[i] = saved_background

    saved_background = win.subsurface(dealer_value_rect).copy()  # saving background for dealers value spot
    dealer_value_background = saved_background
    reset_dealer_values()

    win.blit(background, (0, 0))  # resetting


class Card:
    def __init__(self, value, type, visible):
        self.type = type
        self.value = value
        self.visible = visible

    def __str__(self):
        return "Value: {} type: {} visible: {}".format(self.value, self.type, self.visible)

    def __repr__(self):
        return "Value: {} type: {} visible: {}".format(self.value, self.type, self.visible)

    def realValue(self):
        if self.value < 11:
            return self.value
        if self.value > 10 and self.value < 14:
            return 10
        return 1


def sum(playing_deck):  # calcultes sum including aces

    sum = 0
    ace_flag = False
    for card in playing_deck:
        if card.visible:
            sum += card.realValue()
            if card.value == 14:
                ace_flag = True
    if sum < 12 and ace_flag:
        sum += 10
    return sum


def add_deck(deck):  # adds a deck of cards to the list
    for i in range(2, 15):
        deck.append(Card(i, "hearts", True))
    for i in range(2, 15):
        deck.append(Card(i, "diamonds", True))
    for i in range(2, 15):
        deck.append(Card(i, "clubs", True))
    for i in range(2, 15):
        deck.append(Card(i, "spades", True))


def deal(deck, win, player_cards, dealer_cards):
    deal_backend(deck, player_cards, dealer_cards)
    deal_frontend(player_cards, dealer_cards, win)
    blackjack_handler(player_cards, dealer_cards, win, deck)


def deal_backend(deck, player_cards, dealer_cards):
    for i in range(2):
        card = deck[random.randint(0, len(deck) - 1)]
        deck.remove(card)
        player_cards[slot_in_play].append(card)

        card = deck[random.randint(0, len(deck) - 1)]
        deck.remove(card)
        if i == 1:
            card.visible = False
        dealer_cards.append(card)


def deal_frontend(player_cards, dealer_cards, win):
    for i in range(2):
        card_pic = pygame.image.load(
            "pictures/cards/{}_{}.png".format(player_cards[slot_in_play][i].type,
                                              player_cards[slot_in_play][i].value))  # player first card
        win.blit(card_pic, player_positions[slot_in_play])
        change_player_values()

        if i == 1:
            card_pic = pygame.image.load("pictures/back.png")
            win.blit(card_pic, dealer_position)
        else:
            card_pic = pygame.image.load(
                "pictures/cards/{}_{}.png".format(dealer_cards[i].type, dealer_cards[i].value))  # player first card
            win.blit(card_pic, dealer_position)
            change_dealer_values()
    show_value_player(win, player_cards)
    show_value_dealer(win, dealer_cards)


def change_player_values():
    pos = player_positions[slot_in_play]
    x = pos[0]
    y = pos[1]
    player_positions[slot_in_play] = (x + 50, y - 10)


def reset_dealer_values():
    global dealer_position
    dealer_position = (860, 50)


def change_dealer_values():
    global dealer_position
    x = dealer_position[0]
    y = dealer_position[1]
    dealer_position = (x + 50, y + 10)


def set_buttons(win):
    pygame.draw.rect(win, (0, 255, 128), pygame.Rect(1200, 950, 250, 100))
    pygame.draw.rect(win, (255, 0, 0), pygame.Rect(470, 950, 250, 100))

    font = pygame.font.Font(None, 40)  # Font object with default font and size 74
    text_color = "black"  # RGB color for red
    text = font.render('Hit', True, text_color)
    text_rect = text.get_rect(center=(1200 + 250 // 2, 950 + 100 // 2))
    win.blit(text, text_rect)

    font = pygame.font.Font(None, 40)  # Font object with default font and size 74
    text_color = "black"  # RGB color for red
    text = font.render('Stay', True, text_color)
    text_rect = text.get_rect(center=(470 + 250 // 2, 950 + 100 // 2))
    win.blit(text, text_rect)


def blackjack_handler(player_cards, dealer_cards, win, deck):
    # handles blackjack possibilities
    bj_dealer = False
    bj_player = check_blackjack(player_cards[slot_in_play])
    is_ten = check_ace_or_ten(dealer_cards)

    if is_ten:
        bj_dealer = check_blackjack(dealer_cards)
        backup = print_centered_text(win, "Checking for blackjack...")
        pygame.display.flip()
        time.sleep(1)
        delete_centered_text(win, backup)
        pygame.display.flip()

    if not bj_player and not bj_dealer:
        return

    dealer_cards[1].visible = True  # for showValue

    if bj_player and not is_ten:  # waiting if hadnt waited
        pygame.display.flip()
        time.sleep(1)

    load_dealer_hidden(dealer_cards, win)
    show_value_dealer(win, dealer_cards)
    pygame.display.flip()
    time.sleep(1)

    if bj_player and not bj_dealer:
        print_centered_text(win, "Player blackjack! You win!")
    elif bj_dealer and not bj_player:
        print_centered_text(win, "Dealer blackjack! You lose!")
    elif bj_dealer and bj_player:
        print_centered_text(win, "Push!")

    start_next(deck, win, player_cards, dealer_cards)


def check_ace_or_ten(dealer_cards):
    if dealer_cards[0].realValue() == 10 or dealer_cards[0].realValue() == 1:
        return True
    return False


def load_dealer_hidden(dealer_cards, win):
    card_pic = pygame.image.load(
        "pictures/cards/{}_{}.png".format(dealer_cards[len(dealer_cards) - 1].type,
                                          dealer_cards[len(dealer_cards) - 1].value))  # dealer hidden
    win.blit(card_pic, dealer_position)


def hit_backend(deck, player_cards):
    card = deck[random.randint(0, len(deck) - 1)]
    deck.remove(card)
    player_cards[slot_in_play].append(card)


def hit_frontend(player_cards, win):
    card_pic = pygame.image.load(
        "pictures/cards/{}_{}.png".format(player_cards[slot_in_play][len(player_cards[slot_in_play]) - 1].type,
                                          player_cards[slot_in_play][len(player_cards[slot_in_play]) - 1].value))
    win.blit(card_pic, player_positions[slot_in_play])
    show_value_player(win, player_cards)


def hit(deck, win, player_cards, dealer_cards):
    hit_backend(deck, player_cards)
    hit_frontend(player_cards, win)

    change_player_values()


def bust_detection(player_cards, dealer_cards, win, deck):
    if sum(player_cards[slot_in_play]) > 21:
        is_stay = condition(dealer_cards, player_cards, True, win)
        if is_stay:
            stay(deck, win, dealer_cards, player_cards)
        return True
    return False


def stay(deck, win, dealer_cards, player_cards):
    dealer_cards[1].visible = True
    while True:
        load_dealer_hidden(dealer_cards, win)
        show_value_dealer(win, dealer_cards)
        pygame.display.flip()  # updating
        change_dealer_values()
        # show_value_dealer(win, dealer_cards)
        if sum(dealer_cards) < 17:
            card = deck[random.randint(0, len(deck) - 1)]
            deck.remove(card)
            dealer_cards.append(card)
            time.sleep(1.5)
        else:
            condition(dealer_cards, player_cards, False, win)
            return


def show_value_player(win, player_cards):
    win.blit(player_value_background[slot_in_play], player_value_rects[slot_in_play])
    font = pygame.font.Font(None, 40)  # Font object with default font and size 74
    text_color = "blue"  # RGB color for red
    text = font.render(str(sum(player_cards[slot_in_play])), True, text_color)
    win.blit(text, player_value_rects[slot_in_play])


def show_value_dealer(win, dealer_cards):
    win.blit(dealer_value_background, dealer_value_rect)
    font = pygame.font.Font(None, 40)  # Font object with default font and size 74
    text_color = "black"  # RGB color for red
    text = font.render(str(sum(dealer_cards)), True, text_color)
    win.blit(text, dealer_value_rect)


def reset(win, player_cards, dealer_cards):
    global slot_in_play
    slot_in_play = 0
    reset_positions()
    for hand in player_cards:
        hand.clear()
    dealer_cards.clear()
    background = pygame.image.load("pictures/background.jpg")
    win.blit(background, (0, 0))  # Adjust the position as needed


def reset_positions():
    global dealer_position
    dealer_position = 860, 50
    player_positions[0] = (860, 780)
    player_positions[1] = (460, 780)
    player_positions[2] = (1260, 780)
    player_positions[3] = (60, 780)
    player_positions[4] = (1660, 780)


def print_checking(win):
    # Create a font object
    font = pygame.font.Font(None, 165)  # None uses the default font, 74 is the font size
    # Render text
    text = font.render(("Checking for blackjack..."), True, "black")  # True for anti-aliasing
    # Get the rectangle for the text
    text_rect = text.get_rect(center=(960, 540))  # Center the text in the middle of the screen
    win.blit(text, text_rect)


def print_centered_text(win, msg):
    # Create a font object
    font = pygame.font.Font(None, 165)  # None uses the default font, 74 is the font size
    # Render text
    text = font.render((msg), True, "black")  # True for anti-aliasing
    # Get the rectangle for the text
    text_rect = text.get_rect(center=(960, 540))  # Center the text in the middle of the screen
    saved_background = win.subsurface(text_rect).copy()
    win.blit(text, text_rect)
    pygame.display.flip()
    return saved_background, text_rect


def delete_centered_text(win, backup):  # receives tuple for backup surface and position
    background = backup[0]
    rect = backup[1]
    win.blit(background, rect)


def condition(dealer_cards, player_cards, busted, win):
    if len(player_cards[1]) != 0:
        is_stay = sub_condition(dealer_cards, player_cards, busted, win)
        return is_stay
    if busted:
        print_centered_text(win, "Busted! You lost!")
        return False

    sum_player = sum(player_cards[0])
    sum_dealer = sum(dealer_cards)

    if sum_dealer > sum_player and not sum_dealer > 21:
        msg = "You lost!"
        player_cards[0].clear()
        player_cards[0].append(-1)
    elif sum_player > sum_dealer or sum_dealer > 21:
        msg = "You won!"
        player_cards[0].clear()
        player_cards[0].append(-1)
    else:
        msg = "Push!"
        player_cards[0].clear()
        player_cards[0].append(-1)
    print_centered_text(win, msg)


def sub_condition(dealer_cards, player_cards, busted, win):
    global slot_in_play
    if busted:
        cords = build_center_cards_cords(player_cards)
        print_to_center_rec(win, cords, "Busted!")
        player_cards[slot_in_play][0] = -1
        if slot_in_play == 0:
            for i in range(len(player_cards) - 1):
                if len(player_cards[i + 1]) == 0:
                    return False
                if player_cards[i + 1][0] != -1:
                    return True
        return False

    sum_dealer = sum(dealer_cards)

    while slot_in_play != 5:

        while len(player_cards[slot_in_play]) == 0 or player_cards[slot_in_play][0] == -1:
            slot_in_play = slot_in_play + 1
            if slot_in_play == 5:
                return

        sum_player = sum(player_cards[slot_in_play])

        if sum_dealer > sum_player and not sum_dealer > 21:
            msg = "You lost!"
            player_cards[slot_in_play].clear()
            player_cards[slot_in_play].append(-1)
        elif sum_player > sum_dealer or sum_dealer > 21:
            msg = "You won!"
            player_cards[slot_in_play].clear()
            player_cards[slot_in_play].append(1)
        else:
            msg = "Push!"
            player_cards[slot_in_play].clear()
            player_cards[slot_in_play].append(0)

        cords = build_center_cards_cords(player_cards)
        print_to_center_rec(win, cords, msg)
        slot_in_play = slot_in_play + 1
        pygame.display.flip()


def print_to_center_rec(win, cords, msg):
    # Create a font object
    font = pygame.font.Font(None, 70)  # None uses the default font, 74 is the font size
    # Render text
    text = font.render(msg, True, "black")  # True for anti-aliasing
    # Get the rectangle for the text
    text_rect = text.get_rect(center=cords)  # Center the text in the middle of the screen
    win.blit(text, text_rect)
    pygame.display.flip()


def start_next(deck, win, player_cards, dealer_cards):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Check if the ESC key is pressed
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:  # staying
                    reset(win, player_cards, dealer_cards)
                    if len(deck) < 15:
                        reshuffle(deck)
                        backup = print_centered_text(win, "reshuffled!")
                        time.sleep(1)
                        delete_centered_text(win, backup)
                    deal(deck, win, player_cards, dealer_cards)
                    return


def reshuffle(deck):
    deck.clear()
    add_deck(deck)


def check_blackjack(playing_cards):
    sum = 0
    ace_flag = False
    for card in playing_cards:
        sum += card.realValue()
        if card.value == 14:
            ace_flag = True
    if sum < 12 and ace_flag:
        sum += 10
    if sum == 21:
        return True
    return False


def build_center_cards_cords(player_cards):
    x1 = second_card_player_positions[slot_in_play][0] - 50  # x cordinate
    x2 = player_positions[slot_in_play][0] + 150  # average of the x,y cordinates
    y1 = player_positions[slot_in_play][1] + 10
    y2 = second_card_player_positions[slot_in_play][1] + 301
    y = (y1 + y2) / 2
    x = (x1 + x2) / 2
    return x, y


def input_handler(deck, win, player_cards, dealer_cards):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Check if the ESC key is pressed
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:  # hitting
                    hit(deck, win, player_cards, dealer_cards)
                    if bust_detection(player_cards, dealer_cards, win, deck):
                        if slot_in_play == 0 and not dealer_cards[1].visible:
                            load_dealer_hidden(dealer_cards, win)
                            dealer_cards[1].visible = True
                            show_value_dealer(win, dealer_cards)
                            pygame.display.flip()
                        return
                if event.key == pygame.K_RETURN:  # staying
                    if slot_in_play > 0:
                        return
                    stay(deck, win, dealer_cards, player_cards)
                    return
                if event.key == pygame.K_p:  # Check if 'P' is pressed
                    splitting(player_cards, win, deck, dealer_cards)
        pygame.display.flip()


def split_check(player_cards):  # TEMP!!!!!!!!!!!! ALWAYS CAN SPLIT
    if player_cards[slot_in_play][0].realValue() == player_cards[slot_in_play][1].realValue():
        if len(player_cards[slot_in_play]) == 2:
            return True
    return False


def splitting_backend(deck, player_cards, original_slot_in_play):
    card = player_cards[original_slot_in_play].pop()
    player_cards[slot_in_play].append(card)
    card = deck[random.randint(0, len(deck) - 1)]
    deck.remove(card)
    player_cards[slot_in_play].append(card)


def splitting_frontend(win, player_hands, original_slot_in_play):
    card_pic = pygame.image.load("pictures/cards/{}_{}.png".format(player_hands[slot_in_play][0].type,
                                                                   player_hands[slot_in_play][0].value))
    win.blit(card_pic, player_positions[slot_in_play])
    change_player_values()

    card_pic = pygame.image.load("pictures/cards/{}_{}.png".format(player_hands[slot_in_play][1].type,
                                                                   player_hands[slot_in_play][1].value))
    win.blit(card_pic, player_positions[slot_in_play])
    change_player_values()
    show_value_player(win, player_hands)
    win.blit(player_card_background[original_slot_in_play], card_delete_locations_rects[original_slot_in_play])
    card_pic = pygame.image.load("pictures/cards/{}_{}.png".format(player_hands[original_slot_in_play][0].type,
                                                                   player_hands[original_slot_in_play][0].value))
    win.blit(card_pic,
             (player_positions[original_slot_in_play][0] - 100, player_positions[original_slot_in_play][1] + 20))


def dec_slot_in_play(player_cards):
    global slot_in_play
    slot_in_play = slot_in_play - 1
    while len(player_cards[slot_in_play]) == 2:
        slot_in_play = slot_in_play - 1


def inc_slot_in_play(player_cards):
    global slot_in_play
    original_slot_in_play = slot_in_play
    slot_in_play = slot_in_play + 1
    while len(player_cards[slot_in_play]) == 2:
        slot_in_play = slot_in_play + 1
    return original_slot_in_play


def splitting(player_cards, win, deck, dealer_cards):
    # if not split_check(player_cards):
    # return
    original_slot_in_play = inc_slot_in_play(player_cards)
    splitting_backend(deck, player_cards, original_slot_in_play)
    splitting_frontend(win, player_cards, original_slot_in_play)
    input_handler(deck, win, player_cards, dealer_cards)
    dec_slot_in_play(player_cards)
    add_missing_card(player_cards, deck, win)


def add_missing_card(player_cards, deck, win):
    add_missing_card_backend(player_cards, deck)
    add_missing_card_frontend(player_cards, win)


def add_missing_card_backend(player_cards, deck):
    card = deck[random.randint(0, len(deck) - 1)]
    player_cards[slot_in_play].append(card)


def add_missing_card_frontend(player_cards, win):
    card_pic = pygame.image.load(
        "pictures/cards/{}_{}.png".format(player_cards[slot_in_play][len(player_cards[slot_in_play]) - 1].type,
                                          player_cards[slot_in_play][
                                              len(player_cards[slot_in_play]) - 1].value))  # dealer hidden
    win.blit(card_pic, second_card_player_positions[slot_in_play])
    show_value_player(win, player_cards)


def change_chip_locations():
    chip_locations[slot_in_play] = (chip_locations[slot_in_play][0], chip_locations[slot_in_play][1] - 5)


def get_chips(amount):
    # Available chip denominations
    chips = [1000, 500, 100, 25, 5, 1]
    result = []

    for chip in chips:
        count = amount // chip  # Find how many chips of this denomination
        if count > 0:
            result.append((chip, count))  # Store (chip value, count)
            amount -= count * chip  # Subtract the chip value from the total amount

    return result 


def print_chips_on_screen(win, chips):
    center_x = chip_locations[slot_in_play][0]  # The center x-position of the card area
    y_start = chip_locations[slot_in_play][1]  # Starting y position for stacks
    chip_height = 5  # Height of each chip in a stack
    x_offset = 40  # Horizontal space between chip stacks

    num_chip_types = len(chips)  # Get the number of chip types

    x_positions = []
    y_positions = []

    # Calculate the starting x positions based on the number of chip types
    if num_chip_types == 1:
        x_positions = [center_x]
        y_positions = [y_start]
    elif num_chip_types == 2:
        x_positions = [center_x - x_offset, center_x + x_offset]
        y_positions = [y_start, y_start]
    elif num_chip_types == 3:
        x_positions = [center_x - 2*x_offset, center_x, center_x + 2*x_offset]
        y_positions = [y_start, y_start, y_start]
    elif num_chip_types == 4:
        x_positions = [center_x - x_offset, center_x + x_offset, center_x - x_offset, center_x + x_offset]
        y_positions = [y_start, y_start, y_start - 80, y_start - 80]

    # Loop through the chip types and stack them at the corresponding x positions
    for i in range(len(chips)):
        x = x_positions[i]
        print(chips)
        chip_image = pygame.image.load("pictures/chips/{}.png".format(chips[i][0]))
        for j in range(chips[i][1]):
            win.blit(chip_image, (x, y_positions[i]))
            y_positions[i] = y_positions[i] - chip_height


def switch_chip_index(value):
    if value == 1:
        pass


def main():
    pygame.init()
    win = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Blackjack")  # settings
    background = pygame.image.load("pictures/background.jpg")
    background_saver(win, background)

    deck = []
    dealer_cards = []
    player_cards = [[] for _ in range(5)]
    add_deck(deck)
    # win.blit(chip, chip_locations[slot_in_play])
    # change_chip_locations()
    # win.blit(chip, (chip_locations[slot_in_play]))
    # win.blit(chip, (player_positions[0][0] + 80, player_positions[0][1] - 110))
    buy_in = input("enter buy in amount")
    chips = get_chips(int(buy_in))
    print_chips_on_screen(win, chips)
    deal(deck, win, player_cards, dealer_cards)

    while True:
        input_handler(deck, win, player_cards, dealer_cards)
        print("start next")
        start_next(deck, win, player_cards, dealer_cards)


if __name__ == "__main__":
    main()
