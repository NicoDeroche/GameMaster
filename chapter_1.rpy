


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




# start of the first chapter
label start_chapter_1:
    stop music
    $ mini_game=False
 

    scene bg maison nuit
    show screen show_chapter_1
    pause 3
    show smartphone at shake
    play music ringtone
    pause 2
    ed "Hum ?"
    ed "Je dors !"
    ed "Elle insiste, la sadique..."
    hide smartphone
    stop music

   
    show ed pyjama sourire  at left with dissolve
    ed "Oui, allo ?"
    show julie parle at right with dissolve
    julie "Salut frangin, ça roule ?"
    julie "Je venais juste aux nouvelles..."
    show ed pyjama sceptique at left with dissolve
    ed "A propos de quoi ?"
    show julie surprise at right with dissolve
    julie "Des sélections de {b}Game Master{/b}, bien sûr !"
    julie "Il y a du monde ?"
    ed "Les sélections de Game Mast..."
    show ed pyjama surpris at left with dissolve
    ed "{i}NOM D'UN CLAFOUTIS !{/i}"
    ed "Mon réveil n'a pas sonné !"
    show julie colere at right with dissolve
    julie "Tu déconnes !?"
    julie "Les candidats sont attendus à 10h, et il est 9h30 !"
    show ed pyjama pense  at left with dissolve
    ed "Le rendez-vous est bien dans la zone industrielle ?"
    show julie surprise at right with dissolve
    julie "Oui, ils ont loué un entrepôt..."
    ed "Alors c'est encore jouable !"
    ed "Je m'habille en vitesse, et je file."
    show julie parle at right with dissolve
    show ed pyjama sourire  at left with dissolve
    ed "Je te tiens au courant."
    ed "A plus, frangine !"
    show julie sourire at right with dissolve
    julie "A plus, Ed..."

    hide ed
    hide julie



    scene bg maison jour with Pixellate(3,5)

    
    show ed chemise sourire at left with dissolve
    ed "L'entrepôt se situe dans la Z.I. de la Coquillette."
    ed "J'y serai dans 10 mn."
    show ed chemise pense at left with dissolve
    ed "Il faut juste que je me rappelle où j'ai rangé mes chaussures..."
    call screen chaussures_click

screen chaussures_click:
    imagebutton:
        xpos 0.65
        ypos 0.76
        idle "chaussures click.png"
        action Jump("chaussuresTrouvees")

label chaussuresTrouvees :
    scene bg maison jour
  
    show chaussures at positionChaussures with dissolve
    show ed chemise heureux at left with dissolve
    ed "Ah, les voilà !"
    ed "Let's a go !"


    hide chaussures
    hide ed

    show bg car transition
    play sound car_pass_by_sound
    show car transition at carPosition
    pause 5
    hide car transition


    stop sound
    show bg parking
    show ed chemise sourire at left with dissolve
    ed "Il est 9h55, ça devrait être bon...."
    chris "Toi aussi tu es à la bourre ?"
    show chris bras croises at right with dissolve
    chris "Ma voiture est tombée en panne à 10 kms d'ici."
    chris "J'ai été obligé de venir en courant..."
    show chris mains poches at right with dissolve
    chris "Et toi, qu'est-ce qui t'est arrivé ?"
    show ed chemise gene at left with dissolve
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
    show sylvie sourire with dissolve
    sylvie "Bonjour messieurs !"
    sylvie "Je me présente : {b}Sylvie Cristal{/b} !\nJ'organise les sélections de la zone Ouest."
    sylvie "Vous pouvez me donner vos noms ?"
    hide sylvie
    show chris bras croises at right with dissolve
    chris "Bien sûr ! Je suis {b}Christophe Tonga{/b}."
    show ed chemise sourire at left with dissolve
    ed "Et moi {b}Edouard Pinson{/b}."
    hide ed
    hide chris
    show sylvie ecrit with dissolve
    sylvie "Très bien, c'est noté !"
    show sylvie sourire with dissolve
    sylvie "Veuillez me suivre, nous allons rejoindre les autres candidats."

    scene bg entrepot
    show sylvie sourire at left with dissolve
    sylvie "Messieurs dames,\nles sélections de {b}Game Master{/b} vont commencer !"
    sylvie "Cette compétition est organisée par {b}Virgile Brizor{/b}, pdg de {b}B-Tech{/b} et pionnier de la robotique."
    sylvie "Le principe est simple :\nà chaque épreuve, vous devrez affronter des robots conçus par B-Tech."
    show ed chemise heureux at right with dissolve
    ed "Des robots géants, c'est trop cool !"
    show ed chemise main levee at right with dissolve
    ed "Mais, euh... Ce n'est pas un tournoi de jeux vidéo ?"
    sylvie "Je pense qu'il y a méprise..."
    show ed chemise sceptique at right with dissolve
    sylvie "Pour que ce soit plus fun, les épreuves sont inspirées de jeux vidéo célèbres."
    sylvie "Mais les créatures que vous affronterez seront bien réelles !"
    show ed chemise surpris at right with dissolve
    ed "Ah... Ce n'est pas un peu dangereux ?"


    sylvie "Votre mental et votre physique seront mis à rude épreuve, c'est certain."
    hide ed
    show chris mains poches at right with dissolve
    chris "Et quel est le prix pour le gagnant ?"
    sylvie "Le gagnant de la compétition remportera la somme de\n{b}100 000 €{/b}."
    show chris bras leves at right with dissolve
    chris "Ok, je vais me donner à fond !"
    sylvie "Je vais vous appeler à tour de rôle pour me rejoindre devant l'entrepôt."
    sylvie "Si vous remportez l'épreuve, vous serez qualifiés."
    sylvie "La suite de la compétition se passera au siège de la B-Tech,\net sera diffusée en streaming sur Internet."

    scene bg entree entrepot with Pixellate(3,5)
    show sylvie ecrit at left with dissolve
    sylvie "Candidat suivant : Edouard Pinson !"
    show ed chemise sourire at right with dissolve
    ed "Je suis là..."
    show sylvie sourire at left with dissolve
    sylvie "Veuillez signer cette décharge. C'est pour nous couvrir en cas d'accident."
    show ed chemise surpris at right with dissolve
    ed "D'accident ?"
    sylvie "Je vous l'ai dit, cette compétition n'est pas sans risque."
    show ed chemise pense at right with dissolve
    menu:
        "Ok, je signe.\n Si c'est basé sur les jeux vidéo, j'ai mes chances.":
            jump entree_entrepot

        "Non, désolé, tout ceci me semble un peu trop dangereux.":
            jump again_entree


label again_entree :
    ed "Quand même..."
    ed "Il y a 100 000 € à la clé... Ce n'est pas rien."

    menu:
        "Bon d'accord, je signe.":
            jump entree_entrepot

        "Non, j'ai trop peur.":
            jump again_entree

label entree_entrepot :
    show ed chemise sourire at right with dissolve
    sylvie "Merci, tout est en ordre."
    sylvie "Amusez-vous bien !"
    scene bg interieur entrepot
    #show apple big at applePos with dissolve
    #show snake at snakePos with dissolve
    show ed chemise heureux at right with dissolve
    ed "J'hallucine !\nUn robot serpent !"
    show ed chemise pense at right with dissolve
    ed "Il y a aussi une pomme..."
    ed "C'est comme dans ce vieux jeu sur portable."
    scene bg interieur entrepot bis
    show ed chemise sourire at right with dissolve
    play sound snake_coming_sound
    snake "Sssssssssssssss"
    #show snake at snakeMove
  
    ed "Et en plus il fait du bruit et il bouge !"
    show ed chemise heureux at right with dissolve
    ed "Trop stylé !"
    scene bg interieur entrepot ter
    show ed chemise heureux at right with dissolve
    play sound snake_coming_sound
    snake "Sssssssssssssss"
    show ed chemise sceptique at right with dissolve
 
    ed "Euh... Attends..."
    show ed chemise surpris at right with dissolve
    ed "{i}NOM D'UN SALSIFIS !{/i}"
    ed "Il veut me bouffer !"
    jump start_snake_game



    
label after_snake_game:
    stop music
    window auto  
    if mini_game==False:
        scene bg entree entrepot
        show sylvie sourire at left with dissolve
        show ed chemise sourire at right with dissolve
        sylvie "Bravo Mr Pinson, vous êtes qualifiés !"
        hide sylvie
        chris "Bien joué mec !"
        show chris bras croises at left with dissolve
        chris "Tu as un physique de crevette, mais je savais que tu allais assurer !"
        show ed chemise gene at right with dissolve
        ed "Euh... merci."
        hide chris
        show sylvie sourire at left with dissolve
        show ed chemise sourire at right with dissolve
        sylvie "Mr Tonga a également réussi cette épreuve."
        sylvie "Il me reste quelques candidats à faire passer."
        sylvie "L'hélicoptère viendra chercher les compétiteurs sélectionnés d'ici 15 mn."
        sylvie "Je vous laisse aller chercher votre sac de voyage dans votre véhicule ?"
        show ed chemise surpris at right with dissolve
        ed "{i}NOM D'UN OUISTITI !{/i}"
        ed "Je n'ai pas pris de sac !"

        stop music
        window hide  # Hide the window and quick menu while in mini game
        call screen end_chapter_1
    else :
        call screen mini_games


screen show_chapter_1 :

    add Text(_("Chapitre 1 : Serpent mécanique"), font='gui/jd_code.ttf', size=50, color="#77d079")  xalign 0.5 yalign 0.5 
    timer 2 action [Hide("show_chapter_1")]


#end chapter
screen end_chapter_1():

    
    add Image("images/snake_game/mini_game_end_background.png") xalign 0.5 yalign 0.5 
    add Text(_("BRAVO !!!!\nVous avez terminé le Chapitre 1 de Game Master !\nLe Chapitre 2 est en cours de développement...\n\nMerci d'avoir joué à ce jeu !\nS'il vous a plu, merci de mettre un commentaire sur itch.io, ça me boostera !"), font='gui/jd_code.ttf', size=50, color="#77d079")  xalign 0.5 yalign 0.5 
    textbutton _("Menu principal"):
        style "return_button"

        action MainMenu()