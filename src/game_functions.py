import random
import pygame
from pygame.locals import *


from game_classes import *
from utility_functions import *

#### SCREEN RELATED FUNCTIONS:

def screen_reset(surface,settings):
    return surface.fill(settings['SETTINGS']["main_window"]['color'])

def draw_action(surface,settings,pos,p_field,action):
    print('clicked position',pos[0],pos[1])
    cell_size = settings['SETTINGS'][p_field]['size'][0]/settings['SETTINGS'][p_field]['num_cells_per_row']
    ship=Shot(pos,surface,settings['SETTINGS'][p_field]['xy'],settings['SETTINGS']['ship_colors'][action],cell_size)
    ship.draw()
    pygame.display.flip()
    return None

def draw_ship(surface,settings,pos,p_field,color):
    print('clicked position',pos[0],pos[1])
    cell_size = settings['SETTINGS'][p_field]['size'][0]/settings['SETTINGS'][p_field]['num_cells_per_row']
    ship=Shot(pos,surface,settings['SETTINGS'][p_field]['xy'],settings['SETTINGS']['ship_colors'][color],cell_size)
    ship.draw()
    pygame.display.flip()
    return None

def erase_ship(surface,settings,pos,p_field):
    print('clicked position',pos[0],pos[1])
    cell_size = settings['SETTINGS'][p_field]['size'][0]/settings['SETTINGS'][p_field]['num_cells_per_row']
    ship=Shot(pos,surface,settings['SETTINGS'][p_field]['xy'],settings['SETTINGS']['ship_colors']['field'],cell_size)
    ship.draw()
    pygame.display.flip()
    return None

def status_message(surface, field, message):
    field.draw()
    font = pygame.font.SysFont('arial',30)
    line1 = font.render(message,True,(0,0,0))
    surface.blit(line1,(60,360))
    pygame.display.flip()
    return None


## GAMEPLAY FUNCTIONS: ################################################################################

#### STAGE SETUP ######################################################################################

def Intro(surface,settings):

    # Intro text:
    
    
    greeting = settings['MESSAGES']['start']
    intro = settings['MESSAGES']['intro']

    font_title = pygame.font.SysFont('arial',greeting['section_font'])
    font_intro = pygame.font.SysFont('arial',intro['section_font'])
    
    
    with open(greeting['text_location'],'r') as f:
        text = f.readline().lstrip().rstrip()
        text_xy = greeting['xy']
        #print(greeting['section_name']==text.rstrip())
        if text == greeting['section_name']: 
            text=f.readline().lstrip().rstrip()
            
            line_space = 0
            while text != greeting['section_end']:
                print(text)
                line = font_title.render(text,True,(0,0,0))
                surface.blit(line,(text_xy[0],text_xy[1]+line_space))
                line_space+=10
                text=f.readline().lstrip().rstrip()
                if line_space ==100:
                    break
    
    with open(intro['text_location'],'r') as f:
        
        text = f.readline().lstrip().rstrip()
        while text != intro['section_name']:
            text = f.readline().lstrip().rstrip()
        text = f.readline().lstrip().rstrip()
        text_xy = intro['xy']
        print(text)
        
        line_space = 0
        while text != intro['section_end']:
            print(text)
            line = font_intro.render(text,True,(0,0,0))
            surface.blit(line,(text_xy[0],text_xy[1]+line_space))
            line_space+=30
            text=f.readline().lstrip().rstrip()
            if line_space == 200:
                break

    debug_text = "Debug Mode On/Off:"
    opponent_text = "Opponent Type:"
    line_debug = font_intro.render(debug_text,True,(0,0,0))
    line_opponent = font_intro.render(opponent_text,True,(0,0,0))
    surface.blit(line_debug,(820,60))
    surface.blit(line_opponent,(820,120))
    
    debug_Button = Button(surface,settings['SETTINGS']['debug_button']['xy'],
                                 settings['SETTINGS']['debug_button']['size'],
                                 settings['SETTINGS']['debug_button']['color_on'],
                                 settings['SETTINGS']['debug_button']['color_off'],'Debug')
    
    play_Button = Button(surface,settings['SETTINGS']['play_button']['xy'],
                                 settings['SETTINGS']['play_button']['size'],
                                 settings['SETTINGS']['play_button']['color_on'],
                                 settings['SETTINGS']['play_button']['color_off'],'  Play  ')

    rndm_Button = Button(surface,settings['SETTINGS']['rndm_button']['xy'],
                                 settings['SETTINGS']['rndm_button']['size'],
                                 settings['SETTINGS']['rndm_button']['color_on'],
                                 settings['SETTINGS']['rndm_button']['color_off'],'Random')
    
    rndmplus_Button = Button(surface,settings['SETTINGS']['rndmplus_button']['xy'],
                                 settings['SETTINGS']['rndmplus_button']['size'],
                                 settings['SETTINGS']['rndmplus_button']['color_on'],
                                 settings['SETTINGS']['rndmplus_button']['color_off'],'Random Plus')

    StatusField = Field(surface,settings['SETTINGS']['status']['xy'],settings['SETTINGS']['status']['size'],settings['SETTINGS']['status']['color'])
    
    debug_Button.draw()
    rndm_Button.draw()

    play_Button.draw()
    rndmplus_Button.draw()

    pygame.display.flip()

    return debug_Button, play_Button, rndm_Button, rndmplus_Button, StatusField

def Game_Setup(surface,settings):

    PlayerField=Field(surface,settings['SETTINGS']['p1_field']['xy'],settings['SETTINGS']['p1_field']['size'],settings['SETTINGS']['p1_field']['color'],True)
    EnemyField=Field(surface,settings['SETTINGS']['p2_field']['xy'],settings['SETTINGS']['p2_field']['size'],settings['SETTINGS']['p2_field']['color'],True)
    PlayerInventory=Field(surface,settings['SETTINGS']['p1_inventory']['xy'],settings['SETTINGS']['p1_inventory']['size'],settings['SETTINGS']['p1_inventory']['color'],False)
    EnemyInventory=Field(surface,settings['SETTINGS']['p2_inventory']['xy'],settings['SETTINGS']['p2_inventory']['size'],settings['SETTINGS']['p2_inventory']['color'],False)

    StatusField = Field(surface,settings['SETTINGS']['status']['xy'],settings['SETTINGS']['status']['size'],settings['SETTINGS']['status']['color'])
    StartButton = Button(surface,settings['SETTINGS']['start_button']['xy'],
                                 settings['SETTINGS']['start_button']['size'],
                                 settings['SETTINGS']['start_button']['color_on'],
                                 settings['SETTINGS']['start_button']['color_off'],'Start')
    
    
    
    EnemyField.draw()
    PlayerField.draw()
    EnemyInventory.draw()
    PlayerInventory.draw()
    StatusField.draw()
    StartButton.draw()

    pygame.display.flip()


    return EnemyField, PlayerField, EnemyInventory, PlayerInventory, StatusField, StartButton


#### COMPUTER SHIP SETUP ##############################################################################

def computer_ship_setup(ship_log, ship_settings,ship_types):
    # Ship selection is fairly random for now, later will add more optimized constructor based on 
    # probabilities
    # Total number of ships possible
    total_ships = sum([x['num_ships_max'] for x in ship_settings.values()])
    # ship_id tracks how many ships have been added
    ship_id=0
    # available is a list that tracks indices open for ship placement
    available = list(range(len(ship_log)))
    # this dictionary tracks how many individual ships have been added
    ship_dict={}
    # until all the ships are placed
    while ship_id < total_ships:

        rand_ship_type = random.choice(ship_types) # randomply choose ship type
        rand_ship_size = ship_settings[rand_ship_type]['num_cells'] # get corresponding size
        #random index from ship log that is not in the occupied
        rand_ship_ind = random.choice(available) 
        # 0 is vertical up, 1 is horizontal right, 2 is vertical down, 3 is horizonal left
        # depending on the index and boundary only some are available. 
        b = boundary_check(rand_ship_ind)

        if b == "nb":
            orient_vec = [0,1,2,3]
        elif b == "lb":
            orient_vec = [0,1,3]
        elif b == "rb":
            orient_vec = [0,1,2]
        elif b == "ub":
            orient_vec = [1,2,3]
        elif b == "bb":
            orient_vec = [0,2,3]
        elif b == "ul":
            orient_vec = [1,3]
        elif b == "ur":
            orient_vec = [1,2]
        elif b == "bl":
            orient_vec = [0,3]
        elif b == "br":
            orient_vec = [0,2]
        
        rand_ship_orient = random.choice(orient_vec)
       
        # get indices of all parts of the ship depending on the orientation
        if rand_ship_orient == 0:
            ship = [(rand_ship_ind-x) for x in range(rand_ship_size)]
        elif rand_ship_orient == 1:
            ship = [(rand_ship_ind+x) for x in range(rand_ship_size)]
        elif rand_ship_orient == 2:
            ship = [(rand_ship_ind-10*x) for x in range(rand_ship_size)]
        elif rand_ship_orient == 3:
            ship = [(rand_ship_ind+10*x) for x in range(rand_ship_size)]
       

        # check if all the indices are free 
        count = 0
        for i in ship:
            if i in available:
                count+=1
        # if all the spots are free, add the ships to the log and remove all the indices from available
        if count==rand_ship_size:
            for k in ship:
                ship_log[k]=1
                # get neighboring and ship indices and remove them from available
                boundary_type, diag_inds = diagonal_check(k, ship_log, True)
                boundary_type, hv_inds = h_v_neighbor_check(k, ship_log, True)
                remove_inds = [k]+diag_inds+hv_inds
                print(remove_inds)
                available  = list(set(available) - set(remove_inds))
                
            ship_id+=1
            # update ship dictionary with placed ship
            if rand_ship_type not in ship_dict.keys():
                ship_dict[rand_ship_type]=1
            else:
                ship_dict[rand_ship_type]+=1
            # check if there are too many ships of a particular type
            if ship_dict[rand_ship_type]==ship_settings[rand_ship_type]['num_ships_max']:
                ship_types.remove(rand_ship_type)
                print('Enough of ',rand_ship_type)


        print(ship_id," ship(s) added")
    print("Ships added: ", ship_dict)
    message = 'Opponent ships added!'
    return ship_log, 'Success', message
         


#### MOVES ###############################################################################

def hit_or_miss(ind, ship_log, ship_cells_hit, moves):
    # ship_cells_hit counts how many ship cells have been hit, if all then game ends

    if ship_log[ind]==0:
        action = 'miss'
        moves.append([ind, action])
        return ship_cells_hit, action, moves
    else:
        ship_cells_hit +=1
        num_neighbors, neighbors = find_ship_inds(ind, ship_log)
        print("Number of neighbors: ",num_neighbors,"neighbors are :", neighbors)
        if num_neighbors == 0:
            action = 'sunk'
            moves.append([ind, action])
            return ship_cells_hit, action, moves
        
        count = 0
        for j in neighbors:
            if j in [x[0] for x in moves]:
                count+=1
        print("how many neighbors been hit: ",count,"neighbors of ",ind,"are ", neighbors)
        if count==num_neighbors:
            for move in moves:
                if move[0] in neighbors:
                    move[1]='hit-sunk'
            action = 'sunk' 
        else: 
            action = 'hit'
        
        moves.append([ind, action])     
        return ship_cells_hit, action, moves

def player_turn(pos, field_xy, field_cell_size, ship_log, player_moves,sch):
    shot_index = pos_to_ind(pos,field_xy,field_cell_size)

    moves_tried = [x[0] for x in player_moves]
    
    if shot_index in moves_tried:
        turn = 0
        action = 'Try again.'
        message = "You have already tried this cell."
        return turn, action, message, player_moves, sch


    sch, action, player_moves = hit_or_miss(shot_index,ship_log,sch,player_moves)
    
    turn = 0
    if action == "miss":
        turn = 1

    if sch == 20:
        message = 'Player Wins!'
    else: 
        #if action == 'sunk':
        #    sch+=1
        message = action
    return turn, action, message, player_moves, sch


def computer_turn(Opponent,pos, field_cell_size, ship_log, computer_moves,sch):
    shot_index = Opponent.move(computer_moves)
    sch, action, computer_moves = hit_or_miss(shot_index,ship_log, sch,computer_moves)
    shot_pos = ind_to_pos(shot_index,pos,field_cell_size)
    
    turn = 1
    if action == "miss":
        turn = 0
    if sch == 20:
        message = 'Computer Wins!'
    else: 
        #if action == 'sunk':
        #    sch+=1
        message = action
    return turn, shot_pos, action, message, computer_moves, sch


# function to check if the move already has been made and if it has - don't count it
# saves computer from hitting same index
# saves player from accidentaly clicking same index

# how to make player shot on click instead of on hover?






