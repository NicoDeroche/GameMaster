
transform islandPosition:
    xalign 0
    yalign 0
    xanchor 0.0
    yanchor 0
    linear 5 xoffset -3735




# start of the second chapter
label start_chapter_2:

    stop music
    $ mini_game=False
   
    scene bg maison nuit
    show bg ile at islandPosition
    show screen show_chapter_optional_background
    show screen show_chapter_2
    show helico
   
    
    pause 6
    sylvie "Messieurs-dames,\nnous sommes arrivés !"
    hide helico
    hide bg ile
    
    #devant hotel
    show sylvie sourire at left with dissolve 
    sylvie  "Bienvenue sur {b}l'île de la Baleine Blanche{/b}, qui abrite le siège de la B-Tech."
    sylvie "Vous serez logés et nourris pendant la durée de votre séjour."
    sylvie "L'île dispose aussi de magasins, si vous avez besoin de faire des achats..."
    show chris bras croises at right with dissolve
    chris "Des vêtements par exemple ?"
    hide chris
    chris "Alors voici les participants de la zone Ouest ?"
    sylvie "Monsieur Brizor ? Je ne pensais pas vous voir aujourd'hui."
    show virgile sourire at right with dissolve
    virgile "J'étais impatient de voir les premiers candidats !"
    sylvie "Messieurs-dames, voici votre hôte : Virgile Brizor !"
    hide sylvie
    virgile "J'espère que vous avez apprécié l'épreuve des sélections."
    virgile "Le serpent géant était génial, non ?"
    virgile "Pour la suite de la compétition, j'ai prévu un beau programme, vous n'allez pas être déçus."
    virgile "Il y aura des défis grandioses, des robots qui vont vous donner du fil à retordre, ça va être formidable !"
    virgile "Je compte sur vous pour vous battre, et donner le meilleur de vous-mêmes !"
    virgile "Vous savez, j'ai nommé cette île en référence au roman de Herman Melville, \"Moby-Dick\"."
    virgile "Le capitaine Achab est un modèle de ténacité et de résilience, je le trouve fascinant."
    show ed chemise main levee at left with dissolve
    ed "Le capitaine Achab ne périt-il pas noyé, à la fin de l'histoire ?"
    virgile "Ha ha ha !\nEn effet, il a une fin tragique."
    virgile "Mais il est mort en combattant, je trouve que c'est tout à son honneur."
    ed "C'est une façon de voir les choses..."
    virgile "Bien, je dois vous laisser... On se revoit demain"
    virgile "Sylvie, vous pouvez continuer votre présentation."
    hide ed
    show sylvie sourire at left with dissolve
    sylvie "Bien, Monsieur Brizor."
    hide virgile
    sylvie "L'hôtel est juste à côté, si vous voulez bien me suivre..."



    #dans hotel
    sylvie "Des chambres individuelles vous sont affectées."
    sylvie "Voici les cartes d'accès, veuillez prendre la vôtre."

    #table
    sylvie "Monsieur Pinson, ce n'est pas votre carte !"

    #hotel
    sylvie "Le restaurant est situé en face de l'hôtel."
    sylvie "Il est ouvert de 8h à 9h, 12h à 14h, et 19h à 20h."
    sylvie "Les participants des autres zones sont en route pour l'île, ils arriveront dans la soirée."
    sylvie "L'épreuve débutera demain à 9h30.\nSoyez ponctuels."
    sylvie "Je vous souhaite une bonne soirée !"
    hide sylvie


    show ed chemise sourire at left with dissolve
    ed "Allo frangine ?"
    show julie parle at right with dissolve
    julie "Salut Ed, ça va ?"
    ed "Pas trop mal, j'ai passé les sélections !"
    julie "Super, je suis trop contente !"
    ed "Mais tu sais, ce n'est pas un tournoi de jeux vidéo..."
    julie "Ah bon ?"
    ed "Non, en fait on se bat contre des robots dirigés par I.A., c'est ouf."
    ed "On m'a déposé en hélico sur une île au milieu de l'Atlantique..."
    julie "Quoi ?"
    ed "Oui, c'est un truc de dingue !"
    ed "La suite de la compétition va être diffusée sur Internet."
    julie "Ok, je vais suivre ça. Fais bien attention à toi, frangin."
    ed "Je vais essayer.\nA plus, sister !"


    #ed appelle sa soeur pour demande qu'elle soit sur place demain vers 10h pour ouvrir la porte
    # chris toque car il n'a pas de wifi, ils parlent un peu : ville de résidence
    # sophia toque car elle n'a pas de wifi : tu ne viens pas de Bretagne ?
    # ils parlent de leur motiviation (et métier ?)
    #je suis étudiant en informatique, j'aime les JV, je participe souvent à des concours de JV
    #moi je suis coach sportif, mais j'ai besoin d'argent pour mon fiston, pour une prothèse
    #je suis chef de chantier, je veux prouver à Virgile qu'une femme peut gagner cette compétition


    #mouvement dans la nuit : un mille pattes

    # lendemain, sur une place, début de la deuxième épreuve


screen show_chapter_2 :

    add Text(_("Chapitre 2 : Explosions en série"), font='gui/jd_code.ttf', size=50, color="#77d079")  xalign 0.5 yalign 0.5 
    timer 2 action [Hide("show_chapter_2")]

    