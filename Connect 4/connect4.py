import pygame, sys, math
import numpy as np

BOARD_COLOR = (41, 76, 133)
BG_COLOR = (242, 242,242)
SHADOW_COLOR = (33, 59, 102)
PL1_COLOR = (219, 37, 37)
PL2_COLOR = (247, 195, 74)
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)

FONTSIZE = 35
WIDTH = 700
HEIGHT = 700

def create_board():
	board = np.zeros((ROW_COUNT, COLUMN_COUNT))
	return board

def drop_token(board, row, col, token):
	board[row][col] = token

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def is_fullboard(board):
	return np.all((board != 0))

def is_winning(board, token):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == token and board[r][c+1] == token and board[r][c+2] == token and board[r][c+3] == token:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == token and board[r+1][c] == token and board[r+2][c] == token and board[r+3][c] == token:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == token and board[r+1][c+1] == token and board[r+2][c+2] == token and board[r+3][c+3] == token:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == token and board[r-1][c+1] == token and board[r-2][c+2] == token and board[r-3][c+3] == token:
				return True

def draw_board(board):
	pygame.draw.rect(screen, BG_COLOR, (0, 100, 100*COLUMN_COUNT, 100*(ROW_COUNT + 1)))
	pygame.draw.rect(screen, BOARD_COLOR, (0, 100, 100*COLUMN_COUNT, 100*(ROW_COUNT + 1)), border_radius = 15)
	offset = 3

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.circle(screen, 
			SHADOW_COLOR, (int(c*SQUARESIZE+SQUARESIZE/2  + offset), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)  + offset), int(RADIUS*(1 + offset*0.01)))
			
			pygame.draw.circle(screen, 
			BG_COLOR, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == 1:
				pygame.draw.circle(screen, 
				PL1_COLOR, (int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, 
				PL2_COLOR, (int(c*SQUARESIZE+SQUARESIZE/2), HEIGHT-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	pygame.display.update()

def blink_board(board):
	for i in range(1, 5):
		draw_board(board)
		pygame.display.update()
		pygame.time.wait(100)
		pygame.draw.rect(screen, BG_COLOR, (0, 0, WIDTH, HEIGHT))
		pygame.display.update()
		pygame.time.wait(100)
	draw_board(board)
	pygame.time.wait(1500)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("consolas", FONTSIZE)
pygame.display.set_caption('Connect 4')
pygame.display.set_icon(pygame.image.load('data/icon.ico'))
clock = pygame.time.Clock()

game_state = "init"
turn = 0
clicked = False
lastPos = WIDTH / 2
board = create_board()

while True:
	posx = lastPos
	col = int(math.floor(posx/SQUARESIZE))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN and game_state != "playing":
			if event.key == pygame.K_SPACE:
				pygame.draw.rect(screen, BG_COLOR, (0, 0, WIDTH, HEIGHT))
				game_state = "playing"
				turn = 0
				board = create_board()
				draw_board(board)

		if event.type == pygame.MOUSEMOTION:
			posx = event.pos[0]

		if event.type == pygame.MOUSEBUTTONDOWN:
			posx = event.pos[0]
			col = int(math.floor(posx/SQUARESIZE))
			clicked = True

	if game_state == "init":
		start_screen = pygame.image.load('data/startscreen.png')
		screen.blit(start_screen, (0, 0))
		pygame.display.update()

	if game_state == "game_over":
		pygame.draw.rect(screen, BG_COLOR, (0, 0, WIDTH, HEIGHT))
		
		color = PL1_COLOR
		player_name = "Red"
		if turn == 0:
			color = PL2_COLOR
			player_name = "Yellow"
		
		if turn == -1:
			win_surface = font.render('Game tie. Good job!', True, (0, 0, 0))	
		else:
			win_surface = font.render(f'Player {player_name} has win the game!' , True, color)
		
		win_rect = win_surface.get_rect(center = (WIDTH / 2, HEIGHT / 2))
		screen.blit(win_surface, win_rect)

		pygame.display.update()
		pygame.time.wait(1500)		
		
		game_state = "init"
	
	if game_state == "playing":
		pygame.draw.rect(screen, BG_COLOR, (0, 0, WIDTH, SQUARESIZE))

		if turn == 0:
			pygame.draw.circle(screen, PL1_COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
		else: 
			pygame.draw.circle(screen, PL2_COLOR, (posx, int(SQUARESIZE/2)), RADIUS)

		if is_valid_location(board, col) and clicked:
			row = get_next_row(board, col)
			drop_token(board, row, col, turn + 1)
			draw_board(board)
			clicked = False

			if is_winning(board, turn + 1):
				blink_board(board)
				game_state = "game_over"
					
			turn += 1
			turn = turn % 2

		if is_fullboard(board):
			turn = -1
			game_state = "game_over"
			
		lastPos = posx
		pygame.display.update()
	
	clock.tick(120)