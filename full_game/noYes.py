def draw_misc():
    global game_over, window_del
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    
     
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))
    
    if game_over:
        # Load game over PNG image
        game_over_image = pygame.image.load('14.jpg').convert_alpha()
        scaled_width = game_over_image.get_width() // 4
        scaled_height = game_over_image.get_height() // 4
        scaled_image = pygame.transform.scale(game_over_image, (950, 600))
        window_del = False
        # Calculate position to center the image on the screen
        center_x = (900 - scaled_width) // 2
        center_y = (950 - scaled_height) // 2
        screen.fill("black")
        screen.blit(scaled_image, (0, 150))  # Draw centered scaled image
        
        # Add Yes and No buttons
        button_yes = pygame.image.load('yes.png').convert_alpha()
        button_no = pygame.image.load('no.png').convert_alpha()
        
        # Calculate positions for buttons
        button_yes_x = 250
        button_no_x = 400
        button_y = 450
        
        screen.blit(button_yes, (button_yes_x, button_y))
        screen.blit(button_no, (button_no_x, button_y))
        
        pygame.display.update()

        # Event handling for game over screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Check if Yes button is clicked
                if button_yes_x <= mouse_x <= button_yes_x + button_yes.get_width() and \
                   button_y <= mouse_y <= button_y + button_yes.get_height():
                    # Restart the game
                    game_over = False
                    # Reset game state as needed
                    # restart_game()  # Implement your game restart logic
                    
                # Check if No button is clicked
                elif button_no_x <= mouse_x <= button_no_x + button_no.get_width() and \
                     button_y <= mouse_y <= button_y + button_no.get_height():
                    pygame.quit()
                    quit()  # Exit the game
    
    if game_won:
        # Load victory PNG image
        victory_image = pygame.image.load('15.jpg').convert_alpha()
        scaled_width = victory_image.get_width() // 4
        scaled_height = victory_image.get_height() // 4
        scaled_image = pygame.transform.scale(victory_image, (scaled_width, scaled_height))
        
        center_x = (900 - scaled_width) // 2
        center_y = (950 - scaled_height) // 2
        
        screen.blit(scaled_image, (center_x, center_y))
        
        gameover_text = font.render('Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (center_x , center_y - 20))
