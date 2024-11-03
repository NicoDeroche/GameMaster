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


        

# start of the game
label start:
    jump start_chapter_1
  
    #jump start_chapter_2
    


