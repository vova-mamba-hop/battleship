import os
import datetime as dt

def pos_to_grid(pos,field_xy,cell):
    # Assign coordinate on the screen to the nearest grid cell
    # i,j of grid points
    posx=(pos[0]-field_xy[0])//cell
    posy=(pos[1]-field_xy[1])//cell
    return [posx,posy]


def grid_to_ind(grid_coordinate):
    # Convert ship grid coordinates to the index in the ship array
    k = 10*(grid_coordinate[0])+(grid_coordinate[1])
    return k

def pos_to_ind(pos,field_xy,cell):
    return grid_to_ind(pos_to_grid(pos,field_xy,cell))

def grid_to_pos(i,j,field_xy,cell):
    pos = [((i+0.5)*cell + field_xy[0]),((j+0.5)*cell + field_xy[1])]
    return pos

def ind_to_grid(k):
    i = k%10
    j = k//10
    return j,i

def ind_to_pos(ind,field_xy,cell):
    i,j = ind_to_grid(ind)
    return grid_to_pos(i,j,field_xy,cell)
    
def direction(i,j):
    diff = j - i
    sign = diff//abs(diff)
    if diff%10 == 0:
        return 10*sign # right, letf if negative
    elif diff%10 != 0:
        return 1*sign # down, up if negative


def boundary_check(k):
    # dirty way to check which boundary index is in, grid is 10 by 10, so far hardcoded
    ub = list(range(10,90,10))
    bb = list(range(19,99,10))
    lb = list(range(1,9))
    rb = list(range(91,99))
    corners = {0:"ul",9:"bl",90:"ur",99:"br"}
    if k in lb:
        return 'lb'
    elif k in rb:
        return 'rb'
    elif k in bb:
        return 'bb'
    elif k in ub:
        return 'ub'
    elif k in list(corners.keys()):
        return corners[k]
    else:
        return 'nb'


def diagonal_check(k,log,just_values=False):
    # check if selected ship cell touches the corner of any other cell
    # grid is 10 by 10 and indices are hardcoded for now
    #check boundary conditions:
    boundary = boundary_check(k)
    print(boundary)

    if boundary == 'lb':
        neighbor_indices = [k+9,k+11]
    elif boundary =='rb':
        neighbor_indices = [k-11,k-9]
    elif boundary =='ub':
        neighbor_indices = [k+11,k-9]
    elif boundary =='bb':
        neighbor_indices = [k+9,k-11]
    elif boundary =='bl':
        neighbor_indices = [k+9]
    elif boundary =='br':
        neighbor_indices = [k-11]
    elif boundary =='ul':
        neighbor_indices = [k+11]
    elif boundary =='ur':
        neighbor_indices = [k-9]
    elif boundary =='nb':
        neighbor_indices = [k-11,k-9,k+9,k+11]

    if just_values:
        return boundary, neighbor_indices

    for ind in neighbor_indices:
        if log[ind] != 0:
            return False
    return True
    
def h_v_neighbor_check(k, log=None, just_values=False):
    #check if selected cells are next to each other along x-axis

    boundary = boundary_check(k)

    if boundary == 'lb':
        neighbor_indices = [k-1,k+1,k+10]
    elif boundary == 'rb': 
        neighbor_indices = [k-10,k-1,k+1]
    elif boundary == 'ub': 
        neighbor_indices = [k-10,k+1,k+10]
    elif boundary == 'bb': 
        neighbor_indices = [k-10,k-1,k+10]
    elif boundary == 'bl': 
        neighbor_indices = [k-1,k+10]
    elif boundary == 'br': 
        neighbor_indices = [k-1,k-10]
    elif boundary == 'ul': 
        neighbor_indices = [k+10,k+1]
    elif boundary == 'ur': 
        neighbor_indices = [k-10,k+1]
    elif boundary == 'nb': 
        neighbor_indices = [k-10,k-1,k+1,k+10]

    if just_values:
        return boundary, neighbor_indices

    for ind in neighbor_indices:
        if log[ind]!= 0: 
            return False, boundary, neighbor_indices
    return True, boundary, neighbor_indices


#or true false? Updated ship log if success. Maybe return -1 for remove, 0 for error, 1 for sucess?
def ship_log_update(ship_index, ship_log):
    #Check if cell is occupied, if it is, remove
    if ship_log[ship_index] == 0:
        ship_log[ship_index] = 1
        message = 'Ship Log Updated!'
        return ship_log, 'add', message
    else:
        ship_log[ship_index] = 0
        message = "Removed"
        return ship_log, "remove", message
    

def v_check(k, ship_log, visited, cell_count,dir='right'):
    if dir == 'left':
        n = -10
        m = 0
        one = -1
    else:
        n = 10
        m = len(ship_log)
        one = 1
    # If cell is occupied, check and add vertical neighbors if they are also occupied
    if one*(k+n)<m:
        if ship_log[k+n]==0:
            print("empty neighbor to the :",dir,"k ", k, "index ", k+n, cell_count, visited)
            return cell_count, visited
        elif ship_log[k+n]==1:
            cell_count+=1
            visited.append((k+n))
            print("non-empty neighbor to the :",dir,"k ", k, "index ", k+n, cell_count, visited)
            #print(k+10,ship_log[k+10],cell_count,visited)
            cell_count, visited = v_check((k+n), ship_log, visited, cell_count,dir)
    else: 
        return cell_count, visited
    
    return cell_count,visited


def h_check(k, ship_log, visited, cell_count,dir='down'):
    if dir == 'up':
        n = -1
        m = 9
    else:
        n = 1
        m = 0
    if (k+n)%10 !=m:
        if ship_log[k+n]==0:
            print("empty neighbor to the :",dir,"k ", k, "index ", k+n, cell_count, visited)
            return cell_count, visited
        elif ship_log[k+n]==1:
            cell_count+=1
            visited.append((k+n))
            print("non-empty neighbor to the :",dir,"k ", k, "index ", k+n, cell_count, visited)
            cell_count, visited = h_check((k+n), ship_log, visited, cell_count,dir)
    else: 
        return cell_count, visited
    
    return cell_count,visited


def ship_log_check(ship_log, ship_settings):
    #calculate number of cells that can be filled in 
    cell_max = sum([ship_settings[x]['num_cells']*ship_settings[x]['num_ships_max'] for x in ship_settings])
    # dictionary that will have how many ships needs to be
    ships_max=dict(zip([ship_settings[x]['num_cells'] for x in ship_settings],
                       [ship_settings[x]['num_ships_max'] for x in ship_settings]))  
    ships_placed = {} # how manyships have been added
    visited_indices =[]
    
    if sum(ship_log) > cell_max:
        message = 'Too many ships!'
        return ship_log,'Error', message
    
    if sum(ship_log) < cell_max:
        message = 'Not all ships placed!'
        return ship_log,'Error',message

    for k in range(len(ship_log)):
        # go through every index, and check horizonatl and vertical neighbors
        # add neighbors to visited indices array to avoid double counting
        if ship_log[k] == 1 and k not in visited_indices:
            if diagonal_check(k,ship_log):
            
                visited_indices.append(k)
                ship_count=1
                ship_count, visited_indices = h_check(k, ship_log, visited_indices, ship_count)
                ship_count, visited_indices = v_check(k, ship_log, visited_indices, ship_count)
                if ship_count not in list(ships_placed.keys()):
                    ships_placed[ship_count]=1
                else:
                    ships_placed[ship_count]+=1
            else:
                message = "Ship corners cannot touch. Please correct."
                return ship_log,'Error',message
    #Compare number of added ships to the allowed number
    for type in ship_settings.keys():
        nc = ship_settings[type]['num_cells']
        if nc not in ships_placed.keys():
            message = 'Missing a '+type+'.'
            return ship_log,'Error', message
            
        else:
            if ships_placed[nc]>ships_max[nc]:
                message = 'Too many '+ type +'s!'
                return ship_log,'Error', message
            elif ships_placed[nc]<ships_max[nc]:
                message = 'Missing a '+ type +'!'
                return ship_log,'Error', message
    
    message = 'Everything is in order!'
    return ship_log, 'Success', message



def find_ship_inds(ind, ship_log):
    # given an index and the log 
    inds = []
    num_cells_visited = 0
    b = boundary_check(ind)
    if b == 'nb':
        num_cells_visited, inds = h_check(ind, ship_log, inds, num_cells_visited)
        num_cells_visited, inds = v_check(ind, ship_log, inds, num_cells_visited,'left')
        num_cells_visited, inds = v_check(ind, ship_log, inds, num_cells_visited)
        num_cells_visited, inds = h_check(ind, ship_log, inds, num_cells_visited,'up')
    elif b == 'ub':
        num_cells_visited, inds = v_check(ind, ship_log, inds, num_cells_visited)
        num_cells_visited, inds = v_check(ind, ship_log, inds, num_cells_visited,'left')
        num_cells_visited, inds = h_check(ind, ship_log, inds, num_cells_visited)
    elif b == 'bb':
        num_cells_visited, inds = v_check(ind, ship_log, inds, num_cells_visited)
        num_cells_visited, inds = v_check(ind, ship_log, inds, num_cells_visited,'left')
        num_cells_visited, inds = h_check(ind, ship_log, inds, num_cells_visited,'up')
    elif b == 'lb':
        num_cells_visited, inds = v_check(ind, ship_log, inds, num_cells_visited)
        num_cells_visited, inds = h_check(ind, ship_log, inds, num_cells_visited)
        num_cells_visited, inds = h_check(ind, ship_log, inds, num_cells_visited,'up')
    elif b == 'rb':
        num_cells_visited, inds = v_check(ind, ship_log, inds, num_cells_visited,'left')
        num_cells_visited, inds = h_check(ind, ship_log, inds, num_cells_visited)
        num_cells_visited, inds = h_check(ind, ship_log, inds, num_cells_visited,'up')
    elif b == 'ul':
        num_cells_visited, inds = v_check(ind, ship_log, inds, num_cells_visited)
        num_cells_visited, inds = h_check(ind, ship_log, inds, num_cells_visited)
    elif b == 'ur':
        num_cells_visited, inds = v_check(ind, ship_log, inds, num_cells_visited,'left')
        num_cells_visited, inds = h_check(ind, ship_log, inds, num_cells_visited)
    elif b == 'bl':
        num_cells_visited, inds = v_check(ind, ship_log, inds, num_cells_visited)
        num_cells_visited, inds = h_check(ind, ship_log, inds, num_cells_visited,'up')
    elif b == 'br':
        num_cells_visited, inds = v_check(ind, ship_log, inds, num_cells_visited,'left')
        num_cells_visited, inds = h_check(ind, ship_log, inds, num_cells_visited,'up')
    
    # based on input index, find the other indices that belong to this ship
    print("Boundary is ", b, "neighbor indices are :", inds)
    return num_cells_visited, inds


def write_log(filename,message):
    time_now = dt.datetime.now()
    date_n_time = time_now.strftime("%Y%m%d_%H%M%S%f")
    
    with open(filename, "a") as f:
        f.write("[" + date_n_time + "]: " + message + "\n")

    return None    
        




    

