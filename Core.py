import pygame
import random
import tkinter as tk

pygame.init()

#  PyGame window and image initialisation
win = pygame.display.set_mode((750, 600))
pygame.display.set_caption("Snakes and Ladders")
bg = pygame.image.load('assets/board.png')
char = pygame.image.load('assets/idle.png')


def start_game():
    # tkinter window for getting inputs from users
    def set_name():
        # takes the input from te user and sets it as name for that player respectively
        global init
        player[0].name, player[1].name = e1.get(), e2.get()
        # when init == 0, no actions except instructions and start game can be performed
        # if init == 1, user has set the names for players. so, now the game can be started
        init = 1

        # the text on the button that shows current player's turn needs to be updated
        turn_button.update_text(str(player[0].name) + "'s turn")

    def close_win():
        # closes the window
        master.destroy()

    master = tk.Tk()
    master.title("start game")
    master.geometry("250x100+900+100")
    tk.Label(master, text="player 1 name").grid(row=0)
    tk.Label(master, text="player 2 name").grid(row=1)

    e1 = tk.Entry(master)
    e2 = tk.Entry(master)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    tk.Button(master, text='Save', command=set_name).grid(row=3, column=1, sticky=tk.W, pady=4)
    tk.Button(master, text='start game', command=close_win).grid(row=3, column=0, sticky=tk.W, pady=4)
    tk.mainloop()


def end_game(pla_number):
    # tkinter window that executes when a player wins the game
    # displays a text consisting of winning player's name a predefined text
    def close_win():
        # closes the window
        master.destroy()
        pygame.quit()

    master = tk.Tk()
    master.title("game finished")
    master.geometry("100x100+900+100")
    text = player[pla_number].name + " won"
    tk.Label(master, text=text).grid(row=0)
    tk.Button(master, text='end game', command=close_win).grid(row=1, sticky=tk.W, pady=8)
    tk.mainloop()


class Player(object):
    def __init__(self, x, y):
        self.speed = 51  # length of one tile on the screen
        self.x, self.y = x, y  # x and y co-ordinates for the position
        self.direction = 0  # the direction of the players heading
        self.pos = 1  # position of the tile player is present in
        self.name = "player"  # name of the player
        self.roll = 0  # the recent roll of the player

    def draw(self, win):
        # placing the players on the screen
        win.blit(char, (self.x, self.y))

    def change_dir(self):
        # changes direction of the player's heading
        # 0 = right, 1 = left
        if self.direction == 0:
            self.direction = 1
        else:
            self.direction = 0


def redraw_game_window():
    global turn_button_text  # to update the turn value on the screen after every turn
    pygame.display.update()
    win.blit(bg, (0, 0))     # background update

    for pla in range(len(player)): # player position update
        player[pla].draw(win)

    # button value updating
    dice_button.draw(win)
    start_game_button.draw(win)
    instructions_button.draw(win)
    turn_button.draw(win)
    dice_roll_button.draw(win)
    turn_button_text = str(player[player_number].name) + "'s turn"
    turn_button.update_text(turn_button_text)


def display_dice_iterations(count):
    # black rectangle to act as a canvas
    # since the data will be updating after every turn it overlaps the previous data present
    # and replaces it with updated values
    # pygame.draw.rect(win, (0, 0, 0), (520, 320, 250, 250), 0)
    # # setting up 2 fonts for the heading and for the count respectively
    # font = pygame.font.SysFont('arial', 30)
    # font1 = pygame.font.SysFont('arial', 18)
    # text = font.render("- - Dice count - - ", True, (120, 255, 69))
    # text1 = font1.render(" 1  :   " + str(count[1]), True, (120, 255, 69))
    # text2 = font1.render(" 2  :   " + str(count[2]), True, (120, 255, 69))
    # text3 = font1.render(" 3  :   " + str(count[3]), True, (120, 255, 69))
    # text4 = font1.render(" 4  :   " + str(count[4]), True, (120, 255, 69))
    # text5 = font1.render(" 5  :   " + str(count[5]), True, (120, 255, 69))
    # text6 = font1.render(" 6  :   " + str(count[6]), True, (120, 255, 69))
    # # placing text on the frame
    # win.blit(text, (520, 320))
    # win.blit(text1, (530, 350))
    # win.blit(text2, (530, 370))
    # win.blit(text3, (530, 390))
    # win.blit(text4, (630, 350))
    # win.blit(text5, (630, 370))
    # win.blit(text6, (630, 390))
    pass


def display_player_positions():
    # black rectangle is needed to act as a canvas
    # since the data will be updated after every turn it overlaps the previous data present
    # and replaces it with updated values
    pygame.draw.rect(win, (0, 0, 0), (0, 500, 500, 300), 0)
    pygame.draw.rect(win, (0, 0, 0), (400, 500, 550, 250), 0)
    # setting the font
    font = pygame.font.SysFont('arial', 35)
    text1 = font.render(str(player[0].name) + "'s position : " + str(player[0].pos), True, (120, 255, 69))
    text2 = font.render(str(player[1].name) + "'s position : " + str(player[1].pos), True, (120, 255, 69))
    # placing text on the frame
    win.blit(text1, (10, 520))
    win.blit(text2, (400, 520))


def move_player(n):
    # takes player number as argument and moves the player accordingly
    global dice_roll_button_text

    def change_player():
        # changes player
        global player_number, turn_button_text
        if player_number == 1:
            player_number = 0
        else:
            player_number = 1

    def dice_roll():
        # returns a random number between 1 to 6 same as that of a dice
        val = random.randint(1, 6)
        # print(val)
        return val

    def win_check(x):
        positions = {94: 6, 95: 5, 96: 4, 97: 3, 98: 2, 99: 1}  # pos values with corresponding dice roll to win
        plapos = positions[x-roll]
        if roll > plapos:
            # as the player has run out of options for moving, the movements need to be restricted
            player[n].pos -= roll
        else:
            player[n].x -= player[n].speed*roll

        if player[n].pos == 100:
            # player has won the game so the ame finishes
            end_game(n)

    def snake_check():
        pass

    def ladder_check():
        # checks to see if there's a ladder on that position and moves the player to the appropriate location if true
        if player[player_number].pos == 3:
            player[player_number].x -= player[player_number].speed*2
            player[player_number].y -= player[player_number].speed*4
            player[player_number].pos = 41
            direction_update()

        elif player[player_number].pos == 6:
            player[player_number].x += player[player_number].speed*1
            player[player_number].y -= player[player_number].speed*2
            player[player_number].pos = 27
            direction_update()

        elif player[player_number].pos == 11:
            player[player_number].y -= player[player_number].speed*3
            player[player_number].pos = 50
            direction_update()

        elif player[player_number].pos == 36:
            player[player_number].x -= player[player_number].speed*1
            player[player_number].y -= player[player_number].speed*2
            player[player_number].pos = 57
            direction_update()

        elif player[player_number].pos == 55:
            player[player_number].x -= player[player_number].speed*2
            player[player_number].y -= player[player_number].speed*4
            player[player_number].pos = 97
            direction_update()

        elif player[player_number].pos == 60:
            player[player_number].y -= player[player_number].speed*2
            player[player_number].pos = 80
            direction_update()

        elif player[player_number].pos == 67:
            player[player_number].x += player[player_number].speed
            player[player_number].y -= player[player_number].speed*2
            player[player_number].pos = 88
            direction_update()

    def direction_update():
        # when the player comes across a ladder or a snake, they update the direction of moving
        # this is achieved by linking the y coordinates to the appropriate direction
        dir_dict = {455: 0, 404: 1, 353: 0, 302: 1, 251: 0, 200: 1, 149: 0, 98: 1, 47: 0, -4: 1}
        player[player_number].direction = dir_dict[player[player_number].y]

    def movement(n):
        # moves the player by one tile in appropriate direction
        if player[n].direction == 0:
            if player[n].x == 459:
                player[n].y -= player[n].speed
                player[n].change_dir()
            else:
                player[n].x += player[n].speed

        elif player[n].direction == 1:
            if player[n].x == 0:
                player[n].y -= player[n].speed
                player[n].change_dir()
            else:
                player[n].x -= player[n].speed

    roll = dice_roll()  # dice roll
    player[n].roll = roll  # saving the values in the player class

    # updating the dice roll text on the screen
    dice_roll_button_text = str(player[player_number].name) + " rolled " + str(player[player_number].roll)
    dice_roll_button.update_text(dice_roll_button_text)

    # saving the position of the player by summing up the dice rolls
    player[n].pos += roll

    # saving each dice roll in dict
    dice_count[roll] += 1

    if player[n].y == -4 and player[n].x < 357:
        # when the player reaches a certain position where the tiles in front < 6, we need to restrict his movements
        win_check(player[n].pos)

    else:
        # making the movements in one block at at time, so the position can be noted and evaluated
        for number in range(roll):
            movement(n)

    ladder_check()  # checks to see if there is a ladder starting on player's position

    # changing player turn
    change_player()


class Button(object):
    # a button class that eases up the button creation
    # takes color(hex values) x and y co-ordinates, width, height and the text
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    # for placing it on the screen
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        font = pygame.font.SysFont('arial', 40)
        text = font.render(self.text, 1, (0, 0, 0))
        win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    # tells us if the mouse pointer is over the element or not
    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

    def update_color(self, color):
        # updates the color of the button
        self.color = color

    def update_text(self, text):
        # updates the text of the button
        self.text = text


player = [1, 2]
dice_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}  # dice rolls happened in the game

for i in range(len(player)):
    # creating the players up in the board
    player[i] = Player(0, 455)

# setting up the buttons on the screen
start_game_button = Button((96, 69, 96), 503, 2, 240, 95, "start game")
dice_button = Button((96, 69, 96), 503, 100, 240, 95, "roll dice")
instructions_button = Button((96, 69, 96), 503, 198, 240, 95, "instructions")
turn_button = Button((120, 72, 5), 503, 296, 240, 95, text="turn")
dice_roll_button = Button((120, 72, 5), 503, 394, 240, 95, text="roll ")


run = True
direction, player_number = 1, 0
init = 0

# main loop
while run:
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()  # gets the position of the mouse pointer
        if event.type == pygame.QUIT:
            run = False # exits us out of the loop thus ending the game

        if event.type == pygame.MOUSEBUTTONDOWN:
            # checks if the mouse button is down and then the position of the mouse pointer
            # if the pointer location falls inside of the button the functions gets called

            if dice_button.is_over(pos):
                if init == 1:
                    move_player(player_number)
            if start_game_button.is_over(pos):
                if init != 1:
                    start_game()

        # hover functionality for the buttons
        if dice_button.is_over(pygame.mouse.get_pos()):
            if init == 1:
                dice_button.update_color((200, 2, 225))
        else:
            dice_button.update_color((120, 72, 5))

        if start_game_button.is_over(pygame.mouse.get_pos()):
            if init != 1:
                start_game_button.update_color((200, 2, 225))
        else:
            start_game_button.update_color((120, 72, 5))

        if instructions_button.is_over(pygame.mouse.get_pos()):
            instructions_button.update_color((200, 2, 225))
        else:
            instructions_button.update_color((120, 72, 5))

    # redraws game window
    redraw_game_window()
    display_dice_iterations(dice_count)
    display_player_positions()

pygame.quit()


