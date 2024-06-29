#### IMPORT LIBRARIES 

import time
import datetime as dt

import random
import pygame

from pygame.locals import *

import json

### LOCAL LIBRARIES/PACKAGES

from game_functions import *
from utility_functions import *

### OPPONENT CLASSES

# For now files for opponent classes need to be in the same directory, but will move to separate directory later to avoid clutter

from opponent_rndm import *
from opponent_rndmplus import *

#___________________________________________________________________________________
#___________________________________________________________________________________


class BATTLESHIP:

    def __init__(self,FPS):
        # Load parameters file with information about field size and color schemes
        parameter_file = '../parameters/game_parameters.json'
        with open(parameter_file) as f:
            self.settings = json.load(f)
        
        #initiate pygame library
        pygame.init()

        # Set internal FPS variable and the background of the main window
        self.fps = FPS
        self.surface=pygame.display.set_mode(self.settings['SETTINGS']["main_window"]['size'])
        # Screen reset redraws elements of the game (pygame way of refreshing the window to update it)
        # This reset initiates the origianl window
        screen_reset(self.surface,self.settings)

        # calculate the time right now, used as an ID for log files
        self.start_time = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Log and Game progress log filenames and paths
        self.log_file = "../logs/" + self.start_time + "_debug_log.txt"
        self.game_log = "../logs/"+ self.start_time + "_game_log.txt"
    
    # The game:
    def run(self):

        # Clock is for refresh rate
        clock=pygame.time.Clock()

        game = True # if false the game exits
        debug = False # If True, more information is saved to debug logs
        Opponent = False # This prompts user to select an opponent and once initialized and changed to True the game will proceed.

        ### INTRO SCREEN ###
        game_stage="main_menu" # set game stage for the intro screen  
        print("Starting stage: ",game_stage)

        # Get elements of the Intro screen
        debug_Button, play_Button, rndm_Button, rndmplus_Button, StatusField = Intro(self.surface,self.settings)

        # Initialize lists for player and computer moves. 
        computer_moves=[]
        player_moves=[]

        while game:
            # Refreshes screen and checks for action
            while game_stage == "main_menu":
                clock.tick(self.fps)
                # Print statement to track which part of the game we are in
                # print(game_stage)
                for event in pygame.event.get():
                    # Pressing ESC exits the game, every other key advances it to the next stage
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            exit()
                    
                    if event.type == MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()

                        if rndm_Button.collision(pos):
                            if Opponent == False:
                                Opponent = rndm()
                                rndm_Button.button_on()
                            else:
                                Opponent = False
                                rndm_Button.button_off()

                        if rndmplus_Button.collision(pos):
                            if Opponent == False:
                                Opponent = rndmplus(computer_moves)
                                rndmplus_Button.button_on()
                            else:
                                Opponent = False
                                rndmplus_Button.button_off()


                        if debug_Button.collision(pos):
                            if debug == False:
                                debug = True
                                debug_Button.button_on()
                                print('Debug mode on')
                            else: 
                                debug = False
                                debug_Button.button_off()
                                print('Debug mode off')
                                

                        if play_Button.collision(pos):
                            if Opponent != False:
                                game_stage = 'game_setup'
                            else: 
                                print('No opponent selected.')
                                message = "Please select an opponent type first."
                                status_message(self.surface,StatusField,message)

                    # Exiting the window through the cross in the corner
                    elif event.type == QUIT:
                            exit()

            ### GAME SETUP ###
            screen_reset(self.surface,self.settings) # Redraw the game window for the next stage
            # Create graphic elements of the game window.
            # Line breaking this way for readability
            EnemyField, PlayerField, \
            EnemyInventory, PlayerInventory, StatusField, StartButton = Game_Setup(self.surface,self.settings)
            field_cell_size = self.settings['SETTINGS']['p1_field']['cell_size']
            # Initiate Ship Logs.  
            ship_settings = self.settings['SHIPS']
            ship_types = list(ship_settings.keys())
            p1_ship_log=[0 for x in range(100)]
            p2_ship_log=[0 for x in range(100)]

            print("Fields and logs have been initiated")

            while game_stage == 'game_setup':
                clock.tick(self.fps)
                
                for event in pygame.event.get():
                    # Keyboard action
                    if event.type == KEYDOWN:
                        # Press ESC to quit
                        if event.key == K_ESCAPE:
                            exit()
                        # Press Enter to move to the next stage
                        #elif event.key == K_RETURN:
                        #    game_stage = 'game'
                    # Mouse action
                    if event.type == MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()

                    
                        #### SHIP BUILDING LOGIC ####
                        if PlayerField.collision(pos):
                            ship_index = pos_to_ind(pos,PlayerField.pos, field_cell_size)
                            p1_ship_log, action, message = ship_log_update(ship_index, p1_ship_log)
                            print("Click coordinates: ",pos, "Field Start: ", PlayerField.pos, "Cell Size: ", field_cell_size, 
                                "Array index: ", ship_index)
                            if action=='add':
                                draw_ship(self.surface,self.settings,pos,'p1_field','setup')
                                status_message(self.surface,StatusField,message)
                            elif action =='remove':
                                erase_ship(self.surface,self.settings,pos,'p1_field')
                                status_message(self.surface,StatusField,message)
                            
                            


                        if StartButton.collision(pos):
                            message = 'Checking Ship Placement ...'
                            status_message(self.surface,StatusField,message)
                            p1_ship_log ,status, message = ship_log_check(p1_ship_log,ship_settings)
                            status_message(self.surface,StatusField,message)
                            if status == 'Success':
                                # computer places ships
                                p2_ship_log, status, message = computer_ship_setup(p2_ship_log, ship_settings,ship_types)

                                print(sum(x for x in p2_ship_log if x==1))

                                for i in range(10):
                                    print(p2_ship_log[(10*i):10*(i+1)])

                                if status == 'Success':

                                    if debug:
                                        # if debug mode is on, briefly show where computer has placed ships.
                                        for j in range(len(p2_ship_log)):
                                            if p2_ship_log[j]==1:
                                                pos2 = ind_to_pos(j,EnemyField.pos,field_cell_size)
                                                draw_ship(self.surface, self.settings,pos2,'p2_field','setup')
                                    # display the message that computer has placed ships
                                    status_message(self.surface,StatusField,message)
                                    # take a pause just to read the message
                                    time.sleep(2)
                                    message = "Let's Play!"
                                    # display the above message and start the game.
                                    status_message(self.surface,StatusField,message)
                                    time.sleep(2)
                                    game_stage = 'game'

    # quit refers to closing of the window
                    elif event.type == QUIT:
                        exit()
            ### GAME STAGE ###
                                    
            screen_reset(self.surface,self.settings) # Redraw the game window for the next stage
            # Create graphic elements of the game window.
            # Line breaking this way for readability
            EnemyField, PlayerField, \
            EnemyInventory, PlayerInventory, StatusField, StartButton = Game_Setup(self.surface,self.settings)
            # redraw player ships in grey
            for ship_index in range(len(p1_ship_log)):
                if p1_ship_log[ship_index] == 1:
                    p1_ship_pos = ind_to_pos(ship_index,PlayerField.pos,field_cell_size)
                    draw_ship(self.surface,self.settings,p1_ship_pos,'p1_field','game')

            # randomly select who starts. 0 - player, 1 - computer
            turn = random.randint(0,1)
            
            sch_p = 0
            sch_c = 0

            if turn ==0:
                status_message(self.surface,StatusField,'Player Starts')
            else:
                status_message(self.surface,StatusField,'Computer Starts')
                time.sleep(2)

                while turn == 1:
                    time.sleep(2)
                    turn, shot_pos, action, message, computer_moves, sch_c = computer_turn(Opponent, PlayerField.pos, field_cell_size, p1_ship_log, computer_moves,sch_c)
                    draw_action(self.surface,self.settings,shot_pos,'p1_field',action)
                    if action == 'sunk':
                        for move in computer_moves:
                            if move[1]=='hit-sunk':
                                recolor_pos = ind_to_pos(move[0],PlayerField.pos,field_cell_size)
                                draw_action(self.surface,self.settings,recolor_pos,'p1_field',action)
                    status_message(self.surface,StatusField,"Computer turn: "+message)
                    if debug:
                        log_message = ''.join(["Action: ",action,"; Message: ",message,"; Click position: ",str(shot_pos), \
                                    "; Ship index: ",str(pos_to_ind(shot_pos, PlayerField.pos, field_cell_size)), \
                                    "; SCH C: ", str(sch_c)])
                        write_log(self.log_file, "Computer: "+ log_message)
                    write_log(self.game_log, "Computer: Index: "+str(computer_moves[-1][0]) + " Action: " + computer_moves[-1][1])
            


            while game_stage == 'game':
                clock.tick(self.fps)
                
                for event in pygame.event.get():
                    # Keyboard action
                    if event.type == KEYDOWN:
                        # Press ESC to quit
                        if event.key == K_ESCAPE:
                            exit()
                        # Press Enter to move to the next stage
                        #elif event.key == K_RETURN:
                        #    game_stage = 'game'
                    # Mouse action
                    if event.type == MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()

                        if EnemyField.collision(pos):
                            if turn == 0:
                                
                                turn, action,message, player_moves, sch_p = player_turn(pos, EnemyField.pos, field_cell_size, p2_ship_log, player_moves, sch_p)
                                
                                if action != 'Try again.':
                                    draw_action(self.surface,self.settings,pos,'p2_field',action)

                                if action == 'sunk':
                                    print(player_moves)
                                    for move in player_moves:
                                        if move[1]=='hit-sunk':
                                            recolor_pos = ind_to_pos(move[0],EnemyField.pos,field_cell_size)
                                            draw_action(self.surface,self.settings,recolor_pos,'p2_field',action)

                                status_message(self.surface,StatusField,"Player turn: "+message)
                                if debug:
                                    log_message = ''.join(["Action: ",action,"; Message: ",message,"; Click position: ",str(pos), \
                                                "; Ship index: ",str(pos_to_ind(pos, EnemyField.pos, field_cell_size)), \
                                                "; SCH P: ", str(sch_p)])
                                    write_log(self.log_file, "Player: "+log_message)
                                write_log(self.game_log, "Player: Index: "+str(player_moves[-1][0]) + " Action: " + player_moves[-1][1])
                                time.sleep(2)

                                if message == "Player Wins!":
                                    turn = 0
                                    time.sleep(5)
                                    game_stage = 'end'

                                while turn == 1:
                                    time.sleep(2)
                                    turn, shot_pos, action, message, computer_moves, sch_c = computer_turn(Opponent, PlayerField.pos, field_cell_size, p1_ship_log, computer_moves, sch_c)
                                    draw_action(self.surface,self.settings,shot_pos,'p1_field',action)
                                    if action == 'sunk':
                                        for move in computer_moves:
                                            if move[1]=='hit-sunk':
                                                recolor_pos = ind_to_pos(move[0],PlayerField.pos,field_cell_size)
                                                draw_action(self.surface,self.settings,recolor_pos,'p1_field',action)
                                    status_message(self.surface,StatusField,"Computer turn: "+message)
                                    if debug:
                                        log_message = ''.join(["Action: ",action,"; Message: ",message,"; Click position: ",str(shot_pos), \
                                                "; Ship index: ",str(pos_to_ind(shot_pos, PlayerField.pos, field_cell_size)), \
                                                "; SCH C: ", str(sch_c)])
                                        write_log(self.log_file, "Computer: "+log_message)
                                    write_log(self.game_log, "Computer: Index: "+str(computer_moves[-1][0]) + " Action: " + computer_moves[-1][1])



                                    if message == 'Computer Wins!':
                                        turn=0
                                        time.sleep(2)
                                        game_stage = 'end'

                           

                        elif event.type == QUIT:
                            exit()
                            
            ### GAME OVER STAGE ###
            
            # Finish logs

            player_moves_log = ' , '.join(["["+str(x[0])+" , "+x[1]+"]" for x in player_moves])
            computer_moves_log = ' , '.join(["["+str(x[0])+" , "+x[1]+"]" for x in computer_moves])

            write_log(self.game_log, "All of player moves: \n" + player_moves_log + "\n")
            write_log(self.game_log, "All of game computer moves: \n" + computer_moves_log + "\n")

            p1_ship_log_text = ' , '.join([str(x) for x in p1_ship_log]) 
            p2_ship_log_text = ' , '.join([str(x) for x in p2_ship_log])

            write_log(self.game_log, "Player ships: \n" + p1_ship_log_text + "\n")
            write_log(self.game_log, "Computer ships: \n" + p2_ship_log_text + "\n")

            screen_reset(self.surface,self.settings) # Redraw the game window for the next stage
            # Create graphic elements of the game window.
            # Line breaking this way for readability
            EnemyField, PlayerField, \
            EnemyInventory, PlayerInventory, StatusField, StartButton = Game_Setup(self.surface,self.settings)
            # redraw player and computer ships in grey
            for ship_index in range(len(p1_ship_log)):
                if p1_ship_log[ship_index] == 1:
                    p1_ship_pos = ind_to_pos(ship_index,PlayerField.pos,field_cell_size)
                    draw_ship(self.surface,self.settings,p1_ship_pos,'p1_field','game')
                if p2_ship_log[ship_index] == 1:
                    p2_ship_pos = ind_to_pos(ship_index,EnemyField.pos,field_cell_size)
                    draw_ship(self.surface,self.settings,p2_ship_pos,'p2_field','game')
            # redraw all of the moves on top:
            for move in player_moves:
                player_pos = ind_to_pos(move[0],EnemyField.pos,field_cell_size)
                draw_ship(self.surface,self.settings,player_pos,'p2_field',move[1])
            
            for move in computer_moves:
                computer_pos = ind_to_pos(move[0],PlayerField.pos,field_cell_size)
                draw_ship(self.surface,self.settings,computer_pos,'p1_field',move[1])

                            
            status_message(self.surface,StatusField,"Thank you for playing, press Start to play again!")  
                    
            while game_stage == 'end':
                clock.tick(self.fps)
            
                for event in pygame.event.get():
                # Keyboard action
                    if event.type == KEYDOWN:
                    # Press ESC to quit
                        if event.key == K_ESCAPE:
                            exit()
                    # Press Enter to move to the next stage
                    #elif event.key == K_RETURN:
                    #    game_stage = 'game'
                    # Mouse action
                    if event.type == MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()

                        if StartButton.collision(pos):
                            game_stage = "game_setup"
                            


                    elif event.type == QUIT:
                            exit()

#___________________________________________________________________________________
#___________________________________________________________________________________


if __name__=="__main__":
    game=BATTLESHIP(60)
    game.run()
