# @Author: Aditya Dutta
# @Date: 05/20/2025
# @Teacher: Mr. Carreiro
# @Description: A two-player Pokemon-themed pong game where players control Pikachu and Bulbasaur paddles across 4 progressively challenging levels, 
#               each with a unique background. The ball starts at the center with a random direction and maintains constant speed using. 
#               Difficulty increases by increasing ball speed through  Mr. Carreiro's formula. Players gain points by returning 
#               the ball and lose lives by missing it. The game ends when a player reaches 100 points, loses all lives, or has a higher score by the 
#               end of level 4, followed by a game over screen showing the winner and a reason why they won. Features include score, lives, and level tracking, a 
#               visual indicator for points remaining until the next level, intro and win screens, and game reset when the space key is clicked. 
#               I built the game using a variety of functions, conditionals, and structured logic for amazing gameplay! Have fun playing!

import pygame
import pgzero
import pgzrun
import random
import math

WIDTH = 800
HEIGHT = 600


print("Change")

# Load game assets (images for ball, background, and paddles)
ball = Actor('pongball')  # Ball actor
background = Actor('background') # Background for level 1
backgroundL2 = Actor('backgroundl2') # Background for level 2
backgroundL3 = Actor('backgroundl3') # Background for level 3
backgroundL4 = Actor('backgroundl4') # Background for level 4
player1 = Actor('p1') # Player 1 paddle (Pikachu)
player2 = Actor('p2') # Player 2 paddle (Bulbasaur)

# Set starting positions
ball.pos = 400, 300
player1.pos = 100, 300     # Left side
player2.pos = 700, 300     # Right side

# Initialize game state variables
speed = 5  # Initial ball speed
level = 1  # Starting level
scoreplayer1 = 0 # Player 1 score
scoreplayer2 = 0 # Player 2 score
livesplayer1 = 3 # Player 1 lives
livesplayer2 = 3 # Player 2 lives
total_points = 0 # Combined total score
next_level_points = 10 # First level-up score boundary
# Next level points will increase by 50% each time  

# Initialize the mixer to avoid sound conflict so the background music runs along with the sound effects
pygame.mixer.init()
# Load and play background music using pygame.mixer.music
pygame.mixer.music.load("backgroundmusic.wav")
pygame.mixer.music.play(-1)  # Loop forever

# Game over control variables
game_over = False # True when someone loses
winning_player = "" # Stores name of winner
win_reason = "" # This variable stores the reason for winning. 
# For example, if Player 1 wins, it will be "Player 1 wins by score" or "Player 1 wins because Player 2 lost all of their lives" or "Player 1 wins by end of level 4"
game_state = "intro"  # Can be "intro", "playing"

# Initialize ball movement direction
ball_dx = random.uniform(-1, 1)
ball_dy = random.uniform(-1, 1)
magnitude = math.sqrt(ball_dx**2 + ball_dy**2)
bM_dx = (ball_dx / magnitude) * speed # X-direction velocity
bM_dy = (ball_dy / magnitude) * speed # Y-direction velocity

# Normalize the ball direction to keep constant speed. Whenever the ball direction changes, it will maintain the same speed. So when the ball resets, it will not change speed.
def ball_direction():
    global bM_dx, bM_dy, speed
    magnitude = math.sqrt(bM_dx**2 + bM_dy**2)
    bM_dx = (bM_dx / magnitude) * speed
    bM_dy = (bM_dy / magnitude) * speed

# Main game logic for movement, scoring, lives, and level progression
def main_game():
    global bM_dx, bM_dy, scoreplayer2, scoreplayer1, livesplayer1, livesplayer2
    global game_over, winning_player, total_points, next_level_points, level, speed, win_reason

    ball.x += bM_dx # This will move the ball horizontally
    ball.y += bM_dy # This will move the ball vertically

    # Bounce off left/right walls
    # If the ball goes greater than the width of the screen, it will bounce back
    # If the ball goes less than 0, it will bounce back
    if ball.x < 0 or ball.x > WIDTH:
        bM_dx *= -1
    # Bounce off top/bottom walls
    # If the ball goes greater than the height of the screen, it will bounce back
    # If the ball goes less than 0, it will bounce back
    if ball.y < 0 or ball.y > HEIGHT:
        bM_dy *= -1

     # Detect collision with Player 1's paddle
     # bM_dx < 0 means the ball is moving left, so only check collision when it's approaching Player 1
     # ball.right > player1.left ensures the ball has slightly entered the paddle to prevent double collision
     # If the ball collides with Player 1's paddle, it will increase Player 1's score by 1
    if ball.colliderect(player1) and bM_dx < 0 and ball.right > player1.left:
        scoreplayer1 += 1
        sounds.ballcolide.play()
        bM_dx = abs(bM_dx) # Reverse direction to the right
        bM_dy += random.uniform(-3.5, 3.5) # Add some vertical randomness to the ball's direction
        ball_direction() # Calls ball_direction() function to make direction of ball consistent with speed

    # Detect collision with Player 2's paddle
    # bM_dx > 0 means the ball is moving right, so only check collision when it's approaching Player 2
    # ball.left < player2.right ensures the ball has slightly entered the paddle to prevent double collision
    # If the ball collides with Player 2's paddle, it will increase Player 2's score by 1
    if ball.colliderect(player2) and bM_dx > 0 and ball.left < player2.right:
        scoreplayer2 += 1
        sounds.ballcolide.play()
        bM_dx = -abs(bM_dx) # Reverse direction to the left
        bM_dy += random.uniform(-3.5, 3.5) # Add some vertical randomness to the ball's direction
        ball_direction() # Calls ball_direction() function to make direction of ball consistent with speed
    
    # Check if the ball goes out of bounds on the left or right side
    # If the ball goes out of bounds on the left side, it will decrease Player 1's lives by 1
    if ball.x <= 82:
        livesplayer1 -= 1
        sounds.lose.play()
        ball.pos = (400, 300) # Reset ball position to center
        ball_dx = random.uniform(-1, 1) # Randomize ball x direction
        ball_dy = random.uniform(-1, 1) # Randomize ball y direction
        magnitude = math.sqrt(ball_dx**2 + ball_dy**2) # Calculate magnitude of the ball's direction
        bM_dx = (ball_dx / magnitude) * speed
        bM_dy = (ball_dy / magnitude) * speed

    if ball.x >= WIDTH - 122:
        sounds.lose.play()
        livesplayer2 -= 1 # Reduce Player 1's life
        ball.pos = (400, 300) # Reset ball position to center
        # Generate a new random direction for the ball
        ball_dx = random.uniform(-1, 1) # Randomize ball x direction
        ball_dy = random.uniform(-1, 1) # Randomize ball y direction
        magnitude = math.sqrt(ball_dx**2 + ball_dy**2) # Calculate the magnitude of the new direction
        bM_dx = (ball_dx / magnitude) * speed
        bM_dy = (ball_dy / magnitude) * speed

    if scoreplayer1 >= next_level_points or scoreplayer2 >= next_level_points:  # Check if invidual points reach the next level points. If it does, it will increase the level by 1 and calculate the next level points
        sounds.levelup.play()
        level += 1 # Increase level by 1
        speed += 2 # Increase speed by 2
        next_level_points = int(next_level_points + (next_level_points * 1.5)) # Uses the formula and int to do floor division to calculate the next level points.
        # Because next_level_points is a global variable, changes made inside the function will persist outside the function.
        ball_direction() # Normalize the ball direction to keep constant speed

    # Check for game over by lives
    if livesplayer1 <= 0: # Player 1 loses all lives
        game_over = True # Set game_over to True
        win_reason = "Player 1 lost all lives"
        winning_player = "Player 2" # Make Player 2 the winner
        pygame.mixer.music.stop() # Stop the background music when the game is over
    elif livesplayer2 <= 0: # Player 2 loses all liv es
        game_over = True # Set game_over to True
        win_reason = "Player 2 lost all lives"
        winning_player = "Player 1" # Make Player 1 the winner
        pygame.mixer.music.stop() # Stop the background music when the game is over

    # Check for game over by score
    if scoreplayer1 >= 100: # Player 1 reaches 100 points
        game_over = True # Set game_over to True
        winning_player = "Player 1" # Make Player 1 the winner
        win_reason = "Player 1 reached 100 points" # Reason for winning is that Player 1 reached 100 points
        pygame.mixer.music.stop() # Stop the background music when the game is over
    elif scoreplayer2 >= 100: # Player 2 reaches 100 points
        game_over = True # Set game_over to True
        win_reason = "Player 2 reached 100 points" # Reason for winning is that Player 2 reached 100 points
        winning_player = "Player 2" # Make Player 2 the winner
        pygame.mixer.music.stop() # Stop the background music when the game is over

    # Check for game over by end of level 4
    if level == 5:
        game_over = True # Set game_over to True
        if scoreplayer1 > scoreplayer2: # If Player 1 has more points than Player 2 at the end of Level 4
            winning_player = "Player 1"
            win_reason = "Had more points at end of Level 4" # If Player 1 has more points than Player 2 at the end of Level 4
            pygame.mixer.music.stop()
        else: # If Player 2 has more points than Player 1 at the end of Level 4
            winning_player = "Player 2" # If Player 2 has more points than Player 1 at the end of Level 4
            win_reason = "Had more points at end of Level 4" # Reason for winning is that Player 2 had more points than Player 1 at the end of Level 4
            pygame.mixer.music.stop()
            
def control_players(): # Control player movement
    player1.x = 50 # Locks player 1's x position to 50
    player2.x = 730 # Locks player 2's x position to 730

    if keyboard.w and player1.top > 0: # If the W key is pressed and Player 1's top is greater than 0, it will move Player 1 up
        player1.y -= 5 # Move player in the opposite direction to prevent going off the top of the screen
    if keyboard.s and player1.bottom < HEIGHT: # If the S key is pressed and Player 1's bottom is less than the height of the screen, it will move Player 1 down
        player1.y += 5 # Move player in the opposite direction to prevent going off the bottom of the screen

    if keyboard.up and player2.top > 0: # If the UP arrow key is pressed and Player 2's top is greater than 0, it will move Player 2 up
        player2.y -= 5 # Move player in the opposite direction to prevent going off the top of the screen
    if keyboard.down and player2.bottom < HEIGHT: # If the DOWN arrow key is pressed and Player 2's bottom is less than the height of the screen, it will move Player 2 down
        player2.y += 5 # Move player in the opposite direction to prevent going off the bottom of the screen

def drawMainGame(): # Draw the main game screen
    screen.clear() # Clear the screen
    background.draw() # Draw the background for level 1
    ball.draw() # Draw the ball
    player1.draw() # Draw Player 1 paddle (Pikachu)
    player2.draw() # Draw Player 2 paddle (Bulbasaur)
    screen.draw.text(f"Lives P1: {livesplayer1}", (0, 0), color="white", fontsize=30) # Display Player 1's lives
    screen.draw.text(f"Lives P2: {livesplayer2}", (670, 0), color="white", fontsize=30) # Display Player 2's lives
    screen.draw.text(f"Score P1: {scoreplayer1}", (0, 30), color="white", fontsize=30)# Display Player 1's score
    screen.draw.text(f"Score P2: {scoreplayer2}", (670, 30), color="white", fontsize=30) # Display Player 2's score
    screen.draw.text(f"Level: {level}", center=(WIDTH // 2, 30), color="white", fontsize=40) # Display current level
    screen.draw.text(f"Next level in: {max(0, next_level_points)} points", center=(WIDTH // 2, 70), color="orange", fontsize=30) # Display points needed for next level

def drawLevel2(): # Draw the level 2 screen
    screen.clear() # Clear the screen
    backgroundL2.draw() # Draw the background for level 2
    ball.draw() # Draw the ball
    player1.draw() # Draw Player 1 paddle (Pikachu)
    player2.draw() # Draw Player 2 paddle (Bulbasaur)
    screen.draw.text(f"Lives P1: {livesplayer1}", (0, 0), color="white", fontsize=30) # Display Player 1's lives
    screen.draw.text(f"Lives P2: {livesplayer2}", (670, 0), color="white", fontsize=30) # Display Player 2's lives
    screen.draw.text(f"Score P1: {scoreplayer1}", (0, 30), color="white", fontsize=30) # Display Player 1's score
    screen.draw.text(f"Score P2: {scoreplayer2}", (670, 30), color="white", fontsize=30) # Display Player 2's score
    screen.draw.text(f"Level: {level}", center=(WIDTH // 2, 30), color="white", fontsize=40) # Display current level
    screen.draw.text(f"Next level in: {max(0, next_level_points)} points", center=(WIDTH // 2, 70), color="orange", fontsize=30) # Display points needed for next level

def drawLevel3(): # Draw the level 3 screen
    screen.clear()
    backgroundL3.draw() # Draw the background for level 3
    ball.draw() # Draw the ball
    player1.draw() # Draw Player 1 paddle (Pikachu)
    player2.draw() # Draw Player 2 paddle (Bulbasaur)
    screen.draw.text(f"Lives P1: {livesplayer1}", (0, 0), color="white", fontsize=30) # Display Player 1's lives
    screen.draw.text(f"Lives P2: {livesplayer2}", (670, 0), color="white", fontsize=30) # Display Player 2's lives
    screen.draw.text(f"Score P1: {scoreplayer1}", (0, 30), color="white", fontsize=30) # Display Player 1's score
    screen.draw.text(f"Score P2: {scoreplayer2}", (670, 30), color="white", fontsize=30) # Display Player 2's score
    screen.draw.text(f"Level: {level}", center=(WIDTH // 2, 30), color="white", fontsize=40) # Display current level
    screen.draw.text(f"Next level in: {max(0, next_level_points)} points", center=(WIDTH // 2, 70), color="orange", fontsize=30) # Display points needed for next level

def drawLevel4(): # Draw the level 4 screen
    screen.clear()
    backgroundL4.draw()
    ball.draw() # Draw the ball
    player1.draw() # Draw Player 1 paddle (Pikachu)
    player2.draw() # Draw Player 2 paddle (Bulbasaur)
    screen.draw.text(f"Lives P1: {livesplayer1}", (0, 0), color="white", fontsize=30) # Display Player 1's lives
    screen.draw.text(f"Lives P2: {livesplayer2}", (670, 0), color="white", fontsize=30) # Display Player 2's lives
    screen.draw.text(f"Score P1: {scoreplayer1}", (0, 30), color="white", fontsize=30) # Display Player 1's score
    screen.draw.text(f"Score P2: {scoreplayer2}", (670, 30), color="white", fontsize=30) # Display Player 2's score
    screen.draw.text(f"Level: {level}", center=(WIDTH // 2, 30), color="white", fontsize=40) # Display current level
    screen.draw.text(f"Next level in: {max(0, next_level_points)} points", center=(WIDTH // 2, 70), color="orange", fontsize=30) # Display points needed for next level

def draw_game_over(): # Draw the game over screen
    screen.clear() # Clear the screen
    gameover = Actor('gameoverscreen') # Game over background
    gameover.draw() # Draw the game over background
    screen.draw.text(f"{winning_player} Wins!", center=(WIDTH // 2, HEIGHT // 2 + 100), fontsize=60, color="blue") # Display the winning player
    screen.draw.text(win_reason, center=(WIDTH // 2, HEIGHT // 2 + 170), fontsize=40, color="white") # Display the reason for winning
    screen.draw.text("Press SPACE to Play Again", center=(WIDTH // 2, HEIGHT // 2 + 240), fontsize=40, color="yellow") # Display instructions to play again


def draw_intro():
    background.draw() # Draw the background for the intro screen
    screen.draw.text("Welcome to Pokémon Pong!", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=60, color="yellow") # Display welcome message
    screen.draw.text("Press SPACE to Play", center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=40, color="white") # Display instructions to start the game
    screen.draw.text("Press E to Exit", center=(WIDTH // 2, HEIGHT // 2 + 70), fontsize=40, color="red") # Display instructions to exit the game

def draw():
    screen.clear() # Clear the screen before drawing
    if game_state == "intro": # If the game is in the intro state
        draw_intro() # Draw the intro screen
    elif game_over: # If the game is over
        draw_game_over() # Draw the game over screen

    elif level ==1: # If the game is in level 1
        drawMainGame() # Draw the main game screen for level 1
    elif level == 2: # If the game is in level 2
        drawLevel2() # Draw the level 2 screen
    elif level == 3: # If the game is in level 3
        drawLevel3() # Draw the level 3 screen
    elif level == 4: # If the game is in level 4
        drawLevel4() # Draw the level 4 screen
    

def update():
    global game_state, game_over
    global level, speed, scoreplayer1, scoreplayer2, livesplayer1, livesplayer2
    global total_points, next_level_points, winning_player, win_reason
    global ball_dx, ball_dy, bM_dx, bM_dy, ball
    # Must use global variables to reset them if the player restarts the game

    # Start the game from the intro screen
    if game_state == "intro" and keyboard.space:
        game_state = "playing" # Change game state to playing
    if keyboard.e:
        quit()
    # Restart the game if it's over and SPACE is pressed
    elif game_over and keyboard.space: # If the game is over and SPACE is pressed
        # Reset all game variables to their initial values
        game_over = False
        game_state = "playing"
        level = 1
        speed = 5
        scoreplayer1 = 0
        scoreplayer2 = 0
        livesplayer1 = 5
        livesplayer2 = 5
        total_points = 0
        next_level_points = 10
        winning_player = ""
        win_reason = ""
        ball.pos = (400, 300)
        ball_dx = random.uniform(-1, 1)
        ball_dy = random.uniform(-1, 1)
        magnitude = math.sqrt(ball_dx**2 + ball_dy**2)
        bM_dx = (ball_dx / magnitude) * speed
        bM_dy = (ball_dy / magnitude) * speed

    if game_state == "playing" and not game_over: # If the game is in playing state and not over
        main_game() # Call the main game logic
        control_players() # Call the player control function


pgzrun.go()