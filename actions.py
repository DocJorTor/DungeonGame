import random
from models import Player, Monster, Object
from config import monsters


def cont2():
    move_on = input('')


def intro():
    print('\n\n\n\n\nWelcome to the dungeon simulator. You will make a character and see if they can make it to the end'
          '\nof the dungeon without dying. Along the way you may find items. Red potions boost your strength,'
          '\nblue potions boost your speed, and steaks improve your health. Glowing items have a chance for a much'
          '\nbigger reward, but also for a massive negative effect. You can always choose to not pick up an item.'
          '\nYou will choose how many monsters you will need to defeat, and items may or may not be available.'
          '\nThis game relied HEAVILY on RNG. Press any key to continue the game when stops occur. Good luck.\n\n\n')


def choose_your_stats():

    def build(attribute, total):
        value = int(input(f"Enter value to put into {attribute}: "))
        if value <= total:
            total -= value
            print(f"You have put {value} points into {attribute}: ")
        else:
            print(f"Too many points requestd, you only have {total} left")
            return build(attribute, total)
        return attribute, value, total

    stat_points = 50
    name = input("What is your player's name?: ")
    print('You have 50 base points to allot to your character')
    strength = health = speed = a = v = t = 0
    storage = (a, v, t)
    while stat_points != 0:
        stats = ['strength', 'speed','health']
        for s in stats:
            storage = build(s, stat_points)
            if storage[0] == 'strength':
                strength += storage[1]
            elif storage[0] == 'speed':
                speed += storage[1]
            elif storage[0] == 'health':
                health += storage[1]   
            stat_points = storage[2] 
        print(f"\nYour stats are:\nStrength: {strength}\nSpeed: {speed}\nHealth: {health}")
        print(f"You have {stat_points} points left!")
    print('Your stats are now locked.')
    return Player(name, health, strength, speed)


def monster_creation(amount = 0, importing=False):
    mm = []
    if importing:
        for m in monsters:
            mm.append(Monster(random.randint(m[0][0], m[0][1]), random.randint(m[1][0], m[1][1]), random.randint(m[2][0], m[2][1])))
    else:
        for _ in range(0,amount):
            strength = int(input("Enter min monster strength: "))
            strengthRange = int(input("Enter strength range: "))
            strengthRange += strength

            speed = int(input("Enter min monster speed: "))
            speedRange = int(input("Enter speed range: "))
            speedRange += speed

            health = int(input("Enter min monster health: "))
            healthRange = int(input("Enter health range: "))
            healthRange += health

            mm.append(Monster(random.randint(health, healthRange), random.randint(strength, strengthRange), random.randint(speed, speedRange)))

    return mm

def objects():
    steak = Object('Steak', 20)
    glowing_steak = Object('Glowing Steak', random.randint(-30, 30))
    red_potion = Object('Red Potion', 10)
    glowing_red_potion = Object('Dark Red Potion', random.randint(-20, 20))
    blue_potion = Object('Blue Potion', 10)
    glowing_blue_potion = Object('Dark Blue Potion', random.randint(-20, 20))
    return steak, glowing_steak, red_potion, glowing_red_potion, blue_potion, glowing_blue_potion


def confrontation(player, monster):
    if player.speed > monster.speed:
        playerFirst = True
    elif player.speed < monster.speed:
        playerFirst = False
    else:
        num = random.randint(1, 2)
        playerFirst = True if num == 2 else False
    print(f'\nMonster stats:\nHealth: {monster.health}\nSpeed: {monster.speed}\nStrength: {monster.strength}')
    print(f'\nPlayer stats:\nHealth: {player.health}\nSpeed: {player.speed}\nStrength: {player.strength}')
    cont2()
    if playerFirst:
        print(f"\n{player.name} attacked first.")
        cont2()
        while (player.health > 0) and (monster.health > 0):
            monster.health -= player.strength
            print(f'Monster lost {player.strength} points of health!')
            print(f'Monster has {monster.health} points of health left.')
            cont2()
            if monster.health > 0:
                player.health -= monster.strength
                print(f'{player.name} lost {monster.strength} points of health!')
                print(f'{player.name} has {player.health} points of health left.')
                cont2()
            else:
                break
    else:
        print(f"\nMonster attacked first.")
        while (player.health > 0) and (monster.health > 0):
            player.health -= monster.strength
            print(f'{player.name} lost {monster.strength} points of health!')
            print(f'{player.name} has {player.health} points of health left.')
            cont2()
            if player.health > 0:
                monster.health -= player.strength
                print(f'Monster lost {player.strength} points of health!\n')
                print(f'Monster has {monster.health} points of health left.')
                cont2()
            else:
                break
    if player.health <= 0:
        print(f'{player.name} has died. GAME OVER')
        return False
    else:
        print(f"The monster has died. {player.name} has {player.health} health points left.")
        return True


def item_pickup(s, gs, r, gr, b, gb):
    chance = random.randint(1, 100)
    if 1 <= chance <= 8:
        choice = input('You found a glowing steak! Would you like to pick it up?:(y/n) ')
        if choice == 'y':
            return gs
        else:
            print('You chose to walk away.')
    elif 8 < chance <= 17:
        choice = input('You found a glowing red potion! Would you like to pick it up?:(y/n) ')
        if choice == 'y':
            return gr
        else:
            print('You chose to walk away.')
    elif 17 < chance <= 25:
        choice = input('You found a glowing blue potion! Would you like to pick it up?:(y/n) ')
        if choice == 'y':
            return gb
        else:
            print('You chose to walk away.')
    elif 25 < chance <= 45:
        choice = input('You found a steak! Would you like to pick it up?:(y/n) ')
        if choice == 'y':
            return s
        else:
            print('You chose to walk away.')
    elif 45 < chance <= 65:
        choice = input('You found a red potion! Would you like to pick it up?:(y/n) ')
        if choice == 'y':
            return r
        else:
            print('You chose to walk away.')
    elif 65 < chance <= 78:
        choice = input('You found a blue potion! Would you like to pick it up?:(y/n) ')
        if choice == 'y':
            return b
        else:
            print('You chose to walk away.')
            return False
    else:
        print('You did not find an item :(')
        return False


def cont():
    move_on = input('Press Enter to continue')


def findItem(item_found, player):
    if item_found.name == 'Glowing Steak':
        player.health += item_found.effect
        print(f"Health changed by {item_found.effect}. Player health is now: {player.health}")
        cont2()
    if item_found.name == 'Dark Red Potion':
        player.strength += item_found.effect
        print(f"Strength changed by {item_found.effect}. Player strength is now: {player.strength}")
        cont2()
    if item_found.name == 'Dark Blue Potion':
        player.speed += item_found.effect
        print(f"Speed changed by {item_found.effect}. Player speed is now: {player.speed}")
        cont2()
    if item_found.name == 'Blue Potion':
        player.speed += item_found.effect
        print(f"Speed changed by {item_found.effect}. Player speed is now: {player.speed}")
        cont2()
    if item_found.name == 'Red Potion':
        player.strength += item_found.effect
        print(f"Strength changed by {item_found.effect}. Player strength is now: {player.strength}")
        cont2()
    if item_found.name == 'Steak':
        player.health += item_found.effect
        print(f"Health changed by {item_found.effect}. Player health is now: {player.health}")
        cont2()
