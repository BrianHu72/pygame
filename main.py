import pygame  
import random  
import colors  

pygame.init() # Initializes game

# Initialize the screen for pygame
screen_width = 800
screen_height = 600 
gameScreen = pygame.display.set_mode((screen_width,screen_height))

# Initializing clock
clock = pygame.time.Clock()

# Game Description
pygame.display.set_caption('Launch Rocket!')

# Loading images
icon = pygame.image.load('Images/icon.png')
backgroundImage = pygame.image.load('Images/space.png')
rocketImage = pygame.image.load('Images/rocket.png')
asteroidImage = pygame.image.load('Images/asteroid.png')

# Changes the default icon in the top left corner
pygame.display.set_icon(icon) 

# Extracting dimension of images
asteroidWidth, asteroidHeight = asteroidImage.get_rect().size
rocketWidth, rocketHeight = rocketImage.get_rect().size

isPaused = False
score = 0

# quit out of pygame and our python program
def quitGame():
    pygame.quit() #pygame's built-in method to quit the game
    quit() #quit python program

# Updates score display and save for record
def updateScoreDisplay(score):
    recordFile = open('record.txt', 'r+')   
    recordScore = int(recordFile.readlines()[0].strip('\n'))  
    highScore = recordScore  
    # Create a pygame Font from system font resources
    font = pygame.font.SysFont(None, 40) 
    color = colors.white
    if score > highScore:
        color = colors.yellow
        surface = font.render("New High Score!", True, colors.yellow)
        gameScreen.blit(surface, (0, 43))
        highScore = score
        # write the highest score in file
        recordFile.seek(0)
        recordFile.truncate()
        recordFile.write(str(score))
    recordFile.close()
    scoreTextSurface = font.render("Score: " + str(score), True, color)
    highScoreTextSurface = font.render("Highest Score: " + str(highScore), True, colors.red)
    gameScreen.blit(scoreTextSurface, (5,0))
    gameScreen.blit(highScoreTextSurface, (5,30))
    

def displayAsteroid(x,y):
    gameScreen.blit(asteroidImage, (x,y)) 
def displayRocket(x,y):
    gameScreen.blit(rocketImage, (x,y))

#  display text to the screen
def displayText(message, style, color):
    textSurf = style.render(message, True, color)
    return textSurf, textSurf.get_rect()

def crash():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        style = pygame.font.Font('freesansbold.ttf', 60)
        textSurf, textRect = displayText('GAME OVER!', style, colors.darkRed)
        textRect.center = (screen_width/2, screen_height/4)
        gameScreen.blit(textSurf, textRect)

        displayButton('PLAY AGAIN', colors.green, 200, 250, 400, 80, colors.blue, colors.brightBlue, startGame)
        displayButton('QUIT', colors.green, 200, 350, 400, 80, colors.blue, colors.brightBlue, quitGame)
        
        pygame.display.update()
        clock.tick(15)
        
def displayButton(text, color, x, y, width, height, i, hoverColor, actionListener = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    xCordinate = mouse[0]
    yCordinate = mouse[1]
    # if mouse is hovering on button, 
    if x < xCordinate < x + width and y < yCordinate < y + height: 
        pygame.draw.rect(gameScreen, hoverColor, (x, y, width, height))
        if click[0] == 1 and actionListener != None: #1 means clicked
            # invoke passed in click listener when click happened
            actionListener()
    else:
        pygame.draw.rect(gameScreen, i, (x, y, width, height))

    smallText = pygame.font.Font('freesansbold.ttf', 40)
    textSurf, textRect = displayText(text, smallText, color)
    textRect.center = (screen_width/2, (y+(height/2)+4))
    gameScreen.blit(textSurf, textRect)

def unpause():
    global isPaused
    isPaused = False

def paused():
    while isPaused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
        gameScreen.blit(backgroundImage, (0,0))
        style = pygame.font.Font('freesansbold.ttf', 115)
        textSurf, textRect = displayText('PAUSED', style, colors.red)
        textRect.center = (screen_width/2, screen_height/4)
        gameScreen.blit(textSurf, textRect)

        
        displayButton('CONTINUE', colors.red, 200, 250, 400, 80, colors.blue, colors.brightBlue, unpause)
        displayButton('QUIT', colors.red, 200, 350, 400, 80, colors.blue, colors.brightBlue, menu)
        
        pygame.display.update()
        clock.tick(15)

def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #when close cross is clicked
                quitGame()
        gameScreen.blit(backgroundImage, (0,0))
        style = pygame.font.Font('freesansbold.ttf', 60)
        textSurf, textRect = displayText('Launch Your Rocket', style, colors.yellow)
        textRect.center = (screen_width/2, screen_height/4)
        gameScreen.blit(textSurf, textRect)
        
        displayButton('PLAY', colors.red, 200, 250, 400, 80, colors.blue, colors.brightBlue, startGame)
        displayButton('QUIT', colors.red, 200, 350, 400, 80, colors.blue, colors.brightBlue, quitGame)

        pygame.display.update()
        clock.tick(15)



def startGame():
    global score
    global isPaused

    pygame.event.clear()

    # x cordinate 0 being left most and increase to right, y cordinate increase to bottom
    rocket_x = 0.5*(screen_width-rocketWidth)
    rocket_y = screen_height*0.8
    rocketSpeed = 25  

    num_asteroids = 2
    
    asteroid_x = []
    asteroid_y = []
    asteroid_speed = []

    # Initialize the cordinatees and speed of asteroids
    for i in range(num_asteroids):
        asteroid_x.append(random.randint(0, screen_width))     # Random x-position spawn
        asteroid_y.append(-(random.randint(asteroidHeight + 100, asteroidHeight + 200)))  
        # Random y-position spawn
        asteroid_speed.append(random.randint(7, 15))   
        
    score = 0 # initialize the score and flag
    gameOver = False

    while not gameOver:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            rocket_x -= rocketSpeed
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            rocket_x += rocketSpeed
        if pressed[pygame.K_ESCAPE] or pressed[pygame.K_p]: #letter p
            isPaused = True
            paused()

        # Displays the background 
        gameScreen.blit(backgroundImage, (0, 0))

        # Asteroids keep falling out of the sky
        for k in range(num_asteroids):                 
            displayAsteroid(asteroid_x[k], asteroid_y[k])    # Create asteroid 
            asteroid_y[k] += asteroid_speed[k]   # Move the asteroid downward

        displayRocket(rocket_x, rocket_y)         
        updateScoreDisplay(score)  # Update the score

        if rocket_x > screen_width-rocketWidth or rocket_x < 0:
            crash() #crash if rocket goes off screen

       # When an asteroid falls to bottom, player gets a point, new asteroid start from top
        for j in range(num_asteroids):            
            if asteroid_y[j] > screen_height:     # When the asteroid goes off screen
                asteroid_y[j] = -asteroidHeight    # Spawn the asteroid off the screen
                asteroid_x[j] = random.randint(0, screen_width) # Spawn the asteroid on a random x-position
                asteroid_speed[j] = random.randint(10, 17) # New random speed
                score += 1   # Increase the score by 1 point
            # Collision detection
            if rocket_y < asteroid_y[j] + asteroidHeight-30: # Checks to see if the asteroid and the rocket are crossing on the y-axis
                # Then checks to see if the rocket is underneath an asteroid at the same time
                #  if the rocket's left corner is between the asteroids left AND right corners OR if the rocket's right corner is between the asteroid's left AND right corners 
                rocket_right = rocket_x + rocketWidth
                asteroid_right = asteroid_x[j] + asteroidWidth
                if rocket_x > asteroid_x[j] and rocket_x < asteroid_right or rocket_right > asteroid_x[j] and rocket_right < asteroid_right:
                    crash()   

        #Toward the end of every while loop, need to draw a new frame to update the display and set the frame rate
        pygame.display.update()
        clock.tick(30) # set the frame rate



menu()
startGame()
