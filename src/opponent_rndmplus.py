import random
from utility_functions import *

class rndmplus:
    def __init__(self, moves):
        self.name = 'Random Plus'
        self.dscr = 'Opponent takes random shots, but remembers if it hit something on the previous move'
        self.previous_moves = moves
        self.available_moves = list(range(0,100))
        self.moves_to_try = []

    def update_logs(self, moves):   
        self.previous_moves = moves
        last_move = self.previous_moves[-1][0]
        last_result = self.previous_moves[-1][1]
        # if previous shot was a miss, remove just that index from the possible shots
        # if shot sunk a ship, remove the ship index and all of the neighbors
        # if it was hit? not sure yet just the index for now
        if last_result == 'miss':
            self.available_moves.remove(last_move)

        # NEED TO CORRECT FOR BIGGER SHIPS AND THEIR BOUNDARIES
        elif last_result == 'sunk':
            # it is redundunt to go over all the indices every time but will do for now
            inds_to_remove = []
            for move in self.previous_moves:
                if 'sunk' in move[1]:
                    boundary, diag_to_remove = diagonal_check(move[0],None,'True')
                    boundary, hv_to_remove = h_v_neighbor_check(move[0], None, 'True')
                    inds_to_remove+= diag_to_remove+hv_to_remove+[last_move]
            self.available_moves = [x for x in self.available_moves if x not in inds_to_remove]
        
        elif last_result == 'hit':
            self.available_moves.remove(last_move)
        
        return None
    

    def update_moves_to_try(self):
        last_move = self.previous_moves[-1][0]
        last_result = self.previous_moves[-1][1]
        
        # if the last move sunk a ship, remove all other indices from the possible moves
        if last_result == "sunk":
            self.moves_to_try=[]

        # if last move was first in a series and a miss, continue with random shots
        elif last_result == "miss" and len(self.moves_to_try) == 0:
            self.moves_to_try=[]

        # if it is a first hit of a ship, all 4 neighbors are possible if they are in the available list
        elif last_result == "hit" and len(self.moves_to_try) == 0:
            # saving the move from which the neighbors are computed will help idetify directions later
            self.center = last_move
            # orthog parameter 0 means ship direction has not been determined yet
            self.orthog = 0
            # identify all of the neighbors
            boundary, self.moves_to_try = h_v_neighbor_check(last_move, None, 'True')
            # only keep the neighbors that are in the available list
            self.moves_to_try = [x for x in self.moves_to_try if x in self.available_moves]

        # if it is a miss, just remove the suggestion from moves_to_try
        elif last_result == "miss" and len(self.moves_to_try) > 0 :
            self.moves_to_try.remove(last_move)
            
        # if this is a next successful hit of the same ship, we need to dismiss orthogonal neighbors
        # and recursively travel along the line of the ship 
        elif last_result == "hit" and len(self.moves_to_try) > 0 :
            # check if they are available
            self.moves_to_try = [x for x in self.moves_to_try if x in self.available_moves]
            # leaves moves in one direction, but only once, because later cells will all be added in the similar direction
            if self.orthog == 0:
                self.moves_to_try = [x for x in self.moves_to_try if (last_move - x)%2 == 0]
                print("moves after removing orthogonal ",self.moves_to_try, len(self.moves_to_try))
                self.orthog = 1
            
            # the above step is supposed to be only done when there are 4 neighboring elements,
            # so after that step there are two elements in one line
            # needs to be a function
            
            self.dir = direction(self.center,last_move)

            print("Direction of new possible move", self.dir)
            print("Because center is at ", self.center, " and last move was ", last_move)

            
                
            
            # add index in the direction of last successful index
            new_ind = last_move + self.dir  
            #ADDED CHECK OF NEW_IND for boundary
            if new_ind<0 or new_ind>=100:
                pass
            elif last_move%10==9 and new_ind%10==0:
                pass
            elif last_move%10==0 and new_ind%10==9:
                pass
            else:
                if new_ind in self.available_moves:
                    self.moves_to_try.append(new_ind)
                    print("New move to be added", new_ind)
                else:
                    print("Move has already been tried, nothing added.")
                
            
            
        return None
        

 

    def move(self, move_log):
        # if this is a first move, the move log will be empty so we just do the random move and return
        if len(move_log) == 0:
            return random.choice(self.available_moves)
        
        self.update_logs(move_log) # update the local copy of previous moves and available moves
        print("before the update ",self.moves_to_try)
        self.update_moves_to_try()
        print("after the update ",self.moves_to_try)
        if len(self.moves_to_try) != 0:
            move_ind = random.choice(self.moves_to_try)
        else:    
            move_ind = random.choice(self.available_moves)
        return move_ind