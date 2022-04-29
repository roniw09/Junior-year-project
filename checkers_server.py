import socket, threading
from by_size import *


players = []
in_game = []


def reply_by_code(fields, id):
    global players, in_game
    code = fields[0]
    if code == 'PLAY':
        players[id - 1][1] = True
        search = True
        opponent = None
        while search or (players[id - 1] not in in_game):
            for player in players:
                if player[1] and (player[0] not in in_game):
                    in_game.append((players[id - 1], player))
                    opponent = player
                    search = False
        play_game(players[id - 1], opponent)
        return 'ENGM'
    pass


def play_game(client, opponent):
    send_with_size(client, 'COLR' + '~' + 'RED')
    send_with_size(client, 'COLR' + '~' + 'BLACK')


def handle_client(client, id, addr):
    global in_game
    data = recv_by_size(client)
    if data == b'':
        print('client disconnected')
        return
    fields = data.split('~')
    response = reply_by_code(fields, id)
    send_with_size(client, response)

    pass


def main():
    global players
    srv_sock = socket.socket()
    srv_sock.bind(('0.0.0.0', 8802))

    srv_sock.listen(20)
    i = 1
    while True:
        print('\nMain thread: before accepting ...')
        cli_sock, addr = srv_sock.accept()
        t = threading.Thread(target=handle_client, args=(cli_sock, i, addr))
        t.start()
        i += 1
        players.append((t, False))
        if i > 3:  # for tests change it to 4
            print('\nMain thread: going down for maintenance')
            break

    # all_to_die = True
    print('Main thread: waiting to all clints to die')
    for t in players:
        t.join()
    srv_sock.close()
    print('Bye ..')


if __name__ == '__main__':
    main()
