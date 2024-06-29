import pygame
from pygame.locals import *



class Field:
    def __init__(self,parent_screen,pos,size,color,grid=None):
        self.size=size
        self.color = color
        self.field=pygame.Surface(self.size)
        self.field.fill(self.color)
        self.pos = pos
        self.parent_screen=parent_screen
        self.area=pygame.Rect(self.pos,self.size)
        self.grid = grid

    def collision(self,mouse_position):
        self.mouse_position=mouse_position
        return self.area.collidepoint(self.mouse_position)


    def draw(self):
        self.parent_screen.blit(self.field,self.pos)

        if self.grid:
            for i in range(10):
                pygame.draw.line(self.parent_screen,(0,0,0), (self.pos[0]+(self.size[0]/10)*i, self.pos[1]), (self.pos[0]+(self.size[0]/10)*i, self.pos[1]+self.size[1]))
                pygame.draw.line(self.parent_screen,(0,0,0), (self.pos[0], self.pos[1]+(self.size[0]/10)*i), (self.pos[0]+self.size[1], self.pos[1]+(self.size[0]/10)*i))

class Button:
    def __init__(self,parent_screen,pos,size,color_on,color_off,text=None):
        self.button_field=Field(parent_screen,pos,size,color_off)
        self.color_on = color_on
        self.color_off = color_off
        self.text = text
        self.button_field.draw()

    def collision(self,mouse_position):
        self.mouse_position=mouse_position
        return self.button_field.area.collidepoint(self.mouse_position)


    def draw(self):
        self.button_field.parent_screen.blit(self.button_field.field,self.button_field.pos)
        self.label()

    def button_on(self):
        self.button_field=Field(self.button_field.parent_screen,self.button_field.pos,self.button_field.size,self.color_on)
        self.draw()
        #self.button_field.draw()
        pygame.display.flip()

    def button_off(self):
        self.button_field=Field(self.button_field.parent_screen,self.button_field.pos,self.button_field.size,self.color_off)
        self.draw()
        #self.button_field.draw()
        pygame.display.flip()

    def label(self):
        font = pygame.font.SysFont('arial',20)
        text_line = font.render(self.text,True,(0,0,0))
        self.button_field.parent_screen.blit(text_line,self.button_field.pos)



class Shot:
    def __init__(self,pos,parent_screen,field_xy,color_array,CELL_SIZE):
        self.parent_screen=parent_screen
        self.size=CELL_SIZE
        self.shot=pygame.Surface((CELL_SIZE,CELL_SIZE))
        # the posx and posy are coordinates of the lowest corner of the cell to which pos belongs to
        # needed for coloring the cell because draw line needs corner coordinate to define the
        # rectangle that will cover the cell.
        self.posx = ((pos[0]-field_xy[0])//CELL_SIZE)*CELL_SIZE+field_xy[0] # or pos[0]-pos[0]%CELL_SIZE
        self.posy = ((pos[1]-field_xy[1])//CELL_SIZE)*CELL_SIZE+field_xy[1]
        self.shot.fill(color_array)


    def draw(self):
        self.parent_screen.blit(self.shot,(self.posx,self.posy))
        pygame.draw.line(self.parent_screen,(0,0,0), (self.posx,self.posy), (self.posx+self.size,self.posy))
        pygame.draw.line(self.parent_screen,(0,0,0), (self.posx,self.posy), (self.posx,self.posy+self.size))
        pygame.draw.line(self.parent_screen,(0,0,0), (self.posx+self.size,self.posy), (self.posx+self.size,self.posy+self.size))
        pygame.draw.line(self.parent_screen,(0,0,0), (self.posx,self.posy+self.size), (self.posx+self.size,self.posy+self.size))
        print('shot position',(self.posx,self.posy))





