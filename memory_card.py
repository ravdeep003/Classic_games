# implementation of card game - Memory

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

back_image = simplegui.load_image("https://dl.dropboxusercontent.com/u/38413745/back_card.png")

#Start a new game
def new_game():
    global cards, state, turn, exposed
    turn = 0
    state = 0 			   # State of cards
    exposed = [False] * 16 # By default all cards are facing down
    list1 = range(8)
    cards = list1 + list1
    random.shuffle(cards) # creates random deck of card  
    label.set_text("Turns = " + str(turn))
                    
# Mouse click event handlers
def mouseclick(pos):
    global exposed, state, first_card, second_card, turn
    start = 0
    end = 49
    for i in range(16):
        if pos[0] >= start and pos[0] <= end and exposed[i] == False: 
            if state == 0:
                state = 1
                first_card = i
            elif state == 1:
                state = 2
                second_card = i
                turn += 1
                label.set_text("Turns = " + str(turn))
            else:
                if cards[first_card] != cards[second_card]:
                    exposed[first_card],exposed[second_card] = (False, False)
                state = 1
                first_card = i
            exposed[i] = True    
            break
        start += 50
        end += 50
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    (text_width, text_height) = (15, 70)
    image_width, image_height = 221,300
    dest_width = 25
    width = 0
    for i in range(16):
        if exposed[i]:
            canvas.draw_text(str(cards[i]),(text_width,text_height), 55, "White")
        else:
            #point_list = [(width,0), (width+50,0) ,(width+50,100),(width,100)]
            #canvas.draw_polygon(point_list, 2, "Black","Green")
            canvas.draw_image(back_image,(image_width / 2, image_height / 2),(image_width,image_height),(dest_width,50),(50,100))
        text_width += 50
        dest_width += 50
        width += 50
        
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

new_game()
frame.start()