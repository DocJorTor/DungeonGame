import random
from actions import intro, choose_your_stats, objects, confrontation, item_pickup, cont, cont2, monster_creation, findItem

def main():
    game_score = 0
    intro()
    player = choose_your_stats()
    i = input("Import?: (y/n): ")
    current_round = 1
    if i.lower() == 'y':
        monsters = monster_creation(0,True)
        amount = len(monsters)
    else:
        amount = int(input('How many monsters would you like to fight?: '))
        monsters = monster_creation(amount,False)

    for i in range(1, amount + 1):
        items = objects()
        print(f"\nConfrontation number {current_round}\n----------------------\n")
        cont2()
        random.shuffle(monsters)
        monster = monsters[0]
        game_on = confrontation(player, monster)
        if game_on:
            item_found = item_pickup(*items)
            if item_found:
                findItem(item_found, player)
            if player.health <= 0:
                print(f'{player.name} has died. GAME OVER')
                break
            current_round += 1
            game_score += player.strength
            monsters.remove(monster)
            if current_round % 5 == 0:
                print(f'Congrats, {player.name} made it five rounds. They found a nice fire to relax by. Health +50.')
                player.health += 50
        else:
            if player.health > 0:
                print(f'YOU WIN! You had {player.health} health points left.\n')
                if player.health >= 50:
                    print('You cleared the cave easily.')
                    game_score += 20
                if 11 <= player.health < 20:
                    print('You\'re a little scratched, but alive.')
                    game_score += 10
                if player.health < 11:
                    print('You barely made it out alive.')
                break
            else:
                print("You lost")
                break

    game_score *= current_round
    print('\nThe game has ended.')
    print(f'\nYour score was {game_score}.')


main()
