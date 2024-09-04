style dialog_text is text:
    size 20
    font "gui/ShortStack.ttf"
    color "#000"
    xalign 0.5
    yalign 0.5



# start mini game
label start_mini_game:
    $ mini_game=True
    jump start_snake_game





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
    ypos 500
    xpos -200
    linear 5 xpos 1500


transform zoomOut:
    xalign 0.5
    yalign 0.5
    linear 2.5 rotate 360 zoom 0


transform zoomIn:
    xalign 0.5
    yalign 0.5
    zoom 0
    linear 2.5 rotate 360 zoom 1




transform snakeMove:
    linear 1 xoffset -10 yoffset +10 zoom 1.15
    

transform snakeMove2:
    linear 1 xoffset -20 yoffset +20 zoom 1.30
    

transform snakeMove3:
    linear 1 xoffset -30 yoffset +30 zoom 1.45
    

transform positionChaussures:
    xalign 0.7
    yalign 0.5




# start of the game
label start:
    stop music
    $ mini_game=False
   

    scene bg maison nuit
    pause 2
    show smartphone at shake
    play music ringtone
    pause 2
    ed "Hum ?"
    ed "Je dors !"
    ed "Elle insiste, la sadique..."
    hide smartphone
    stop music

    scene bg maison matin
    show ed smile  at left with dissolve
    ed "Oui, allo ?"
    show julie talk at right with dissolve
    julie "Salut frangin, ça roule ?"
    julie "Je venais juste aux nouvelles..."
    show ed surprised at left  with dissolve
    ed "A propos de quoi ?"
    julie "Des sélections de {b}Game Master{/b}, bien sûr !"
    julie "Il y a du monde ?"
    ed "Les sélections de Game Mast..."
    show ed shame at left  with dissolve
    ed "Nom d'un ouistiti !"
    ed "Mon réveil n'a pas sonné !"
    show julie smile at right  with dissolve
    julie "Tu déconnes !?"
    julie "Les candidats sont attendus à 10h, et il est 9h30 !"
    show ed think at left with dissolve
    #ed regarde sa montre
    ed "Le rendez-vous est bien dans la zone industrielle ?"
    julie "Oui, ils ont loué un entrepôt..."
    ed "Alors c'est encore jouable !"
    ed "Je m'habille en vitesse, et je file."
    ed "Je te tiens au courant."
    ed "A plus, frangine !"
    #leo content
    show julie smile with dissolve
    julie "A plus, Ed..."

    hide ed
    hide julie

    show bg car transition
    show car transition at zoomOut
    pause 2.5
    show chaussures at zoomIn
    pause 2.5
    hide car transition
    hide chaussures

    scene bg maison jour
    #TODO il ne faut pouvoir cliquer sur les clés que après
    
    show ed shame at left with dissolve


    #ed pas content
    ed "L'entrepôt se situe dans la Z.I. de la Coquillette"
    ed "J'y serai dans 10 mn"
    ed "il faut juste que je me rappelle où j'ai rangé mes chaussures"
    call screen chaussures_click

screen chaussures_click:
    imagebutton:
        xpos 0.76
        ypos 0.9
        idle "chaussures click.png"
        action Jump("chaussuresTrouvees")

label chaussuresTrouvees :
    scene bg maison jour
  
    show chaussures at positionChaussures with dissolve
    show ed smile at left with dissolve
    ed "Ah, les voilà !"
    ed "C'est parti !"


    hide chaussures
    hide ed

    show bg car transition
    play sound car_pass_by_sound
    show car transition at carPosition
    pause 5
    hide car transition


    stop sound
    show bg parking
    show ed smile at left with dissolve
    ed "Il est 9h55, ça devrait être bon...."
    chris "Toi aussi tu es à la bourre ?"
    ed "Pardon ?"
    show chris sad at right with dissolve
    chris "Ma voiture est tombée en panne à 10 kms d'ici."
    chris "J'ai été obligé de venir en courant..."
    show chris smile at right with dissolve
    chris "Et toi, qu'est-ce qui t'est arrivé ?"
    show ed shame at left with dissolve
    ed "Moi ? Euh..."
    menu:
        "J'ai eu une panne de réveil":
            jump panne_reveil
        "C'est une longue histoire...":
            jump longue_histoire

label panne_reveil:
    chris "Ha ha, ça arrive toujours au mauvais moment !"
    jump fin_explication

label longue_histoire:
    chris "Ha ha, ça sent la panne de réveil,  ça !"
    jump fin_explication

label fin_explication:
    hide ed
    hide chris
    show sylvie write with dissolve
    sylvie "Bonjour messieurs !"
    sylvie "Je me présente : {b}Sylvie Cristal{/b} !\nJ'organise les sélections de votre région."
    sylvie "Vous pouvez me donner vos noms ?"
    hide sylvie
    show chris smile at right with dissolve
    chris "Bien sûr ! Je suis {b}Christophe Tonga{/b}."
    show ed smile at left with dissolve
    ed "Et moi {b}Edouard Pinson{/b}."
    hide ed
    hide chris
    show sylvie smile with dissolve
    sylvie "Très bien, c'est noté !"
    sylvie "Veuillez me suivre, nous allons rejoindre les autres candidats."

    scene bg entrepot
    show sylvie smile at left with dissolve
    sylvie "Messieurs dames,\nles sélections de {b}Game Master{/b} vont commencer !"
    sylvie "Cette compétition est organisée par {b}Virgile Brizor{/b}, pdg de {b}B-Tech{/b} et pionnier de l'I.A."
    sylvie "Le principe est simple :\nà chaque épreuve, vous devrez affronter des robots conçus par B-Tech."
    hide sylvie
    show ed surprised at left with dissolve
    ed "Des robots géants, c'est trop cool !"
    ed "Mais, euh... Ce n'est pas un tournoi de jeux vidéo ?"
    hide ed
    show sylvie smile at left with dissolve
    sylvie "Je pense qu'il y a méprise..."
    sylvie "Pour que ce soit plus fun, les épreuves sont inspirées de jeux vidéo célèbres."
    sylvie "Mais les créatures que vous affronterez seront bien réelles !"
    hide sylvie
    show ed surprised at left with dissolve
    ed "Ah... Ce n'est pas un peu dangereux ?"
    hide ed
    show sylvie smile at left with dissolve
    sylvie "Votre mental et votre physique seront mis à rude épreuve, c'est certain."
    show chris smile at right with dissolve
    chris "Et quel est le prix pour le gagnant ?"
    hide chris
    hide ed
    show sylvie smile at left with dissolve
    sylvie "Le gagnant de la compétition remportera la somme de\n{b}100 000 €{/b}."
    hide sylvie
    show chris smile at right with dissolve
    chris "Ok, je vais me donner à fond !"
    hide chris
    show sylvie smile at left with dissolve
    sylvie "Je vais vous appeler à tour de rôle pour me rejoindre devant l'entrepôt."
    sylvie "Si vous remportez l'épreuve, vous serez qualifiés."
    sylvie "La suite de la compétition se passera au siège de la B-Tech,\net sera diffusée en streaming sur Internet."

    scene bg entree entrepot
    show sylvie smile at right with dissolve
    sylvie "Candidat suivant : Edouard Pinson !"
    show ed shame at left with dissolve
    ed "Je suis là..."
    sylvie "Veuillez signer cette décharge. C'est pour nous couvrir en cas d'accident."
    show ed surprised at left with dissolve
    ed "D'accident ?"
    sylvie "Je vous l'ai dit, cette compétition n'est pas sans risque."

    menu:
        "Ok, je signe.\n Si c'est basé sur les jeux vidéo, j'ai mes chances.":
            jump entree_entrepot

        "Non, désolé, tout ceci me semble un peu trop dangereux.":
            jump again_entree


label again_entree:
    show ed surprised at left with dissolve
    ed "Quand même..."
    ed "Il y a 100 000 € à la clé... Ce n'est pas rien."

    menu:
        "Bon d'accord, je signe.":
            jump entree_entrepot

        "Non, j'ai trop peur.":
            jump again_entree

label entree_entrepot :
    sylvie "Merci, tout est en ordre."
    sylvie "Amusez-vous bien !"
    scene bg interieur entrepot
    show apple big at applePos with dissolve
    show snake at snakePos with dissolve
    play sound snake_coming_sound
    snake "Sssssssssssssss"
    show ed smile at left with dissolve
    ed "C'est ça leur robot géant ?"
    ed "Ha ha ha !"
    ed "Il n'a pas l'air très menaçant."
    ed "Voyons... Il y a aussi une pomme."
    ed "C'est comme dans ce vieux jeu sur portable."
    show snake at snakeMove
    show ed surprised at left with dissolve
    ed "Tiens, il bouge !\n Trop stylé !"
    show snake at snakeMove2
    play sound snake_coming_sound
    ed "Euh... Attends..."
    show snake at snakeMove3
    ed "Nom d'un clafoutis !"
    ed "C'est après moi qu'il en a !"
    "Attention, ça va commencer !\nUtilisez les flèches de direction pour vous déplacer. "
    jump start_snake_game



    
label after_snake_game:
    stop music
    window auto  
    $ quick_menu = True
    if mini_game==False:
        scene bg entree entrepot
        show sylvie smile at right with dissolve
        show ed smile at left with dissolve
        sylvie "Bravo Mr Pinson, vous êtes qualifiés !"
        hide sylvie
        chris "Bien joué mec !"
        show chris smile at right with dissolve
        chris "Tu as un physique de crevette, mais je savais que tu allais assurer !"
        ed "Euh... merci."
        hide chris
        show sylvie smile at right with dissolve
        sylvie "Mr Tonga a également réussi cette épreuve."
        sylvie "Il me reste quelques candidats à faire passer."
        sylvie "L'hélicoptère viendra chercher les compétiteurs sélectionnés d'ici 15 mn."
        sylvie "Je vous laisse aller chercher votre sac de voyage dans votre véhicule ?"
        show ed surprised at left with dissolve
        ed "Nom d'une salsifi !!!"
        ed "Je n'ai pas pris de sac !"
    else :
        play music main_menu
        call screen main_menu
  
