# Austin Chen and Micah Lam
# HackPNW 2024 Spring
import science_questions
import pygame,sys,math,random, pygame.gfxdraw
import sympy as sp
# Initialize Pygame
pygame.init()
# Set up some constants
WIDTH, HEIGHT = 1000, 1000
FONT = pygame.font.Font(None, 36)
SUBJECTS = ['Numerical Odyssey', 'Discovery Quests', 'Time Traveler Trivia']
GRADES = list(range(1, 11))
QUESTION_BUTTON_SPACING = 100
# Set up the display
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
pygame.display.set_caption('Study Quest')
# Functions for drawing text and buttons
def draw_text(text, x, y):
	text_surface = FONT.render(text, True, TEXT_COLOR)
	text_rect = text_surface.get_rect(center=(x, y))
	screen.blit(text_surface, text_rect)
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
		while pygame.mouse.get_pressed()[0]:  # Wait for the mouse button to be released
			pygame.event.pump()  # Process events to prevent the application from becoming unresponsive
	draw_text(text, x + width / 2, y + height / 2)
	if is_back_button:
		# Draw the back arrow
		arrow_color = (255, 255, 255)  # White
		arrow_margin = 10  # Margin from the edges of the button
		arrow_width = 10  # Width of the arrow
		arrow_height = height / 4  # Height of the arrow
		arrow_points = [(x + arrow_margin, y + height / 2), (x + arrow_margin + arrow_width, y + height / 2 - arrow_height / 2), (x + arrow_margin + arrow_width, y + height / 2 + arrow_height / 2)]
		pygame.draw.polygon(screen, arrow_color, arrow_points)
	# Draw the text at the center of the button
	text_x = x + width / 2
	text_y = y + height / 2
	draw_text(text, text_x, text_y)
def draw_rounded_rect(surface, rect, color, corner_radius):
	"""Draw a rectangle with rounded corners"""
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
# Python
# Python
class InputBox:
	def __init__(self, x, y, w, h, text=''):
		self.rect = pygame.Rect(x, y, w, h)
		self.color = pygame.Color('dodgerblue2')
		self.text = text
		self.font = pygame.font.Font(None, 32)
		self.txt_surface = self.font.render(text, True, self.color)
		self.active = False
	def handle_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
			else:
				self.active = False
			self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
		if event.type == pygame.KEYDOWN:
			if self.active:
				if event.key == pygame.K_RETURN:
					print(self.text)
					self.text = ''
				elif event.key == pygame.K_BACKSPACE:
					self.text = self.text[:-1]
				else:
					self.text += event.unicode
				self.txt_surface = self.font.render(self.text, True, self.color)
	def draw(self, screen):
		pygame.draw.rect(screen, self.color, self.rect, 2)
		screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
# Initialize the game state
state = {
	'screen_stack': ['title'],
	'subject': None,
	'grade': None,
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

def generate_and_solve_math_problem():
	x = sp.symbols('x')
	operator = random.choice(['+', '-', '*', '/', 'log', 'exp', 'algebra'])
	
	if operator == 'algebra':
		# Generate a, b, c such that b^2 - 4ac is a perfect square
		a = random.randint(1, 10)
		perfect_square = random.choice([i**2 for i in range(1, 11)])  # perfect squares from 1 to 100
		b = random.randint(-10, 10)
		c = (b**2 - perfect_square) // (4*a)
		superscript = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
		equation = f"{a}x{str(2).translate(superscript)} + {b}x + {c} = 0"
		solution = sp.solve(sp.Eq(a * x**2 + b * x + c, 0), x)
		solution = ', '.join([f"x = {round(sol.evalf(), 2)}" for sol in solution])
	else:
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
		elif operator == '/':
			equation = f"{num1} ÷ {num2} = "
			solution = round(num1 / num2, 2)
		elif operator == 'log':
			subscript = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
			equation = f"log{str(num1).translate(subscript)}(x) = {num2}"
			solution = round(num1 ** num2, 2)
		elif operator == 'exp':
			superscript = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
			equation = f"{num1}{str(num2).translate(superscript)} ="
			solution = round(num1 ** num2, 2)
		else:
			equation = "Invalid operator"
			solution = "N/A"
	return equation, solution
equation, solution = generate_and_solve_math_problem()
# print(f"Equation: {equation}\nAnswer: {solution}")
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
		# Create a gradient from green to red
		color = (255 * i // len(GRADES), 255 - 255 * i // len(GRADES), 0)
		hover_color = (min(255, color[0] + 50), max(0, color[1] - 50), 0)
		x = button_spacing * (i + 1)
		draw_circle_button(str(grade), x, HEIGHT / 2 - button_radius, button_radius, color, hover_color, make_grade_lambda(grade))
	draw_text('Level Select', WIDTH / 2, HEIGHT / 4)
def draw_subject_buttons():
	if state['grade'] is None:  # Ignore clicks on subject buttons if grade is not yet selected
		return
	button_width = 300
	button_height = 50
	button_spacing = (WIDTH - button_width * len(SUBJECTS)) // (len(SUBJECTS) + 1)
	for i, subject in enumerate(SUBJECTS):
		x = button_spacing * (i + 1) + button_width * i
		y = HEIGHT / 2 - button_height / 2
		draw_square_button(subject, x, y, button_width, button_height, BUTTON_COLOR, BUTTON_HOVER_COLOR, make_subject_lambda(subject))
	draw_text('Choose Game Mode', WIDTH / 2, HEIGHT / 4)  # Add this line
# Adjust the y-coordinate of the welcome text to be at the top of the screen
draw_text('Welcome to Study Quest!', WIDTH / 2, HEIGHT / 10)
def draw_back_button():
	button_width = 100
	button_height = 50
	x = WIDTH - button_width - 20  
	y = HEIGHT - button_height - 20  
	draw_square_button("Back", 50, 50, 100, 50, (0, 0, 255), (0, 0, 128), back, True)
def reset_state():
	state['subject'] = None
	state['grade'] = None
	state['screen'] = 'title'
# Main game loop
def draw_title_screen():
	draw_text('Welcome to Study Quest!', WIDTH / 2, HEIGHT / 3)
	draw_text('Click Start to begin', WIDTH / 2, HEIGHT / 2)
	button_width = 200
	button_height = 50
	x = (WIDTH - button_width) / 2
	y = HEIGHT * 2 / 3
	draw_square_button('Start', x, y, button_width, button_height, BUTTON_COLOR, BUTTON_HOVER_COLOR, start_game)
 
def text_objects(text, font):
	text_surface = font.render(text, True, (0, 0, 0))  # Replace (0, 0, 0) with the color you want for the text
	return text_surface, text_surface.get_rect()
def draw_button(text, x, y, width, height, color, hover_color, action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	if x + width > mouse[0] > x and y + height > mouse[1] > y:
		pygame.draw.rect(screen, hover_color, (x, y, width, height))
		if click[0] == 1 and action is not None:
			action()
	else:
		pygame.draw.rect(screen, color, (x, y, width, height))
	small_text = pygame.font.Font("freesansbold.ttf", 20)
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
	# Create a font object
	font = pygame.font.Font(None, 25)
	# Get the width of the text
	text_width, _ = font.size(question_text)
	# Calculate the center position for the question
	question_center_x = (WIDTH - text_width) / 2
	# Draw the question at the center
	draw_text(question_text, question_center_x, 50)
	# Increase button size
	button_width = 400
	button_height = 150
	button_y_start = 200
	button_spacing = 50
	# Calculate total width of two buttons and a space
	total_width = 2 * button_width + button_spacing
	for i, answer_text in enumerate(answer_texts):
		# Centralize buttons
		button_x = (i % 2) * (button_width + button_spacing) + (WIDTH - total_width) / 2
		button_y = (i // 2) * (button_height + button_spacing) + button_y_start
		draw_button(answer_text, button_x, button_y, button_width, button_height, (0, 0, 255), (0, 0, 128), lambda: process_answer(i))
def process_answer(answer_index):
	# This function will process the user's answer
	# Replace this with your own logic
	print(f"User selected answer {answer_index}")
def get_correct_answer_index(grade, question_number):
	questions = get_questions_for_grade(grade)
	question_data = questions[question_number]
	return question_data[-1]  # Get the last element of the list, which is the correct answer index
def process_answer(answer_index):
	# This function will process the user's answer
	correct_answer_index = get_correct_answer_index(state['grade'], state['question_number'])
	if answer_index + 1 == correct_answer_index:  # Add 1 to the user's answer index
		state['screen_stack'].append('correct_answer')
	else:
		state['screen_stack'].append('wrong_answer')
# Then, in your main game loop, add the following conditions:
def draw_correct_answer_screen():
	screen.fill((0, 0, 0))  # Fill the screen with black color
	draw_text('Correct!', WIDTH / 2, HEIGHT / 2)  # Draw the text
	draw_button('Next Question', button_x, button_y, button_width, button_height, (0, 0, 255), (0, 0, 128), next_question)

def draw_wrong_answer_screen():
	screen.fill((0, 0, 0))  # Fill the screen with black color
	draw_text('Wrong Answer!', WIDTH / 2, HEIGHT / 2)  # Draw the text
	draw_button('Next Question', button_x, button_y, button_width, button_height, (0, 0, 255), (0, 0, 128), next_question)

button_width = 200
button_height = 50
button_x = WIDTH - button_width - 10  # 10 is the margin from the right edge
button_y = HEIGHT - button_height - 10  # 10 is the margin from the bottom edge	
next_question_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
# def next_question():
# 	state['question_number'] += 1  # Go to the next question
# 	if state['question_number'] >= len(get_questions_for_grade(state['grade'])):  # If there are no more questions
# 		state['question_number'] = None  # Reset the question number
# 		state['screen_stack'].append('game_over')  # Go to the game over screen
# 	else:
# 		state['screen_stack'].pop()  # Remove the correct answer screen from the stack to go back to the game
# state['processing_question'] = False
def next_question():
    if state.get('processing_question', False):
        return

    state['processing_question'] = True

    # Check if there are questions for the current grade
    questions = get_questions_for_grade(state['grade'])
    if not questions:
        state['question_number'] = None
        state['processing_question'] = False
        state['screen_stack'].append('game_over')
        return

    # Move to the next question
    state['question_number'] = (state['question_number'] + 1) % len(questions)
    print(f"Next question number: {state['question_number']}")  # Debugging line

    # Pop the correct/wrong answer screen or game_over screen from the stack
    screen_to_pop = 'correct_answer' if 'correct_answer' in state['screen_stack'] else 'wrong_answer' if 'wrong_answer' in state['screen_stack'] else 'game_over'
    state['screen_stack'].remove(screen_to_pop)

    state['processing_question'] = False

# Replace your existing next_question function with this improved version.




# Main game loop
while True:
	
	current_screen = state['screen_stack'][-1]
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if state['screen_stack'][-1] == 'game':  # Only handle events during the game screen
				if next_question_button_rect.collidepoint(event.pos) and not state.get('processing_question', False):
					state['processing_question'] = True  # Indicate that a question is currently being processed
					next_question()

		# Add this section to handle events for InputBox (Numerical Odyssey)
		elif current_screen == 'game' and state['subject'] == 'Numerical Odyssey' and InputBox is not None:
			InputBox.handle_event(event)
		# Draw the InputBox (Numerical Odyssey) if it exists
	if current_screen == 'game' and state['subject'] == 'Numerical Odyssey' and InputBox is not None:
		InputBox.draw(screen)

	screen.fill((0, 0, 0))
	# input_box.draw(screen)
	if current_screen == 'title':
		draw_title_screen()
	elif current_screen == 'grade':
		draw_level_buttons()
		draw_back_button()
	elif current_screen == 'subject':
		draw_text(f"Current Level: {state['grade']}", WIDTH / 2, 100)  
		draw_subject_buttons()
		draw_back_button()
	else:  # current_screen == 'game'
		draw_text(f"Current Level: {state['grade']}", WIDTH / 2, 50)  
		draw_text(f"Current Subject: {state['subject']}", WIDTH / 2, 100)  
		draw_back_button()
		screen.fill((0, 0, 0))
	if current_screen == 'title':
		draw_title_screen()
	elif current_screen == 'grade':
		if state['grade'] is None:
			draw_text('Welcome to Study Quest!', WIDTH / 2, 50)  # Move the welcome text to the top
		draw_level_buttons()
		draw_back_button()
	elif state['subject'] is None:
		draw_text(f"Current Level: {state['grade']}", WIDTH / 2, 100)  # Display the chosen grade below the welcome text
		draw_subject_buttons()
	else:
		draw_text(f"Current Level: {state['grade']}", WIDTH / 2, 50)  # Display the chosen grade at the top
		draw_text(f"Current Subject: {state['subject']}", WIDTH / 2, 100)  # Display the chosen subject below the grade
		if state['subject'] == 'Discovery Quests':
			draw_question_and_answers()
	if current_screen == 'correct_answer':
		draw_correct_answer_screen()
	elif current_screen == 'wrong_answer':
		draw_wrong_answer_screen()
	if state.get('processing_question', False) and state['question_number'] is not None:
		state['processing_question'] = False
	pygame.display.flip()