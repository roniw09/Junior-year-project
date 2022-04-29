import socket, pygame
from by_size import *
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, SERVER_IP, SERVER_PORT
from checkers.game import Game

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def extract_reply(reply):
    pass


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def playing():
    pass


def main():
    client_socket = socket.socket()
    try:
        client_socket.connect(('127.0.0.1', 8802))
        print("Connected!")
    except:
        print('cant connect')
        return

    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    in_game = False

    while run:
        clock.tick(FPS)
        if game.winner() is not None:
            print(game.winner())
            client_socket.close()
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client_socket.close()
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # row, col = get_row_col_from_mouse(pos)
                # game.select(row, col)
                if 183 <= pos[0] <= 505 and 350 <= pos[1] <= 448:
                    send_with_size(client_socket, 'PLAY')
                    response = recv_by_size(client_socket)
                    game = extract_reply(response)
                    playing()

        game.update()
    
    pygame.quit()


if __name__ == '__main__':
    main()
