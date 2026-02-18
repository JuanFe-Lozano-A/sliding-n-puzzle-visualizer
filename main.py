import pygame
from core.board import Board
from core.state_manager import StateManager, GameState
from core.shuffler import Shuffler
from solvers.a_star import AStarSolver
from solvers.bfs import BFSSolver
from ui.renderer import Renderer
from ui.components import Button, Slider, DecisionLog
from ui.colors import *

def main():
    pygame.init()
    n = 4  # Board size
    board = Board(n)
    shuffler = Shuffler(board)
    shuffler.shuffle()

    screen_size = n * 80
    screen = pygame.display.set_mode((screen_size + 400, screen_size))
    pygame.display.set_caption("Sliding N-Puzzle")

    renderer = Renderer(screen, board)
    state_manager = StateManager()

    # UI Components
    solve_button = Button(screen_size + 50, 50, 150, 50, "Solve (A*)")
    bfs_button = Button(screen_size + 50, 120, 150, 50, "Solve (BFS)")
    shuffle_button = Button(screen_size + 50, 190, 150, 50, "Shuffle")
    pause_button = Button(screen_size + 220, 190, 150, 50, "Pause")
    board_size_slider = Slider(screen_size + 220, 260, 150, 20, 2, 9, n)
    decision_log = DecisionLog(screen_size + 20, 300, 360, screen_size - 320)

    def new_game(size):
        nonlocal board, shuffler, renderer, screen, screen_size
        n = int(size)
        board = Board(n)
        shuffler = Shuffler(board)
        shuffler.shuffle()
        screen_size = n * 80
        screen = pygame.display.set_mode((screen_size + 400, screen_size))
        renderer = Renderer(screen, board)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if solve_button.is_clicked(pos):
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
                                            if pause_button.is_clicked(pygame.mouse.get_pos()):
                                                state_manager.set_state(GameState.SOLVING)

                            renderer.highlight_piece(board.get_empty_pos())
                            board.move(move)
                            renderer.move_animation(board.get_empty_pos(), (board.get_empty_pos()[0], board.get_empty_pos()[1]), duration=speed_slider.value)
                            decision_log.add_message(f"Move: {move} - {solver.get_decision_basis()}")
                    state_manager.set_state(GameState.PLAYING)

                if bfs_button.is_clicked(pos):
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
                                            if pause_button.is_clicked(pygame.mouse.get_pos()):
                                                state_manager.set_state(GameState.SOLVING)

                            renderer.highlight_piece(board.get_empty_pos())
                            board.move(move)
                            renderer.move_animation(board.get_empty_pos(), (board.get_empty_pos()[0], board.get_empty_pos()[1]), duration=speed_slider.value)
                            decision_log.add_message(f"Move: {move} - {solver.get_decision_basis()}")
                    state_manager.set_state(GameState.PLAYING)

                if shuffle_button.is_clicked(pos):
                    shuffler.shuffle(100)
                
                if pause_button.is_clicked(pos):
                    if state_manager.get_state() == GameState.PAUSED:
                        state_manager.set_state(GameState.PLAYING)
                    else:
                        state_manager.set_state(GameState.PAUSED)

                new_size = board_size_slider.get_value(pos)
                if new_size is not None and int(new_size) != n:
                    new_game(new_size)

                speed_slider.get_value(pos)


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
                 decision_log.add_message("Manual Move")


        # Drawing
        screen.fill(WHITE)
        renderer.draw_grid()
        renderer.draw_pieces()
        solve_button.draw(screen)
        bfs_button.draw(screen)
        shuffle_button.draw(screen)
        pause_button.draw(screen)
        speed_slider.draw(screen)
        board_size_slider.draw(screen)
        decision_log.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
