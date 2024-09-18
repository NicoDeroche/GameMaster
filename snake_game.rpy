            
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
       
            # Set game values
            self.CELL_SIZE = 70

            #end game if victory or game over
            self.end_game=False
            self.victory=False
         

            # Some displayables we use.
            self.player = Image("images/snake_game/player_stand.png")
            self.apple = [Image("images/snake_game/apple0.png"),Image("images/snake_game/apple1.png"),Image("images/snake_game/apple2.png"),Image("images/snake_game/apple3.png"),Image("images/snake_game/apple4.png"),Image("images/snake_game/apple5.png"),Image("images/snake_game/apple6.png"),Image("images/snake_game/apple7.png")]
            self.index_apple=len(self.apple)-1
            self.snake_head=Image("images/snake_game/snake_head_left.png")
            self.snake_head_bite=Image("images/snake_game/snake_head_bite_left.png")
            
 
            # limit of the game (border size is 10px)
            self.pymin = 10
            self.pymax = 720 - 10 - self.CELL_SIZE 
            self.pxmin = 10
            self.pxmax = 1280 - 10 - self.CELL_SIZE 


            #position of player
            self.px = 10
            self.py =  10+70*8
            #initial direction
            self.direction=DirectionEnum.LEFT
            
            
            
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


            self.snake_accumulated_time=0
            self.apple_accumulated_time=0
            self.last_player_move_accumulated_time=0
            self.start_player_move=0
            self.player_moving=False
            self.index_player_move=0


            # The time of the past render-frame.
            self.last_frame_rendering = None

            # time between snake movements
            self.SNAKE_FRAME_DURATION=0.7
            # time between images during apple display
            self.APPLE_FRAME_DURATION=0.3
            # time before we show stand image for player
            self.PLAYER_STANDING=0.5
            # time between images during player move
            self.PLAYER_MOVE_DURATION=0.1
            

            # initial position of apple
            self.ax = 10+ 8*self.CELL_SIZE
            self.ay = 10+4*self.CELL_SIZE  

            self.end_text=""

            return

        # compute image and position of player
        def compute_player_move(self):
            self.index_player_move=self.index_player_move+1
            self.player = Image("images/snake_game/player_"+self.direction.name+"_"+str(self.index_player_move)+".png")
            if(self.direction==DirectionEnum.UP):
                self.py-=self.CELL_SIZE/2
            elif(self.direction==DirectionEnum.DOWN):
                self.py+=self.CELL_SIZE/2
            elif(self.direction==DirectionEnum.LEFT):
                self.px-=self.CELL_SIZE/2
            else:
                self.px+=self.CELL_SIZE/2


        #victory message
        def victory(self):
            #you won !
            self.end_game=True
            self.victory=True
            self.end_text="GAGNÉ !\nAppuyez sur Entrée"


        # This draws the player.
        def draw_player(self, render,  width, height, st, at):

            # Render the player image.
            player = renpy.render(self.player, width, height, st, at)

            # renpy.render returns a Render object, which we can
            # blit to the Render we're making.
            render.blit(player, (int(self.px), int(self.py)))



        # This draws the apple
        def draw_apple( self, render, width, height, st, at):

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


        #player should stay in the frame
        def check_player_keep_in(self):
            if self.py < self.pymin:
                self.py = self.pymin
            if self.py > self.pymax:
                self.py = self.pymax
            if self.px < self.pxmin:
                self.px = self.pxmin
            if self.px > self.pxmax:
                self.px = self.pxmax

        # Draws the screen
        def render(self, width, height, st, at):

            # The Render object we'll be drawing into.
            render = renpy.Render(width, height)

            # Figure out the time elapsed since the previous frame.
            if self.last_frame_rendering is None:
                self.last_frame_rendering = st
            dtime = st - self.last_frame_rendering
            self.last_frame_rendering = st

 



           

            # This draws the snake body
            def snake(sxy):

                # Render the snake body image
                
                # renpy.render returns a Render object, which we can
                # blit to the Render we're making
                for i,body in reversed(list(enumerate(sxy))):
                    #snake head
                    if (i==0):
                        snake_head = renpy.render( self.snake_head, width, height, st, at)
                        render.blit(snake_head, (int(body[0]), int(body[1])))
                    #snake tail
                    elif (i==len(sxy)-1):
                        if(self.sxy[0][0]==self.ax and self.sxy[0][1]==self.ay ):
                            #redraw apple somewhere else
                            self.ax = 10+ random.randint(2, 15)*self.CELL_SIZE
                            self.ay = 10+random.randint(2, 7)*self.CELL_SIZE  
                            self.index_apple=0
                        # snake head collides with snake tail
                        if(self.sxy[0][0]==body[0] and self.sxy[0][1]==body[1] ):
                            self.victory()
                        #compute tail direction from previous element of snake body
                        if(body[0]==sxy[len(sxy)-2][0]+self.CELL_SIZE):
                            snake_tail = renpy.render( Image("images/snake_game/snake_tail_left.png"), width, height, st, at)
                        elif (body[0]==sxy[len(sxy)-2][0]-self.CELL_SIZE):
                            snake_tail = renpy.render( Image("images/snake_game/snake_tail_right.png"), width, height, st, at)
                        elif (body[1]==sxy[len(sxy)-2][1]+self.CELL_SIZE):
                            snake_tail = renpy.render( Image("images/snake_game/snake_tail_up.png"), width, height, st, at)
                        else:
                            snake_tail = renpy.render( Image("images/snake_game/snake_tail_down.png"), width, height, st, at)
                        render.blit(snake_tail, (int(body[0]), int(body[1])))
                    else:
                        if(body[0]==self.ax and body[1]==self.ay ):
                            #redraw apple somewhere else
                            self.ax = 10+ random.randint(2, 15)*self.CELL_SIZE
                            self.ay = 10+random.randint(2, 7)*self.CELL_SIZE  
                            self.index_apple=0
                        # snake head collides with snake body
                        if(self.sxy[0][0]==body[0] and self.sxy[0][1]==body[1] ):
                            self.victory()
                        #draw snake body
                        if(self.sxy[i-1][0]==body[0]-self.CELL_SIZE and self.sxy[i-1][1]==body[1] ):
                            #previous part of body is left
                            if(self.sxy[i+1][0]==body[0]+self.CELL_SIZE and self.sxy[i+1][1]==body[1] ):
                                snake_body = renpy.render(Image("images/snake_game/snake_body_left_right.png"), width, height, st, at)
                            elif(self.sxy[i+1][0]==body[0] and self.sxy[i+1][1]==body[1]-self.CELL_SIZE):
                                snake_body = renpy.render(Image("images/snake_game/snake_body_left_up.png"), width, height, st, at)
                            else:
                                snake_body = renpy.render(Image("images/snake_game/snake_body_left_down.png"), width, height, st, at)

                        elif(self.sxy[i-1][0]==body[0]+self.CELL_SIZE  and self.sxy[i-1][1]==body[1] ):
                            #previous part of body is right
                            if(self.sxy[i+1][0]==body[0]-self.CELL_SIZE and self.sxy[i+1][1]==body[1] ):
                                snake_body = renpy.render(Image("images/snake_game/snake_body_right_left.png"), width, height, st, at)
                            elif(self.sxy[i+1][0]==body[0] and self.sxy[i+1][1]==body[1]-self.CELL_SIZE):
                                snake_body = renpy.render(Image("images/snake_game/snake_body_right_up.png"), width, height, st, at)
                            else:
                                snake_body = renpy.render(Image("images/snake_game/snake_body_right_down.png"), width, height, st, at)
                            

                        elif(self.sxy[i-1][0]==body[0] and self.sxy[i-1][1]==body[1]-self.CELL_SIZE ):
                            #previous part of body is up
                            if(self.sxy[i+1][0]==body[0] and self.sxy[i+1][1]==body[1]+self.CELL_SIZE ):
                                snake_body = renpy.render(Image("images/snake_game/snake_body_up_down.png"), width, height, st, at)
                            elif(self.sxy[i+1][0]==body[0]-self.CELL_SIZE and self.sxy[i+1][1]==body[1]):
                                snake_body = renpy.render(Image("images/snake_game/snake_body_up_left.png"), width, height, st, at)
                            else:
                                snake_body = renpy.render(Image("images/snake_game/snake_body_up_right.png"), width, height, st, at)
                            
                            

                        else :
                            #previous part of body is down
                            if(self.sxy[i+1][0]==body[0] and self.sxy[i+1][1]==body[1]-self.CELL_SIZE ):
                                snake_body = renpy.render(Image("images/snake_game/snake_body_down_up.png"), width, height, st, at)
                            elif(self.sxy[i+1][0]==body[0]-self.CELL_SIZE and self.sxy[i+1][1]==body[1]):
                                snake_body = renpy.render(Image("images/snake_game/snake_body_down_left.png"), width, height, st, at)
                            else:
                                snake_body = renpy.render(Image("images/snake_game/snake_body_down_right.png"), width, height, st, at)
                            
                            
                           

                            
                        
                        render.blit(snake_body, (int(body[0]), int(body[1])))

        
                


            def process_game_step():

                
                if self.end_game==False:
                    # computes distance between snake head and player
                    # shorten the biggest distance (horizontal or vertical)
                    if(abs(self.sxy[0][0]-self.px)>abs(self.sxy[0][1]-self.py)):
                        #move horizontally
                        if(self.sxy[0][0]>self.px ):
                            if(self.snake_head !=  Image("images/snake_game/snake_head_right.png")):
                                self.snake_head_bite =  Image("images/snake_game/snake_head_bite_right.png")
                                self.sxy.insert(0, (self.sxy[0][0]-self.CELL_SIZE, self.sxy[0][1]))
                                self.snake_head =  Image("images/snake_game/snake_head_left.png")
                                self.snake_head_bite =  Image("images/snake_game/snake_head_bite_left.png")
                            else:
                                #move vertically
                                if(self.sxy[0][1]>self.py):
                                    self.sxy.insert(0, (self.sxy[0][0], self.sxy[0][1]-self.CELL_SIZE))
                                    self.snake_head =  Image("images/snake_game/snake_head_up.png")
                                    self.snake_head_bite =  Image("images/snake_game/snake_head_bite_up.png")
                                else:
                                    self.sxy.insert(0, (self.sxy[0][0], self.sxy[0][1]+self.CELL_SIZE))
                                    self.snake_head =  Image("images/snake_game/snake_head_down.png")
                                    self.snake_head_bite =  Image("images/snake_game/snake_head_bite_down.png")
                        else:
                            if(self.snake_head !=  Image("images/snake_game/snake_head_left.png")):
                                self.snake_head_bite =  Image("images/snake_game/snake_head_bite_left.png")
                                self.sxy.insert(0, (self.sxy[0][0]+self.CELL_SIZE, self.sxy[0][1]))
                                self.snake_head =  Image("images/snake_game/snake_head_right.png")
                                self.snake_head_bite =  Image("images/snake_game/snake_head_bite_right.png")
                            else:
                                #move vertically
                                if(self.sxy[0][1]>self.py):
                                    self.sxy.insert(0, (self.sxy[0][0], self.sxy[0][1]-self.CELL_SIZE))
                                    self.snake_head =  Image("images/snake_game/snake_head_up.png")
                                    self.snake_head_bite =  Image("images/snake_game/snake_head_bite_up.png")
                                else:
                                    self.sxy.insert(0, (self.sxy[0][0], self.sxy[0][1]+self.CELL_SIZE))
                                    self.snake_head =  Image("images/snake_game/snake_head_down.png")
                                    self.snake_head_bite =  Image("images/snake_game/snake_head_bite_down.png")
                    else:
                        #move vertically
                        if(self.sxy[0][1]>self.py):
                            if(self.snake_head !=  Image("images/snake_game/snake_head_down.png")):
                                self.snake_head_bite =  Image("images/snake_game/snake_head_bite_down.png")
                                self.sxy.insert(0, (self.sxy[0][0], self.sxy[0][1]-self.CELL_SIZE))
                                self.snake_head =  Image("images/snake_game/snake_head_up.png")
                                self.snake_head_bite =  Image("images/snake_game/snake_head_bite_up.png")
                            else:
                                if(self.sxy[0][0]>self.px  ):
                                        self.sxy.insert(0, (self.sxy[0][0]-self.CELL_SIZE, self.sxy[0][1]))
                                        self.snake_head =  Image("images/snake_game/snake_head_left.png")
                                        self.snake_head_bite =  Image("images/snake_game/snake_head_bite_left.png")
                                else:
                                        self.sxy.insert(0, (self.sxy[0][0]+self.CELL_SIZE, self.sxy[0][1]))
                                        self.snake_head =  Image("images/snake_game/snake_head_right.png")
                                        self.snake_head_bite =  Image("images/snake_game/snake_head_bite_right.png")
                        else:
                            if(self.snake_head !=  Image("images/snake_game/snake_head_up.png")):
                                self.snake_head_bite =  Image("images/snake_game/snake_head_bite_up.png")
                                self.sxy.insert(0, (self.sxy[0][0], self.sxy[0][1]+self.CELL_SIZE))
                                self.snake_head =  Image("images/snake_game/snake_head_down.png")
                                self.snake_head_bite =  Image("images/snake_game/snake_head_bite_down.png")
                            else:
                                if(self.sxy[0][0]>self.px  ):
                                    self.sxy.insert(0, (self.sxy[0][0]-self.CELL_SIZE, self.sxy[0][1]))
                                    self.snake_head =  Image("images/snake_game/snake_head_left.png")
                                    self.snake_head_bite =  Image("images/snake_game/snake_head_bite_left.png")
                                else:
                                    self.sxy.insert(0, (self.sxy[0][0]+self.CELL_SIZE, self.sxy[0][1]))
                                    self.snake_head =  Image("images/snake_game/snake_head_right.png")
                                    self.snake_head_bite =  Image("images/snake_game/snake_head_bite_right.png")
                        
                    # snake head collides with player
                    if(self.sxy[0][0]==self.px and self.sxy[0][1]==self.py):
                        self.snake_head=self.snake_head_bite
                        renpy.sound.play(snake_eating_sound)
                        self.end_game=True
                        if mini_game==True:
                            self.end_text="PERDU !\nAppuyez sur Entrée pour rejouer\nou Echap pour quitter"
                        else:
                            self.end_text="PERDU !\nAppuyez sur Entrée pour rejouer\nou Echap pour poursuivre l'histoire"


                

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


                
            # player cannot go out
            self.check_player_keep_in()
         
            # draw everything
            self.draw_apple(render, width, height, st, at)

            #hide player if lost
            if self.end_game!=True:
                self.draw_player(render, width, height, st, at)


            snake(self.sxy)
            

            # make snake move at interval
            self.snake_accumulated_time += dtime
            self.apple_accumulated_time += dtime
            self.last_player_move_accumulated_time += dtime
            self.start_player_move += dtime


            # show player standing when not moving
            if self.last_player_move_accumulated_time >= self.PLAYER_STANDING:
                self.last_player_move_accumulated_time -= self.PLAYER_STANDING
                self.player = Image("images/snake_game/player_stand.png")
                

            # show player second move
            if self.start_player_move >= self.PLAYER_MOVE_DURATION and self.player_moving:
                if self.index_player_move==1:
                    
                    self.start_player_move -= self.PLAYER_MOVE_DURATION

                    self.compute_player_move()

                    self.last_player_move_accumulated_time=0
                else :
                    self.player_moving=False
                    

            # move snake
            if self.snake_accumulated_time >= self.SNAKE_FRAME_DURATION:
                self.snake_accumulated_time -= self.SNAKE_FRAME_DURATION
                process_game_step()

           
           
            # redraw the screen
            renpy.redraw(self, 0)

            # Return the Render object.
            return render


        # show screen after game (home screen or next screen of history)
        def show_next_screen(self):
                self.__init__()
                renpy.jump("after_snake_game")

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

            if  ev.type == pygame.KEYDOWN  and ev.key == pygame.K_RETURN and self.end_game==True :
                if self.victory==True:
                    self.show_next_screen()
                if self.end_game:
                    self.__init__()


            # player move up
            if self.end_game == False and ev.type == pygame.KEYDOWN   and ev.key == pygame.K_UP and (self.py != self.ay + self.CELL_SIZE or  self.px!=self.ax):
                if not self.player_moving:
                    collide=False
                    for body in self.sxy:
                        if (self.py == body[1] + self.CELL_SIZE and self.px==body[0]):
                            collide=True
                    
                    if collide != True:
                        self.direction=DirectionEnum.UP
                        self.initial_player_move()
                raise renpy.IgnoreEvent()


            # player move down
            if self.end_game == False and ev.type == pygame.KEYDOWN and ev.key == pygame.K_DOWN and (self.py != self.ay - self.CELL_SIZE or self.px!=self.ax ):
                if not self.player_moving:
                    collide=False
                    

                    for body in self.sxy:
                        if (self.py == body[1] - self.CELL_SIZE and self.px==body[0]):
                            collide=True
                    
                    if collide != True:
                        self.direction=DirectionEnum.DOWN
                        self.initial_player_move()
                raise renpy.IgnoreEvent()


            # player move right
            if self.end_game == False and ev.type == pygame.KEYDOWN and ev.key == pygame.K_RIGHT and (self.px != self.ax - self.CELL_SIZE or self.py!=self.ay):
               
                if not self.player_moving:
                    collide=False
                    
                    for body in self.sxy:
                        if (self.px == body[0] - self.CELL_SIZE and self.py==body[1]):
                            collide=True
                    
                    if collide != True:
                        self.direction=DirectionEnum.RIGHT
                        self.initial_player_move()
                       
                        
                raise renpy.IgnoreEvent()


            # player move left
            if self.end_game == False and ev.type == pygame.KEYDOWN and ev.key == pygame.K_LEFT and (self.px != self.ax + self.CELL_SIZE or self.py!=self.ay):
                
                if not self.player_moving:
                    collide=False
                    
                    for body in self.sxy:
                        if (self.px == body[0] + self.CELL_SIZE and self.py==body[1]):
                            collide=True
                    
                    if collide != True:
                        self.direction=DirectionEnum.LEFT
                        self.initial_player_move()
                raise renpy.IgnoreEvent()

            # Ensure the screen updates
            renpy.restart_interaction()
            raise renpy.IgnoreEvent()    

    def display_end_game_text(st, at):
            return Text( snake_game.end_text, font='gui/jd_code.ttf', size=50, color="#33e43c"), .1

    def display_end_game_background(st, at):
        if snake_game.end_game == True:
            return Image("images/snake_game/mini_game_end_background.png"), 30
        else :
            return Null(width=0), .1

default snake_game = SnakeGameDisplayable()


# label to start snake game
label start_snake_game:
    play music snake_game_music
    window hide  # Hide the window and quick menu while in mini game
    $ quick_menu = False
    call screen snake_game


#start snake game
screen snake_game():
    add "images/snake_game/background_snake.png"
    add snake_game
    add DynamicDisplayable(display_end_game_background) 
    add DynamicDisplayable(display_end_game_text) xalign 0.5 yalign 0.5 
    
   