import pygame
import sys
import random

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        # Initialises the player object
        super().__init__()
        self.image = pygame.Surface((8, 45))
        self.image.fill('White')
        self.rect = self.image.get_rect(midleft = (20,200))
        self.velocity = 0
        self.direction = 0 # 0 = no movement, 1 = down movement, 2 = up movement
    
    def player_input(self):
        # Moves the player based on user input on up and down arrow keys
        keys = pygame.key.get_pressed() # gets all possible key inputs
        if keys[pygame.K_UP]:
            self.direction = 2 
            self.velocity = 5 # sets the players velocity to 5
            if self.rect.y <= 0: # stops the player from moving outside of the map
                self.rect.y = 0
            else:
                self.rect.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.direction = 1
            self.velocity = 5 # sets the players velocity to 5
            if self.rect.y >= 355: # stops the player moving outside of the map
                self.rect.y = 355
            else:
                self.rect.y += self.velocity
    
    def get_direction(self):
        return self.direction

    def get_velocity(self):
        return self.velocity

    def update(self):
        self.player_input()



class Opponent(pygame.sprite.Sprite):
    
    def __init__(self):
        # Initialises the opponent object
        super().__init__()
        self.image = pygame.Surface((8, 45))
        self.image.fill('White')
        self.rect = self.image.get_rect(midright = (780,200))
        self.velocity = 3.5 # the opponenet velocity sets the ai difficulty 
        self.direction = 0 # down movement = 1, up movement = 2, no movement = 0

    def get_direction(self):
        return self.direction
    
    def get_velocity(self):
        return self.velocity

    def update(self, ball):
        if ball.getVector().x >= 0 and ball.rect.x >= 400: # This restricts the opponent to moving on when the ball is moving towards the opponent and has crossed the half way line of the screen
            if self.rect.top > ball.rect.top:
                self.direction = 1 # sets opponent direction to up
                self.rect.y -= self.velocity # moves the opponent up if the ball is above the opponent 
            elif self.rect.bottom < ball.rect.bottom:
                self.direction = 2 # sets the opponent direction to down
                self.rect.y += self.velocity # moves the opponent down if the ball is below the opponent  



    
class Ball(pygame.sprite.Sprite):
    
    def __init__(self):
        # Initialises the ball object
        super().__init__()
        self.image = pygame.Surface((6,6))
        self.image.fill('White')
        self.rect = self.image.get_rect(center = (400,200))
        self.velocity = 6 # constant velocity
        self.v = pygame.Vector2((random.randint(-1000, 1000), random.randint(-1000, 1000))).normalize() # creates a unit vector
        self.game_running = 0 # game running = 0, opponent win = 1, player win = 2

    def check_out_of_bounds(self):
        if self.rect.y <= 0: # if the ball is hitting the roof then rebound the ball
            self.v.y = -self.v.y
            
            
        if self.rect.y >= 394: # if the ball is hitting the floor then rebound the ball
            self.v.y = -self.v.y
            

        if self.rect.x <= 0: # sets the game state to the opponent has won
            self.game_running = 1
            

        if self.rect.x >= 794: # sets the game state to the player has won
            self.game_running = 2
            

    def getVector(self):
        return self.v
    
    def reposVector(self, newv):
        self.v = newv

    def resetVector(self):
        self.v.xy = (random.randint(-1000, 1000), random.randint(-1000, 1000))
        self.v = self.v.normalize()

    def get_game_running(self):
        return self.game_running

    def set_game_running(self, game_bool):
        self.game_running = game_bool

    def update(self):
        self.check_out_of_bounds()
        self.rect.x += self.v.x * self.velocity
        self.rect.y += self.v.y * self.velocity



def handle_collisions(object):
    # handles the collisions of the ball when colliding with the player or opponent object
    if object.rect.colliderect(ball_object.rect):
        tempVector = ball_object.getVector()
        if object.get_direction() == 1: # if the player/opponent is moving down then rebound the ball
            tempVector.x = -tempVector.x 
            ball_object.reposVector(tempVector) 
        elif object.get_direction() == 2: # if the player/opponent is moving up then reflect the ball
            ball_object.reposVector(tempVector.reflect(tempVector))


def display_score():
    # displays and updates the scores of the player/opponent 
    player1_score_surface = my_font.render(f'{player_score}' , False, 'White')
    player2_score_surface = my_font.render(f'{opponent_score}' , False, 'White')
    screen.blit(player1_score_surface, (250,10))
    screen.blit(player2_score_surface, (500,10))


pygame.init() # intiates all the parts of pygame
screen = pygame.display.set_mode((800,400)) # Creates a display window with width 800 pixels and height 400 pixels
pygame.display.set_caption('Pong') 
clock = pygame.time.Clock() # Creates clock object

# Player
player = pygame.sprite.GroupSingle()
player.add(Player())


# Ball
ball = pygame.sprite.GroupSingle()
ball.add(Ball())

# AI Opponenet
opponent = pygame.sprite.GroupSingle()
opponent.add(Opponent())



player_object = player.sprite 
ball_object = ball.sprite
opponent_object = opponent.sprite


# Score
pygame.font.init() 
my_font = pygame.font.SysFont('Comic Sans MS', 120)
player_score = 0
opponent_score = 0



while True:  # game loop

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # uninitialises the pygame module
                sys.exit() # terminates python script 

    if ball_object.get_game_running() == 0: # if the game is running then execute
        handle_collisions(player_object)
        handle_collisions(opponent_object)
        screen.fill('black')
        display_score()


        ball.draw(screen)
        ball.update()
        player.draw(screen)
        player.update()
        opponent.draw(screen)
        opponent.update(ball_object)

    else: # otherwise the game is not running
        if ball_object.get_game_running() == 1: # if the opponent won the round
            opponent_score += 1
        else:  # else the player must have won
            player_score += 1
        # Makes the game active again and resets all the positions of the game entites 
        ball_object.set_game_running(0) # Makes the game active again
        opponent_object.rect.midright = 780,200
        player_object.rect.midleft = 20,200
        ball_object.rect.center = 400, 200
        ball_object.resetVector()

    


    

    pygame.display.update() # updates the display surface - screen variable is the display surface
    clock.tick(60) # sets the frame rate to 60fps
