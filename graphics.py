import pygame
import pygame_gui
import sys

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 182, 193)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

GHOST_COLORS = {
    "a": RED,
    "b": PINK,
    "c": CYAN,
    "d": ORANGE
}

TILE_SIZE = 30

class PygameRenderer:
    def __init__(self, map_width, map_height):
        pygame.init()
        self.width = max(800, map_width * TILE_SIZE)
        self.height = max(600, (map_height * TILE_SIZE) + 100)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Evolutionary Pac-Man")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        
        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.map_width = map_width
        self.map_height = map_height

    def draw_state(self, game):
        self.screen.fill(BLACK)
        
        # Center the map
        offset_x = (self.width - (len(game.map[0]) * TILE_SIZE)) // 2
        offset_y = (self.height - (len(game.map) * TILE_SIZE)) // 2 - 20
        
        for row_idx, row in enumerate(game.map):
            for col_idx, tile in enumerate(row):
                x = offset_x + col_idx * TILE_SIZE
                y = offset_y + row_idx * TILE_SIZE
                
                if tile == "#":
                    pygame.draw.rect(self.screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
                elif tile == "0":
                    pygame.draw.circle(self.screen, WHITE, (x + TILE_SIZE // 2, y + TILE_SIZE // 2), TILE_SIZE // 6)
                elif tile == "1":
                    pygame.draw.circle(self.screen, YELLOW, (x + TILE_SIZE // 2, y + TILE_SIZE // 2), TILE_SIZE // 2 - 2)
                elif tile in GHOST_COLORS:
                    pygame.draw.circle(self.screen, GHOST_COLORS[tile], (x + TILE_SIZE // 2, y + TILE_SIZE // 2), TILE_SIZE // 2 - 2)

        # Draw Score
        score_text = self.font.render(f"Score: {game.score}", True, WHITE)
        self.screen.blit(score_text, (10, self.height - 35))
        
        self.manager.draw_ui(self.screen)
        pygame.display.flip()

    def handle_events(self):
        time_delta = self.clock.tick(60)/1000.0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            self.manager.process_events(event)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return "1"
                elif event.key == pygame.K_RIGHT:
                    return "2"
                elif event.key == pygame.K_DOWN:
                    return "3"
                elif event.key == pygame.K_LEFT:
                    return "4"
        
        self.manager.update(time_delta)
        return events

    def wait(self, milliseconds):
        pygame.time.wait(milliseconds)

    def draw_menu(self):
        self.screen.fill(BLACK)
        self.manager.draw_ui(self.screen)
        pygame.display.flip()

    def draw_grid(self, games):
        self.screen.fill(BLACK)
        num_games = len(games)
        grid_size = int(np.ceil(np.sqrt(num_games)))
        
        # Calculate smaller tile size for grid view
        grid_tile_size = min(self.width // (grid_size * self.map_width), 
                             (self.height - 100) // (grid_size * self.map_height))
        grid_tile_size = max(2, grid_tile_size) # Ensure it's at least 2 pixels
        
        game_width = self.map_width * grid_tile_size
        game_height = self.map_height * grid_tile_size
        
        for i, game in enumerate(games):
            row_grid = i // grid_size
            col_grid = i % grid_size
            
            base_x = col_grid * (game_width + 5)
            base_y = row_grid * (game_height + 5)
            
            for row_idx, row in enumerate(game.map):
                for col_idx, tile in enumerate(row):
                    x = base_x + col_idx * grid_tile_size
                    y = base_y + row_idx * grid_tile_size
                    
                    if tile == "#":
                        pygame.draw.rect(self.screen, BLUE, (x, y, grid_tile_size, grid_tile_size))
                    elif tile == "0":
                        pygame.draw.circle(self.screen, WHITE, (x + grid_tile_size // 2, y + grid_tile_size // 2), max(1, grid_tile_size // 6))
                    elif tile == "1":
                        pygame.draw.circle(self.screen, YELLOW, (x + grid_tile_size // 2, y + grid_tile_size // 2), max(1, grid_tile_size // 2 - 1))
                    elif tile in GHOST_COLORS:
                        pygame.draw.circle(self.screen, GHOST_COLORS[tile], (x + grid_tile_size // 2, y + grid_tile_size // 2), max(1, grid_tile_size // 2 - 1))

        pygame.display.flip()

import numpy as np
