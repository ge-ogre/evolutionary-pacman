import pygame
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
        self.width = map_width * TILE_SIZE
        self.height = (map_height * TILE_SIZE) + 40 # extra space for score
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Evolutionary Pac-Man")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

    def draw_state(self, game):
        self.screen.fill(BLACK)
        
        for row_idx, row in enumerate(game.map):
            for col_idx, tile in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                
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
        
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return "1"
                elif event.key == pygame.K_RIGHT:
                    return "2"
                elif event.key == pygame.K_DOWN:
                    return "3"
                elif event.key == pygame.K_LEFT:
                    return "4"
        return None

    def wait(self, milliseconds):
        pygame.time.wait(milliseconds)
