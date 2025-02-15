import pygame
import sys
pygame.init()
BLACK = (0, 0, 0)
WHITE = (100,110,200)
window_width = 350
window_height = 340
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Game Menu")
font = pygame.font.SysFont("times new roman", 40)
background_image = pygame.image.load ("C:\\Users\\20101\\Desktop\\project Ai\\menu image 1.jpg")
background_image = pygame.transform.scale(background_image, (window_width, window_height))
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
    def draw(self):
        pygame.draw.rect(window, WHITE, self.rect)
        text = font.render(self.text, True, BLACK)
        window.blit(text, (self.rect.x + 10, self.rect.y + 10))
    def click(self):
        if self.action:
            self.action()
def start_connect4():
    print("Starting Connect 4...")
    import connect4
def start_tictactoe():
    print("Starting Tic-Tac-Toe...")
    import tictoc
def exit_game():
    pygame.quit()
    sys.exit()
button_width = 200
button_height = 50
button_connect4 = Button("Connect 4", (window_width - button_width) // 2, 50, button_width, button_height, start_connect4)
button_tictactoe = Button("Tic-Tac-Toe", (window_width - button_width) // 2, 120, button_width, button_height, start_tictactoe)
button_exit = Button("    Exit", (window_width - button_width) // 2, 190, button_width, button_height, exit_game)
def menu():
    while True:
        window.blit(background_image, (0, 0)) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_connect4.rect.collidepoint(pos):
                    button_connect4.click()
                elif button_tictactoe.rect.collidepoint(pos):
                    button_tictactoe.click()
                elif button_exit.rect.collidepoint(pos):
                    button_exit.click()
        button_connect4.draw()
        button_tictactoe.draw()
        button_exit.draw()
        pygame.display.update()  
menu()


