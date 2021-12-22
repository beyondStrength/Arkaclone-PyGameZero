import pgzrun
from random import randint

#Setup
WIDTH = 800
HEIGHT = 600

gameStart = False
lifes = 3

paddle = Actor("paddle")
paddle.x = WIDTH/2
paddle.y = HEIGHT*9/10

ball = Actor("ball")
ball.x = WIDTH/2
ball.y = HEIGHT/2

ball_speedX = 10
ball_speedY = -10


bricks = []
def buildBricks():
    brick = Actor("brick") 
    for y in range(int(brick.height), int(HEIGHT/3), int(brick.height*1.5)):
        for x in range(int(brick.width*1.2), (WIDTH - brick.width), int(brick.width*1.5)):
            brick = Actor("brick")
            brick.pos = x, y
            bricks.append(brick)

def gameOver():
    global lifes, ball_speedY, gameStart
    if keyboard.K_RETURN:
        lifes = 3
        bricks.clear()
        buildBricks()
        paddle.pos = WIDTH/2, HEIGHT*9/10
        ball.pos = WIDTH/2, HEIGHT/2
        ball_speedY = abs(ball_speedY)*-1
        clock.unschedule(gameOver)
    
def movePaddle():
    global ballDirection
    if keyboard.left and paddle.x > paddle.width/2:
        paddle.pos = paddle.x - 10, paddle.y
    if keyboard.right and paddle.x < WIDTH-(paddle.width/2):
        paddle.pos = paddle.x + 10, paddle.y
    if keyboard.space:
        ballDirection += 90

def moveBall():
    global ball_speedX, ball_speedY, lifes, gameStart
    ball.x += ball_speedX
    ball.y += ball_speedY

    if ball.x < 0+ball.width/2:
        ball_speedX = abs(ball_speedX)
    if ball.x > WIDTH-ball.width/2:
        ball_speedX = abs(ball_speedX)*-1
    if ball.y < 0+ball.height/2:
        ball_speedY = abs(ball_speedY)
    if ball.y > HEIGHT-ball.height/2:
        if lifes > 0:
            ball_speedY = abs(ball_speedY)*-1
            ball.x = WIDTH/2
            ball.y = HEIGHT/2
            lifes-=1
        else:
            gameStart = False
            clock.schedule_interval(gameOver, 0.001)
 
       

def collisions():
    global ball_speedX, ball_speedY
    if ball.colliderect(paddle):
        if ball.x > paddle.x:
            ball_speedX = abs(ball_speedX)
        else:
            ball_speedX = abs(ball_speedX)*-1
        
        ball_speedY *= -1

    for b in bricks:
        if ball.colliderect(b):
            bricks.remove(b)
            ball_speedY *= -1
            break


#Start
buildBricks()

#Update
def update():
    global gameStart
    if not gameStart:
        if keyboard.left:
            gameStart = True
        if keyboard.right:
            gameStart = True
    else: 
        movePaddle()
        collisions()
        moveBall()
        if len(bricks) < 1:
            clock.schedule_interval(gameOver, 0.001)



#Draw
def draw():
    screen.fill((0,0,0))
    paddle.draw()
    ball.draw()
    for b in bricks:
        b.draw()


pgzrun.go()


