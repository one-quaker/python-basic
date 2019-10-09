import random
import time
import sys


STONE = 'stone 🏔'
PAPER = 'paper ✉️'
SCISSORS = 'scissors ✂️'


ITEM_LIST = (STONE, PAPER, SCISSORS)
USER_SCORE = 0
ENEMY_SCORE = 0
ROUND = 1


GAME_LOG = []


def who_win(*choice_list):
    rules = {
        (STONE, STONE): None,
        (STONE, PAPER): PAPER,
        (STONE, SCISSORS): STONE,

        (PAPER, STONE): PAPER,
        (PAPER, PAPER): None,
        (PAPER, SCISSORS): SCISSORS,

        (SCISSORS, STONE): STONE,
        (SCISSORS, PAPER): SCISSORS,
        (SCISSORS, SCISSORS): None,
    }
    return rules[choice_list]


def print_stat():
    print(32 * '-')
    print(f'User score: {USER_SCORE}\nEnemy score: {ENEMY_SCORE}')
    print(32 * '-')


def make_csv(data):
    import csv
    import datetime

    ts = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    fn = f'match-{ts}.csv'
    with open(fn, mode='w') as csv_file:
        fieldnames = ['round', 'user_choice', 'enemy_choice', 'user_score', 'enemy_score', 'winner']
        writer = csv.writer(csv_file)

        writer.writerow(fieldnames)
        for line in data:
            writer.writerow(line)


def print_winner():
    msg = '\ngame over!\n'
    if USER_SCORE > ENEMY_SCORE:
        msg += 'User win!!! 🍾😎💪'
    elif USER_SCORE < ENEMY_SCORE:
        msg += 'Enemy win!!! 💀🤖💀'
    else:
        msg += 'Draw! 🙂🤝🤖'
    print(msg.upper())


while True: # game loop
    print_stat()

    user_input = input('\nMake your choice:\n1: {0}\n2: {1}\n3: {2}\n\n'.format(*ITEM_LIST))
    user_choice = None

    if user_input in ('1', '2', '3'):
        user_choice = ITEM_LIST[int(user_input) - 1]
    else:
        print('\nInvalid choice "{}"\nPlease try again...\n'.format(user_input))
        time.sleep(1)
        continue

    if user_choice:
        enemy_choice = random.choice(ITEM_LIST)
        result = who_win(user_choice, enemy_choice)
        print(f'\nround {ROUND} 🥊\n😎 user: {user_choice}\n🤖 enemy: {enemy_choice} \n')

        if result == user_choice:
            print('User win! 😎\n')
            USER_SCORE += 1
            winner = 'user'
        elif result == enemy_choice:
            print('Enemy win! 🤖\n')
            ENEMY_SCORE += 1
            winner = 'enemy'
        else:
            print('Draw! 🤝\nNext round!\n')
            winner = ''
        GAME_LOG.append([ROUND, user_choice, enemy_choice, USER_SCORE, ENEMY_SCORE, winner])
        ROUND += 1

    if ROUND > 5 and USER_SCORE != ENEMY_SCORE: # if all True - stop game loop
        break


print_stat()
# print(GAME_LOG)
make_csv(GAME_LOG)
print_winner()
