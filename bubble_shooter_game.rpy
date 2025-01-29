init python:


#TODO 
#traductions credits, bubble shooter, histoire
#intersections imprecises


    import random
    from enum import Enum
    import pygame
    import time
    import math
    import logging


    class CannonPositionEnum(Enum):
        DOWN = 0
        TOP = 1
        MIDDLE= 2

    class ColorEnum(Enum):
        GOLDEN=0
        RED = 1
        GREEN = 2
        BLUE= 3
        PURPLE = 4
        RED_EXPLODE_1=5
        GREEN_EXPLODE_1=6
        BLUE_EXPLODE_1=7
        PURPLE_EXPLODE_1=8
        RED_EXPLODE_2=9
        GREEN_EXPLODE_2=10
        BLUE_EXPLODE_2=11
        PURPLE_EXPLODE_2=12
        RED_EXPLODE_3=13
        GREEN_EXPLODE_3=14
        BLUE_EXPLODE_3=15
        PURPLE_EXPLODE_3=16
        RED_EXPLODE_4=17
        GREEN_EXPLODE_4=18
        BLUE_EXPLODE_4=19
        PURPLE_EXPLODE_4=20
        RED_EXPLODE_5=21
        GREEN_EXPLODE_5=22
        BLUE_EXPLODE_5=23
        PURPLE_EXPLODE_5=24
        RED_EXPLODE_6=25
        GREEN_EXPLODE_6=26
        BLUE_EXPLODE_6=27
        PURPLE_EXPLODE_6=28
        RED_EXPLODE_7=29
        GREEN_EXPLODE_7=30
        BLUE_EXPLODE_7=31
        PURPLE_EXPLODE_7=32


    class BubbleDirectionEnum(Enum):
        UP = 1
        DOWN = 2

    class BubbleShooterGameDisplayable(renpy.Displayable):

        def __init__(self):

            renpy.Displayable.__init__(self)
            
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(filename='debug.log', encoding='utf-8', level=logging.DEBUG)
            
            self.BORDER_WIDTH = 10  # Width of the border
            self.BORDER_COLOR = (128, 128, 128)  # Color of the border
            self.BUBBLE_IMAGE_SIZE=70
            self.BUBBLE_REAL_SIZE=60
            
            self.init=True
            self.should_draw_buttons=True
            #angle de rotation à chaque fois qu'on appuie sur gauche ou droite
            self.ANGLE_STEP=2
            #angle maximum du distance
            self.MAX_ANGLE=35
            self.cannon_moving=False
            self.start_cannon_move=0
            self.CANNON_MOVE_DURATION=0.2
            self.show_next_bubble=False
            #evite les latences clavier
            self.cannon_next_direction=Null

            #les images 
            self.BUBBLE_IMAGES = [Image("images/bubble_shooter_game/golden_bubble.png"),
            Image("images/bubble_shooter_game/red_bubble.png"),Image("images/bubble_shooter_game/green_bubble.png"),Image("images/bubble_shooter_game/blue_bubble.png"),Image("images/bubble_shooter_game/purple_bubble.png")
            ,Image("images/bubble_shooter_game/red_bubble.png"),Image("images/bubble_shooter_game/green_bubble.png"),Image("images/bubble_shooter_game/blue_bubble.png"),Image("images/bubble_shooter_game/purple_bubble.png")
            ,Image("images/bubble_shooter_game/red_bubble.png"),Image("images/bubble_shooter_game/green_bubble.png"),Image("images/bubble_shooter_game/blue_bubble.png"),Image("images/bubble_shooter_game/purple_bubble.png")
            ,Image("images/bubble_shooter_game/red_bubble.png"),Image("images/bubble_shooter_game/green_bubble.png"),Image("images/bubble_shooter_game/blue_bubble.png"),Image("images/bubble_shooter_game/purple_bubble.png")
            ,Image("images/bubble_shooter_game/red_bubble_2.png"),Image("images/bubble_shooter_game/green_bubble_2.png"),Image("images/bubble_shooter_game/blue_bubble_2.png"),Image("images/bubble_shooter_game/purple_bubble_2.png")        
            ,Image("images/bubble_shooter_game/red_bubble_3.png"),Image("images/bubble_shooter_game/green_bubble_3.png"),Image("images/bubble_shooter_game/blue_bubble_3.png"),Image("images/bubble_shooter_game/purple_bubble_3.png")        
            ,Image("images/bubble_shooter_game/red_bubble_4.png"),Image("images/bubble_shooter_game/green_bubble_3.png"),Image("images/bubble_shooter_game/blue_bubble_4.png"),Image("images/bubble_shooter_game/purple_bubble_4.png")          
            ]

            self.BUBBLE_COLOR_EXPLOSE=4
            self.BUBBLE_COLOR_EXPLOSE_NOT_ORPHAN=20
            
            self.CANNON_BASE_IMAGE=[Image("images/bubble_shooter_game/elephant.png"),Image("images/bubble_shooter_game/elephant_red.png"),Image("images/bubble_shooter_game/elephant_green.png"),Image("images/bubble_shooter_game/elephant_blue.png"),Image("images/bubble_shooter_game/elephant_purple.png")]
            self.CANNON_IMAGE=[Image("images/bubble_shooter_game/canon.png"),Image("images/bubble_shooter_game/canon_red.png"),Image("images/bubble_shooter_game/canon_green.png"),Image("images/bubble_shooter_game/canon_blue.png"),Image("images/bubble_shooter_game/canon_purple.png")]
            self.TARGET_IMAGE=Image("images/bubble_shooter_game/target.png")
            self.bubble_properties = dict()  # Map to store properties of the bubbles

            self.buttons_idle = [Image("images/bubble_shooter_game/up_idle.png"),Image("images/bubble_shooter_game/down_idle.png")]
            self.buttons_pushed = [Image("images/bubble_shooter_game/up_pushed.png"),Image("images/bubble_shooter_game/down_pushed.png")]
 

            #au joueur de jouer
            self.player_turn=False
     
            self.SCREEN_HEIGHT= 720  
            self.SCREEN_WIDTH = 1280
            self.CANNON_BASE_WIDTH=140

            #ligne paire = 17 bubbles, ligne impaire = 18 bubbles
            self.MAX_LINE_SIZE = int(( self.SCREEN_HEIGHT-self.BORDER_WIDTH*2)/(self.BUBBLE_IMAGE_SIZE))
            self.MAX_LINE_NUMBER = int(( self.SCREEN_WIDTH-self.BORDER_WIDTH*2 - self.BUBBLE_IMAGE_SIZE*5)/(self.BUBBLE_IMAGE_SIZE))

            self.LAUNCH_COORDS_DOWN=(self.SCREEN_WIDTH - self.BORDER_WIDTH- self.BUBBLE_IMAGE_SIZE*1.5,
                        self.SCREEN_HEIGHT- self.BORDER_WIDTH-self.BUBBLE_IMAGE_SIZE*1.5)
            self.LAUNCH_COORDS_TOP=  (self.SCREEN_WIDTH - self.BORDER_WIDTH- self.BUBBLE_IMAGE_SIZE*1.5,
                        self.BORDER_WIDTH+self.BUBBLE_IMAGE_SIZE*0.5)
            self.LAUNCH_COORDS_MIDDLE =   (self.SCREEN_WIDTH - self.BORDER_WIDTH- self.BUBBLE_IMAGE_SIZE*1.5,
                        self.BORDER_WIDTH+4.5*self.BUBBLE_IMAGE_SIZE)

            #liste des angles des canons
            self.angles=[0,0,0]

            self.last_bubble_launch=0
            #temps entre les lancements des bubbles
            self.BUBBLE_LAUNCH_DELAY=2
            self.last_iteration_time=0
            # temps entre chaque deplacement d'une bubble
            self.BUBBLE_TIME_DELAY = 0.01
            #temps maximal pour une bubble pour arriver à la cible la plus lointaine
            self.MAX_TIME = 1
            #temps entre chaque animation d'explosion
            self.EXPLODE_DELAY=0.1
            self.last_explode_step=0

            # The time of the past render-frame.
            self.last_frame_rendering = None


            #position du lancement (gauche ou droite)
            self.launch_position=CannonPositionEnum.DOWN
            self.last_launch_position=CannonPositionEnum.TOP
            self.current_bubble_color =  random.choice([ColorEnum.RED,ColorEnum.GREEN,ColorEnum.BLUE,ColorEnum.PURPLE])    # Randomly choose a color for the bubble
            self.current_iteration= None
            self.current_bubble_x = None
            self.current_bubble_y = None
            self.launch_coords=self.LAUNCH_COORDS_DOWN
            self.target_pos=None
            self.bubble_launched=False
            self.target_col=None
            self.target_row=None
            self.direction_pushed=None
            self.end_game=False
            self.wait_for_start=True
            self.victory=False

            self.DISTANCE_BUBBLE_MOVES_EACH_DELAY=self.compute_distance_bubble_moves_each_delay()
    
            self.information_text=_("Attention, ça va commencer !\n\nA vous de trouver comment gagner...\n\nUtilisez les flèches de direction pour bouger la trompe de l'éléphant.\nAppuyez sur Espace ou cliquez pour tirer.\n\nAppuyez sur Entrée ou Clic Gauche pour lancer le jeu.")

            #couleur speciale pour une bubble
            self.add_bubble(1,self.MAX_LINE_SIZE/2, ColorEnum.GOLDEN) 
            #initialisation des 50 premières bubbles
            for i in range(70):
                if self.last_launch_position==CannonPositionEnum.DOWN:
                    #on lançait depuis la gauche, on lance depuis la droite
                    self.launch_position=CannonPositionEnum.TOP
                    self.launch_coords = self.LAUNCH_COORDS_TOP  # Start position of the bubble

                else:
                    #on lançait depuis la droite, on lance depuis la gauche
                    self.launch_position=CannonPositionEnum.DOWN
                    self.launch_coords = self.LAUNCH_COORDS_DOWN  # Start position of the bubble

                self.current_bubble_color = random.choice([ColorEnum.RED,ColorEnum.GREEN,ColorEnum.BLUE,ColorEnum.PURPLE])    # Randomly choose a color for the bubble

                self.init_ennemy_launch()
                self.add_bubble(self.target_row, self.target_col, self.current_bubble_color)
                #suppression des éventuelles bubbles voisines de même couleur
                self.delete_bubbles_same_color(self.target_row, self.target_col, self.current_bubble_color)
            self.init=False
            #on reinitialise les canons (canon gauche, droite, milieu)
            self.angles=[0,0,0]  
            #c'est au tour du joueur
            self.player_turn=True
            self.compute_player_target_candidate_bubble_position()

            
    
        def game_over(self):
            self.end_game=True
            renpy.music.stop()
            renpy.sound.play(lose_sound)
            if mini_game==True:
                self.information_text=_("PERDU !\nAppuyez sur Entrée ou Clic Gauche pour rejouer.\nAppuyez sur Echap ou Clic GM pour quitter.")
            else:
                self.information_text=_("PERDU !\nAppuyez sur Entrée ou Clic Gauche pour rejouer.\nAppuyez sur Echap ou Clic GM pour poursuivre l'histoire.")



        def initial_cannon_move(self,angle):
            self.cannon_moving=True
            self.angles[CannonPositionEnum.MIDDLE.value]+=angle
            #on a une limitation d'angle
            if self.angles[CannonPositionEnum.MIDDLE.value]<-self.MAX_ANGLE:
                self.angles[CannonPositionEnum.MIDDLE.value]=-self.MAX_ANGLE
            if self.angles[CannonPositionEnum.MIDDLE.value]>self.MAX_ANGLE:
                self.angles[CannonPositionEnum.MIDDLE.value]=self.MAX_ANGLE
            #calcule du candidat
            self.compute_player_target_candidate_bubble_position() 
            renpy.redraw(self, 0)



        #construction d'une bubble
        def add_bubble(self,row, col, color):
            if row not in self.bubble_properties:
                self.bubble_properties[row] = dict()  # Store bubble properties
            self.bubble_properties[row][col] = color  # Set color for the bubble at specific row and column


        #draw cannon
        def draw_cannon( self, render, width, height, st, at, xpos, ypos,angle,color):
            # Render the cannon  image
            cannon= renpy.render(Transform(self.CANNON_IMAGE[color],rotate=angle), width, height, st, at)
            # renpy.render returns a Render object, which we can
            # blit to the Render we're making
            render.blit(cannon, (xpos, ypos))


               


        # dessin du socle du canon
        def draw_cannon_base( self, render, width, height, st, at, xpos, ypos,color):

            # Render the cannon base image
            cannon_base= renpy.render(Transform(self.CANNON_BASE_IMAGE[color]), width, height, st, at)
     
            # renpy.render returns a Render object, which we can
            # blit to the Render we're making
            render.blit(cannon_base, (xpos, ypos))


        # dessin de la bubble
        def draw_bubble( self, render, width, height, st, at, color, xpos, ypos):
            if(color.value<len(self.BUBBLE_IMAGES)):
                # Render the bubble image
                bubble = renpy.render(self.BUBBLE_IMAGES[color.value], width, height, st, at)
                    
                # renpy.render returns a Render object, which we can
                # blit to the Render we're making
                render.blit(bubble, (xpos, ypos))
        
        # This draws  buttons
        def draw_buttons(self, render, width, height, st, at):

            if self.direction_pushed==BubbleDirectionEnum.UP:
                image_to_draw = renpy.render( self.buttons_pushed[BubbleDirectionEnum.UP.value-1], width, height, st, at)
            else:
                image_to_draw = renpy.render( self.buttons_idle[BubbleDirectionEnum.UP.value-1], width, height, st, at)
            render.blit(image_to_draw, (self.SCREEN_WIDTH -  self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE *2, self.SCREEN_HEIGHT -  self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE*7))


            if self.direction_pushed==BubbleDirectionEnum.DOWN:
                image_to_draw = renpy.render( self.buttons_pushed[BubbleDirectionEnum.DOWN.value-1], width, height, st, at)
            else:
                image_to_draw = renpy.render( self.buttons_idle[BubbleDirectionEnum.DOWN.value-1], width, height, st, at)
            render.blit(image_to_draw, (self.SCREEN_WIDTH -  self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE*2 , self.SCREEN_HEIGHT -  self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE*4))


        def draw_target( self, render, width, height, st, at, xpos, ypos):
            # Render the target image
            target = renpy.render(self.TARGET_IMAGE, width, height, st, at)
                
            # renpy.render returns a Render object, which we can
            # blit to the Render we're making
            render.blit(target, (xpos, ypos))

        #affichage de la bubble lancee
        def draw_current_bubble(self,render, width, height, st, at, dtime):
                if not self.player_turn:
                    self.last_bubble_launch += dtime

                self.last_iteration_time += dtime
                
                #delay to launch ennemy bubble
                if self.last_bubble_launch >= self.BUBBLE_LAUNCH_DELAY and not self.player_turn:
                    self.last_bubble_launch -= self.BUBBLE_LAUNCH_DELAY
                    self.launch_bubble()

                
                # dessin de la bubble
                if  self.bubble_launched:
                    if self.last_iteration_time >= self.BUBBLE_TIME_DELAY:
                        self.last_iteration_time -= self.BUBBLE_TIME_DELAY
                        self.current_iteration=self.current_iteration+1

                        if self.current_iteration==self.iteration_number-1 or self.iteration_number==0:

                            renpy.sound.play(touch_sound)
                            self.bubble_launched=False
                            #ajoute (definitivement) la bubble à la liste des bubbles
                            self.add_bubble(self.target_row, self.target_col, self.current_bubble_color)
                            self.delete_bubbles_same_color(self.target_row, self.target_col, self.current_bubble_color)
                            
                            #alterne joueur et ennemi
                            self.player_turn=not self.player_turn

                            self.target_pos=None
                            self.target_row=None
                            self.target_col=None
                            self.current_bubble_color = random.choice([ColorEnum.RED,ColorEnum.GREEN,ColorEnum.BLUE,ColorEnum.PURPLE])    # Randomly choose a color for the bubble
           
                            if self.player_turn:  
                                self.compute_player_target_candidate_bubble_position()
                            else:
                                #(x,y)=position en haut à gauche du carré englobant la bubble
                                if self.last_launch_position==CannonPositionEnum.DOWN:
                                    #on lançait depuis la gauche, on lance depuis la droite
                                    self.launch_position=CannonPositionEnum.TOP
                                    self.launch_coords = self.LAUNCH_COORDS_TOP  # Start position of the bubble

                                else:
                                    #on lançait depuis la droite, on lance depuis la gauche
                                    self.launch_position=CannonPositionEnum.DOWN
                                    self.launch_coords = self.LAUNCH_COORDS_DOWN  # Start position of the bubble

                                  
                           
                            
                        else:
                            self.current_bubble_x= self.launch_coords[0] + (self.target_pos[0] - self.launch_coords[0]) * self.current_iteration / self.iteration_number  # Calculate x position
                            self.current_bubble_y = self.launch_coords[1] + (self.target_pos[1] - self.launch_coords[1]) * self.current_iteration / self.iteration_number  # Calculate y position

                    self.draw_bubble(render, width, height, st, at, self.current_bubble_color, self.current_bubble_x, self.current_bubble_y)
               
                   



        #affichage de toutes les bubbles
        def display_bubbles(self,render, width, height, st, at, dtime):
           
            draw_explode_step=False
            if self.last_explode_step >= self.EXPLODE_DELAY:
                    self.last_explode_step -= self.EXPLODE_DELAY
                    draw_explode_step=True
            for row in sorted(self.bubble_properties, key=lambda x: int(x)):
              
                for col in sorted(self.bubble_properties[row], key=lambda x: int(x)):
                    (x,y)=self.compute_target_candidate_bubble_position(row,col)
                    #(x,y)=position en haut à gauche du carré englobant la bubble
                    self.draw_bubble( render, width, height, st, at,  self.bubble_properties[row][col],
                    x,y         )
                    
                    if draw_explode_step:
                        if col in  self.bubble_properties[row] and self.bubble_properties[row][col].value+self.BUBBLE_COLOR_EXPLOSE >= len(self.BUBBLE_IMAGES):
                            #on supprime car on est arrivé à la fin des animations d'explosion
                            del self.bubble_properties[row][col]
                        if col in  self.bubble_properties[row] and self.bubble_properties[row][col].value>self.BUBBLE_COLOR_EXPLOSE:
                            #si couleur d'explosion, on passe à l'animation d'explosion suivante
                            self.bubble_properties[row][col]=ColorEnum(self.bubble_properties[row][col].value+self.BUBBLE_COLOR_EXPLOSE)
        
        def get_parents(self,row,col):
            if self.is_odd(row):
                return (col,col+1)
            else:
                return (col-1,col)

        def explode_orphans(self, row, col):
            #self.logger.debug(f'test explode {row} {col} ')
            if row!=1 and row in self.bubble_properties and col in self.bubble_properties[row] and self.bubble_properties[row][col].value<=self.BUBBLE_COLOR_EXPLOSE :
                #parents
                (col_parent_gauche,col_parent_droite)=self.get_parents(row,col)
    
                #au moins un parent présent et qui n'explose pas
                check_parent_exist=(row-1) in self.bubble_properties and\
                ((col_parent_gauche in self.bubble_properties[row-1] and self.bubble_properties[row-1][col_parent_gauche].value<=self.BUBBLE_COLOR_EXPLOSE) or\
                (col_parent_droite in self.bubble_properties[row-1] and self.bubble_properties[row-1][col_parent_droite].value<=self.BUBBLE_COLOR_EXPLOSE))
    
                #au moins un voisin présent et qui n'explose pas et qui a au moins un parent qui n'explose pas
                check_neighbour_left_exist= (col-1) in self.bubble_properties[row]  and\
                self.bubble_properties[row][col-1].value<=self.BUBBLE_COLOR_EXPLOSE and\
                (row-1) in self.bubble_properties and\
                (((col_parent_gauche-1) in self.bubble_properties[row-1] and self.bubble_properties[row-1][col_parent_gauche-1].value<=self.BUBBLE_COLOR_EXPLOSE) or\
                ((col_parent_droite-1) in self.bubble_properties[row-1] and self.bubble_properties[row-1][col_parent_droite-1].value<=self.BUBBLE_COLOR_EXPLOSE))
    
                check_neighbour_right_exist=(col+1) in self.bubble_properties[row]  and\
                self.bubble_properties[row][col+1].value<=self.BUBBLE_COLOR_EXPLOSE and\
                (row-1) in self.bubble_properties and\
                (((col_parent_gauche+1) in self.bubble_properties[row-1] and self.bubble_properties[row-1][col_parent_gauche+1].value<=self.BUBBLE_COLOR_EXPLOSE) or\
                ((col_parent_droite+1) in self.bubble_properties[row-1] and self.bubble_properties[row-1][col_parent_droite+1].value<=self.BUBBLE_COLOR_EXPLOSE))
    


               
                #self.logger.debug(f'{check_parent_exist} {check_neighbour_left_exist} {check_neighbour_right_exist}')
                #si orphelin
                if not (check_parent_exist or check_neighbour_left_exist or  check_neighbour_right_exist):
                    #self.logger.debug(f'-----explode cascade {row} {col} ')
                    self.explode(row,col,True)


        #affichage de la cible quand c'est au tour du joueur
        def display_target(self,render, width, height, st, at, dtime):  
            if self.target_pos is not None and self.player_turn:
                (x,y)=self.target_pos
                self.draw_target( render, width, height, st, at,x,y)
     
 
        def is_odd(self,line_number):
            return line_number % 2 != 0  # Check if the line number is odd
           
        #equation d'une droite passant par deux points
        def get_line_equation(self,launch_coords, target_pos):
            
            (x1, y1) = launch_coords
            (x2, y2) = target_pos
            
            a = (x2 - x1) / (y2 - y1)
            b = x1 - a * y1
            return (a,b)

        #distance a parcourir entre la position de depart et la cible
        def compute_distance_to_target(self):
            return ((self.target_pos[0] - self.launch_coords[0]) ** 2 + (self.target_pos[1] - self.launch_coords[1]) ** 2) ** 0.5


        def compute_distance_bubble_moves_each_delay(self):
            max_distance = (((self.SCREEN_HEIGHT - self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE/2) - (self.BORDER_WIDTH + self.BUBBLE_IMAGE_SIZE/2)) ** 2 + (
                    (self.SCREEN_WIDTH - self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE/2) - (self.BORDER_WIDTH + self.BUBBLE_IMAGE_SIZE/2.)) ** 2) ** 0.5
            
            return self.BUBBLE_TIME_DELAY * max_distance / self.MAX_TIME


        def identify_bubble_to_target(self):
            
            self.target_row =None
            self.target_col=None
            self.target_pos=None
            #parcours des lignes en commençant par le haut, on évite la dernière (pour ne pas perdre)
            
            for row in range(1,self.MAX_LINE_NUMBER):
                
                #si on est dans ce cas, on n'a pas de cas optimal : on sera à côté d'une bubble de même couleur
                #on prend le dernier
                if((row-1) not in self.bubble_properties and row!=1):
                    continue
                else:
                    
                    #parcours des colonnes, on fait attention à la couleur des voisins
                    self.iterate_col_to_find_candidate(row,False)
              

            if self.target_row is None:
                #candidat par défaut
                
                self.identify_bubble_to_target_ignore_color()
            

        #pas le choix : on aura un voisin de meme couleur
        def identify_bubble_to_target_ignore_color(self):
            #parcours des lignes en ignorant la couleur et en acceptant la dernière ligne
            for row in range(1,self.MAX_LINE_NUMBER+1):
                
                if((row-1) not in self.bubble_properties and row!=1):
                    continue
                else:
                    #on ignore la couleur
                    self.iterate_col_to_find_candidate(row,True)
            

        def iterate_col_to_find_candidate(self,row,ignore_color):
            #parcours des colonnes : si on lance à gauche, on lance vers la gauche
            #si on lance à droite, on lance vers la droite
            
            if(self.launch_position==CannonPositionEnum.DOWN):
                #on ne parcourt que la moitié des lignes (sinon risque d'intersection)
                for col in range(int(self.MAX_LINE_SIZE/2),0,-1):
                    
                    self.find_candidate(row,col,self.current_bubble_color,ignore_color)
            else:
                for col in range(int(self.MAX_LINE_SIZE/2)+1,self.MAX_LINE_SIZE+1):
                    
                    self.find_candidate(row,col,self.current_bubble_color,ignore_color)
            

        def first_checks_for_candidate(self,row,col,color,ignore_color):            
            #candidat si :
            #  pas encore de ligne ou 
            #( pas de bubble a la position et (pas de voisin gauche ou couleur voisin gauche != couleur)
            # et (pas de voisin droite ou couleur voisin droite != couleur))
            # et pas de voisin en train d'exploser
            verification_ligne_courante_ok = row not in self.bubble_properties or\
            ( col not in self.bubble_properties[row] \
            and ((col-1) not in self.bubble_properties[row] or ((ignore_color or self.bubble_properties[row][col-1] != color) and self.bubble_properties[row][col-1].value<5)) \
            and ((col+1) not in self.bubble_properties[row] or ((ignore_color or  self.bubble_properties[row][col+1] != color) and self.bubble_properties[row][col+1].value<5)))
            # MAX_LINE_SIZE uniquement pour les lignes paires (not odd)
            verification_derniere_colonne_ok=(col != self.MAX_LINE_SIZE or not self.is_odd(row))
            # et ligne 1 ou ((au moins un parent) et (pas de parent gauche ou couleur parent gauche != couleur) et (pas de parent droite ou couleur parent droite != couleur))
            # ligne 1 :   1 2 3 4
            # ligne 2 :    1 2 3 4
            # ligne 3 :   1 2 3 4
            (col_parent_gauche,col_parent_droite)=self.get_parents(row,col)
 
            
            verification_ligne_dessus_ok =  row==1  or ( \
            not((col_parent_gauche) not in self.bubble_properties[row-1] and (col_parent_droite) not in self.bubble_properties[row-1])\
            and  ((col_parent_gauche) not in self.bubble_properties[row-1] or ignore_color or self.bubble_properties[row-1][col_parent_gauche] != color)\
            and ((col_parent_droite) not in self.bubble_properties[row-1] or ignore_color or self.bubble_properties[row-1][col_parent_droite] != color)\
            )

            return verification_ligne_courante_ok and verification_derniere_colonne_ok and verification_ligne_dessus_ok
        
        def find_candidate(self,row,col,color,ignore_color):
            
            if self.first_checks_for_candidate(row,col,color,ignore_color) :
                
                candidate_position=self.compute_target_candidate_bubble_position(row,col)
                (x,y)=candidate_position
                
                #on a un candidat, mais il ne faut pas que le trajet vers ce candidat
                #intersecte une bubble deja en place
                #equation de la droite passant par les deux points
                # on enlève le self.BUBBLE_IMAGE_SIZE pour avoir la position "haute" des bubbles, qui peuvent intersectées
                if not self.iterate_to_check_if_intersection(self.launch_coords, candidate_position,row,col):
                    #c'est une bubble lancée par l'IA qui touche la ligne rouge ==> c'est gagné!
                    if row==self.MAX_LINE_NUMBER:
                        self.end_game=True
                        self.victory=True
                        renpy.music.stop()
                        renpy.sound.play(win_sound)
                        self.information_text=_("GAGNÉ !\nAppuyez sur Entrée ou Clic gauche.")

                    #on privilegie près du centre, pour embêter le joueur
                    if (self.wait_for_start and self.target_row is None) or (not self.wait_for_start and ( self.target_row is None or  math.fabs(col-self.MAX_LINE_SIZE/2)<math.fabs(self.target_col-self.MAX_LINE_SIZE/2))):
                        
                        self.target_row=row
                        self.target_col=col
            

        def iterate_to_check_if_intersection(self,launch_coords, target_pos,target_row,target_col):
            (x1, y1) = launch_coords
            (x2, y2) = target_pos
            if  (y1 != y2):
                #calcul de l'équation de la droite
                #on prend le milieu de la bubble
                # dans le cadre qui a (x,y)=coin en haut à gauche
 
                (a,b)=self.get_line_equation((x1+self.BUBBLE_IMAGE_SIZE/2,y1+self.BUBBLE_IMAGE_SIZE/2),(x2+self.BUBBLE_IMAGE_SIZE/2,y2+self.BUBBLE_IMAGE_SIZE/2) )
                
                angle = self.get_angle(launch_coords,target_pos)
                #calcul du delta de y (on veut les deux équations qui couvrent toute la trajectoire de la bubble)
                tolerance=10
                distance=(self.BUBBLE_REAL_SIZE-tolerance)/(math.sin(math.radians(math.fabs(angle)))) 
                bmin=b-distance/2
                bmax=b+distance/2

            
                
                #parcours des lignes en partant du bas, on ignore la ligne où est la cible
                for row in range(max(self.bubble_properties.keys()),target_row,-1):
                    if self.launch_position==CannonPositionEnum.DOWN:
                        
                        #on ne parcourt que la moitié des lignes 
                        for col in range(target_col,0,-1):
                            intersection= col in self.bubble_properties[row] 
                            if  intersection is True:
                                
                                return True
                    elif self.launch_position==CannonPositionEnum.TOP:
                        for col in range(target_col,self.MAX_LINE_SIZE+1):
                            intersection= col in self.bubble_properties[row] and self.check_if_intersection(a,bmin,bmax,row,col)
                            if  intersection is True:
                                
                                return True 
                    else:
                        for col in range(1,self.MAX_LINE_SIZE+1):
                            intersection= col in self.bubble_properties[row] and self.check_if_intersection(a,bmin,bmax,row,col)
                            if  intersection is True:
                                
                                return True 
                return False
            else:
                #cas où les deux points sur la même ligne : on regarde s'il y a des élements sur la même colonne en dessous
                for row in range(max(self.bubble_properties.keys()),target_row,-1):
                    if row in self.bubble_properties and target_col in self.bubble_properties[row]:
                        return True
                return False

        def check_if_intersection(self,a,bmin,bmax,row,col):
            
            #calcule la position de la bubble qui pourrait intersecter
            (x,y)=self.compute_target_candidate_bubble_position(row,col)
            
            #calcule la position théorique de la bubble lancée (équation de la droite)
            #on prend y+RAYON pour correspond au point inférieur de la bubble

            #difference entre la taille de l'image et la taille exacte de la bubble

            #ici on cherche à trouver l'écart "vide" entre le bord gauche de la cellule
            #et le bout gauche de la bubble
            diff_size=int((self.BUBBLE_IMAGE_SIZE-self.BUBBLE_REAL_SIZE)/2)
            
            for i in range(int(y)+diff_size,int(y)+self.BUBBLE_REAL_SIZE):

                x_bubble_lancee=a*i+bmin
                #si on est à moins de distance que le rayon (<=> on est dans le cercle)
                if self.compute_distance(x+self.BUBBLE_IMAGE_SIZE/2,y+self.BUBBLE_IMAGE_SIZE/2,x_bubble_lancee,i)<self.BUBBLE_REAL_SIZE/2:
                    return True

                x_bubble_lancee=a*i+bmax
                if self.compute_distance(x+self.BUBBLE_IMAGE_SIZE/2,y+self.BUBBLE_IMAGE_SIZE/2,x_bubble_lancee,i)<self.BUBBLE_REAL_SIZE/2:
                    return True

            return False
           
    
        def compute_distance(self,x1,y1,x2,y2):
            return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

        #calcule de la position (x,y) de la bubble
        def compute_target_candidate_bubble_position(self,row,col):
            
            increment = 0
            if self.is_odd(row):
                increment = 1
            return (
                    self.BORDER_WIDTH + (row-1) * self.BUBBLE_IMAGE_SIZE ,
                    self.SCREEN_HEIGHT - (self.BORDER_WIDTH + col  * self.BUBBLE_IMAGE_SIZE  + increment * self.BUBBLE_IMAGE_SIZE/2)
                    )
            
            
        #supprime les bubbles de même couleur (s'il y en a)
        def delete_bubbles_same_color(self,row,col,color):
            (col_parent_gauche,col_parent_droite)=self.get_parents(row,col)

            #voisins meme ligne
            deleted=self.delete_bubble_same_color(row,col-1,color)
            deleted=self.delete_bubble_same_color(row,col+1,color) or deleted
            #voisins du dessus
            deleted= self.delete_bubble_same_color(row-1,col_parent_gauche,color)  or deleted
            deleted= self.delete_bubble_same_color(row-1,col_parent_droite,color)  or deleted
            #voisins du dessous
            deleted= self.delete_bubble_same_color(row+1,col_parent_gauche,color)  or deleted
            deleted= self.delete_bubble_same_color(row+1,col_parent_droite,color) or deleted

            if deleted:
                #au moins un voisin de meme couleur
                #on supprime aussi la bubble en paramètre
                #couleur d'explosion
                if not self.wait_for_start:
                    renpy.sound.play(explode_sound)
                self.explode(row,col,False)

        #suppression de la bulle si elle a la couleur en paramètre
        def delete_bubble_same_color(self,row,col,color):
            if row in self.bubble_properties and col in self.bubble_properties[row]:
                if self.bubble_properties[row][col]==color:
                    self.explode(row,col,False)
                    return True
                #on touche la bulle doree
                if self.bubble_properties[row][col]==ColorEnum.GOLDEN and self.player_turn:
                    self.end_game=True
                    self.victory=True
                    renpy.music.stop()
                    renpy.sound.play(win_sound)
                    self.information_text=_("GAGNÉ !\nAppuyez sur Entrée ou Clic gauche.")
            return False

        #initalisation d'une explosion (sauf si init => pas d'animation)
        def explode(self,row,col,orphan):
            #self.logger.debug(f'explode {row} {col} ')
            #couleur d'explosion
            if not self.init:
                if row in self.bubble_properties and col in self.bubble_properties[row]:
                    if orphan:#delai supplementaire pour exploser
                        self.bubble_properties[row][col]=ColorEnum(self.bubble_properties[row][col].value+self.BUBBLE_COLOR_EXPLOSE)
                    else:
                        self.bubble_properties[row][col]=ColorEnum(self.bubble_properties[row][col].value+self.BUBBLE_COLOR_EXPLOSE_NOT_ORPHAN)

            else:
                if row in self.bubble_properties and col in self.bubble_properties[row]:
                    del self.bubble_properties[row][col]
            
            (col_parent_gauche,col_parent_droite)=self.get_parents(row,col)
            #explose les voisins s'ils sont orphelins
            self.explode_orphans(row-1, col_parent_gauche)
            self.explode_orphans(row-1, col_parent_droite)
            self.explode_orphans(row+1, col_parent_gauche)
            self.explode_orphans(row+1, col_parent_droite)
            self.explode_orphans(row, col-1)
            self.explode_orphans(row, col+1)
            
            



        def dessiner_trajectoire(self, render, width, height, st, at):
            """
            Dessine la ligne de trajectoire basée sur l'angle actuel du canon
            Le canon pointe vers le haut quand angle = 0
            """
            if self.player_turn and not self.bubble_launched and not self.end_game and not self.wait_for_start:
                line_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                
                x1, y1 = self.LAUNCH_COORDS_MIDDLE
                angle = self.angles[CannonPositionEnum.MIDDLE.value]
                
                x1_center = x1 + self.BUBBLE_IMAGE_SIZE/2
                y1_center = y1 + self.BUBBLE_IMAGE_SIZE/2
                
                # Pour un angle de 0, la ligne est verticale
                if angle == 0:
                    # Créer une surface compatible Ren'Py pour la ligne
                    line_render = renpy.Render(width, height)
                    # Dessiner une ligne du point de départ jusqu'au haut 
                    pygame.draw.line(line_surface, (255, 0, 0, 128), 
                            (x1_center, y1_center),
                            (self.BORDER_WIDTH,y1_center), 2)
                    render.blit(pygame.Surface.subsurface(line_surface, (0, 0, width, height)), (0, 0))

                    return
                    
                # Pour les autres angles
                angle_radians = math.radians(angle)
                
                # Calcul de la pente
                a = 1/math.tan(angle_radians)
                
                # Calcul de b
                b = x1_center - a * y1_center
                
                # Calcul des intersections
                target_x = 0
                target_y =  -b/a
                
               
                    
                # Dessiner la ligne avec la méthode de Ren'Py
                pygame.draw.line(line_surface, (255, 0, 0, 128),
                        (x1_center, y1_center),
                        (target_x, target_y), 2)
                render.blit(pygame.Surface.subsurface(line_surface, (0, 0, width, height)), (0, 0))


        def launch_bubble(self):
            if not self.end_game:


                if not self.player_turn:
                    self.init_ennemy_launch()

                self.current_bubble_x = self.target_pos[0]   # Calculate x position
                self.current_bubble_y = self.target_pos[1] 
                

                distance_to_target = self.compute_distance_to_target()
                self.bubble_launched=True
                
                self.iteration_number = math.trunc(distance_to_target / self.DISTANCE_BUBBLE_MOVES_EACH_DELAY)
                self.last_iteration_time=0
                self.current_iteration=0
                self.current_bubble_x = self.launch_coords[0]   # Calculate x position
                self.current_bubble_y = self.launch_coords[1]   # Calculate y position

                renpy.sound.play(shoot_sound)


        def get_angle(self,launch_coords, target_pos):
            (x1, y1) = launch_coords
            (x2, y2) = target_pos
            if y2==y1:
                return 0
            else:
                return math.degrees(math.atan(math.fabs(y2 - y1) / math.fabs(x2 - x1) ))   
         
        def init_ennemy_launch(self):

            #pour alterner les canons ennemis
            self.last_launch_position=self.launch_position

           
            self.identify_bubble_to_target()  # Find target position for the bubble
            self.target_pos=self.compute_target_candidate_bubble_position(self.target_row,self.target_col)
            angle = self.get_angle(self.launch_coords,self.target_pos)
            if self.launch_position==CannonPositionEnum.TOP:
                angle=-angle
            
            self.angles[self.launch_position.value]=angle
            

        def check_parents(self,row,col):
            #les colonnes des parents sont differentes si les lignes sont paires ou impaires
            (col_parent_gauche,col_parent_droite)=self.get_parents(row,col)
 
            #premiere ligne ou au moins un parent
            return  row==1  or\
            (col_parent_gauche in self.bubble_properties[row-1]) or  (col_parent_droite  in self.bubble_properties[row-1])
        

        def check_target(self, row, col):
           
            if (row in self.bubble_properties and col  in self.bubble_properties[row] ):
                if self.target_pos is not None and self.target_row<row:
                    self.target_pos=None
                    self.target_row=None
                    self.target_col=None
            else:
                
                if self.check_parents(row,col) and self.target_pos is None:
                    candidate_position=self.compute_target_candidate_bubble_position(row,col)
                    
                    if not self.iterate_to_check_if_intersection(self.launch_coords, candidate_position,row,col):
                        self.target_row=row
                        self.target_col=col
                        self.target_pos=candidate_position

        #calcule de la position cible de la bubble visée par le joueur
        def compute_player_target_candidate_bubble_position(self):
            self.launch_coords=self.LAUNCH_COORDS_MIDDLE
            self.launch_position=CannonPositionEnum.MIDDLE
            self.target_pos=None
            angle = self.angles[CannonPositionEnum.MIDDLE.value]

            x1, y1 = self.LAUNCH_COORDS_MIDDLE
            angle = self.angles[CannonPositionEnum.MIDDLE.value]
                
            x1_center = x1 + self.BUBBLE_IMAGE_SIZE/2
            y1_center = y1 + self.BUBBLE_IMAGE_SIZE/2

           
            if angle != 0:
                # Pour les autres angles
                angle_radians = math.radians(angle)
                    
                # Calcul de la pente
                a = 1/math.tan(angle_radians)
                    
                # Calcul de b
                b = x1_center - a * y1_center

                tolerance=10
                distance=(self.BUBBLE_REAL_SIZE-tolerance)/(math.cos(math.radians(math.fabs(angle)))) 
                bmin=b-distance/2
                bmax=b+distance/2

            for row in range(1,self.MAX_LINE_NUMBER+1):


                #on a parcouru toutes les lignes
                if((row-1) not in self.bubble_properties and row!=1):
                    continue        
                    
                for col in range(1,self.MAX_LINE_SIZE+1):
                    # candidat si intersecte
                    if angle==0:
                        
                        if ((row%2==1) and col==self.MAX_LINE_SIZE/2) or ((row%2==0)\
                        and (col==self.MAX_LINE_SIZE/2 or col==self.MAX_LINE_SIZE/2+1)) :
                            self.check_target(row,col)

                    else:
                        #pas de place 18 pour les lignes impaires
                        if (row%2==1) and col==self.MAX_LINE_SIZE:
                            continue
                        #position de la droite
                        (x,y)=self.compute_target_candidate_bubble_position(row,col)
                        
                        
                        #ici on cherche à trouver l'écart "vide" entre le bord gauche de la cellule
                        #et le bout gauche de la bubble
                        diff_size=int((self.BUBBLE_IMAGE_SIZE-self.BUBBLE_REAL_SIZE)/2)
                        
                        for i in range(int(y)+diff_size,int(y)+self.BUBBLE_REAL_SIZE):

                            x_trajectoire=a*i+b
                            #si on est à moins de distance que le rayon (<=> on est dans le cercle)
                            if self.compute_distance(x+self.BUBBLE_IMAGE_SIZE/2,y+self.BUBBLE_IMAGE_SIZE/2,x_trajectoire,i)<self.BUBBLE_REAL_SIZE/2:
                                
                                self.check_target(row,col)
                                continue
            
                #si pas de cible trouvee, on autorise plus d'ecart par rapport a la trajectoire
                #on regarde tout simplement si la trajectoire traverse une case
                if self.target_pos is None and angle!=0:
                    for col in range(1,self.MAX_LINE_SIZE+1):
                        if (row%2==1) and col==self.MAX_LINE_SIZE:
                            continue
                        #position de la droite
                        (x,y)=self.compute_target_candidate_bubble_position(row,col)
                        for i in range(int(y),int(y)+self.BUBBLE_IMAGE_SIZE): 
                            x_trajectoire=a*i+b
                            if x_trajectoire>x and x_trajectoire<x+self.BUBBLE_IMAGE_SIZE:
                                
                                self.check_target(row,col)
                                continue







        # Draws the screen
        def render(self, width, height, st, at):

            # The Render object we'll be drawing into.
            render = renpy.Render(width, height)


            # Figure out the time elapsed since the previous frame.
            if self.last_frame_rendering is None:
                self.last_frame_rendering = st
            dtime = st - self.last_frame_rendering
            self.last_frame_rendering = st


            if not self.end_game:
                #iteration d'explostion
                self.last_explode_step += dtime
                self.start_cannon_move += dtime 

                #mouvements du canon
                if self.start_cannon_move >= self.CANNON_MOVE_DURATION and self.cannon_moving:
                    self.start_cannon_move -= self.start_cannon_move
                    self.cannon_moving=False
                    #boutons de direction
                    if self.direction_pushed == BubbleDirectionEnum.DOWN or self.cannon_next_direction == BubbleDirectionEnum.DOWN:
                        self.initial_cannon_move(-self.ANGLE_STEP)
                    if self.direction_pushed == BubbleDirectionEnum.UP or self.cannon_next_direction == BubbleDirectionEnum.UP:
                        self.initial_cannon_move(self.ANGLE_STEP)
                    self.cannon_next_direction=None



            # Dessiner la trajectoire avant les bulles
            

            self.draw_current_bubble(render, width, height, st, at,dtime)

            # Display all bubbles
            self.display_bubbles(render, width, height, st, at,dtime)

            #display target
            self.display_target(render, width, height, st, at,dtime)

    
            #socles des canons

            color=0
            if self.launch_position is not None and self.launch_position==CannonPositionEnum.DOWN  and self.launch_coords is not None and self.current_bubble_color is not None:
                color=self.current_bubble_color.value
            self.draw_cannon_base(render, width, height, st, at,width-self.BORDER_WIDTH-self.CANNON_BASE_WIDTH,height-self.BORDER_WIDTH-self.CANNON_BASE_WIDTH,color)
            self.draw_cannon(render, width, height, st, at,width-260,height-250,self.angles[0],color)

            color=0
            if self.launch_position is not None and self.launch_position==CannonPositionEnum.TOP  and self.launch_coords is not None and self.current_bubble_color is not None:
                color=self.current_bubble_color.value
            self.draw_cannon_base(render, width, height, st, at,width-self.BORDER_WIDTH-self.CANNON_BASE_WIDTH,self.BORDER_WIDTH,color)
            self.draw_cannon(render, width, height, st, at,width-260,-90,self.angles[1],color)

            color=0
            if self.launch_position is not None and self.launch_position==CannonPositionEnum.MIDDLE  and self.launch_coords is not None and self.current_bubble_color is not None:
                color=self.current_bubble_color.value
            self.draw_cannon_base(render, width, height, st, at,width-self.BORDER_WIDTH-self.CANNON_BASE_WIDTH,self.BORDER_WIDTH+self.BUBBLE_IMAGE_SIZE*4,color)
            self.draw_cannon(render, width, height, st, at,width-260,height/2-170,self.angles[2],color)
                

            #self.dessiner_trajectoire(render, width, height, st, at)

            if self.should_draw_buttons:
                #draw the buttons
                self.draw_buttons(render, width, height, st, at)
          
            # redraw the screen
            renpy.redraw(self, 0)

            # Return the Render object.
            return render

        #calcul de l'angle exact vers la cible (qui peut être légèrement différent de l'angle du canon)
        def compute_exact_angle(self):
            #calcul de l'angle exact vers la cible
            angle_exact = self.get_angle(self.launch_coords,self.target_pos)
            (x_launch,y_launch)=self.launch_coords
            (x_target,y_target)=self.target_pos
            if y_target>y_launch:
                angle_exact=-angle_exact
            self.angles[self.launch_position.value]=angle_exact

        # Handles events to move player
        def event(self, ev, x, y, st):

            #quit
            if  ev.type == pygame.KEYDOWN  and ev.key == pygame.K_ESCAPE :
                self.show_next_screen()
                raise renpy.IgnoreEvent()

            if  ((ev.type == pygame.KEYDOWN  and ev.key == pygame.K_RETURN)or(ev.type == pygame.MOUSEBUTTONUP and ev.button == 1)) and (self.end_game or self.wait_for_start):
                if self.victory==True:
                    self.show_next_screen()
                if self.end_game:
                    self.show_game_screen()
                if self.wait_for_start:
                    #top à la vachette !
                    self.information_text=""
                    self.wait_for_start=False

                raise renpy.IgnoreEvent() 


            # canon moves right
            if not self.end_game  and not self.wait_for_start and ev.type == pygame.KEYDOWN and ev.key == pygame.K_UP and self.player_turn:
                if not self.cannon_moving:
                    self.should_draw_buttons=False
                    self.initial_cannon_move(self.ANGLE_STEP)
                else:
                    self.cannon_next_direction=BubbleDirectionEnum.UP
                raise renpy.IgnoreEvent()


            # player moves left
            if not self.end_game and not self.wait_for_start  and ev.type == pygame.KEYDOWN and ev.key == pygame.K_DOWN and self.player_turn:
                if not self.cannon_moving:
                    self.should_draw_buttons=False
                    self.initial_cannon_move(-self.ANGLE_STEP) 
                else:
                    self.cannon_next_direction=BubbleDirectionEnum.DOWN
                raise renpy.IgnoreEvent()


            # player shoots
            if not self.end_game and not self.bubble_launched and self.target_pos and not self.wait_for_start and ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE and self.player_turn:
                if self.target_row==self.MAX_LINE_NUMBER:
                    self.game_over()
                    return
                self.should_draw_buttons=False
                self.compute_exact_angle()
                self.launch_bubble()  
                raise renpy.IgnoreEvent()

            if not self.end_game and not self.wait_for_start and self.player_turn and ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:  # Left mouse button
                    # Get the mouse position when clicked
                    # we use renpy function instead of pygame fuction because we
                    # want the virtual position (virtual width=1280,virtual height=720)
                    mouse_x, mouse_y = renpy.get_mouse_pos()
                    

                    if   self.should_draw_buttons and mouse_x > self.SCREEN_WIDTH -  self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE*2  \
                    and mouse_x < self.SCREEN_WIDTH -  self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE  \
                    and mouse_y > self.SCREEN_HEIGHT -  self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE*7 \
                    and mouse_y < self.SCREEN_HEIGHT -  self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE*6: 

                        self.direction_pushed=BubbleDirectionEnum.UP
                        self.initial_cannon_move(self.ANGLE_STEP) 

                    elif   self.should_draw_buttons and mouse_x > self.SCREEN_WIDTH -  self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE*2  \
                    and mouse_x < self.SCREEN_WIDTH -  self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE  \
                    and mouse_y > self.SCREEN_HEIGHT -  self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE*4 \
                    and mouse_y < self.SCREEN_HEIGHT -  self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE*3 : 

                        self.direction_pushed=BubbleDirectionEnum.DOWN
                        self.initial_cannon_move(-self.ANGLE_STEP) 

                raise renpy.IgnoreEvent()

            if ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:  # Left mouse button releade
                    # si on n'a pas cliqué sur un bouton de direction : on lance la bubble
                    if self.direction_pushed is None:
                        if not self.bubble_launched and not self.wait_for_start and self.target_pos:
                            if self.target_row==self.MAX_LINE_NUMBER:
                                self.game_over()
                                return
                            self.compute_exact_angle()
                            self.launch_bubble() 
                    else:
                        self.direction_pushed=None
                raise renpy.IgnoreEvent()


            # Ensure the screen updates
            renpy.restart_interaction()
            raise renpy.IgnoreEvent()  


                # show screen after game (home screen or next screen of history)
        def show_next_screen(self):
            self.__init__()
            renpy.jump("after_bubble_shooter_game")  

                            # show screen after game (home screen or next screen of history)
        def show_game_screen(self):
            self.__init__()
            renpy.jump("start_bubble_shooter_game")  

    def display_end_bubble_shooter_game_text(st, at):
        return Text( bubble_shooter_game.information_text, font='gui/jd_code.ttf', size=50, color="#77d079"), .1 

    def display_end_bubble_shooter_game_background(st, at):
        if bubble_shooter_game.end_game or bubble_shooter_game.wait_for_start:
            return Image("images/bubble_shooter_game/mini_game_end_background.png"), 30
        else :
            return Null(width=0), .1

default bubble_shooter_game = BubbleShooterGameDisplayable()

# label to start snake game
label start_bubble_shooter_game:
    stop sound
    stop music
    play music bubble_shooter_game_music
    window hide  # Hide the window and quick menu while in mini game
    call screen bubble_shooter_game


label after_bubble_shooter_game:
    stop music
    window auto  
    call screen mini_games


#start bubble shooter game 
screen bubble_shooter_game():
    add "images/bubble_shooter_game/background_bubble_shooter.png"
    add bubble_shooter_game
    add DynamicDisplayable(display_end_bubble_shooter_game_background) 
    add DynamicDisplayable(display_end_bubble_shooter_game_text) xalign 0.5 yalign 0.5 
    imagebutton:
        # image GM
        idle "gui/overlay/menu_button_idle.png"
        hover "gui/overlay/menu_button_hover.png"
        
        # Position du bouton
        xalign 0.99
        yalign 0.01
        
        # Action à réaliser lors du clic
        action Function(snake_game.show_next_screen)



