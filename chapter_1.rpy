


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
    ypos 277
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
    play sound hum_sound
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
    play sound huh_sound
    ed "Les sélections de Game Mast..."
    play sound what_sound
    show ed pyjama surpris at left with vpunch
    ed "{i}NOM D'UN CLAFOUTIS !{/i}"
    show ed pyjama surpris at left with vpunch
    ed "Mon réveil n'a pas sonné !"
    play sound what_sound
    show julie colere at right with vpunch
    julie "TU RIGOLES ?!!!"
    julie "Les candidats sont attendus à 10h, et il est 9h30 !"
    play sound ok_sound
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
    play sound yeah_sound
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
    show ed chemise sceptique at left with dissolve
    chris "J'ai été obligé de venir en courant..."
    play sound huh_sound
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
    play sound hahaha_sound
    show chris rire at right with dissolve
    chris "Ha ha, ça arrive toujours au mauvais moment !"
    jump fin_explication

label longue_histoire:
    play sound hahaha_sound
    show chris rire at right with dissolve
    chris "Ha ha, ça sent la panne de réveil,  ça !"
    jump fin_explication

label fin_explication:
    hide ed
    hide chris
    show sylvie deux mains tablette with dissolve
    sylvie "Bonjour messieurs !"
    sylvie "Je me présente : {b}Sylvie Cristal{/b} !\nJ'organise les sélections de la zone Ouest."
    show sylvie ecrit with dissolve
    sylvie "Vous pouvez me donner vos noms ?"
    hide sylvie
    show chris mains hanche at right with dissolve
    chris "Bien sûr ! Je suis {b}Christophe Tonga{/b}."
    show chris mains poches at right with dissolve
    show ed chemise sourire at left with dissolve
    ed "Et moi {b}Edouard Pinson{/b}."
    hide ed
    hide chris
    show sylvie sourire with dissolve
    sylvie "Très bien, c'est noté !"
    show sylvie deux mains tablette with dissolve
    sylvie "Veuillez me suivre, nous allons rejoindre les autres candidats."

    scene bg entrepot
    show sylvie deux mains tablette at right with dissolve
    sylvie "Messieurs dames,\nles sélections de {b}Game Master{/b} vont commencer !"
    sylvie "Cette compétition est organisée par {b}Virgile Brizor{/b}, pdg de {b}B-Tech{/b} et pionnier de la robotique."
    show sylvie une main tablette at right with dissolve
    sylvie "Le principe est simple :\nà chaque épreuve, vous devrez affronter des robots conçus par B-Tech."
    show sylvie deux mains tablette at right with dissolve
    play sound yeah_sound
    show ed chemise heureux at left with dissolve
    ed "Des robots géants, c'est trop cool !"
    play sound humhum_sound
    show ed chemise main levee at left with dissolve
    ed "Mais, euh... Ce n'est pas un tournoi de jeux vidéo ?"
    play sound hahaha_woman_sound
    show sylvie mains levees at right with dissolve
    sylvie "Je pense qu'il y a méprise..."
    show ed chemise sceptique at left with dissolve
    sylvie "Pour que ce soit plus fun, les épreuves sont inspirées de jeux vidéo célèbres."
    sylvie "Mais les créatures que vous affronterez seront bien réelles !"
    show sylvie deux mains tablette at right with dissolve
    play sound ok_sound
    show ed chemise pense at left with dissolve
    ed "Je vois..."
    show ed chemise surpris at left with dissolve
    ed "Mais... Ce n'est pas un peu dangereux ?"

    show sylvie une main tablette at right with dissolve
    sylvie "Votre mental et votre physique seront mis à rude épreuve, c'est certain."
    show sylvie deux mains tablette at right with dissolve
    hide ed
    show chris mains hanche at left with dissolve
    chris "Le gagnant de la compétition repart bien avec {b}100 000 €{/b} ?"
    show sylvie deux mains tablette at right with dissolve
    sylvie "Tout à fait."
    play sound wow_sound
    show chris bras leves at left with dissolve
    chris "Ok, je vais me donner à fond !"
    show chris mains poches at left with dissolve
    show sylvie ecrit with dissolve
    sylvie "Je vais vous appeler à tour de rôle pour me rejoindre devant l'entrepôt."
    sylvie "Si vous remportez l'épreuve, vous serez qualifiés."
    show sylvie sourire with dissolve
    sylvie "La suite de la compétition se passera au siège de la B-Tech,\net sera diffusée en streaming sur Internet."

    scene bg entree entrepot with Pixellate(3,5)
    show sylvie ecrit at right with dissolve
    sylvie "Candidat suivant : Edouard Pinson !"
    show sylvie sourire at right with dissolve
    show ed chemise sourire at left with dissolve
    ed "Je suis là..."
    
    sylvie "Veuillez signer cette décharge. C'est pour nous couvrir en cas d'accident."
    play sound huh_sound
    show ed chemise surpris at left with dissolve
    ed "D'accident ?"
    show sylvie mains levees ecran blanc at right with dissolve
    sylvie "Je vous l'ai dit, cette compétition n'est pas sans risque."
    show sylvie une main tablette at right with dissolve
    sylvie "Vous avez déjà fait du bowling ?"
    show ed chemise sceptique at left with dissolve
    ed "Euh... oui."
    sylvie "Et vous avez trouvé ça dangereux ?"
    ed "Euh... non."
    show sylvie deux mains tablette at right with dissolve
    sylvie "La première épreuve est une sorte de bowling."
    show ed chemise pense at left with dissolve
    menu:
        "Ok, je signe.\n Si c'est basé sur les jeux vidéo, j'ai mes chances.":
            play sound ok_sound
            jump entree_entrepot

        "Non, désolé, tout ceci me semble un peu trop dangereux.":
            jump again_entree


label again_entree :
    ed "Quand même..."
    ed "Il y a 100 000 € à la clé... Ce n'est pas rien."

    menu:
        "Bon d'accord, je signe.":
            play sound ok_sound
            jump entree_entrepot

        "Non, j'ai trop peur.":
            jump again_entree

label entree_entrepot :
    show ed chemise sourire at left with dissolve
    show sylvie ecrit at right with dissolve
    sylvie "Merci, tout est en ordre."
    show sylvie une main tablette at right with dissolve
    sylvie "Amusez-vous bien !"
    scene bg interieur entrepot 2
    play sound what_sound
    show ed chemise surpris at left with vpunch
    ed "{i}NOM D'UNE PAPETERIE !{/i}"
    show ed chemise surpris at left with vpunch
    ed "C'est quoi ce délire ?!"
    show ed chemise surpris at left with vpunch
    ed "Ça n'a rien à avoir avec un bowling !"
    show ed chemise pense at left
    ed "Visiblement, il faut que je monte sur ce éléphant..."
    jump start_bubble_shooter_game




    

label after_bubble_shooter_game:
    stop music
    window auto  
    if mini_game==False:
        scene bg entree entrepot
        play sound win_sound
        show sylvie mains levees at right with dissolve
        show ed chemise sourire at left with dissolve
        sylvie "Bravo Mr Pinson, vous avez terminé l'épreuve !"
        play sound yeah_sound
        show ed chemise heureux at left with dissolve
        ed "C'est bon, je suis qualifié ?"
        play sound hahaha_woman_sound
        show sylvie sourire at right with dissolve
        sylvie "Hélas non, il y a une deuxième épreuve..."
        play sound sigh_sound
        show ed chemise decu at left with dissolve
        ed "Ah."
        show ed chemise grand sourire at left with dissolve
        ed "La première épreuve était assez facile, ça va..."
        show ed chemise sourire at left with dissolve
        show sylvie deux mains tablette at right with dissolve
        sylvie "La deuxième sera un peu plus... sportive."
        play sound huh_sound
        show ed chemise sceptique at left with dissolve
        ed "Ah ?"
        show sylvie une main tablette at right with dissolve
        sylvie "Vous m'accompagnez à l'entrepôt voisin ?" 
        play sound ok_sound
        ed "Allons-y..."

        scene bg entree entrepot 2 with Pixellate(3,5)
        show ed chemise sourire at left with dissolve
        show sylvie deux mains tablette at right with dissolve
        sylvie "N'ayez crainte, tout va bien se passer !"
        
        scene bg interieur entrepot
        #show apple big at applePos with dissolve
        #show snake at snakePos with dissolve
        show ed chemise grand sourire at right with dissolve
        ed "J'hallucine !\nUn robot serpent !"
        show ed chemise pense at right with dissolve
        ed "Il y a aussi une pomme..."
        ed "C'est comme dans ce vieux jeu sur portable."
        scene bg interieur entrepot bis
        show ed chemise pense at right
        play sound snake_coming_sound
        snake "Sssssssssssssss"
        #show snake at snakeMove
        play sound yeah_sound
        show ed chemise heureux at right with dissolve
        ed "Et en plus il fait du bruit et il bouge !"
        
        ed "Trop stylé !"
        scene bg interieur entrepot ter
        show ed chemise heureux at right
        play sound snake_coming_sound
        snake "Sssssssssssssss"
        show ed chemise heureux at right
        play sound huh_sound
        show ed chemise sceptique at right with dissolve
    
        ed "Euh... Attends..."
        play sound what_sound
        show ed chemise surpris at right with vpunch
        ed "{i}NOM D'UN SALSIFIS !{/i}"
        show ed chemise surpris at right with vpunch
        ed "Il veut me bouffer !"
        jump start_snake_game

       
        
    
label after_snake_game:
    stop music
    window auto  
    if mini_game==False:
        scene bg entree entrepot 2
        play sound win_sound
        show sylvie mains levees at right with dissolve
        show ed chemise grand sourire at left with dissolve
        sylvie "Bravo Mr Pinson, vous êtes qualifiés !"
        hide sylvie
        play sound wow_sound
        chris "Bien joué mec !"
        show chris bras croises at right with dissolve
        chris "Tu as un physique de crevette, mais je savais que tu allais assurer !"
        show ed chemise gene at left with dissolve
        ed "Euh... merci."
        hide chris
        show sylvie deux mains tablette at right with dissolve
        show ed chemise sourire at left with dissolve
        sylvie "Mr Tonga a également réussi cette épreuve."
        show sylvie sourire at right with dissolve
        sylvie "Il me reste quelques candidats à faire passer."
        sylvie "L'hélicoptère viendra chercher les compétiteurs sélectionnés d'ici 15 mn."
        show sylvie une main tablette at right with dissolve
        sylvie "Je vous laisse aller chercher votre sac de voyage dans votre véhicule ?"
        show sylvie deux mains tablette at right with dissolve
        play sound what_sound
        show ed chemise surpris at left with vpunch
        ed "{i}NOM D'UN OUISTITI !{/i}"
        show ed chemise surpris at left with vpunch
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
    add Text(_("GENIAL !!!!\nVous avez terminé le Chapitre 1 de Game Master !\n\nMerci d'avoir joué à ce jeu !\nS'il vous a plu, si vous en voulez plus,\nmerci de mettre un commentaire sur itch.io, ça me boostera !"), font='gui/jd_code.ttf', size=50, color="#77d079")  xalign 0.5 yalign 0.5 
    textbutton _("Menu principal"):
        style "main_menu_button"

        action MainMenu()