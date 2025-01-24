            
init python:

    import random
    from enum import Enum
    import pygame


    global mini_game
    global snake_failure
    
    mini_game=True


    class DirectionEnum(Enum):
        LEFT = 1
        RIGHT = 2
        UP = 3
        DOWN = 4

    class SnakeGameDisplayable(renpy.Displayable):

        def __init__(self):

            renpy.Displayable.__init__(self)

            #self.logger = logging.getLogger(__name__)
            #logging.basicConfig(filename='debug.log', encoding='utf-8', level=logging.DEBUG)
           
       
            # Set game values
            self.CELL_SIZE = 70

            #end game if victory or game over
            self.end_game=False
            self.victory=False
            self.waiting_for_start=True
         
            self.should_draw_buttons=True
            #direction button pushed
            self.direction_pushed=None

            # Some displayables we use.
            self.player = Image("images/snake_game/player_stand.png")
            self.apple = [Image("images/snake_game/apple0.png"),Image("images/snake_game/apple1.png"),Image("images/snake_game/apple2.png"),Image("images/snake_game/apple3.png"),Image("images/snake_game/apple4.png"),Image("images/snake_game/apple5.png"),Image("images/snake_game/apple6.png"),Image("images/snake_game/apple7.png")]
            self.index_apple=len(self.apple)-1
            self.snake_head=Image("images/snake_game/snake_head_left.png")
            self.snake_head_bite=Image("images/snake_game/snake_head_bite_left.png")
            self.buttons_idle = [Image("images/snake_game/left_idle.png"),Image("images/snake_game/right_idle.png"),Image("images/snake_game/up_idle.png"),Image("images/snake_game/down_idle.png")]
            self.buttons_pushed = [Image("images/snake_game/left_pushed.png"),Image("images/snake_game/right_pushed.png"),Image("images/snake_game/up_pushed.png"),Image("images/snake_game/down_pushed.png")]
 
            self.MAX_HEIGHT=720
            self.MAX_WIDTH=1280
            self.BORDER_WIDTH=10
            # limit of the game (border size is 10px)
            self.PY_MIN =  self.BORDER_WIDTH
            self.PY_MAX =  self.MAX_HEIGHT -  self.BORDER_WIDTH - self.CELL_SIZE 
            self.PX_MIN =  self.BORDER_WIDTH
            self.PX_MAX = self.MAX_WIDTH -  self.BORDER_WIDTH - self.CELL_SIZE 


            #position of player
            self.px = 10
            self.py =  10+70*8
            #initial direction
            self.player_direction=DirectionEnum.RIGHT
            self.player_next_direction=Null
            self.snake_direction=DirectionEnum.LEFT
            
            
            #position of snake head
            sx= 1280-10-70*5
            sy= 10+70
            #positions of snake body
            self.sxy = []
           
            # default snake body
            self.sxy.append( (sx+self.CELL_SIZE,sy))
            self.sxy.append( (sx+self.CELL_SIZE*2,sy))
            self.sxy.append( (sx+self.CELL_SIZE*3,sy))
            self.sxy.append( (sx+self.CELL_SIZE*4,sy))


            self.snake_sound_accumulated_time=0
            self.snake_accumulated_time=0
            self.apple_accumulated_time=0
            self.last_player_move_accumulated_time=0
            self.start_player_move=0
            self.player_moving=False
            self.index_player_move=0


            # The time of the past render-frame.
            self.last_frame_rendering = None
            self.SNAKE_SOUND_DURATION=10
            # time between snake movements
            self.SNAKE_FRAME_DURATION=0.7
            # time between images during apple display
            self.APPLE_FRAME_DURATION=0.3
            # time before we show stand image for player
            self.PLAYER_STANDING=0.3
            # time between images during player move
            self.PLAYER_MOVE_DURATION=0.1
            

            # initial position of apple
            self.ax = 10+ 8*self.CELL_SIZE
            self.ay = 10+4*self.CELL_SIZE  

            self.information_text= _("Attention, ça va commencer !\n\nVous gagnez si le serpent ne peut plus bouger.\nUtilisez les flèches du clavier ou les boutons pour vous déplacer.\n\nAppuyez sur Entrée ou Clic Gauche pour lancer le jeu.")


            return

        # compute image and position of player
        def compute_player_move(self):
                   
            self.index_player_move=self.index_player_move+1
            self.player = Image("images/snake_game/player_"+self.player_direction.name+"_"+str(self.index_player_move)+".png")
            if(self.player_direction==DirectionEnum.UP):
                self.py-=self.CELL_SIZE/4
            elif(self.player_direction==DirectionEnum.DOWN):
                self.py+=self.CELL_SIZE/4
            elif(self.player_direction==DirectionEnum.LEFT):
                self.px-=self.CELL_SIZE/4
            else:
                self.px+=self.CELL_SIZE/4


        #victory message
        def check_victory(self,body):
            if(self.sxy[0][0]==body[0] and self.sxy[0][1]==body[1] ) and not self.victory:
                #you won !
                self.end_game=True
                self.victory=True
                renpy.music.stop()
                renpy.sound.play(win_sound)
                self.information_text=_("GAGNÉ !\nAppuyez sur Entrée ou Clic gauche.")


        # This draws the player.
        def draw_player(self, render,  width, height, st, at,dtime):

            # Render the player image.
            player = renpy.render(self.player, width, height, st, at)

            # renpy.render returns a Render object, which we can
            # blit to the Render we're making.
            render.blit(player, (int(self.px), int(self.py)))

            self.last_player_move_accumulated_time += dtime
            self.start_player_move += dtime


            # show player standing when not moving
            if self.last_player_move_accumulated_time >= self.PLAYER_STANDING:
                self.last_player_move_accumulated_time -= self.PLAYER_STANDING
                self.player = Image("images/snake_game/player_stand.png")
                

            # show player second move
            if self.start_player_move >= self.PLAYER_MOVE_DURATION and self.player_moving:
                if self.index_player_move<4:
                    
                    self.start_player_move -= self.PLAYER_MOVE_DURATION

                    self.compute_player_move()

                    self.last_player_move_accumulated_time=0
                else :
                    self.player_moving=False
                    #gestion mouvement clavier
                    if self.player_next_direction!=Null :
                        
                        if not self.check_collide(self.player_next_direction):
                            self.player_direction=self.player_next_direction
                            self.initial_player_move()
                    
                        self.player_next_direction=Null

                    #gestion mouvement souris
                    if self.direction_pushed is not None:
                        if not self.check_collide(self.direction_pushed):
                            self.player_direction=self.direction_pushed
                            self.initial_player_move()


        # This draws the apple
        def draw_apple( self, render, width, height, st, at,dtime):

            # Render the apple image
            apple = renpy.render(self.apple[self.index_apple], width, height, st, at)
                
            # renpy.render returns a Render object, which we can
            # blit to the Render we're making
            render.blit(apple, (int(self.ax), int(self.ay)))

            # show apple display when appear
            if self.apple_accumulated_time >= self.APPLE_FRAME_DURATION:
                self.apple_accumulated_time -= self.APPLE_FRAME_DURATION
                if self.index_apple<len(self.apple)-1:
                    self.index_apple += 1

            self.apple_accumulated_time += dtime

        def redraw_apple_if_collide(self,x_pos,y_pos):
            if(x_pos==self.ax and y_pos==self.ay ):
                #redraw apple somewhere else
                self.ax = 10+ random.randint(2, 15)*self.CELL_SIZE
                self.ay = 10+random.randint(2, 7)*self.CELL_SIZE  
                self.index_apple=0

        def get_direction_of_snake_previous_or_next(self,body,i):
            if(body[0]==self.sxy[i][0]+self.CELL_SIZE):
                return DirectionEnum.LEFT
            elif (body[0]==self.sxy[i][0]-self.CELL_SIZE):
                return DirectionEnum.RIGHT
            elif (body[1]==self.sxy[i][1]+self.CELL_SIZE):
                return DirectionEnum.UP
            else:
                return DirectionEnum.DOWN
                   

        # This draws the snake body
        def draw_snake(self, render, width, height, st, at, dtime):

            # Render the snake body image
                
            # renpy.render returns a Render object, which we can
            # blit to the Render we're making
            for i,body in reversed(list(enumerate(self.sxy))):
                #snake head
                if (i==0):
                    image_to_draw = renpy.render( self.snake_head, width, height, st, at)
                #snake tail
                elif (i==len(self.sxy)-1):
                    self.redraw_apple_if_collide(self.sxy[0][0],self.sxy[0][1])
                    # snake head collides with snake tail
                    self.check_victory(body)
                    #compute tail direction from previous element of snake body
                    previous_direction=self.get_direction_of_snake_previous_or_next(body,i-1)
                    image_to_draw = renpy.render( Image("images/snake_game/snake_tail_"+previous_direction.name+".png"), width, height, st, at)
                else:
                    self.redraw_apple_if_collide(body[0],body[1])
                    # snake head collides with snake body
                    self.check_victory(body)
                    #draw snake body
                    previous_direction=self.get_direction_of_snake_previous_or_next(body,i-1)
                    next_direction=self.get_direction_of_snake_previous_or_next(body,i+1)
                    image_to_draw = renpy.render( Image("images/snake_game/snake_body_"+previous_direction.name+"_"+next_direction.name+".png"), width, height, st, at)

                render.blit(image_to_draw, (int(body[0]), int(body[1])))


            self.snake_accumulated_time += dtime
            self.snake_sound_accumulated_time+= dtime


            if self.snake_sound_accumulated_time >= self.SNAKE_SOUND_DURATION:
                self.snake_sound_accumulated_time -= self.SNAKE_SOUND_DURATION
                renpy.sound.play(snake_coming_sound)

            # move snake
            if self.snake_accumulated_time >= self.SNAKE_FRAME_DURATION:
                self.snake_accumulated_time -= self.SNAKE_FRAME_DURATION
                self.process_game_step()

                
            
              


        # This draws  buttons
        def draw_buttons(self, render, width, height, st, at, dtime):

            if self.direction_pushed==DirectionEnum.LEFT:
                image_to_draw = renpy.render( self.buttons_pushed[DirectionEnum.LEFT.value-1], width, height, st, at)
            else:
                image_to_draw = renpy.render( self.buttons_idle[DirectionEnum.LEFT.value-1], width, height, st, at)
            
            render.blit(image_to_draw, (self.MAX_WIDTH -  self.BORDER_WIDTH - self.CELL_SIZE*3 , self.MAX_HEIGHT -  self.BORDER_WIDTH - self.CELL_SIZE*2))

            if self.direction_pushed==DirectionEnum.RIGHT:
                image_to_draw = renpy.render( self.buttons_pushed[DirectionEnum.RIGHT.value-1], width, height, st, at)
            else:
                image_to_draw = renpy.render( self.buttons_idle[DirectionEnum.RIGHT.value-1], width, height, st, at)
            render.blit(image_to_draw, (self.MAX_WIDTH -  self.BORDER_WIDTH - self.CELL_SIZE , self.MAX_HEIGHT -  self.BORDER_WIDTH - self.CELL_SIZE*2))

            if self.direction_pushed==DirectionEnum.UP:
                image_to_draw = renpy.render( self.buttons_pushed[DirectionEnum.UP.value-1], width, height, st, at)
            else:
                image_to_draw = renpy.render( self.buttons_idle[DirectionEnum.UP.value-1], width, height, st, at)
            render.blit(image_to_draw, (self.MAX_WIDTH -  self.BORDER_WIDTH - self.CELL_SIZE*2 , self.MAX_HEIGHT -  self.BORDER_WIDTH - self.CELL_SIZE*3))


            if self.direction_pushed==DirectionEnum.DOWN:
                image_to_draw = renpy.render( self.buttons_pushed[DirectionEnum.DOWN.value-1], width, height, st, at)
            else:
                image_to_draw = renpy.render( self.buttons_idle[DirectionEnum.DOWN.value-1], width, height, st, at)
            render.blit(image_to_draw, (self.MAX_WIDTH -  self.BORDER_WIDTH - self.CELL_SIZE*2 , self.MAX_HEIGHT -  self.BORDER_WIDTH - self.CELL_SIZE))

           

           
        #player should stay in the frame
        def check_player_keep_in(self):
            if self.py < self.PY_MIN:
                self.py = self.PY_MIN
            if self.py > self.PY_MAX:
                self.py = self.PY_MAX
            if self.px < self.PX_MIN:
                self.px = self.PX_MIN
            if self.px > self.PX_MAX:
                self.px = self.PX_MAX


        def check_game_over(self):
                # snake head collides with player
                if(self.sxy[0][0]==self.px and self.sxy[0][1]==self.py and not self.end_game):
                    self.snake_head=self.snake_head_bite
                    renpy.sound.play(snake_eating_sound)
                    self.end_game=True
                    renpy.music.stop()
                    renpy.sound.play(lose_sound)
                    if mini_game==True:
                        self.information_text=_("PERDU !\nAppuyez sur Entrée ou Clic Gauche pour rejouer.\nAppuyez sur Echap ou Clic GM pour quitter.")
                    else:
                        self.information_text=_("PERDU !\nAppuyez sur Entrée ou Clic Gauche pour rejouer.\nAppuyez sur Echap ou Clic GM pour poursuivre l'histoire.")


        def check_apple_bite(self):
            if not self.end_game and not self.waiting_for_start:
                # snake collides with apple
                if(self.sxy[0][0]==self.ax and self.sxy[0][1]==self.ay):
                    self.snake_head=self.snake_head_bite
                    renpy.sound.play(snake_eating_sound)

                    #draw apple somewhere else
                    self.ax = 10+ random.randint(2, 15)*self.CELL_SIZE
                    self.ay = 10+random.randint(2, 7)*self.CELL_SIZE  
                    self.index_apple=0
                else :
                    #move snake (if apple is eaten we dont pop, so size increases)
                    self.sxy.pop()


        #snake move and collisions
        def process_game_step(self):
            if not self.end_game and not self.waiting_for_start:
                # computes distance between snake head and player
                # shorten the biggest distance (horizontal or vertical)
                if(abs(self.sxy[0][0]-self.px)>abs(self.sxy[0][1]-self.py)):
                    #move horizontally
                    if(self.sxy[0][0]>self.px ):
                        if(self.snake_direction!=DirectionEnum.RIGHT):
                            self.sxy.insert(0, (self.sxy[0][0]-self.CELL_SIZE, self.sxy[0][1]))
                            self.snake_direction=DirectionEnum.LEFT
                        else:
                            #move vertically
                            if(self.sxy[0][1]>self.py):
                                self.sxy.insert(0, (self.sxy[0][0], self.sxy[0][1]-self.CELL_SIZE))
                                self.snake_direction=DirectionEnum.UP
                            else:
                                self.sxy.insert(0, (self.sxy[0][0], self.sxy[0][1]+self.CELL_SIZE))
                                self.snake_direction=DirectionEnum.DOWN
                    else:
                        if(self.snake_direction!=DirectionEnum.LEFT):
                            self.sxy.insert(0, (self.sxy[0][0]+self.CELL_SIZE, self.sxy[0][1]))
                            self.snake_direction=DirectionEnum.RIGHT
                        else:
                            #move vertically
                            if(self.sxy[0][1]>self.py):
                                self.sxy.insert(0, (self.sxy[0][0], self.sxy[0][1]-self.CELL_SIZE))
                                self.snake_direction=DirectionEnum.UP
                            else:
                                self.sxy.insert(0, (self.sxy[0][0], self.sxy[0][1]+self.CELL_SIZE))
                                self.snake_direction=DirectionEnum.DOWN
                else:
                    #move vertically
                    if(self.sxy[0][1]>self.py):
                        if(self.snake_direction!=DirectionEnum.DOWN):
                            self.sxy.insert(0, (self.sxy[0][0], self.sxy[0][1]-self.CELL_SIZE))
                            self.snake_direction=DirectionEnum.UP
                        else:
                            if(self.sxy[0][0]>self.px  ):
                                self.sxy.insert(0, (self.sxy[0][0]-self.CELL_SIZE, self.sxy[0][1]))
                                self.snake_direction=DirectionEnum.LEFT
                            else:
                                self.sxy.insert(0, (self.sxy[0][0]+self.CELL_SIZE, self.sxy[0][1]))
                                self.snake_direction=DirectionEnum.RIGHT
                    else:
                        if(self.snake_direction!=DirectionEnum.UP):
                            self.sxy.insert(0, (self.sxy[0][0], self.sxy[0][1]+self.CELL_SIZE))
                            self.snake_direction=DirectionEnum.DOWN
                        else:
                            if(self.sxy[0][0]>self.px  ):
                                self.sxy.insert(0, (self.sxy[0][0]-self.CELL_SIZE, self.sxy[0][1]))
                                self.snake_direction=DirectionEnum.LEFT
                            else:
                                self.sxy.insert(0, (self.sxy[0][0]+self.CELL_SIZE, self.sxy[0][1]))
                               
            self.snake_head =  Image("images/snake_game/snake_head_"+self.snake_direction.name+".png")
            self.snake_head_bite =  Image("images/snake_game/snake_head_bite_"+self.snake_direction.name+".png")
                     
            self.check_game_over()
            self.check_apple_bite()

        # Draws the screen
        def render(self, width, height, st, at):

            # The Render object we'll be drawing into.
            render = renpy.Render(width, height)

            # Figure out the time elapsed since the previous frame.
            if self.last_frame_rendering is None:
                self.last_frame_rendering = st
            dtime = st - self.last_frame_rendering
            self.last_frame_rendering = st
                
            # player cannot go out
            self.check_player_keep_in()
         
            if self.should_draw_buttons:
                #draw the buttons
                self.draw_buttons(render, width, height, st, at,dtime)

            # draw the apple
            self.draw_apple(render, width, height, st, at,dtime)

            #hide player if lost
            if not self.end_game or self.victory:
                self.draw_player(render, width, height, st, at,dtime)


            self.draw_snake(render, width, height, st, at,dtime)
            
            
           
            # redraw the screen
            renpy.redraw(self, 0)

            # Return the Render object.
            return render


        # show screen after game (home screen or next screen of history)
        def show_next_screen(self):
            self.__init__()
            renpy.jump("after_snake_game")

        def show_game_screen(self):
            self.__init__()
            renpy.jump("start_snake_game")

        def initial_player_move(self):
            self.start_player_move=0
            self.player_moving=True
            self.index_player_move=0
            self.compute_player_move()
            renpy.redraw(self, 0)



        # Handles events to move player
        def event(self, ev, x, y, st):


            #quit
            if  ev.type == pygame.KEYDOWN  and ev.key == pygame.K_ESCAPE :
                self.show_next_screen()

            if  ((ev.type == pygame.KEYDOWN  and ev.key == pygame.K_RETURN)or(ev.type == pygame.MOUSEBUTTONUP and ev.button == 1)) and (self.end_game or self.waiting_for_start) :
                if self.victory==True:
                    self.show_next_screen()
                if self.end_game:
                    self.show_game_screen()
                if self.waiting_for_start:
                    self.information_text=""
                    self.waiting_for_start=False


            # player move up
            if not self.end_game  and not self.waiting_for_start and ev.type == pygame.KEYDOWN   and ev.key == pygame.K_UP :
                #hide direction buttons
                self.should_draw_buttons=False
                if not self.player_moving:
                    collide=self.check_collide(DirectionEnum.UP)
                         
                    if not collide :
                        self.player_direction=DirectionEnum.UP
                        self.initial_player_move()
                else:
                    self.player_next_direction=DirectionEnum.UP

                raise renpy.IgnoreEvent()


            # player move down
            if not self.end_game  and not self.waiting_for_start and ev.type == pygame.KEYDOWN and ev.key == pygame.K_DOWN :
                #hide direction buttons
                self.should_draw_buttons=False
                if not self.player_moving:
                    collide=self.check_collide(DirectionEnum.DOWN)
                      
                    if not collide:
                        self.player_direction=DirectionEnum.DOWN
                        self.initial_player_move()
                else:
                    self.player_next_direction=DirectionEnum.DOWN

                raise renpy.IgnoreEvent()


            # player move right
            if not self.end_game  and not self.waiting_for_start and ev.type == pygame.KEYDOWN and ev.key == pygame.K_RIGHT :
                #hide direction buttons
                self.should_draw_buttons=False
                if not self.player_moving:
                    collide=self.check_collide(DirectionEnum.RIGHT)
                                       
                    if not collide:
                        self.player_direction=DirectionEnum.RIGHT
                        self.initial_player_move()
                else:
                    self.player_next_direction=DirectionEnum.RIGHT    
                        
                raise renpy.IgnoreEvent()


            # player move left
            if not self.end_game and not self.waiting_for_start and ev.type == pygame.KEYDOWN and ev.key == pygame.K_LEFT :
                #hide direction buttons
                self.should_draw_buttons=False
                if not self.player_moving:
                    collide=self.check_collide(DirectionEnum.LEFT)
                    
                    if not collide :
                        self.player_direction=DirectionEnum.LEFT
                        self.initial_player_move()
                else:
                    self.player_next_direction=DirectionEnum.LEFT
                raise renpy.IgnoreEvent()



            if ev.type == pygame.MOUSEBUTTONDOWN and self.should_draw_buttons:
                if ev.button == 1:  # Left mouse button
                    # Get the mouse position when clicked
                    # we use renpy function instead of pygame fuction because we
                    # want the virtual position (virtual width=1280,virtual height=720)
                    mouse_x, mouse_y = renpy.get_mouse_pos()
                    #self.logger.debug(f'{mouse_x} ')
                    if  mouse_x > self.MAX_WIDTH -  self.BORDER_WIDTH - self.CELL_SIZE*3  \
                    and mouse_x < self.MAX_WIDTH -  self.BORDER_WIDTH - self.CELL_SIZE*2  \
                    and mouse_y > self.MAX_HEIGHT -  self.BORDER_WIDTH - self.CELL_SIZE*2 \
                    and mouse_y < self.MAX_HEIGHT -  self.BORDER_WIDTH - self.CELL_SIZE*1: 

                        self.direction_pushed=DirectionEnum.LEFT
                    
                    if  mouse_x > self.MAX_WIDTH -  self.BORDER_WIDTH - self.CELL_SIZE  \
                    and mouse_x < self.MAX_WIDTH -  self.BORDER_WIDTH   \
                    and mouse_y > self.MAX_HEIGHT -  self.BORDER_WIDTH - self.CELL_SIZE*2 \
                    and mouse_y < self.MAX_HEIGHT -  self.BORDER_WIDTH - self.CELL_SIZE*1: 

                        self.direction_pushed=DirectionEnum.RIGHT

                    if  mouse_x > self.MAX_WIDTH -  self.BORDER_WIDTH - self.CELL_SIZE*2  \
                    and mouse_x < self.MAX_WIDTH -  self.BORDER_WIDTH - self.CELL_SIZE  \
                    and mouse_y > self.MAX_HEIGHT -  self.BORDER_WIDTH - self.CELL_SIZE*3 \
                    and mouse_y < self.MAX_HEIGHT -  self.BORDER_WIDTH - self.CELL_SIZE*2: 

                        self.direction_pushed=DirectionEnum.UP

                    if  mouse_x > self.MAX_WIDTH -  self.BORDER_WIDTH - self.CELL_SIZE*2  \
                    and mouse_x < self.MAX_WIDTH -  self.BORDER_WIDTH - self.CELL_SIZE  \
                    and mouse_y > self.MAX_HEIGHT -  self.BORDER_WIDTH - self.CELL_SIZE \
                    and mouse_y < self.MAX_HEIGHT -  self.BORDER_WIDTH : 

                        self.direction_pushed=DirectionEnum.DOWN

                    if self.direction_pushed is not None:
                        if not self.player_moving:
                            collide=self.check_collide(self.direction_pushed)
                            
                            if not collide :
                                self.player_direction=self.direction_pushed
                                self.initial_player_move()
                        

                raise renpy.IgnoreEvent()

            if ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:  # Left mouse button
                    self.direction_pushed=None
                raise renpy.IgnoreEvent()

            # Ensure the screen updates
            renpy.restart_interaction()
            raise renpy.IgnoreEvent()   


        def check_collide(self,direction):
            if direction==DirectionEnum.LEFT:
                #check collision with snake
                for body in self.sxy:
                    if (self.px == body[0] + self.CELL_SIZE and self.py==body[1]):
                        return True
                #check collision with apple
                return (self.px == self.ax + self.CELL_SIZE and self.py==self.ay)
            if direction==DirectionEnum.RIGHT:
                for body in self.sxy:
                    if (self.px == body[0] - self.CELL_SIZE and self.py==body[1]):
                        return  True
                return (self.px == self.ax - self.CELL_SIZE and self.py ==self.ay)
            if direction==DirectionEnum.UP:
                for body in self.sxy:
                    if (self.py == body[1] + self.CELL_SIZE and self.px==body[0]):
                        return True
                return (self.py == self.ay + self.CELL_SIZE and self.px==self.ax )
            if direction==DirectionEnum.DOWN:
                for body in self.sxy:
                    if (self.py == body[1] - self.CELL_SIZE and self.px==body[0]):
                        return True
                return (self.py == self.ay - self.CELL_SIZE and  self.px==self.ax)
        

    def display_end_snake_game_text(st, at):
            return Text( snake_game.information_text, font='gui/jd_code.ttf', size=50, color="#77d079"), .1

    def display_end_snake_game_background(st, at):
        if snake_game.end_game or snake_game.waiting_for_start:
            return Image("images/snake_game/mini_game_end_background.png"), 30
        else :
            return Null(width=0), .1





default snake_game = SnakeGameDisplayable()


# label to start snake game
label start_snake_game:
    stop sound
    stop music
    play music snake_game_music
    window hide  # Hide the window and quick menu while in mini game
    call screen snake_game


#start snake game
screen snake_game():
    add "images/snake_game/background_snake.png"
    add snake_game 
    add DynamicDisplayable(display_end_snake_game_background) 
    add DynamicDisplayable(display_end_snake_game_text) xalign 0.5 yalign 0.5 
    imagebutton:
        # image GM
        idle "gui/overlay/menu_button_idle.png"
        hover "gui/overlay/menu_button_hover.png"
        
        # Position du bouton
        xalign 0.99
        yalign 0.01
        
        # Action à réaliser lors du clic
        action Function(snake_game.show_next_screen)
    
   