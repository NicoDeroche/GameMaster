init python:

    import random
    from enum import Enum
    import pygame
    import time
    import math
    import logging



    class CannonDirectionEnum(Enum):
        LEFT = 1
        RIGHT = 2


    class CannonPositionEnum(Enum):
        LEFT = 0
        RIGHT = 1
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

            #angle de rotation à chaque fois qu'on appuie sur gauche ou droite
            self.ANGLE_STEP=5
            #angle maximum du distance
            self.MAX_ANGLE=75
            self.cannon_moving=False
            self.start_cannon_move=0
            self.CANNON_MOVE_DURATION=0.1

            #les images 
            self.BUBBLE_IMAGES = [Image("images/bubble_shooter_game/golden_bubble.png"),
            Image("images/bubble_shooter_game/red_bubble.png"),Image("images/bubble_shooter_game/green_bubble.png"),Image("images/bubble_shooter_game/blue_bubble.png"),Image("images/bubble_shooter_game/purple_bubble.png")
            ,Image("images/bubble_shooter_game/red_bubble_2.png"),Image("images/bubble_shooter_game/green_bubble_2.png"),Image("images/bubble_shooter_game/blue_bubble_2.png"),Image("images/bubble_shooter_game/purple_bubble_2.png")        
            ,Image("images/bubble_shooter_game/red_bubble_3.png"),Image("images/bubble_shooter_game/green_bubble_3.png"),Image("images/bubble_shooter_game/blue_bubble_3.png"),Image("images/bubble_shooter_game/purple_bubble_3.png")        
            ,Image("images/bubble_shooter_game/red_bubble_4.png"),Image("images/bubble_shooter_game/green_bubble_3.png"),Image("images/bubble_shooter_game/blue_bubble_4.png"),Image("images/bubble_shooter_game/purple_bubble_4.png")          
            ]
            self.CANNON_BASE_IMAGE=Image("images/bubble_shooter_game/socle_canon.png")
            self.CANNON_BASE_MIDDLE_IMAGE=Image("images/bubble_shooter_game/socle_canon_milieu.png")
            self.CANNON_IMAGE=Image("images/bubble_shooter_game/canon.png")
            self.bubble_properties = dict()  # Map to store properties of the bubbles

            #au joueur de jouer
            self.player_turn=False
     
            self.SCREEN_HEIGHT= 720  
            self.SCREEN_WIDTH = 1280
            self.CANNON_BASE_WIDTH=120
            #ligne paire = 17 bubbles, ligne impaire = 18 bubbles
            self.MAX_LINE_SIZE = int(( self.SCREEN_WIDTH-self.BORDER_WIDTH*2)/(self.BUBBLE_IMAGE_SIZE))
            self.MAX_LINE_NUMBER = int(( self.SCREEN_HEIGHT-self.BORDER_WIDTH*2 - self.BUBBLE_IMAGE_SIZE*2)/(self.BUBBLE_IMAGE_SIZE))
            self.LAUNCH_COORDS_LEFT=(self.BORDER_WIDTH,
                        self.SCREEN_HEIGHT- self.BORDER_WIDTH-self.BUBBLE_IMAGE_SIZE)
            self.LAUNCH_COORDS_RIGHT=  (self.SCREEN_WIDTH - self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE,
                        self.SCREEN_HEIGHT- self.BORDER_WIDTH-self.BUBBLE_IMAGE_SIZE)
            self.LAUNCH_COORDS_MIDDLE =   (self.SCREEN_WIDTH/2 - self.BUBBLE_IMAGE_SIZE,
                        self.SCREEN_HEIGHT- self.BORDER_WIDTH-self.BUBBLE_IMAGE_SIZE)

            #liste des angles des canons
            self.angles=[0,0,0]

            #self.last_bubble_launch=0
            #temps entre les lancements des bubbles
            #self.BUBBLE_LAUNCH_DELAY=2
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
            self.launch_position=None
            self.last_launch_position=CannonPositionEnum.RIGHT
            self.current_bubble_color = None
            self.current_iteration= None
            self.current_bubble_x = None
            self.current_bubble_y = None
            self.launch_coords=None
            self.target_pos=None
            self.bubble_launched=False
            self.target_col=None
            self.target_row=None

            self.end_game=False
            self.wait_for_start=True
            self.victory=False

            self.DISTANCE_BUBBLE_MOVES_EACH_DELAY=self.compute_distance_bubble_moves_each_delay()
    
            self.information_text=_("Attention, ça va commencer !\n\nVous gagnez si :\n- vous touchez la balle orange\n- ou si votre adversaire touche la ligne rouge.\nVous perdez si vous touchez la ligne rouge.\nUtilisez les flèches de direction pour vous déplacer.\nAppuyez sur Espace pour tirer.\n\nAppuyez sur Entrée ou Clic Gauche pour lancer le jeu.")

            #couleur speciale pour une bubble
            self.add_bubble(1,self.MAX_LINE_SIZE/2, ColorEnum.GOLDEN) 
            #initialisation des 50 premières bubbles
            for i in range(50):
                self.init_ennemy_launch()
                self.add_bubble(self.target_row, self.target_col, self.current_bubble_color)
                #suppression des éventuelles bubbles voisines de même couleur
                self.delete_bubbles_same_color(self.target_row, self.target_col, self.current_bubble_color)
            self.init=False
            #on reinitialise les canons (canon gauche, droite, milieu)
            self.angles=[45,-45,0]  
            #c'est au tour du joueur
            self.player_turn=True
            


        def initial_cannon_move(self,angle):
            self.cannon_moving=True
            self.angles[CannonPositionEnum.MIDDLE.value]+=angle
            #on a une limitation d'angle
            if self.angles[CannonPositionEnum.MIDDLE.value]<-self.MAX_ANGLE:
                self.angles[CannonPositionEnum.MIDDLE.value]=-self.MAX_ANGLE
            if self.angles[CannonPositionEnum.MIDDLE.value]>self.MAX_ANGLE:
                self.angles[CannonPositionEnum.MIDDLE.value]=self.MAX_ANGLE
            renpy.redraw(self, 0)



        #construction d'une bubble
        def add_bubble(self,row, col, color):
            if row not in self.bubble_properties:
                self.bubble_properties[row] = dict()  # Store bubble properties
            self.bubble_properties[row][col] = color  # Set color for the bubble at specific row and column


        #draw cannon
        def draw_cannon( self, render, width, height, st, at, xpos, ypos,angle):
            # Render the cannon  image
            cannon= renpy.render(Transform(self.CANNON_IMAGE,rotate=angle), width, height, st, at)
            # renpy.render returns a Render object, which we can
            # blit to the Render we're making
            render.blit(cannon, (xpos, ypos))


            
            


        # dessin du socle du canon
        def draw_cannon_base( self, render, width, height, st, at, xpos, ypos,zoom):

            # Render the cannon base image
            cannon_base= renpy.render(Transform(self.CANNON_BASE_IMAGE,xzoom=zoom), width, height, st, at)
     
            # renpy.render returns a Render object, which we can
            # blit to the Render we're making
            render.blit(cannon_base, (xpos, ypos))

        # dessin du socle du canon du milieu
        def draw_cannon_base_middle( self, render, width, height, st, at, xpos, ypos):

            # Render the cannon base image
            cannon_base_middle= renpy.render(self.CANNON_BASE_MIDDLE_IMAGE, width, height, st, at)
     
            # renpy.render returns a Render object, which we can
            # blit to the Render we're making
            render.blit(cannon_base_middle, (xpos, ypos))

        # dessin de la bubble
        def draw_bubble( self, render, width, height, st, at, color, xpos, ypos):
            if(color.value<len(self.BUBBLE_IMAGES)):
                # Render the bubble image
                bubble = renpy.render(self.BUBBLE_IMAGES[color.value], width, height, st, at)
                    
                # renpy.render returns a Render object, which we can
                # blit to the Render we're making
                render.blit(bubble, (xpos, ypos))

        #affichage de la bubble lancee
        def draw_current_bubble(self,render, width, height, st, at, dtime):
                #self.last_bubble_launch += dtime
                self.last_iteration_time += dtime
                
                # show player standing when not moving
                # if self.last_bubble_launch >= self.BUBBLE_LAUNCH_DELAY:
                #     self.last_bubble_launch -= self.BUBBLE_LAUNCH_DELAY
                #     self.launch_bubble()

                
                # dessin de la bubble
                if  self.bubble_launched:
                    if self.last_iteration_time >= self.BUBBLE_TIME_DELAY:
                        self.last_iteration_time -= self.BUBBLE_TIME_DELAY
                        self.current_iteration=self.current_iteration+1

                        if self.current_iteration==self.iteration_number-1 or self.iteration_number==0:
                            self.bubble_launched=False
                            #ajoute (definitivement) la bubble à la liste des bubbles
                            self.add_bubble(self.target_row, self.target_col, self.current_bubble_color)
                            self.delete_bubbles_same_color(self.target_row, self.target_col, self.current_bubble_color)
                            #elf.logger.debug(f'{self.bubble_properties}')
                            #alterne joueur et ennemi
                            if self.player_turn:
                                self.player_turn=False
                                self.launch_bubble()
                            else:
                                self.player_turn=True
                            
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
                increment = 1
                if (row % 2 == 0):
                    increment = 0
                #parcours des bubbles
                for col in sorted(self.bubble_properties[row], key=lambda x: int(x)):
                    #(x,y)=position en haut à gauche du carré englobant la bubble
                    self.draw_bubble( render, width, height, st, at,  self.bubble_properties[row][col],
                    self.BORDER_WIDTH + (col - 1) * self.BUBBLE_IMAGE_SIZE  + increment * self.BUBBLE_IMAGE_SIZE/2,
                    self.BORDER_WIDTH + (row-1) * self.BUBBLE_IMAGE_SIZE  )
                    
                    if draw_explode_step:
                        if col in  self.bubble_properties[row] and self.bubble_properties[row][col].value+4 >= len(self.BUBBLE_IMAGES):
                            #on supprime car on est arrivé à la fin des animations d'explosion
                            del self.bubble_properties[row][col]
                        if col in  self.bubble_properties[row] and self.bubble_properties[row][col].value>4:
                            #si couleur d'explosion, on passe à l'animation d'explosion suivante
                            self.bubble_properties[row][col]=ColorEnum(self.bubble_properties[row][col].value+4)
                    
 
        def is_odd(self,line_number):
            return line_number % 2 != 0  # Check if the line number is odd
           
        #equation d'une droite passant par deux points
        def get_line_equation(self,launch_coords, target_pos):
            
            (x1, y1) = launch_coords
            (x2, y2) = target_pos
            
            a = (x2 - x1) / (y2 - y1)
            b = x1 - a * y1
            self.logger.debug(f'x launch {x1} y launch {y1} x target {x2} y target {y2} a {a} b {b}]')
            return (a,b)

        #distance a parcourir entre la position de depart et la cible
        def compute_distance_to_target(self):
            return ((self.target_pos[0] - self.launch_coords[0]) ** 2 + (self.target_pos[1] - self.launch_coords[1]) ** 2) ** 0.5


        def compute_distance_bubble_moves_each_delay(self):
            max_distance = (((self.SCREEN_HEIGHT - self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE/2) - (self.BORDER_WIDTH + self.BUBBLE_IMAGE_SIZE/2)) ** 2 + (
                    (self.SCREEN_WIDTH - self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE/2) - (self.BORDER_WIDTH + self.BUBBLE_IMAGE_SIZE/2.)) ** 2) ** 0.5
            
            return self.BUBBLE_TIME_DELAY * max_distance / self.MAX_TIME


        def identify_bubble_to_target(self):

            #parcours des lignes en commançant par le haut, on évite la dernière (pour ne pas perdre)
            for row in range(1,self.MAX_LINE_NUMBER):

                #si on est dans ce cas, on n'a pas de cas optimal : on sera à côté d'une bubble de même couleur
                #on prend le dernier
                if((row-1) not in self.bubble_properties and row!=1):
                    return self.identify_bubble_to_target_ignore_color()

                #parcours des colonnes, on fait attention à la couleur des voisins
                candidate=self.iterate_col_to_find_candidate(row,False)
                if candidate is not None:
                    return candidate
              

            #candidat par défaut
            return self.identify_bubble_to_target_ignore_color()

        #pas le choix : on aura un voisin de meme couleur
        def identify_bubble_to_target_ignore_color(self):
            #parcours des lignes en ignorant la couleur et en acceptant la dernière ligne
            for row in range(1,self.MAX_LINE_NUMBER+1):
                #on ignore la couleur
                candidate= self.iterate_col_to_find_candidate(row,True)
                if candidate is not None:
                    return candidate
            return None

        def iterate_col_to_find_candidate(self,row,ignore_color):
            #parcours des colonnes : si on lance à gauche, on lance vers la gauche
            #si on lance à droite, on lance vers la droite
            if(self.launch_position==CannonPositionEnum.LEFT):
                #on ne parcourt que la moitié des lignes (sinon risque d'intersection)
                for col in range(int(self.MAX_LINE_SIZE/2),0,-1):
                    candidate=self.find_candidate(row,col,self.current_bubble_color,ignore_color)
                    if  candidate is not None:
                        return candidate
            else:
                for col in range(int(self.MAX_LINE_SIZE/2)+1,self.MAX_LINE_SIZE+1):
                    candidate=self.find_candidate(row,col,self.current_bubble_color,ignore_color)
                    if  candidate is not None:
                        return candidate
            return None

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
            if self.is_odd(row):
                col_parent_gauche=col
                col_parent_droite=col+1
            else:
                col_parent_gauche=col-1
                col_parent_droite=col
 
            
            verification_ligne_dessus_ok =  row==1  or ( \
            not((col_parent_gauche) not in self.bubble_properties[row-1] and (col_parent_droite) not in self.bubble_properties[row-1])\
            and  ((col_parent_gauche) not in self.bubble_properties[row-1] or ignore_color or self.bubble_properties[row-1][col_parent_gauche] != color)\
            and ((col_parent_droite) not in self.bubble_properties[row-1] or ignore_color or self.bubble_properties[row-1][col_parent_droite] != color)\
            )

            return verification_ligne_courante_ok and verification_derniere_colonne_ok and verification_ligne_dessus_ok
        
        def find_candidate(self,row,col,color,ignore_color):
            
            if self.first_checks_for_candidate(row,col,color,ignore_color) :
                
                candidate_position=self.compute_target_candidate_bubble_position(row,col)
                
                #on a un candidat, mais il ne faut pas que le trajet vers ce candidat
                #intersecte une bubble deja en place
                #equation de la droite passant par les deux points
                # on enlève le self.BUBBLE_IMAGE_SIZE pour avoir la position "haute" des bubbles, qui peuvent intersectées
                if not self.iterate_to_check_if_intersection(self.launch_coords, candidate_position,row,col):
                    #c'est une bubble lancée par l'IA qui touche la ligne rouge ==> c'est gagné!
                    if row==self.MAX_LINE_NUMBER:
                        self.end_game=True
                        self.victory=True
                        self.information_text=_("GAGNÉ !\nAppuyez sur Entrée")
                    return (candidate_position,row,col)
            return None

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
                distance=(self.BUBBLE_REAL_SIZE-tolerance)/(math.cos(math.radians(math.fabs(angle)))) 
                bmin=b-distance/2
                bmax=b+distance/2

                
                #parcours des lignes en partant du bas, on ignore la ligne où est la cible
                for row in range(max(self.bubble_properties.keys()),target_row-1,-1):

                    if(self.launch_position==CannonPositionEnum.LEFT):
                        
                        #on ne parcourt que la moitié des lignes 
                        for col in range(target_col,0,-1):
                            intersection=self.check_if_intersection(a,bmin,bmax,row,col)
                            if  intersection is True:
                                return True
                    else:
                        for col in range(target_col,self.MAX_LINE_SIZE+1):
                            intersection=self.check_if_intersection(a,bmin,bmax,row,col)
                            if  intersection is True:
                                return True 
                return False
            else:
                #cas où les deux points sur la même colonne ou la même ligne : pas d'intersaction
                return False

        def check_if_intersection(self,a,bmin,bmax,row,col):
            if col in self.bubble_properties[row]:
                #calcule la position de la bubble qui pourrait intersectée
                (x,y)=self.compute_target_candidate_bubble_position(row,col)
               
                #calcule la position théorique de la bubble lancée (équation de la droite)
                #on prend x+RAYON pour correspond au point inférieur de la bubble

                #difference entre la taille de l'image et la taille exacte de la bubble
                diff_size=int((self.BUBBLE_IMAGE_SIZE-self.BUBBLE_REAL_SIZE)/2)
                #self.logger.debug(f'{x} {diff_size} {self.BUBBLE_REAL_SIZE} ')
                for i in range(int(y)+diff_size,int(y)+self.BUBBLE_REAL_SIZE):

                    x_bubble_lancee=a*i+bmin
                   
                    #si on est à moins de distance que le rayon (<=> on est dans le cercle)
                    if self.compute_distance(x+self.BUBBLE_IMAGE_SIZE/2,y+self.BUBBLE_IMAGE_SIZE/2,x_bubble_lancee,i)<self.BUBBLE_REAL_SIZE/2:
                        self.logger.debug(f' intersection min avec {row} {col} : {i} {a*i+bmin} {a*i+bmin+(bmax-bmin)/2} {a*i+bmax}, départ : 710  {710*a+bmin}  {710*i+bmin+(bmax-bmin)/2} {710*a+bmax} {x} {y} {self.compute_distance(x+self.BUBBLE_IMAGE_SIZE/2,y+self.BUBBLE_IMAGE_SIZE/2,x_bubble_lancee,i)}')
                        return True
                    x_bubble_lancee=a*i+bmax
                    if self.compute_distance(x+self.BUBBLE_IMAGE_SIZE/2,y+self.BUBBLE_IMAGE_SIZE/2,x_bubble_lancee,i)<self.BUBBLE_REAL_SIZE/2:
                        self.logger.debug(f'intersection max avec {row} {col} : {i} {a*i+bmin}  {a*i+bmax}, départ : 710  {710*a+bmin}   {710*a+bmax} {x} {y} {self.compute_distance(x+self.BUBBLE_IMAGE_SIZE/2,y+self.BUBBLE_IMAGE_SIZE/2,x_bubble_lancee,i)}')
                        return True
                return False
            else:
                return False
    
        def compute_distance(self,x1,y1,x2,y2):
            return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

        #calcule de la position (x,y) de la bubble
        def compute_target_candidate_bubble_position(self,row,col):
            
            
            if self.is_odd(row):
                return (
                    col * self.BUBBLE_IMAGE_SIZE  + self.BORDER_WIDTH - self.BUBBLE_IMAGE_SIZE/2,
                    self.BORDER_WIDTH + row * self.BUBBLE_IMAGE_SIZE  - (self.BUBBLE_IMAGE_SIZE))  
            else:
                return (
                        col * self.BUBBLE_IMAGE_SIZE + self.BORDER_WIDTH -self.BUBBLE_IMAGE_SIZE , self.BORDER_WIDTH + row * self.BUBBLE_IMAGE_SIZE  - (self.BUBBLE_IMAGE_SIZE))  

        #supprime les bubbles de même couleur (s'il y en a)
        def delete_bubbles_same_color(self,row,col,color):
            if self.is_odd(row):
                col_parent_gauche=col
                col_parent_droite=col+1
            else:
                col_parent_gauche=col-1
                col_parent_droite=col

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
                self.explode(row,col)

        #suppression de la bulle si elle est la couleur en paramètre
        def delete_bubble_same_color(self,row,col,color):
            if row in self.bubble_properties and col in self.bubble_properties[row]\
            and self.bubble_properties[row][col]==color:
                self.explode(row,col)
                return True
            return False

        #initalisation d'une explosion (sauf si init => pas d'animation)
        def explode(self,row,col):
            #couleur d'explosion
            if not self.init:
                self.bubble_properties[row][col]=ColorEnum(self.bubble_properties[row][col].value+4)
            else:
                del self.bubble_properties[row][col]


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


        def get_angle(self,launch_coords, target_pos):
            (x1, y1) = launch_coords
            (x2, y2) = target_pos
            return math.degrees(math.atan(math.fabs(x2 - x1) / math.fabs(y2 - y1) ))   
         
        def init_ennemy_launch(self):
            self.current_bubble_color = random.choice([ColorEnum.RED,ColorEnum.GREEN,ColorEnum.BLUE,ColorEnum.PURPLE])    # Randomly choose a color for the bubble
            #(x,y)=position en haut à gauche du carré englobant la bubble
            if self.last_launch_position==CannonPositionEnum.LEFT:
                #on lançait depuis la gauche, on lance depuis la droite
                self.launch_position=CannonPositionEnum.RIGHT
                self.launch_coords = self.LAUNCH_COORDS_RIGHT  # Start position of the bubble

            else:
                #on lançait depuis la droite, on lance depuis la gauche
                self.launch_position=CannonPositionEnum.LEFT
                self.launch_coords = self.LAUNCH_COORDS_LEFT  # Start position of the bubble


  
            #pour alterner les canons ennemis
            self.last_launch_position=self.launch_position

           
            (self.target_pos,self.target_row,self.target_col) = self.identify_bubble_to_target()  # Find target position for the bubble
            angle = self.get_angle(self.launch_coords,self.target_pos)
            if self.launch_position==CannonPositionEnum.RIGHT:
                angle=-angle
            
            self.angles[self.launch_position.value]=angle
            


        
        def player_shoot(self):
            self.player_turn=False
            self.launch_bubble()





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


            self.draw_current_bubble(render, width, height, st, at,dtime)

            # Display all bubbles
            self.display_bubbles(render, width, height, st, at,dtime)


            #canons
            self.draw_cannon(render, width, height, st, at,-55,height-143,self.angles[0])
            self.draw_cannon(render, width, height, st, at,width-143,height-143,self.angles[1])
            self.draw_cannon(render, width, height, st, at,width/2-95,height-143,self.angles[2])
            

            #socles des canons
            self.draw_cannon_base(render, width, height, st, at,0,height-self.CANNON_BASE_WIDTH,1)
            self.draw_cannon_base(render, width, height, st, at,width-self.CANNON_BASE_WIDTH,height-self.CANNON_BASE_WIDTH,-1)
            self.draw_cannon_base_middle(render, width, height, st, at,width/2-110,height-120)
            # redraw the screen
            renpy.redraw(self, 0)

            # Return the Render object.
            return render



        # Handles events to move player
        def event(self, ev, x, y, st):

            #quit
            if  ev.type == pygame.KEYDOWN  and ev.key == pygame.K_ESCAPE :
                self.show_next_screen()

            if  ((ev.type == pygame.KEYDOWN  and ev.key == pygame.K_RETURN)or(ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1)) and (self.end_game or self.wait_for_start):
                if self.victory==True:
                    self.show_next_screen()
                if self.end_game:
                    self.__init__()
                if self.wait_for_start:
                    #top à la vachette !
                    self.information_text=""
                    self.wait_for_start=False


            # canon move right
            if not self.end_game  and not self.wait_for_start and ev.type == pygame.KEYDOWN and ev.key == pygame.K_RIGHT and self.player_turn:
                if not self.cannon_moving:
                    self.initial_cannon_move(self.ANGLE_STEP)   
                raise renpy.IgnoreEvent()


            # player move left
            if not self.end_game and not self.wait_for_start  and ev.type == pygame.KEYDOWN and ev.key == pygame.K_LEFT and self.player_turn:
                if not self.cannon_moving:
                    self.initial_cannon_move(-self.ANGLE_STEP)   
                raise renpy.IgnoreEvent()


            # player move left
            if not self.end_game and not self.wait_for_start and ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE and self.player_turn:
                self.player_shoot()  
                raise renpy.IgnoreEvent()


            # Ensure the screen updates
            renpy.restart_interaction()
            raise renpy.IgnoreEvent()  


                # show screen after game (home screen or next screen of history)
        def show_next_screen(self):
            self.__init__()
            renpy.jump("after_bubble_shooter_game")  

    def display_end_bubble_shooter_game_text(st, at):
        return Text( bubble_shooter_game.information_text, font='gui/jd_code.ttf', size=50, color="#33e43c"), .1 

    def display_end_bubble_shooter_game_background(st, at):
        if bubble_shooter_game.end_game or bubble_shooter_game.wait_for_start:
            return Image("images/bubble_shooter_game/mini_game_end_background.png"), 30
        else :
            return Null(width=0), .1

default bubble_shooter_game = BubbleShooterGameDisplayable()

# label to start snake game
label start_bubble_shooter_game:
    stop music
    play music snake_game_music
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



