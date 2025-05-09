import pygame
import os
import sys

class Sokoban:
    def __init__(self):
        pygame.init()

        # Load all image assets
        self.load_images()

        # Initialize game state
        self.new_game()

        # Set dimensions based on the map and image size
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.scale = self.images[0].get_width()  # assuming all images are square and same size

        # Create game window
        window_width = self.width * self.scale
        window_height = self.height * self.scale + 40  # extra space for text
        self.window = pygame.display.set_mode((window_width, window_height))

        # Set font and title
        self.game_font = pygame.font.SysFont("Arial", 24)
        pygame.display.set_caption("Sokoban")

        # Start main game loop
        self.main_loop()

    def load_images(self):
        # Load images from the same folder where this script is located
        self.images = []
        base_path = os.path.dirname(__file__)  # path of current script
        tile_names = ["floor", "wall", "target", "box", "robot", "done", "target_robot"]
        for name in tile_names:
            image_path = os.path.join(base_path, name + ".png")
            self.images.append(pygame.image.load(image_path))

    def new_game(self):
        # Reset move counter and load a new map
        self.moves = 0
        self.map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
            [1, 2, 3, 0, 0, 0, 1, 0, 0, 1, 2, 3, 0, 0, 0, 0, 1],
            [1, 0, 0, 1, 2, 3, 0, 2, 3, 0, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 4, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    def main_loop(self):
        # Main game loop
        while True:
            self.check_events()
            self.draw_window()

    def check_events(self):
        # Handle user inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move(0, -1)
                elif event.key == pygame.K_RIGHT:
                    self.move(0, 1)
                elif event.key == pygame.K_UP:
                    self.move(-1, 0)
                elif event.key == pygame.K_DOWN:
                    self.move(1, 0)
                elif event.key == pygame.K_F2:
                    self.new_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def move(self, dy, dx):
        # Process player movement
        if self.game_solved():
            return

        ry, rx = self.find_robot()
        ny, nx = ry + dy, rx + dx  # new robot position

        # Blocked by wall
        if self.map[ny][nx] == 1:
            return

        # Push box
        if self.map[ny][nx] in [3, 5]:
            by, bx = ny + dy, nx + dx  # new box position
            if self.map[by][bx] in [1, 3, 5]:  # if blocked
                return
            self.map[ny][nx] -= 3  # remove box from current cell
            self.map[by][bx] += 3  # move box to next cell

        # Move robot
        self.map[ry][rx] -= 4
        self.map[ny][nx] += 4
        self.moves += 1

    def find_robot(self):
        # Locate the robot's current position
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] in [4, 6]:
                    return y, x

    def draw_window(self):
        # Draw everything to the screen
        self.window.fill((0, 0, 0))

        for y in range(self.height):
            for x in range(self.width):
                tile = self.map[y][x]
                self.window.blit(self.images[tile], (x * self.scale, y * self.scale))

        # Draw text
        text_y = self.height * self.scale + 10
        self.window.blit(self.game_font.render(f"Moves: {self.moves}", True, (255, 0, 0)), (25, text_y))
        self.window.blit(self.game_font.render("F2 = new game", True, (255, 0, 0)), (200, text_y))
        self.window.blit(self.game_font.render("Esc = exit game", True, (255, 0, 0)), (400, text_y))

        # Show winning message
        if self.game_solved():
            win_text = self.game_font.render("Congratulations, you solved this game!", True, (255, 0, 0))
            tx = self.scale * self.width / 2 - win_text.get_width() / 2
            ty = self.scale * self.height / 2 - win_text.get_height() / 2
            pygame.draw.rect(self.window, (0, 0, 0), (tx, ty, win_text.get_width(), win_text.get_height()))
            self.window.blit(win_text, (tx, ty))

        pygame.display.flip()

    def game_solved(self):
        # Check if all targets are filled with boxes
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == 2:
                    return False
        return True

if __name__ == "__main__":
    Sokoban()
