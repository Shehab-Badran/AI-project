import pygame
import sys
import random
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)
board = [[0 for _ in range(3)] for _ in range(3)]  
player_turn = True 
game_over = False 
level = None  
def draw_button(text, color, x, y, w, h):
    pygame.draw.rect(screen, color, (x, y, w, h))
    button_text = small_font.render(text, True, WHITE)
    text_rect = button_text.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(button_text, text_rect)

def choose_level():
    global level
    while True:
        screen.fill(WHITE)
        text = font.render("Choose Level", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(text, text_rect)

        button_width = 200
        button_height = 60
        button_spacing = 20  
        total_button_height = 3 * button_height + 2 * button_spacing
        start_y = (HEIGHT - total_button_height) // 2

        draw_button("Easy", BLACK, WIDTH // 2 - button_width // 2, start_y, button_width, button_height)
        draw_button("Medium", BLACK, WIDTH // 2 - button_width // 2, start_y + button_height + button_spacing, button_width, button_height)
        draw_button("Hard", BLACK, WIDTH // 2 - button_width // 2, start_y + 2 * (button_height + button_spacing), button_width, button_height)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if WIDTH // 2 - button_width // 2 <= mouse_x <= WIDTH // 2 + button_width // 2:
                    if HEIGHT // 2 - button_height // 2 - 50 <= mouse_y <= HEIGHT // 2 - button_height // 2 + 10:
                        level = 'easy'
                        return
                    elif HEIGHT // 2 - button_height // 2 <= mouse_y <= HEIGHT // 2 - button_height // 2 + 60:
                        level = 'medium'
                        return
                    elif HEIGHT // 2 - button_height // 2 + 80 <= mouse_y <= HEIGHT // 2 - button_height // 2 + 140:
                        level = 'hard'
                        return

def alpha_beta_pruning(board, depth, alpha, beta, is_maximizing):
    winner = check_winner()
    if winner == 2: 
        return 1
    elif winner == 1:  
        return -1
    elif is_board_full():  
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == 0:  
                    board[row][col] = 2 
                    score = alpha_beta_pruning(board, depth + 1, alpha, beta, False)
                    board[row][col] = 0 
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break  
        return best_score
    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == 0:  
                    board[row][col] = 1  
                    score = alpha_beta_pruning(board, depth + 1, alpha, beta, True)
                    board[row][col] = 0 
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break  
        return best_score


def best_move():

    best_score = -float('inf')
    move = (-1, -1)
    max_depth = 3  

    if level == 'easy':
        max_depth = 1
    elif level == 'hard':
        max_depth = 5
    
    for row in range(3):
        for col in range(3):
            if board[row][col] == 0:  
                board[row][col] = 2 
                score = alpha_beta_pruning(board, 0, -float('inf'), float('inf'), False)
                board[row][col] = 0 
                if score > best_score:
                    best_score = score
                    move = (row, col)
    return move

def draw_board():
    
    screen.fill(WHITE)
    for x in range(1, 3):
        pygame.draw.line(screen, BLACK, (x * WIDTH // 3, 0), (x * WIDTH // 3, HEIGHT), 3)
        pygame.draw.line(screen, BLACK, (0, x * HEIGHT // 3), (WIDTH, x * HEIGHT // 3), 3)

    for row in range(3):
        for col in range(3):
            if board[row][col] == 1:  # Player
                pygame.draw.circle(screen, BLUE, (col * 200 + 100, row * 200 + 100), 50, 3)
            elif board[row][col] == 2:  # Computer
                pygame.draw.line(screen, RED, (col * 200 + 50, row * 200 + 50),
                                 (col * 200 + 150, row * 200 + 150), 5)
                pygame.draw.line(screen, RED, (col * 200 + 150, row * 200 + 50),
                                 (col * 200 + 50, row * 200 + 150), 5)


def check_winner():
   
    for row in board:
        if row[0] == row[1] == row[2] != 0:
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != 0:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]
    return 0


def is_board_full():
   
    return all(cell != 0 for row in board for cell in row)


def display_message(text):
    screen.fill(WHITE)
    message = font.render(text, True, BLACK)
    text_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(message, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

# Main game loop
running = True
choose_level() 

while running:
    draw_board()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and player_turn and not game_over:
            x, y = event.pos
            row, col = y // 200, x // 200
            if board[row][col] == 0:
                board[row][col] = 1 
                player_turn = False

  
    winner = check_winner()
    if winner:
        draw_board()
        pygame.display.flip()
        if winner == 1:
            display_message("Player Wins!")
        elif winner == 2:
            display_message("Computer Wins!")
        board = [[0 for _ in range(3)] for _ in range(3)]  
        player_turn = True
        game_over = True  
        continue
    elif is_board_full():
        draw_board()
        pygame.display.flip()
        display_message("It's a Draw!")
        board = [[0 for _ in range(3)] for _ in range(3)]  
        player_turn = True
        game_over = True
        continue

   
    if not player_turn and not game_over:
        row, col = best_move()  
        board[row][col] = 2  
        player_turn = True

pygame.quit()
sys.exit()









