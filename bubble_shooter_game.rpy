init python:

    import random
    from enum import Enum
    import pygame
    import time
    import math



    class BubbleShooterGameDisplayable(renpy.Displayable):

        def __init__(self):

            renpy.Displayable.__init__(self)

            
            self.BORDER_WIDTH = 10  # Width of the border
            self.BORDER_COLOR = (128, 128, 128)  # Color of the border
            self.RAYON=35
            self.BUBBLE_IMAGES = [Image("images/bubble_shooter_game/red_bubble.png"),Image("images/bubble_shooter_game/green_bubble.png"),Image("images/bubble_shooter_game/blue_bubble.png"),Image("images/bubble_shooter_game/purple_bubble.png"),Image("images/bubble_shooter_game/golden_bubble.png")]
            
            self.bubble_properties = dict()  # Map to store properties of the bubbles
            
            self.SCREEN_HEIGHT= 720  
            self.SCREEN_WIDTH = 1280
            #ligne paire = 17 bubbles, ligne impaire = 18 bubbles
            self.MAX_LINE_SIZE = int(( self.SCREEN_WIDTH-self.BORDER_WIDTH*2)/(self.RAYON*2))
            self.MAX_LINE_NUMBER = int(( self.SCREEN_HEIGHT-self.BORDER_WIDTH*2)/(self.RAYON*2))

            self.last_bubble_launch=0
            #temps entre les lancements des bubbles
            self.BUBBLE_LAUNCH_DELAY=3
            self.last_iteration_time=0
            # temps entre chaque deplacement d'une bubble
            self.BUBBLE_TIME_DELAY = 0.1
            #temps maximal pour une bubble pour arriver à la cible la plus lointaine
            self.MAX_TIME = 1

            # The time of the past render-frame.
            self.last_frame_rendering = None


            #position du lancement (gauche ou droite)
            self.launch_side=1
            self.current_bubble_color = None
            self.current_iteration= None
            self.current_bubble_x = None
            self.current_bubble_y = None
            self.launch_pos=None
            self.target_pos=None
            self.bubble_launched=False
            self.target_col=None
            self.target_row=None

            self.DISTANCE_BUBBLE_MOVES_EACH_DELAY=self.compute_distance_bubble_moves_each_delay()
    
            self.end_text=""
            self.build_first_lines()  # Draw initial line of bubbles


            #TODO enlever
            self.launch_bubble()
            


        #dessine les 3 premières lignes de bubbles
        def build_first_lines(self):
            #line 1
            for i in range(self.MAX_LINE_SIZE - 1):  
                if (i==self.MAX_LINE_SIZE/2 - 1):
                    #couleur speciale pour une bubble
                    color=len(self.BUBBLE_IMAGES) - 1
                else:
                    color = random.randint(0, len(self.BUBBLE_IMAGES)- 2)  # Randomly select color
                self.add_bubble(1, i + 1, color) 
            #line 2
            for i in range(self.MAX_LINE_SIZE): 
                color = random.randint(0, len(self.BUBBLE_IMAGES) - 2)  
                self.add_bubble(2, i + 1, color)  
            #line 3
            for i in range(self.MAX_LINE_SIZE - 1):
                color = random.randint(0, len(self.BUBBLE_IMAGES) - 2)   
                self.add_bubble(3, i + 1, color) 


        #construction d'une bubble
        def add_bubble(self,row, col, color):
            if row not in self.bubble_properties:
                self.bubble_properties[row] = dict()  # Store bubble properties
            self.bubble_properties[row][col] = color  # Set color for the bubble at specific row and column


        # dessin de la bubble
        def draw_bubble( self, render, width, height, st, at, color, xpos, ypos):

            # Render the apple image
            bubble = renpy.render(self.BUBBLE_IMAGES[color], width, height, st, at)
                
            # renpy.render returns a Render object, which we can
            # blit to the Render we're making
            render.blit(bubble, (xpos, ypos))

        #affichage de la bubble lancee
        def draw_current_bubble(self,render, width, height, st, at, dtime):
            self.last_bubble_launch += dtime
            self.last_iteration_time += dtime
            # show player standing when not moving
            if self.last_bubble_launch >= self.BUBBLE_LAUNCH_DELAY:
                self.last_bubble_launch -= self.BUBBLE_LAUNCH_DELAY
                self.launch_bubble()

            
            # dessin de la bubble
            if  self.bubble_launched:
                if self.last_iteration_time >= self.BUBBLE_TIME_DELAY:
                    self.last_iteration_time -= self.BUBBLE_TIME_DELAY
                    self.current_iteration=self.current_iteration+1

                    if self.current_iteration==self.iteration_number-1:
                        self.bubble_launched=False
                        #ajoute (definitivement) la bubble à la liste des bubbles
                        self.add_bubble(self.target_row, self.target_col, self.current_bubble_color) 
                    else:
                        self.current_bubble_x= self.launch_pos[0] + (self.target_pos[0] - self.launch_pos[0]) * self.current_iteration / self.iteration_number  # Calculate x position
                        self.current_bubble_y = self.launch_pos[1] + (self.target_pos[1] - self.launch_pos[1]) * self.current_iteration / self.iteration_number  # Calculate y position

                self.draw_bubble(render, width, height, st, at, self.current_bubble_color, self.current_bubble_x, self.current_bubble_y)



        #affichage de toutes les bubbles
        def display_bubbles(self,render, width, height, st, at, dtime):
           
            for rows in sorted(self.bubble_properties, key=lambda x: int(x)):
                increment = 1
                if (rows % 2 == 0):
                    increment = 0
                #parcours des bubbles
                for cols in sorted(self.bubble_properties[rows], key=lambda x: int(x)):
                    #(x,y)=position en haut à gauche du carré englobant la bubble
                    self.draw_bubble( render, width, height, st, at,  self.bubble_properties[rows][cols],
                    self.BORDER_WIDTH + (cols - 1) * self.RAYON * 2 + increment * self.RAYON,
                    self.BORDER_WIDTH + (rows-1) * self.RAYON * 2  )
 
        def is_odd(self,line_number):
            return line_number % 2 != 0  # Check if the line number is odd
           
        #equation d'une droite passant par deux points
        def get_line_equation(self,launch_pos, target_pos):
            (x1, y1) = launch_pos
            (x2, y2) = target_pos
            a = (y2 - y1) / (x2 - x1)
            b = y1 - a * x1
            return (a,b)

        #distance a parcourir entre la position de depart et la cible
        def compute_distance_to_target(self):
            return ((self.target_pos[0] - self.launch_pos[0]) ** 2 + (self.target_pos[1] - self.launch_pos[1]) ** 2) ** 0.5


        def compute_distance_bubble_moves_each_delay(self):
            max_distance = (((self.SCREEN_HEIGHT - self.BORDER_WIDTH - self.RAYON) - (self.BORDER_WIDTH + self.RAYON)) ** 2 + (
                    (self.SCREEN_WIDTH - self.BORDER_WIDTH - self.RAYON) - (self.BORDER_WIDTH + self.RAYON)) ** 2) ** 0.5
            
            return self.BUBBLE_TIME_DELAY * max_distance / self.MAX_TIME


        def identify_bubble_to_target(self):
            #parcours des lignes
            for row in range(1,self.MAX_LINE_NUMBER+1):
                #parcours des colonnes : si on lance à gauche, on lance vers la gauche
                #si on lance à droite, on lance vers la droite
                if(self.launch_side==0):
                    #on ne parcourt que la moitié des lignes (sinon risque d'intersection)
                    for col in range(1,int(self.MAX_LINE_SIZE/2)+2):
                        if self.is_candidat(row,col,self.current_bubble_color) :

                            candidate_position=self.compute_target_candidate_bubble_position(row,col)
                            
                            #on a un candidat, mais il ne faut pas que le trajet vers ce candidat
                            #intersecte une bubble deja en place
                            #equation de la droite passant par les deux points
                            # on enlève le self.RAYON pour avoir la position "haute" des bubbles, qui peuvent intersectées
                            if not self.check_if_intersection(self.launch_pos, candidate_position,row):
                                return (candidate_position,row,col)
                else:
                    for col in range(self.MAX_LINE_SIZE,int(self.MAX_LINE_SIZE/2)-2,-1):
                        if self.is_candidat(row,col,self.current_bubble_color) :

                            candidate_position=self.compute_target_candidate_bubble_position(row,col)
                            
                            #on a un candidat, mais il ne faut pas que le trajet vers ce candidat
                            #intersecte une bubble deja en place
                            #equation de la droite passant par les deux points
                            # on enlève le self.RAYON pour avoir la position "haute" des bubbles, qui peuvent intersectées
                            if not self.check_if_intersection(self.launch_pos, candidate_position,row):
                                return (candidate_position,row,col)

            candidate_position=self.compute_target_candidate_bubble_position(1,1)
            return (candidate_position,1,1)


        def is_candidat(self,row,col,color):
            #candidat si :
            #  pas encore de ligne ou 
            #( pas de bubble a la position et (pas de voisin gauche ou couleur voisin gauche != couleur)
            # et (pas de voisin droite ou couleur voisin droite != couleur))
            verification_ligne_courante_ok = row not in self.bubble_properties or\
            ( col not in self.bubble_properties[row] \
            and ((col-1) not in self.bubble_properties[row] or self.bubble_properties[row][col-1] != color) \
            and ((col+1) not in self.bubble_properties[row] or self.bubble_properties[row][col+1] != color))
            # MAX_LINE_SIZE uniquement pour les lignes paires (not odd)
            verification_derniere_colonne_ok=(col != self.MAX_LINE_SIZE or not self.is_odd(row))
            # et ligne 1 ou ((au moins un parent) et (pas de parent gauche ou couleur parent gauche != couleur) et (pas de parent droite ou couleur parent droite != couleur))
            # ligne 1 :   1 2 3 4
            # ligne 2 :    1 2 3 4
            # ligne 3 :   1 2 3 4
            if self.is_odd(row):
                col_parent_gauche=col
                col_parent_droite=col+1
            else:
                col_parent_gauche=col-1
                col_parent_droite=col
 
            verification_ligne_dessus_ok =  row==1  or ( \
            not((col_parent_gauche) not in self.bubble_properties[row-1] and (col_parent_droite) not in self.bubble_properties[row-1])\
            and  ((col_parent_gauche) not in self.bubble_properties[row-1] or self.bubble_properties[row-1][col_parent_gauche] != color)\
            and ((col_parent_droite) not in self.bubble_properties[row-1] or self.bubble_properties[row-1][col_parent_droite] != color)\
            )
            return verification_ligne_courante_ok and verification_derniere_colonne_ok and verification_ligne_dessus_ok
        
        def check_if_intersection(self,launch_pos, target_pos,row):
            (x1, y1) = launch_pos
            (x2, y2) = target_pos
            if (x1 != x2) and (y1 != y2):
                (a,b)=self.get_line_equation(launch_pos, target_pos)
                return False
            else:
                #cas où les deux points sur la même colonne ou la même ligne : pas d'intersaction
                return False

        #calcule de la position (x,y) de la bubble
        def compute_target_candidate_bubble_position(self,row,col):
            
            
            if self.is_odd(row):
                return (
                    col * self.RAYON * 2 + self.BORDER_WIDTH - self.RAYON,
                    self.BORDER_WIDTH + row * self.RAYON * 2 - (self.RAYON*2))  
            else:
                return (
                        col * self.RAYON * 2 + self.BORDER_WIDTH -self.RAYON * 2, self.BORDER_WIDTH + row * self.RAYON * 2 - (self.RAYON*2))  




        def launch_bubble(self):
            self.current_bubble_color = random.randint(0, len(self.BUBBLE_IMAGES) - 2)    # Randomly choose a color for the bubble

            #(x,y)=position en haut à gauche du carré englobant la bubble
            if self.launch_side==0:
                #on lançait depuis la gauche, on lance depuis la droite
                self.launch_side=1
                self.launch_pos = (self.SCREEN_WIDTH - self.BORDER_WIDTH - self.RAYON*2,
                        self.SCREEN_HEIGHT- self.BORDER_WIDTH-self.RAYON*2)  # Start position of the bubble
            else:
                #on lançait depuis la droite, on lance depuis la gauche
                self.launch_side=0
                self.launch_pos = (self.BORDER_WIDTH,
                        self.SCREEN_HEIGHT- self.BORDER_WIDTH-self.RAYON*2)  # Start position of the bubble

        
            (self.target_pos,self.target_row,self.target_col) = self.identify_bubble_to_target( )  # Find target position for the bubble
         
            distance_to_target = self.compute_distance_to_target()
            self.bubble_launched=True
            
            self.iteration_number = math.trunc(distance_to_target / self.DISTANCE_BUBBLE_MOVES_EACH_DELAY)
            self.last_iteration_time=0
            self.current_iteration=0
            self.current_bubble_x = self.launch_pos[0]   # Calculate x position
            self.current_bubble_y = self.launch_pos[1]   # Calculate y position
            
         



        # Draws the screen
        def render(self, width, height, st, at):

            # The Render object we'll be drawing into.
            render = renpy.Render(width, height)

            # Figure out the time elapsed since the previous frame.
            if self.last_frame_rendering is None:
                self.last_frame_rendering = st
            dtime = st - self.last_frame_rendering
            self.last_frame_rendering = st

            self.draw_current_bubble(render, width, height, st, at,dtime)

            # Display all bubbles
            self.display_bubbles(render, width, height, st, at,dtime)

            # redraw the screen
            renpy.redraw(self, 0)

            # Return the Render object.
            return render


        # Handles events to move player
        def event(self, ev, x, y, st):

            #quit
            if  ev.type == pygame.KEYDOWN  and ev.key == pygame.K_ESCAPE :
                self.show_next_screen()
        
            # Ensure the screen updates
            renpy.restart_interaction()
            raise renpy.IgnoreEvent()  


                # show screen after game (home screen or next screen of history)
        def show_next_screen(self):
            self.__init__()
            renpy.jump("after_bubble_shooter_game")  

    def display_end_bubble_shooter_game_text(st, at):
        return Text( bubble_shooter_game.end_text, font='gui/jd_code.ttf', size=50, color="#33e43c"), .1 

default bubble_shooter_game = BubbleShooterGameDisplayable()

# label to start snake game
label start_bubble_shooter_game:
    play music snake_game_music
    window hide  # Hide the window and quick menu while in mini game
    call screen bubble_shooter_game


label after_bubble_shooter_game:
    stop music
    window auto  
    play music main_menu
    call screen main_menu


#start bubble shooter game 
screen bubble_shooter_game():
    add "images/bubble_shooter_game/background_bubble_shooter.png"
    add bubble_shooter_game
    add DynamicDisplayable(display_end_bubble_shooter_game_text) xalign 0.5 yalign 0.5 
