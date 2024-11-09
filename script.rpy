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
define virgile= Character(image='virgile' , kind=bubble, what_style="dialog_text")

screen show_chapter :

    add Text("[chapter_title]", font='gui/jd_code.ttf', size=50, color="#33e43c")  xalign 0.5 yalign 0.5 
    timer 2 action [Hide("show_chapter")]
        
screen show_chapter_optional_background :

    add Image("images/snake_game/mini_game_end_background.png") xalign 0.5 yalign 0.5 
    timer 3 action [Hide("show_chapter_optional_background")]
        

# start of the game
label start:

    #jump start_chapter_1
    jump start_chapter_2
    


