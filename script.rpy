


# start mini game
label start_mini_game:
    $ mini_game=True
    jump start_snake_game





# characters of the story
define l = Character(image='lou', kind=bubble)
define e = Character(image='ed' , kind=bubble)
define s= Character(image='smartphone' , kind=bubble)
define y= Character(image='yuri' , kind=bubble)
define car= Character(image='car' , kind=bubble)
define c= Character(image='chris' , kind=bubble)
define sn= Character(image='snake' , kind=bubble)


# transformations
transform shake(rate=0.090):
    xalign 0.5
    yalign 0.2
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



    
transform middlePause:
    zoom 0
    pause 1
    zoom 1
    xalign 0.3
    yalign 0.1


transform snakeMove:
    linear 1 xoffset -10 yoffset +10 zoom 1.15
    

transform snakeMove2:
    linear 1 xoffset -20 yoffset +20 zoom 1.30
    

transform snakeMove3:
    linear 1 xoffset -30 yoffset +30 zoom 1.45
    

transform positionCles:
    xalign 0.7
    yalign 0.5


transform positionClesMiniature:
        xpos 0.40
        ypos 0.75


# start of the game
label start:
    stop music
    $ mini_game=False
   

    scene black
    show smartphone at shake
    s "DRIIIIIIIIIIIIIING !"
    hide smartphone

    scene bg maison chambre
    show ed smile  at left with dissolve
    e "Oui, allo ?"
    show lou smile at right with dissolve
    l "Salut frangin, ça roule ?"
    l "Je venais juste aux nouvelles..."
    show ed surprised at left  with dissolve
    e "A propos de quoi ?"
    l "Des sélections de {b}Game Master{/b}, bien sûr !"
    l "Il y a du monde ?"
    e "Les sélections de Game Mast..."
    show ed shame at left  with dissolve
    e "Holy crab !!!"
    e "Mon réveil n'a pas sonné !"
    show lou angry at right  with dissolve
    l "Tu déconnes !?"
    l "Les candidats sont attendus à 10h, et il est 9h30 !"
    show ed think at left with dissolve
    #ed regarde sa montre
    e "Le rendez-vous est bien dans la zone industrielle ?"
    l "Oui, ils ont loué un entrepôt..."
    e "Alors c'est encore jouable !"
    e "Je m'habille en vitesse, et je file."
    e "Je te tiens au courant."
    e "A plus, frangine !"
    #leo content
    show lou smile with dissolve
    l "A plus, Ed..."

    scene bg maison sejour
    #TODO il ne faut pouvoir cliquer sur les clés que après
    
    show ed shame at left with dissolve

    show cles voiture miniature at positionClesMiniature
    #ed pas content
    e "Rah, la poisse !"
    e "Où j'ai mis mes clés de voiture ?"
    call screen cles_voiture

screen cles_voiture:
    imagebutton:
        xpos 0.40
        ypos 0.75
        idle "cles voiture miniature.png"
        action Jump("cleTrouvee")

label cleTrouvee :
    scene bg maison sejour
  
    show cles voiture at positionCles with dissolve
    show ed smile at left with dissolve
    e "Ah, les voilà !"
    e "Let's-a go !"


    hide cles voiture
    hide ed

    show bg road
    show car at middlePause
    pause 1
    car "VRRRRRRRRRRROAR  !"
    hide car

    show bg parking
    show ed smile at left with dissolve
    e "Il est 9h55, ça devrait être bon...."
    c "Toi aussi tu es à la bourre ?"
    e"Pardon ?"
    show chris sad at right with dissolve
    c "Ma voiture est tombée en panne à 10 kms d'ici."
    c "J'ai été obligé de venir en courant..."
    show chris smile at right with dissolve
    c "Et toi, qu'est-ce qui t'est arrivé ?"
    show ed shame at left with dissolve
    e "Moi ? Euh..."
    menu:
        "J'ai eu une panne de réveil":
            jump panne_reveil
        "C'est une longue histoire...":
            jump longue_histoire

label panne_reveil:
    c "Ha ha, ça arrive toujours au mauvais moment !"
    jump fin_explication

label longue_histoire:
    c "Ha ha, ça sent la panne de réveil,  ça !"
    jump fin_explication

label fin_explication:
    hide ed
    hide chris
    show yuri smile with dissolve
    y "Bonjour messieurs !"
    y "Je suis {b}Yuri Tanaka{/b}, et je m'occupe des sélections dans votre région."
    y "Vous pouvez me donner vos noms ?"
    hide yuri
    show chris smile at right with dissolve
    c "Bien sûr ! Je suis {b}Christophe Tonga{/b}."
    show ed smile at left with dissolve
    e "Et moi {b}Edouard Pinson{/b}."
    hide ed
    hide chris
    show yuri smile with dissolve
    y "Très bien, c'est noté !"
    y "Veuillez me suivre, nous allons rejoindre les autres candidats."

    scene bg entrepot
    show yuri smile at left with dissolve
    y "Messieurs dames,\n les sélections de {b}Game Master{/b}\nvont commencer !"
    y "Cette compétition est organisée par {b}Virgile Brizor{/b},\npdg de B-Tech et pionnier de l'I.A."
    y "Le principe est simple : à chaque épreuve,\n vous devrez affronter des robots conçus par B-Tech."
    hide yuri
    show ed surprised at left with dissolve
    e "Des robots géants, c'est trop cool !"
    e "Mais, euh... Ce n'est pas un tournoi de jeux vidéo ?"
    hide ed
    show yuri smile at left with dissolve
    y "Je pense qu'il y a méprise..."
    y "Pour que ce soit plus fun, les épreuves sont inspirées de jeux vidéo célèbres."
    y "Mais les créatures que vous affronterez seront bien réelles !"
    hide yuri
    show ed surprised at left with dissolve
    e "Ah... Ce n'est pas un peu dangereux ?"
    hide ed
    show yuri smile at left with dissolve
    y "Votre mental et votre physique seront mis à rude épreuve, c'est certain."
    show chris smile at right with dissolve
    c "Et quel est le prix pour le gagnant ?"
    hide chris
    hide ed
    show yuri smile at left with dissolve
    y "Le gagnant de la compétition remportera la somme de {b}100 000 €{/b}."
    hide yuri
    show chris smile at right with dissolve
    c "Ok, je vais me donner à fond !"
    hide chris
    show yuri smile at left with dissolve
    y "Je vais vous appeler à tour de rôle pour me rejoindre devant l'entrepôt."
    y "Si vous remportez l'épreuve, vous serez qualifiés."
    y "La suite de la compétition se passera au siège de la B-Tech."

    scene bg entree entrepot
    show yuri smile at right with dissolve
    y "Candidat suivant : Edouard Pinson !"
    show ed shame at left with dissolve
    e "Je suis là..."
    y "Veuillez signer cette décharge.\n C'est pour nous couvrir en cas d'accident."
    show ed surprised at left with dissolve
    e "D'accident ?"
    y "Je vous l'ai dit, cette compétition n'est pas sans risque."

    menu:
        "Ok, je signe.\n Si c'est basé sur les jeux vidéo, j'ai mes chances.":
            jump entree_entrepot

        "Non, désolé, tout ceci me semble un peu trop dangereux.":
            jump again_entree


label again_entree:
    show ed surprised at left with dissolve
    e "Quand même..."
    e "Il y a 100 000 € à la clé... Ce n'est pas rien."

    menu:
        "Bon d'accord, je signe.":
            jump entree_entrepot

        "Non, j'ai trop peur.":
            jump again_entree

label entree_entrepot :
    y "Merci, tout est en ordre."
    y "Amusez-vous bien !"
    scene bg interieur entrepot
    show apple big at applePos with dissolve
    show snake at snakePos with dissolve
    sn "SSSSSSSSSSSSSS"
    show ed smile at left with dissolve
    e "C'est ça leur robot géant ?"
    e "Ha ha ha !"
    e "Il n'a pas l'air très menaçant."
    e "Voyons... Il y a aussi une pomme."
    e "C'est comme dans ce vieux jeu sur portable."
    show snake at snakeMove
    show ed surprised at left with dissolve
    e "Tiens, il bouge !\n Trop stylé !"
    show snake at snakeMove2
    e "Euh... Attends..."
    show snake at snakeMove3
    e "Holy crab !!!"
    e "C'est après moi qu'il en a !"
    "Attention, ça va commencer !\nUtilisez les flèches de direction pour vous déplacer. "
    jump start_snake_game



    
label after_snake_game:
    stop music
    window auto  
    $ quick_menu = True
    if mini_game==False:
        scene bg entree entrepot
        show yuri smile at right with dissolve
        y "Bravo Mr Pinson, vous êtes qualifiés !"
    else :
        play music main_menu
        call screen main_menu
  
