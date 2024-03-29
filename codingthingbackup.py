# Austin Chen and Micah Lam
# HackPNW 2024 Spring
import science_questions
import pygame,sys,math,random, pygame.gfxdraw
import sympy as sp
# Initialize Pygame
pygame.init()
# Set up some constants
FONT = pygame.font.Font(None, 36)
SUBJECTS = ['Numerical Odyssey', 'Discovery Quests', 'Time Traveler Trivia']
GRADES = list(range(1, 11))
QUESTION_BUTTON_SPACING = 100
background_image_math = pygame.image.load("mathbackground.jpeg")
backgroundimagescience = pygame.image.load('ScienceBackground.png')
backgroundimagestitlescreen = pygame.image.load('titlescreen.jpeg')
backgroundimageslevelscreen = pygame.image.load('levelscreen.jpeg')
backgroundimagessubjectscreen = pygame.image.load('gamemodeselect.png')


# Set up the display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
background_image = pygame.transform.scale(background_image_math, (WIDTH, HEIGHT))
backgroundimage = pygame.transform.scale(backgroundimagescience, (WIDTH, HEIGHT)).convert()
backgroundimagetitle = pygame.transform.scale(backgroundimagestitlescreen, (WIDTH, HEIGHT)).convert()
backgroundimagelevel = pygame.transform.scale(backgroundimageslevelscreen, (WIDTH, HEIGHT)).convert()
backgroundimagesubect = pygame.transform.scale(backgroundimagessubjectscreen, (WIDTH, HEIGHT)).convert()
pygame.display.set_caption('Study Quest')
# Functions for drawing text and buttons
def draw_text(text, x, y):
	text_surface = FONT.render(text, True, TEXT_COLOR)
	text_rect = text_surface.get_rect(center=(x, y))
	screen.blit(text_surface, text_rect)


def draw_text_with_size(text, x, y, size,color):
	global UserAnswerInput
	font = pygame.font.Font(None, size)
	text_surface = font.render(text, True, (color))
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	screen.blit(text_surface, text_rect)

CanInputMathAnswer = True
user_input = ""
score = 0
BUTTON_COLOR = (0, 200, 200)
BUTTON_HOVER_COLOR = (0, 255, 255)
TEXT_COLOR = (255, 255, 255)
# New function for drawing circular buttons
def draw_circle_button(text, x, y, radius, color, hover_color, action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if (x - mouse[0]) ** 2 + (y - mouse[1]) ** 2 < radius ** 2:
		pygame.draw.circle(screen, hover_color, (x, y), radius)
		if click[0] == 1 and action is not None:
			action()
			pygame.time.wait(300)  # Wait for 200 milliseconds
	else:
		pygame.draw.circle(screen, color, (x, y), radius)
	draw_text(text, x, y)
def draw_square_button(text, x, y, width, height, color, hover_color, action=None, is_back_button=False):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	rect = pygame.Rect(x, y, width, height)
	color = hover_color if rect.collidepoint(mouse) else color
	draw_rounded_rect(screen, rect, color, 10)
	if rect.collidepoint(mouse) and click[0] == 1 and action is not None:
		action()
		while pygame.mouse.get_pressed()[0]:
			pygame.event.pump()
	draw_text(text, x + width / 2, y + height / 2)
	if is_back_button:
		# Draw the back arrow
		arrow_color = (255, 255, 255)
		arrow_margin = 10
		arrow_width = 10
		arrow_height = height / 4
		arrow_points = [(x + arrow_margin, y + height / 2), (x + arrow_margin + arrow_width, y + height / 2 - arrow_height / 2), (x + arrow_margin + arrow_width, y + height / 2 + arrow_height / 2)]
		pygame.draw.polygon(screen, arrow_color, arrow_points)
	text_x = x + width / 2
	text_y = y + height / 2
	draw_text(text, text_x, text_y)
def draw_rounded_rect(surface, rect, color, corner_radius):
	if corner_radius < 0:
		raise ValueError(f"Corner radius {corner_radius} must be >= 0")
	elif corner_radius > min(rect.width, rect.height) / 2:
		raise ValueError(f"Corner radius {corner_radius} must be <= min(rect.width, rect.height) / 2")
	# Draw the four corners
	pygame.gfxdraw.aacircle(surface, rect.left + corner_radius, rect.top + corner_radius, corner_radius, color)
	pygame.gfxdraw.filled_circle(surface, rect.left + corner_radius, rect.top + corner_radius, corner_radius, color)
	pygame.gfxdraw.aacircle(surface, rect.right - corner_radius - 1, rect.top + corner_radius, corner_radius, color)
	pygame.gfxdraw.filled_circle(surface, rect.right - corner_radius - 1, rect.top + corner_radius, corner_radius, color)
	pygame.gfxdraw.aacircle(surface, rect.left + corner_radius, rect.bottom - corner_radius - 1, corner_radius, color)
	pygame.gfxdraw.filled_circle(surface, rect.left + corner_radius, rect.bottom - corner_radius - 1, corner_radius, color)
	pygame.gfxdraw.aacircle(surface, rect.right - corner_radius - 1, rect.bottom - corner_radius - 1, corner_radius, color)
	pygame.gfxdraw.filled_circle(surface, rect.right - corner_radius - 1, rect.bottom - corner_radius - 1, corner_radius, color)
	# Draw the four edge rectangles
	pygame.draw.rect(surface, color, pygame.Rect(rect.left, rect.top + corner_radius, corner_radius, rect.height - 2 * corner_radius))
	pygame.draw.rect(surface, color, pygame.Rect(rect.right - corner_radius, rect.top + corner_radius, corner_radius, rect.height - 2 * corner_radius))
	pygame.draw.rect(surface, color, pygame.Rect(rect.left + corner_radius, rect.top, rect.width - 2 * corner_radius, corner_radius))
	pygame.draw.rect(surface, color, pygame.Rect(rect.left + corner_radius, rect.bottom - corner_radius, rect.width - 2 * corner_radius, corner_radius))
	# Draw the center rectangle
	pygame.draw.rect(surface, color, pygame.Rect(rect.left + corner_radius, rect.top + corner_radius, rect.width - 2 * corner_radius, rect.height - 2 * corner_radius))



# Initialize the game state
state = {
	'screen_stack': ['title'],
	'subject': None,
	'grade': None,
	'score': 0,
}
state['question_number'] = 1
def get_questions_for_grade(grade):
	# Get all attributes of the science_questions module
	all_questions = dir(science_questions)
	
	# Initialize an empty list to store the questions for the grade
	grade_questions = []
	
	# Iterate over all questions
	for question in all_questions:
		# Check if the question is for the given grade
		if question.startswith(f"Grade{grade}"):
			# If it is, add each question separately to the list
			question_list = getattr(science_questions, question)
			grade_questions.append(question_list)

	return grade_questions

def draw_return_button():
	button_radius = 50
	button_x = 10 + button_radius
	button_y = HEIGHT - 10 - button_radius

	draw_circle_button('Return', button_x, button_y, button_radius, (128,128,128), (105,105,105), return_to_start)
def return_to_start():
	state['screen_stack'].clear()
	state['screen_stack'].append('title')

def draw_equation(equation, screen, position, font, color=(255, 255, 255)):

	text = font.render(equation, True, color)
	screen.blit(text, position)

def generate_and_solve_math_problem():
	x = sp.symbols('x')
	operator = random.choice(['+', '-', '*'])

	num1 = random.randint(1, 10)
	num2 = random.randint(1, 10)
	if operator == '+':
		equation = f"{num1} + {num2} = "
		solution = round(num1 + num2, 2)
	elif operator == '-':
		equation = f"{num1} - {num2} = "
		solution = round(num1 - num2, 2)
	elif operator == '*':
		equation = f"{num1} x {num2} = "
		solution = round(num1 * num2, 2)
	return equation, solution
equation, solution = generate_and_solve_math_problem()
	
	
	
def choose_subject(subject):
	state['subject'] = subject
def navigate_to(screen):
	state['screen_stack'].append(screen)
def back():
	if len(state['screen_stack']) > 1:
		state['screen_stack'].pop()
def start_game():
	navigate_to('grade')
def choose_grade(grade):
	state['grade'] = grade
	navigate_to('subject')
def choose_subject(subject):
	state['subject'] = subject
	navigate_to('game')
def make_grade_lambda(grade):
	return lambda: choose_grade(grade)
def make_subject_lambda(subject):
	return lambda: choose_subject(subject)
def draw_level_buttons():
	button_radius = 50
	button_spacing = WIDTH // (len(GRADES) + 1)
	for i, grade in enumerate(GRADES):
		color = (255 * i // len(GRADES), 255 - 255 * i // len(GRADES), 0)
		hover_color = (min(255, color[0] + 50), max(0, color[1] - 50), 0)
		x = button_spacing * (i + 1)
		draw_circle_button(str(grade), x, HEIGHT / 2 - button_radius, button_radius, color, hover_color, make_grade_lambda(grade))
	draw_text_with_size('Level Select', WIDTH / 2, HEIGHT / 4, 60, (255,255,255))
def draw_subject_buttons():
	if state['grade'] is None:
		return
	button_width = 300
	button_height = 50
	button_spacing = (WIDTH - button_width * len(SUBJECTS)) // (len(SUBJECTS) + 1)
	for i, subject in enumerate(SUBJECTS):
		x = button_spacing * (i + 1) + button_width * i
		y = HEIGHT / 2 - button_height / 2
		draw_square_button(subject, x, y, button_width, button_height, BUTTON_COLOR, BUTTON_HOVER_COLOR, make_subject_lambda(subject))
	draw_text_with_size('Choose Game Mode', WIDTH / 2, HEIGHT / 4, 60, (255,255,255))
def draw_back_button():
	button_radius = 50
	button_x = WIDTH - 10 - button_radius
	button_y = HEIGHT - 10 - button_radius

	draw_circle_button('Back', button_x, button_y, button_radius, (128,128,128), (105,105,105), back)

def draw_title_screen():
	draw_text_with_size('Welcome to Study Quest!', WIDTH / 2, HEIGHT / 3, 100,(255,255,255))
	draw_text('Click Start to begin', WIDTH / 2, HEIGHT / 2)
	button_width = 200
	button_height = 50
	x = (WIDTH - button_width) / 2
	y = HEIGHT * 2 / 3
	draw_square_button('Start', x, y, button_width, button_height, BUTTON_COLOR, BUTTON_HOVER_COLOR, start_game)
 
def text_objects(text, font):
	text_surface = font.render(text, True, (0, 0, 0))  # Replace (0, 0, 0) with the color you want for the text
	return text_surface, text_surface.get_rect()
def draw_button(text, x, y, width, height, color, hover_color, on_click, state):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x + width > mouse[0] > x and y + height > mouse[1] > y:
		pygame.draw.rect(screen, hover_color, (x, y, width, height))
		if click[0] == 1 and on_click is not None:
			on_click()
	else:
		pygame.draw.rect(screen, color, (x, y, width, height))

	font_size = int(width / len(text))
	if font_size > height * 0.4:
		font_size = int(height * 0.4)
	small_text = pygame.font.Font(None, font_size)
	text_surf, text_rect = text_objects(text, small_text)
	text_rect.center = ((x + (width / 2)), (y + (height / 2)))
	screen.blit(text_surf, text_rect)
 

def draw_question_and_answers():
	questions = get_questions_for_grade(state['grade'])
	if state['question_number'] is None:
		state['question_number'] = 0
	question_data = questions[state['question_number']]
	question_text = question_data[0]
	answer_texts = question_data[1:-1]
	question_center_x = WIDTH  / 2
	draw_text(question_text, question_center_x, 50)
	button_width = 500
	button_height = 200
	button_y_start = 200
	button_spacing = 20
	total_width = 2 * button_width + button_spacing

	# Define the colors
	colors = [(255, 255, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0)]  # Yellow, Blue, Green, Red
	hover_colors = [(200, 200, 0), (0, 0, 200), (0, 200, 0), (200, 0, 0)]  # Darker versions of the colors

	for i, answer_text in enumerate(answer_texts):
		# Centralize buttons
		button_x = (i % 2) * (button_width + button_spacing) + (WIDTH - total_width) / 2
		button_y = (i // 2) * (button_height + button_spacing) + button_y_start
		draw_button(answer_text, button_x, button_y, button_width, button_height, colors[i], hover_colors[i], lambda i=i: process_answer(i), state)
		
def draw_next_question_button():
	button_color = (0, 255, 0)  # Green
	button_rect = pygame.Rect(WIDTH - 200, HEIGHT - 50, 150, 40)
	pygame.draw.rect(screen, button_color, button_rect)

	font = pygame.font.Font(None, 24)
	text = font.render('Next Question', True, (0, 0, 0))
	screen.blit(text, (WIDTH - 180, HEIGHT - 40))

	return button_rect



def get_correct_answer_index(grade, question_number):
	questions = get_questions_for_grade(grade)
	question_data = questions[question_number]
	return question_data[-1]

def process_answer(answer_index):
	# This function will process the user's answer
	correct_answer_index = get_correct_answer_index(state['grade'], state['question_number'])
	if answer_index + 1 == correct_answer_index:
		state['score'] += 1
		state['screen_stack'].append('correct_answer')
	else:
		state['screen_stack'].append('wrong_answer')
	state['screen_stack'].append('correct_answer' if answer_index + 1 == correct_answer_index else 'wrong_answer')


def draw_correct_answer_screen():
	if 'correct_answer' not in state['screen_stack']:
		state['score'] += 1
		state['screen_stack'].append('correct_answer')
	draw_text('Correct!', WIDTH / 2, HEIGHT / 2)
	draw_button('Next Question', button_x, button_y, button_width, button_height, (0, 0, 255), (0, 0, 128), next_question, state)

def draw_wrong_answer_screen():
	draw_text('Wrong Answer!', WIDTH / 2, HEIGHT / 2)
	draw_button('Next Question', button_x, button_y, button_width, button_height, (0, 0, 255), (0, 0, 128), next_question, state)

button_width = 200
button_height = 50
button_x = WIDTH - button_width - 10
button_y = HEIGHT - button_height - 10
next_question_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
state['processing_question'] = False

def next_question():
	if state.get('processing_question', False):
		return

	state['processing_question'] = True

	questions = get_questions_for_grade(state['grade'])
	if not questions:
		state['question_number'] = None
		state['processing_question'] = False
		state['screen_stack'].append('game_over')
		return

	# Move to the next question
	state['question_number'] = (state['question_number'] + 1) % len(questions)

	# Pop the correct/wrong answer screen or game_over screen from the stack
	screen_to_pop = 'correct_answer' if 'correct_answer' in state['screen_stack'] else 'wrong_answer' if 'wrong_answer' in state['screen_stack'] else 'game_over'
	state['screen_stack'].remove(screen_to_pop)

	state['processing_question'] = False


def generate_new_equation():
	global equation, solution, user_input
	equation, solution = generate_and_solve_math_problem()
	user_input = ""


# Main game loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		elif event.type == pygame.KEYDOWN:
			if state['subject'] == 'Numerical Odyssey':
				if event.key == pygame.K_RETURN and CanInputMathAnswer == True:
					if str(user_input) == str(solution):
						user_input = 'Correct!'
						state['score'] += 1
						CanInputMathAnswer = False		
					elif str(user_input) != str(solution) and CanInputMathAnswer == True:
						user_input = 'Incorrect. The answer was ' + str(solution)
						CanInputMathAnswer = False
				elif event.key == pygame.K_BACKSPACE:
					user_input = user_input[:-1]
				else:
					if event.unicode.isnumeric() or event.unicode in ['-', '.']:
						if CanInputMathAnswer == True:
							user_input += event.unicode
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				if state['subject'] == 'Numerical Odyssey' and next_question_button_rect.collidepoint(event.pos) and user_input != '':  # Check if the mouse is over the button
					CanInputMathAnswer = True
					user_input = ''
					generate_new_equation()

	screen.fill((0, 0, 0))

	current_screen = state['screen_stack'][-1]
	if current_screen == 'title':
		screen.blit(backgroundimagetitle, (0, 0))
		draw_title_screen()
	elif current_screen == 'grade':
		screen.blit(backgroundimageslevelscreen, (0, 0))
		draw_level_buttons()
		draw_back_button()
	elif current_screen == 'subject':
		screen.blit(backgroundimagessubjectscreen, (0, 0))
		draw_text_with_size(f"Level: {state['grade']}", WIDTH - 100, 10, 36, (255,255,255))
		draw_subject_buttons()
		draw_back_button()
	else:
		draw_text_with_size(f"Level: {state['grade']}", WIDTH - 100, 10, 36,(255,255,255))
		if state['subject'] == 'Discovery Quests':
			screen.blit(backgroundimage, (0, 0))
			draw_return_button()
			draw_question_and_answers()
			draw_text_with_size(f"Score: {state['score']}", WIDTH - 100, 50, 36,(255,255,255))
			draw_text_with_size(state['subject'], 100, 10, 24, (255,255,255)) 
		elif state['subject'] == 'Numerical Odyssey':
			screen.blit(background_image, (0, 0))
			draw_return_button()
			draw_text_with_size(f"Level: {state['grade']}", WIDTH - 100, 10, 36,(0,0,0))
			next_question_button = draw_next_question_button()
			draw_text_with_size(f"Question: {equation}", 1000, 50, 80,(0,0,0))
			draw_text_with_size(f"Answer: {user_input}", 1000, 500, 80,(0,0,0))
			draw_text_with_size(f"Score: {state['score']}", WIDTH - 100, 50, 36,(0,0,0))
			draw_text_with_size(state['subject'], 100, 10, 24, (0,0,0)) 

	if current_screen == 'correct_answer':
		screen.blit(backgroundimage, (0, 0))
		draw_correct_answer_screen()

	elif current_screen == 'wrong_answer':
		screen.blit(backgroundimage, (0, 0))
		draw_wrong_answer_screen()

	pygame.display.flip()