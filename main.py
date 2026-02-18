import pygame
from core.board import Board
from core.state_manager import StateManager, GameState
from core.shuffler import Shuffler
from solvers.a_star import AStarSolver
from solvers.bfs import BFSSolver
from ui.renderer import Renderer
from ui.components import Button, Slider, DecisionLog, Metrics
from ui.colors import *

def main():
    pygame.init()
    n = 4  # Board size
    board = Board(n)
    shuffler = Shuffler(board)
    shuffler.shuffle()

    # Fixed dimensions
    SIDEBAR_WIDTH = 400
    INITIAL_WINDOW_WIDTH = 1200
    INITIAL_WINDOW_HEIGHT = 800
    
    screen = pygame.display.set_mode((INITIAL_WINDOW_WIDTH, INITIAL_WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Sliding N-Puzzle")

    state_manager = StateManager()
    
    def calculate_layout(width, height):
        """Calculate board cell size based on window dimensions"""
        board_area_width = width - SIDEBAR_WIDTH
        cell_size = board_area_width // n
        return cell_size

    def create_ui_components(width, height):
        """Create UI components based on window size"""
        board_area_width = width - SIDEBAR_WIDTH
        sidebar_x = board_area_width
        
        solve_button = Button(sidebar_x + 50, 50, 150, 50, "Solve (A*)")
        bfs_button = Button(sidebar_x + 50, 120, 150, 50, "Solve (BFS)")
        shuffle_button = Button(sidebar_x + 50, 190, 150, 50, "Shuffle")
        pause_button = Button(sidebar_x + 220, 190, 150, 50, "Pause")
        board_size_slider = Slider(sidebar_x + 220, 260, 150, 20, 2, 9, n)
        speed_slider = Slider(sidebar_x + 20, 260, 150, 20, 0.5, 20, 1)
        decision_log = DecisionLog(sidebar_x + 20, 300, 360, height - 320)
        metrics_display = Metrics(sidebar_x + 20, height - 40, 360, 20)
        
        return {
            'solve_button': solve_button,
            'bfs_button': bfs_button,
            'shuffle_button': shuffle_button,
            'pause_button': pause_button,
            'board_size_slider': board_size_slider,
            'speed_slider': speed_slider,
            'decision_log': decision_log,
            'metrics_display': metrics_display
        }

    cell_size = calculate_layout(INITIAL_WINDOW_WIDTH, INITIAL_WINDOW_HEIGHT)
    renderer = Renderer(screen, board, cell_size=cell_size)
    ui = create_ui_components(INITIAL_WINDOW_WIDTH, INITIAL_WINDOW_HEIGHT)

    def new_game(size):
        nonlocal board, shuffler, renderer, n, cell_size
        n = int(size)
        board = Board(n)
        shuffler = Shuffler(board)
        shuffler.shuffle()
        renderer.board = board
        # Recalculate cell size based on current window
        width, height = screen.get_size()
        cell_size = calculate_layout(width, height)
        renderer.cell_size = cell_size


    running = True
    clock = pygame.time.Clock()
    
    while running:
        width, height = screen.get_size()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                # Recalculate everything on window resize
                cell_size = calculate_layout(event.w, event.h)
                renderer.cell_size = cell_size
                ui = create_ui_components(event.w, event.h)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if ui['solve_button'].is_clicked(pos):
                    state_manager.set_state(GameState.SOLVING)
                    solver = AStarSolver(board)
                    solution = solver.solve()
                    if solution:
                        for move in solution:
                            if state_manager.get_state() == GameState.PAUSED:
                                while state_manager.get_state() == GameState.PAUSED:
                                    pygame.time.wait(100)
                                    for ev in pygame.event.get():
                                        if ev.type == pygame.MOUSEBUTTONDOWN:
                                            if ui['pause_button'].is_clicked(pygame.mouse.get_pos()):
                                                state_manager.set_state(GameState.SOLVING)

                            renderer.highlight_piece(board.get_empty_pos())
                            board.move(move)
                            metrics = solver.get_metrics()
                            ui['metrics_display'].set_metrics(metrics)
                            renderer.move_animation(board.get_empty_pos(), (board.get_empty_pos()[0], board.get_empty_pos()[1]), duration=ui['speed_slider'].value)
                            ui['decision_log'].add_message(f"Move: {move} - {solver.get_decision_basis()} Metrics: {metrics}")
                    state_manager.set_state(GameState.PLAYING)

                if ui['bfs_button'].is_clicked(pos):
                    state_manager.set_state(GameState.SOLVING)
                    solver = BFSSolver(board)
                    solution = solver.solve()
                    if solution:
                        for move in solution:
                            if state_manager.get_state() == GameState.PAUSED:
                                while state_manager.get_state() == GameState.PAUSED:
                                    pygame.time.wait(100)
                                    for ev in pygame.event.get():
                                        if ev.type == pygame.MOUSEBUTTONDOWN:
                                            if ui['pause_button'].is_clicked(pygame.mouse.get_pos()):
                                                state_manager.set_state(GameState.SOLVING)

                            renderer.highlight_piece(board.get_empty_pos())
                            board.move(move)
                            metrics = solver.get_metrics()
                            ui['metrics_display'].set_metrics(metrics)
                            renderer.move_animation(board.get_empty_pos(), (board.get_empty_pos()[0], board.get_empty_pos()[1]), duration=ui['speed_slider'].value)
                            ui['decision_log'].add_message(f"Move: {move} - {solver.get_decision_basis()} Metrics: {metrics}")
                    state_manager.set_state(GameState.PLAYING)

                if ui['shuffle_button'].is_clicked(pos):
                    shuffler.shuffle(100)
                
                if ui['pause_button'].is_clicked(pos):
                    if state_manager.get_state() == GameState.PAUSED:
                        state_manager.set_state(GameState.PLAYING)
                    else:
                        state_manager.set_state(GameState.PAUSED)

                new_size = ui['board_size_slider'].get_value(pos)
                if new_size is not None and int(new_size) != n:
                    new_game(new_size)

                ui['speed_slider'].get_value(pos)

        # Manual playing logic
        if state_manager.get_state() == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            moved = False
            if keys[pygame.K_UP]:
                moved = board.move("DOWN") # We move the empty space down, which is like moving the tile up
            elif keys[pygame.K_DOWN]:
                moved = board.move("UP")
            elif keys[pygame.K_LEFT]:
                moved = board.move("RIGHT")
            elif keys[pygame.K_RIGHT]:
                moved = board.move("LEFT")
            if moved:
                 ui['decision_log'].add_message("Manual Move")

        # Drawing
        screen.fill(WHITE)
        renderer.draw_grid()
        renderer.draw_pieces()
        ui['solve_button'].draw(screen)
        ui['bfs_button'].draw(screen)
        ui['shuffle_button'].draw(screen)
        ui['pause_button'].draw(screen)
        ui['speed_slider'].draw(screen)
        ui['board_size_slider'].draw(screen)
        ui['decision_log'].draw(screen)
        ui['metrics_display'].draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

