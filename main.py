import pygame
import os
import time
import sys
import Card
import random
import keyboard

RESOLUTION = (1920, 1080)
player_x_pos, player_y_pos = 860, 780
dealer_x_pos, dealer_y_pos = 860, 50
backup_surface1 = pygame.surface
backup_surface2 = pygame.surface


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
        player_cards.append(card)

        card = deck[random.randint(0, len(deck) - 1)]
        deck.remove(card)
        if i == 1:
            card.visible = False
        dealer_cards.append(card)


def deal_frontend(player_cards, dealer_cards, win):
    for i in range(2):
        card_pic = pygame.image.load(
            "pictures/cards/{}_{}.png".format(player_cards[i].type, player_cards[i].value))  # player first card
        win.blit(card_pic, (player_x_pos, player_y_pos))
        change_player_values()

        if i == 1:
            card_pic = pygame.image.load("pictures/back.png")
            win.blit(card_pic, (dealer_x_pos, dealer_y_pos))
        else:
            card_pic = pygame.image.load(
                "pictures/cards/{}_{}.png".format(dealer_cards[i].type, dealer_cards[i].value))  # player first card
            win.blit(card_pic, (dealer_x_pos, dealer_y_pos))
            change_dealer_values()
    showValue_player(win, player_cards)
    showValue_dealer(win, dealer_cards, backup_surface2)
    pygame.display.flip()


def change_player_values():
    global player_x_pos, player_y_pos
    player_x_pos += 50
    player_y_pos -= 10


def change_dealer_values():
    global dealer_x_pos, dealer_y_pos
    dealer_x_pos += 50
    dealer_y_pos += 10


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


def blackjack_handler(player_cards, dealer_cards, win, deck):  # handles blackjack possibilities
    bj_dealer = False
    bj_player = check_blackjack(player_cards)
    is_ten = check_ace_or_ten(dealer_cards)

    if is_ten:
        bj_dealer = check_blackjack(dealer_cards)
        backup = print_centered_text(win, "Checking for blackjack...")
        pygame.display.flip()
        time.sleep(1)
        delete_centered_text(win, backup)

    if not bj_player and not bj_dealer:
        return

    dealer_cards[1].visible = True  # for showValue

    if bj_player and not is_ten:  # waiting if hadnt waited
        time.sleep(1)

    load_dealer_hidden(dealer_cards, win)
    showValue_dealer(win, dealer_cards, backup_surface2)
    pygame.display.flip()
    time.sleep(1)

    if bj_player and not bj_dealer:
        print_centered_text(win, "Player blackjack! You win!")
    elif bj_dealer and not bj_player:
        print_centered_text(win, "Dealer blackjack! You lose!")
    elif bj_dealer and bj_player:
        print_centered_text(win, "Push!")

    start_next(deck, win, player_cards, dealer_cards, backup_surface2)


def check_ace_or_ten(dealer_cards):
    if dealer_cards[0].realValue() == 10 or dealer_cards[0].realValue() == 1:
        return True
    return False


def load_dealer_hidden(dealer_cards, win):
    card_pic = pygame.image.load(
        "pictures/cards/{}_{}.png".format(dealer_cards[1].type, dealer_cards[1].value))  # dealer hidden
    win.blit(card_pic, (910, 60))


def hit(deck, win, player_cards, backup_surface1, dealer_cards, backup_surface2):
    global player_x_pos, player_y_pos

    card = deck[random.randint(0, len(deck) - 1)]
    deck.remove(card)
    player_cards.append(card)
    card_pic = pygame.image.load("pictures/cards/{}_{}.png".format(card.type, card.value))

    backup_rect = pygame.Rect(950, 1020, 50, 30)

    win.blit(backup_surface1, backup_rect.topleft)

    win.blit(card_pic, (player_x_pos, player_y_pos))
    showValue_player(win, player_cards)
    player_x_pos += 50
    player_y_pos -= 10

    if sum(player_cards) > 21:
        condition(dealer_cards, player_cards, True, win)
        pygame.display.flip()
        start_next(deck, win, player_cards, dealer_cards, backup_surface2)
        print("pass")
        return


def stay(deck, win, dealer_cards, backup_surface2, player_cards):
    global dealer_x_pos, dealer_y_pos
    global player_x_pos, player_y_pos
    dealer_cards[1].visible = True
    card = dealer_cards[1]
    while True:
        card_pic = pygame.image.load("pictures/cards/{}_{}.png".format(card.type, card.value))
        win.blit(card_pic, (dealer_x_pos, dealer_y_pos))
        showValue_dealer(win, dealer_cards, backup_surface2)
        pygame.display.flip()  # updating
        dealer_x_pos += 50
        dealer_y_pos += 10
        showValue_dealer(win, dealer_cards, backup_surface2)
        if sum(dealer_cards) < 17:
            card = deck[random.randint(0, len(deck) - 1)]
            deck.remove(card)
            dealer_cards.append(card)
            time.sleep(1.5)
        else:
            condition(dealer_cards, player_cards, False, win)
            return


def showValue_player(win, player_cards, ):
    font = pygame.font.Font(None, 40)  # Font object with default font and size 74
    text_color = "black"  # RGB color for red
    text = font.render(str(sum(player_cards)), True, text_color)
    win.blit(text, (958, 1020))


def showValue_dealer(win, dealer_cards, backup_surface2):
    backup_rect = pygame.Rect(958, 360, 50, 30)
    win.blit(backup_surface2, backup_rect.topleft)

    font = pygame.font.Font(None, 40)  # Font object with default font and size 74
    text_color = "black"  # RGB color for red
    text = font.render(str(sum(dealer_cards)), True, text_color)
    win.blit(text, (958, 360))


def reset(win, player_cards, dealer_cards):
    global dealer_x_pos, dealer_y_pos, player_y_pos, player_x_pos
    dealer_x_pos, dealer_y_pos = 860, 50
    player_x_pos, player_y_pos = 860, 780  # resetting
    player_cards.clear()
    dealer_cards.clear()
    background = pygame.image.load("pictures/background.jpg")
    win.blit(background, (0, 0))  # Adjust the position as needed


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
    if busted:
        print_centered_text(win, "Busted! You lost!")
        return

    sum_player = sum(player_cards)
    sum_dealer = sum(dealer_cards)

    if sum_dealer > sum_player and not sum_dealer > 21:
        print_centered_text(win, "You lost!")
    elif sum_player > sum_dealer or sum_dealer > 21:
        print_centered_text(win, "You won!")
    else:
        print_centered_text(win, "Push!")


def start_next(deck, win, player_cards, dealer_cards, backup_surface2):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Check if the ESC key is pressed
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:  # staying
                    print("resetting")
                    reset(win, player_cards, dealer_cards)
                    deal(deck, win, player_cards, dealer_cards)
                    showValue_player(win, player_cards)
                    showValue_dealer(win, dealer_cards, backup_surface2)
                    return


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


def get_backup_surface(win):
    global backup_surface1, backup_surface2
    print_card_for_saving_background(
        win)  # printing a card to allow to copy the card surface before calling the deal function
    backup_rect1 = pygame.Rect(950, 1020, 50, 30)
    backup_surface1 = pygame.Surface(backup_rect1.size)  # copy screen for allowing to paste count on the same screen
    backup_surface1.blit(win, (0, 0), backup_rect1)

    backup_rect2 = pygame.Rect(958, 360, 50, 30)
    backup_surface2 = pygame.Surface(backup_rect2.size)  # copy screen for allowing to paste count on the same screen
    backup_surface2.blit(win, (0, 0), backup_rect2)


def print_card_for_saving_background(win):
    card_pic = pygame.image.load("pictures/cards/hearts_10.png")
    win.blit(card_pic, (910, 770))


def main():
    pygame.init()
    win = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Blackjack")  # settings
    background = pygame.image.load("pictures/background.jpg")
    win.blit(background, (0, 0))  # Adjust the position as needed
    get_backup_surface(win)

    deck = []
    player_cards = []
    dealer_cards = []
    add_deck(deck)
    deal(deck, win, player_cards, dealer_cards)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Check if the ESC key is pressed
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:  # hitting
                    hit(deck, win, player_cards, backup_surface1, dealer_cards, backup_surface2)
                if event.key == pygame.K_RETURN:  # staying
                    stay(deck, win, dealer_cards, backup_surface2, player_cards)
                    start_next(deck, win, player_cards, dealer_cards, backup_surface2)

        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    main()
