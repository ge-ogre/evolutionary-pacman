import pygame
import json
import os

class MapEditor:
    def __init__(self, renderer):
        self.renderer = renderer
        self.map_width = 20
        self.map_height = 15
        self.grid = [['_' for _ in range(self.map_width)] for _ in range(self.map_height)]
        self.selected_tile = '#'
        self.tile_types = ['#', '0', '1', 'a', 'b', 'c', 'd', '_']
        self.tile_idx = 0

    def run(self):
        running = True
        while running:
            events = self.renderer.handle_events()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.save_map()
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_TAB:
                        self.tile_idx = (self.tile_idx + 1) % len(self.tile_types)
                        self.selected_tile = self.tile_types[self.tile_idx]

            self.draw()

    def handle_click(self, pos):
        offset_x = (self.renderer.width - (self.map_width * 30)) // 2
        offset_y = (self.renderer.height - (self.map_height * 30)) // 2
        
        col = (pos[0] - offset_x) // 30
        row = (pos[1] - offset_y) // 30
        
        if 0 <= col < self.map_width and 0 <= row < self.map_height:
            self.grid[row][col] = self.selected_tile

    def draw(self):
        self.renderer.screen.fill((0, 0, 0))
        offset_x = (self.renderer.width - (self.map_width * 30)) // 2
        offset_y = (self.renderer.height - (self.map_height * 30)) // 2
        
        for r in range(self.map_height):
            for c in range(self.map_width):
                rect = pygame.Rect(offset_x + c * 30, offset_y + r * 30, 30, 30)
                tile = self.grid[r][c]
                if tile == '#':
                    pygame.draw.rect(self.renderer.screen, (0, 0, 255), rect)
                elif tile == '0':
                    pygame.draw.circle(self.renderer.screen, (255, 255, 255), rect.center, 5)
                elif tile == '1':
                    pygame.draw.circle(self.renderer.screen, (255, 255, 0), rect.center, 13)
                elif tile == 'a':
                    pygame.draw.circle(self.renderer.screen, (255, 0, 0), rect.center, 13)
                elif tile == 'b':
                    pygame.draw.circle(self.renderer.screen, (255, 182, 193), rect.center, 13)
                
                pygame.draw.rect(self.renderer.screen, (50, 50, 50), rect, 1)

        # Draw UI info
        info_text = self.renderer.font.render(f"Selected: {self.selected_tile} (TAB to cycle, S to save, ESC to exit)", True, (255, 255, 255))
        self.renderer.screen.blit(info_text, (10, 10))
        
        pygame.display.flip()

    def save_map(self):
        ghosts = []
        for r in range(self.map_height):
            for c in range(self.map_width):
                if self.grid[r][c] in ['a', 'b', 'c', 'd']:
                    ghosts.append(self.grid[r][c])
        
        map_data = {
            "map": self.grid,
            "ghosts": ghosts
        }
        with open("custom_map.json", "w") as f:
            json.dump(map_data, f)
        print("Map saved to custom_map.json")
