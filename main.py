import pygame
import random
import sys

# Définition paramètres de la fenêtre
width = 1280
height = 720
FPS = 60

# Initialisation + création horloge du jeu
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("JetPack Potatoes - Wassim & Giovanny")
clock = pygame.time.Clock()

main_font = pygame.font.Font("font/mainFont.ttf", 50) # Police d'écriture
second_font = pygame.font.Font("font/mainFont.ttf", 30) # Police d'écriture

bg_img = pygame.image.load("images/bg_start.png")
bg_img_game = pygame.image.load("images/bg_playing.png")
bg_img_l = pygame.image.load("images/bg_start.png")
plain_bg = pygame.image.load("images/plain_bg.jpg")
plain_bg = pygame.transform.scale(plain_bg, (width* 2, height))
lava_bg = pygame.image.load("images/lava_bg.jpg")
lava_bg = pygame.transform.scale(lava_bg, (width* 2, height))
candy_bg = pygame.image.load("images/candy_bg.jpg")
candy_bg = pygame.transform.scale(candy_bg, (width* 2, height))
icon = pygame.image.load("images/icon.jpg") # Icone du jeu
pygame.display.set_icon(icon) # Application de l'icone

start_img = pygame.image.load("images/start.png")
start_img = pygame.transform.scale(start_img, (360//2, 155//2))
start_rect = start_img.get_rect(topleft=(540, 460))

jetpack_img = pygame.image.load("images/jetpack.png")
jetpack_img = pygame.transform.scale(jetpack_img, (96, 96))
jetpack_rect = jetpack_img.get_rect(topleft=(540, 525))





########################### Joueur Animation ##########################################

# Image + rectangle d'initialisation
player_surf = pygame.Surface((100, 100))
player_rect = player_surf.get_rect(topleft=(150, 525))

# Saut du joueur (image + rectangle)
player_surf_jump = pygame.image.load("images/potato_jetpack_on.png")
player_surf_jump = pygame.transform.scale(player_surf_jump, (290//4, 370//4))
player_rect_jump = player_surf_jump.get_rect(topleft=(150, 525))

# Descente joueur
player_surf_fall = pygame.image.load("images/potato_jetpack_off.png")
player_surf_fall = pygame.transform.scale(player_surf_fall, (290//4, 370//4))
player_rect_fall = player_surf_jump.get_rect(topleft=(150, 525))

# Etat du joueur avant le lancement (image + rectangle)
player_surf_stand = pygame.image.load("images/potato_ch.png")
player_surf_stand = pygame.transform.scale(player_surf_stand, (290//4, 370//4))
player_rect_stand = player_surf_stand.get_rect(topleft=(150, 525))



############################ Obstacles à éviter ######################################

# "Zapper" (obstacle electrique) (image + rectangle)
zapper_surf = pygame.image.load("images/zapper.png")
zapper_surf = pygame.transform.scale(zapper_surf, (217, 227))
zapper_rect = zapper_surf.get_rect(topleft=(2000, 400))
zapper_surf_mask = pygame.mask.from_surface(zapper_surf) # Masque pour collision parfaite

# Rocket (image + rectangle)
rocket_surf = pygame.image.load("images/rocket.png")
rocket_surf = pygame.transform.scale(rocket_surf, (100, 75))
rocket_rect = rocket_surf.get_rect(topleft=(4000, 400))
rocket_surf_mask = pygame.mask.from_surface(rocket_surf) # Masque pour collision parfaite



############################## Variables Du Jeu ######################################

gravity = 0
isMoving = False
ground_velocity = 10
ground_x = 0
obstacle_velocity = 10 # Vitesse des obstacle
distance_score = 0 # Score en temps réel
score = 0 # Score pour le high score
pass_bg = False
can_fly = False


# Création d'un evenement "distance" qui s'enclenche toutes les 10ms
distance_timer = pygame.USEREVENT
pygame.time.set_timer(distance_timer, 10)

# Joueur en vie ou non ?
playing = False
# Variable pour faire tourner le jeu
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            
        ######################## TOUCHES POUR Déplacement joueur + START ########################
        if event.type == pygame.KEYDOWN: # Si touche maintenue
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if can_fly:
                    isMoving = True
            elif event.key == pygame.K_RETURN: # Touche entrée : commencer la partie
                playing = True
        elif event.type == pygame.KEYUP: # Si touche relâchée
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                isMoving = False
        elif event.type == pygame.MOUSEBUTTONDOWN: # Si bouton souris cliqué
            mouse_pos = event.pos # Prend la position du curseur
            if start_rect.collidepoint(mouse_pos): # Si collision entre curseur et bouton start
                playing = True
        ######################## Gestion score ########################
        if event.type == distance_timer:
            if playing:
                distance_score += 1
    
    # Déplacement du sol lorsque le joueur est en vie
    if playing:
        ground_x -= ground_velocity
        jetpack_rect.x -= ground_velocity  # Mettre à jour la position x du sol
        if ground_x <= -1280:  # Réinitialiser la position du sol lorsqu'il sort de l'écran
            ground_x = 0
            if not pass_bg:
                bg_img = bg_img_game
                pass_bg = True

    
    ######################## Gestion de la gravité ########################
    if not isMoving: # si la touche espace n'est pas maintenu
        gravity += 0.75 # Faire tomber le joueur
        player_rect.y += gravity        
    else:     
        if player_rect.y >= 0:
            player_rect.y -= 10 # Faire voler le joueur
            gravity = -3 # Effet de fluidité
    
    ######################## Gestion animation + collision sol ########################
    
    if player_rect.y >= 525: # Si le joueur est sur le sol
        if can_fly:
            player_surf = player_surf_fall# Changer image
            player_rect = player_rect_fall # Changer rectangle
        else:
            player_surf = player_surf_stand
            player_rect = player_rect_stand
        gravity = 0
        player_rect.y = 525
    else: # Si le joueur est en l'air
        player_surf = player_surf_jump  # Changer image
        player_rect = player_rect_jump  # Changer rectangle
    
    ######################## Gestion obstacles : AU LANCEMENT DU PROGRAMME ########################
            ######################## DURANT UNE PARTIE ########################

    if playing:
        ############ Zapper ############  
        if zapper_rect.x >= -217: # Deplacement zapper jusqu'à la fin d'écran
            zapper_rect.x -= obstacle_velocity
        else: 
            zapper_rect.x = width+217 # Remis a droite
            zapper_rect.y = random.choice([i for i in range(0, height-216, 216)]) # position y au hasard sur l'écran
            
        ############ Rocket ############    
        if rocket_rect.x >= -100:
            rocket_rect.x -= obstacle_velocity * 1.5
        else:
            rocket_rect.x = width+200
            rocket_rect.y = random.choice([i for i in range(0, height-(195), 74)])

    ######################## Gestion du score ########################
    
    if distance_score >= 1000: # A partir de 1000 de score
        # Changement vitesse obstacle + sol
        obstacle_velocity = (1/400)*(distance_score) + (15/2)
        ground_velocity = (1/400)*(distance_score) + (15/2)
    
    ######################## Collision joueur/obstacle ########################

    # Masque pour joueur (collision parfaite)
    player_mask = pygame.mask.from_surface(player_surf)
    jetpack_mask = pygame.mask.from_surface(jetpack_img)
    
    if player_mask.overlap(jetpack_mask, (jetpack_rect.x - player_rect.x,
                                          jetpack_rect.y - player_rect.y)):
        can_fly = True
    # Check si le mask joueur touche un obstacle (overlap(masque, offset))
    if player_mask.overlap(zapper_surf_mask, 
                           (zapper_rect.x - player_rect.x, 
                            zapper_rect.y - player_rect.y)) or player_mask.overlap(rocket_surf_mask,
                                                                                   (rocket_rect.x - player_rect.x,
                                                                                   rocket_rect.y - player_rect.y)):
        # Gestion du highscore
        if distance_score >= score:
            score = distance_score
        ######################## Gestion obstacles & Rénitialisation des variables : ########################
                    ######################## AU RELANCEMENT DE LA PARTIE ########################
        distance_score = 0
        obstacle_velocity = 10
        ground_velocity = 10
        zapper_rect.x = 2000
        zapper_rect.y = random.choice([i for i in range(0, height-216, 216)]) # Definis aléatoirement la position d'apparition
        rocket_rect.x = 4000 
        rocket_rect.y = random.choice([i for i in range(0, height-(195), 74)])
        jetpack_rect.x = 540
        bg_img = bg_img_l
        ground_x = 0
        # Arrete la partie
        playing = False
        can_fly = False
        pass_bg = False

    ######################## Affichage des objets ########################        
    
    screen.blit(bg_img, (ground_x, 0))
    if not can_fly:
        screen.blit(jetpack_img, jetpack_rect)
    screen.blit(player_surf, player_rect)
    screen.blit(zapper_surf, zapper_rect)
    screen.blit(rocket_surf, rocket_rect)
    
    screen.blit(main_font.render(f"Score : {distance_score} ", True, 
                                 pygame.Color("white")), (0, 0))
    if not playing:
        screen.blit(start_img, start_rect)
        screen.blit(main_font.render(f"Espace / Fleche du haut", True, 
                                     pygame.Color("white")), (width//3, height//2))
        screen.blit(main_font.render(f"Pour voler", True, 
                                     pygame.Color("white")), (width//3+125, height//2+50))
    screen.blit(main_font.render(f"Score : {distance_score} ", True, 
                                pygame.Color("white")), (0, 0))
    screen.blit(main_font.render(f"Record : {score} ", True, 
                                 pygame.Color("white")), (0, 50))
    screen.blit(second_font.render(f"velocity : {round(obstacle_velocity, 1)}x ", True, 
                                 pygame.Color("white")), (0, 90))
    
    
    
    ######################## Gestion message STAGE en fonction du score ########################
    colors = ["#90A92F", "#BF507C","#FE8C35", "#BF507C"]
    stages = {(i, i+250, random.choice(colors)): f"Stage {i//1000}" for i in range(1, 10001, 1000)}

    for (start, end, color), n in stages.items():
        if start <= distance_score <= end:
            screen.blit(main_font.render(f"{n}", True,
                                     pygame.Color(color)), (560 ,90))

    
    ######################## Gestion des fonds en fonction du score ########################
    backgrounds = {
        (1000, 2000): candy_bg,
        (2000, 3000): plain_bg,
        (3000, 4000): lava_bg,
        (4000, 5000): plain_bg,
        (5000, 6000): lava_bg,
        (6000, 7000): candy_bg,
        (7000, 8000): lava_bg
    }

    for (start, end), bg in backgrounds.items():
        if start <= distance_score <= end:
            bg_img = bg
            

    
    
    ######################## Gestion des événements ########################
    
    pygame.display.update() # Rafraîchissement de l'écran
    clock.tick(FPS) # Fonctionnement de l'horloge dans le délai fps (ici 60fps)
    
    ########################################################################
