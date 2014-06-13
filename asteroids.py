# program template for Spaceship
#import simplegui
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
ANGULAR_VEL = math.pi / 40
started = False
high_score = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def group_collide(group, other_object):
    remove_sprite = set()
    for sprite in group:
        if sprite.collide(other_object):
            remove_sprite.add(sprite)
    group.difference_update(remove_sprite)
    if len(remove_sprite) > 0:  # if any collision occured than return true
        return True
    else:
        return False

def group_group_collide(group_1, group_2):
    collision_count = 0
    remove_set = set()
    for elements in group_1:
        collision = group_collide(group_2, elements)
        if collision:
            remove_set.add(elements)
            collision_count += 1
    group_1.difference_update(remove_set)
    return collision_count

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.thrust:
            canvas.draw_image(self.image, (self.image_center[0] + self.image_size[0], self.image_center[1]), self.image_size, self.pos, self.image_size, self.angle)
        else:    
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        # position update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # friction update
        self.vel[0] *= .99
        self.vel[1] *= .99
        #angle update
        self.angle += self.angle_vel
        #aceeleration and thrust update
        forward = angle_to_vector(self.angle)
        #self.vel[0],self.vel[1] = [dist([0,0], self.vel)* angle_to_vector(self.angle)[0],dist([0,0], self.vel)* angle_to_vector(self.angle)[1]]
        if self.thrust:
            self.vel[0] += 0.1 * forward[0]
            self.vel[1] += 0.1 * forward[1]
    
    def decrement_angle_vel(self):
        self.angle_vel -= ANGULAR_VEL
        
    def increment_angle_vel(self):
        self.angle_vel += ANGULAR_VEL
    
    def thrusters(self, bool_val):
        self.thrust = bool_val
        if self.thrust:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
        
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        pos = [self.pos[0] + (self.radius * forward[0]),self.pos[1] + (self.radius * forward[1])]
        vel = [self.vel[0] + (6 * forward[0]),self.vel[1] + (6 * forward[1])]
        a_missile =  Sprite(pos, vel, self.angle, 0, missile_image, missile_info, missile_sound)   
        missile_group.add(a_missile)

    def get_position(self):
        return self.pos 

    def get_radius(self):
        return self.radius
       
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH   
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        self.age += 1
        if self.age < self.lifespan:
            return False
        else:
            return True

    def get_position(self):
        return self.pos 

    def get_radius(self):
        return self.radius
 
    def collide(self, other_object):
        sprite_pos = self.pos
        other_object_pos = other_object.get_position()
        sprite_radius = self.radius
        other_object_radius = other_object.get_radius()

        if dist(sprite_pos, other_object_pos) < sprite_radius + other_object_radius:
            return True
        else:
            return False
         
def draw(canvas):
    global time, started, rock_group, lives, score, timer, high_score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    if group_collide(rock_group, my_ship): # if ship and rock collides, decrement live by 1
        lives -= 1
    score += group_group_collide(missile_group,rock_group)
    # dram lives and score
    canvas.draw_text("Lives: " + str(lives), [40,40], 20, "White")
    canvas.draw_text("High Score: " + str(high_score), [350,40], 20, "White")
    canvas.draw_text("Score: " + str(score), [700,40], 20, "White")
    
    # draw and update ship
    my_ship.draw(canvas)
    my_ship.update()

    # draw & update - missle and rock
    process_sprite_group(missile_group, canvas)
    process_sprite_group(rock_group, canvas)

    if lives == 0:
        started = False
        lives = 3
        high_score = max(score,high_score)
        rock_group = set()
        soundtrack.rewind()

     # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, timer, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        score = 0
        soundtrack.play() 
        started = True
                   
# process_sprite_group take a set and a canvas and call the update and draw methods for each sprite in the group
def process_sprite_group(sprite_group, canvas):
    remove = set()
    for sprite in sprite_group:
        remove_sprite = sprite.update()
        sprite.draw(canvas)
        if remove_sprite:
            remove.add(sprite)

   	sprite_group.difference_update(remove)

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, started
    if len(rock_group) < 12 and started:
        pos = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
        vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        angle_vel = random.random() * .2 - .1
        if dist(pos, my_ship.pos) >= 3 * my_ship.radius:
            a_rock = Sprite(pos, vel, 0, angle_vel, asteroid_image, asteroid_info)
            rock_group.add(a_rock)
    

def keydown(key):
    if key == simplegui.KEY_MAP["left"]:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrusters(True)
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()

def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrusters(False)
        
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 1.57, 0.1, asteroid_image, asteroid_info)
rock_group = set()
missile_group = set()
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

