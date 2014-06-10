# Implementation of classic arcade game Pong
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
#import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [-1, 1]
paddle1_pos = [ HALF_PAD_WIDTH, HEIGHT / 2 ]
paddle2_pos = [ (WIDTH - 1) - HALF_PAD_WIDTH, HEIGHT / 2]
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction:
        ball_vel[0] = random.randrange(120, 240) / 60
        ball_vel[1] = - random.randrange(60, 180) / 60 
    else:
        ball_vel[0] = - random.randrange(120, 240) / 60
        ball_vel[1] = - random.randrange(60, 180) / 60
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2# these are ints
    score1 = 0
    score2 = 0
    direction = random.choice([LEFT, RIGHT])
    spawn_ball(direction)

def paddle_cordinates(paddle_pos):
    a = [ paddle_pos[0] - HALF_PAD_WIDTH  , paddle_pos[1] - HALF_PAD_HEIGHT ]
    b = [ paddle_pos[0] + HALF_PAD_WIDTH, paddle_pos[1] - HALF_PAD_HEIGHT ]
    d = [ paddle_pos[0] - HALF_PAD_WIDTH  , paddle_pos[1] + HALF_PAD_HEIGHT ]
    c = [ paddle_pos[0] + HALF_PAD_WIDTH  , paddle_pos[1] + HALF_PAD_HEIGHT ]
    return a, b, c, d

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # collide and bounces off the top and bottom wall
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    # when the ball touches paddle and gutter
    if (ball_pos[0] <= BALL_RADIUS + PAD_WIDTH) and (ball_pos[1] > paddle1_pos[1] - HALF_PAD_HEIGHT) and (ball_pos[1] < paddle1_pos[1] + HALF_PAD_HEIGHT):
        ball_vel[0] = - float( ball_vel[0] * 1.1)
        ball_vel[1] = float( ball_vel[1] * 1.1)
    elif ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        score2 += 1
        spawn_ball(RIGHT)       
    if ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH) and (ball_pos[1] > paddle2_pos[1] - HALF_PAD_HEIGHT) and (ball_pos[1] < paddle2_pos[1] + HALF_PAD_HEIGHT):
        ball_vel[0] = - float( ball_vel[0] * 1.1)
        ball_vel[1] = float( ball_vel[1] * 1.1)
    elif ball_pos[0] >= WIDTH - (BALL_RADIUS + PAD_WIDTH):
        score1 += 1
        spawn_ball(LEFT)
    # draw ball 
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Orange", "Orange")
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos[1] + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT) and (paddle1_pos[1] + paddle1_vel >= HALF_PAD_HEIGHT ):
        paddle1_pos[1] += paddle1_vel
    if (paddle2_pos[1] + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT) and (paddle2_pos[1] + paddle2_vel >= HALF_PAD_HEIGHT ):
        paddle2_pos[1] += paddle2_vel
    # draw paddles
    canvas.draw_polygon(paddle_cordinates(paddle1_pos), 1, "Red", "Red")
    canvas.draw_polygon(paddle_cordinates(paddle2_pos), 1, "Blue", "Blue")
    # draw scores
    canvas.draw_text(str(score1), [200, 40], 20, "White")
    canvas.draw_text(str(score2), [400, 40], 20, "White")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["W"]:
        paddle1_vel = -5
    elif key == simplegui.KEY_MAP["S"]:
        paddle1_vel = 5
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -5
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 5

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["W"] or key == simplegui.KEY_MAP["S"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["up"]or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

def restart():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart, 100)
# start frame
new_game()
frame.start()
