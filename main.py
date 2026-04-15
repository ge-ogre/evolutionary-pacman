import pygame
import pygame_gui
import sys
import os
from game import Game
from ga_algo import run_genetic_algorithm
import maps
from graphics import PygameRenderer
from editor import MapEditor

# App States
MAIN_MENU = 0
SINGLE_PLAYER = 1
GA_CONFIG = 2
GA_TRAIN = 3
MAP_EDITOR = 4
MAP_SELECTION = 5

class PacmanApp:
    def __init__(self):
        # Default map size for renderer init
        self.renderer = PygameRenderer(10, 10)
        self.state = MAIN_MENU
        self.selected_map_key = "3" # Default to Symmetry Map
        self.create_main_menu()

    def create_main_menu(self):
        self.renderer.manager.clear_and_reset()
        self.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 100), (200, 50)),
                                             text='Play Manual',
                                             manager=self.renderer.manager)
        self.train_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 170), (200, 50)),
                                              text='Train GA',
                                              manager=self.renderer.manager)
        self.best_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 240), (200, 50)),
                                             text='Run Best Individual',
                                             manager=self.renderer.manager)
        self.map_select_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 310), (200, 50)),
                                               text='Select Map',
                                               manager=self.renderer.manager)
        self.editor_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 380), (200, 50)),
                                               text='Map Editor',
                                               manager=self.renderer.manager)
        self.quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 450), (200, 50)),
                                             text='Quit',
                                             manager=self.renderer.manager)
        
        map_names = {"1": "Small Map", "2": "Line Map", "3": "Symmetry Map"}
        map_name = map_names.get(self.selected_map_key, "Custom Map")
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((300, 520), (200, 30)),
                                     text=f"Current Map: {map_name}",
                                     manager=self.renderer.manager)

    def create_map_selection_menu(self):
        self.renderer.manager.clear_and_reset()
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((300, 50), (200, 30)),
                                     text='Select Map',
                                     manager=self.renderer.manager)
        
        self.map1_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 120), (200, 50)),
                                              text='Small Map',
                                              manager=self.renderer.manager)
        self.map2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 190), (200, 50)),
                                              text='Line Map',
                                              manager=self.renderer.manager)
        self.map3_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 260), (200, 50)),
                                              text='Symmetry Map',
                                              manager=self.renderer.manager)
        self.back_to_menu_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 350), (200, 50)),
                                                         text='Back',
                                                         manager=self.renderer.manager)

    def create_ga_config_menu(self):
        self.renderer.manager.clear_and_reset()
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((300, 50), (200, 30)),
                                     text='GA Configuration',
                                     manager=self.renderer.manager)
        
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((200, 100), (150, 30)),
                                     text='Population Size:',
                                     manager=self.renderer.manager)
        self.pop_size_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((400, 100), (100, 30)),
                                                                  manager=self.renderer.manager)
        self.pop_size_input.set_text("25")
        
        pygame_gui.elements.UILabel(relative_rect=pygame.Rect((200, 150), (150, 30)),
                                     text='Generations:',
                                     manager=self.renderer.manager)
        self.gen_count_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((400, 150), (100, 30)),
                                                                    manager=self.renderer.manager)
        self.gen_count_input.set_text("50")

        self.start_train_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 250), (200, 50)),
                                                                text='Start Training',
                                                                manager=self.renderer.manager)
        self.back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 320), (200, 50)),
                                                         text='Back',
                                                         manager=self.renderer.manager)

    def run(self):
        while True:
            events = self.renderer.handle_events()
            
            for event in events:
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if self.state == MAIN_MENU:
                        if event.ui_element == self.play_button:
                            self.start_manual_game()
                        elif event.ui_element == self.train_button:
                            self.state = GA_CONFIG
                            self.create_ga_config_menu()
                        elif event.ui_element == self.best_button:
                            self.run_best_agent()
                        elif event.ui_element == self.map_select_button:
                            self.state = MAP_SELECTION
                            self.create_map_selection_menu()
                        elif event.ui_element == self.editor_button:
                            self.start_map_editor()
                        elif event.ui_element == self.quit_button:
                            pygame.quit()
                            sys.exit()
                    elif self.state == GA_CONFIG:
                        if event.ui_element == self.start_train_button:
                            self.start_training()
                        elif event.ui_element == self.back_button:
                            self.state = MAIN_MENU
                            self.create_main_menu()
                    elif self.state == MAP_SELECTION:
                        if event.ui_element == self.map1_button:
                            self.selected_map_key = "1"
                            self.state = MAIN_MENU
                            self.create_main_menu()
                        elif event.ui_element == self.map2_button:
                            self.selected_map_key = "2"
                            self.state = MAIN_MENU
                            self.create_main_menu()
                        elif event.ui_element == self.map3_button:
                            self.selected_map_key = "3"
                            self.state = MAIN_MENU
                            self.create_main_menu()
                        elif event.ui_element == self.back_to_menu_button:
                            self.state = MAIN_MENU
                            self.create_main_menu()

            self.renderer.draw_menu()

    def start_training(self):
        pop_size = int(self.pop_size_input.get_text())
        gen_count = int(self.gen_count_input.get_text())
        selected_map = maps.create_map(self.selected_map_key)
        self.renderer.manager.clear_and_reset()
        # Update renderer map dimensions for grid scaling
        self.renderer.map_width = len(selected_map["map"][0])
        self.renderer.map_height = len(selected_map["map"])
        run_genetic_algorithm(selected_map, population_size=pop_size, num_generations=gen_count, renderer=self.renderer)
        self.state = MAIN_MENU
        self.create_main_menu()

    def run_best_agent(self):
        import tensorflow as tf
        if os.path.exists("best_agent.keras"):
            best_model = tf.keras.models.load_model("best_agent.keras")
            selected_map = maps.create_map(self.selected_map_key)
            game = Game(selected_map)
            self.renderer.manager.clear_and_reset()
            from ga_algo import play_agent
            play_agent(game, best_model, 1000, renderer=self.renderer)
            self.create_main_menu()
        else:
            print("No best_agent.keras found. Train first!")

    def start_manual_game(self):
        selected_map = maps.create_map(self.selected_map_key)
        game = Game(selected_map)
        self.renderer.manager.clear_and_reset()
        game.play_game(self.renderer)
        self.create_main_menu()

    def start_map_editor(self):
        editor = MapEditor(self.renderer)
        self.renderer.manager.clear_and_reset()
        editor.run()
        self.create_main_menu()

if __name__ == "__main__":
    app = PacmanApp()
    app.run()
