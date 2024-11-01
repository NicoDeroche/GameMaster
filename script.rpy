style dialog_text is text:
    size 20
    font "gui/ShortStack.ttf"
    color "#000"
    xalign 0.5
    yalign 0.5






# characters of the story
define julie = Character(image='julie', kind=bubble, what_style="dialog_text")
define ed = Character(image='ed' , kind=bubble, what_style="dialog_text")
define smartphone= Character(image='smartphone' , kind=bubble, what_style="dialog_text")
define sylvie= Character(image='sylvie' , kind=bubble, what_style="dialog_text")
define car= Character(image='car' , kind=bubble, what_style="dialog_text")
define chris= Character(image='chris' , kind=bubble, what_style="dialog_text")
define snake= Character(image='snake' , kind=bubble, what_style="dialog_text")



# transformations
transform shake(rate=0.090):
    xalign 0.8
    yalign 0.5
    linear rate xoffset 2 yoffset -6
    linear rate xoffset -2.8 yoffset -2
    linear rate xoffset 2.8 yoffset -2
    linear rate xoffset -2 yoffset -6
    linear rate xoffset +0 yoffset +0
    repeat

transform middle:
    xalign 0.5
    yalign 0.2


transform applePos:
    xalign 0.4
    yalign 0.6

transform snakePos:
    xalign 0.7
    yalign 0.6



    
transform carPosition:
    ypos 280
    xpos -200
    linear 5 xpos 1500



transform snakeMove:
    linear 1 xoffset -10 yoffset +10 zoom 1.15
    

transform snakeMove2:
    linear 1 xoffset -20 yoffset +20 zoom 1.30
    

transform snakeMove3:
    linear 1 xoffset -30 yoffset +30 zoom 1.45
    

transform positionChaussures:
    xalign 0.65
    yalign 0.55




# start of the game
label start:
    jump start_chapter_1