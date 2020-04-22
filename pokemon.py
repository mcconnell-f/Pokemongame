import random
from characters import CHARACTERS
from moves_dictionary import MOVES_DICTIONARY
import pygame
import math #https://www.knowledgehut.com/blog/programming/python-rounding-numbers
def round_down(n, decimals=0):
    '''Rounds any decimal down to an integer'''
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier
class Pokemon:


    def __init__(self,name):
        name = name.lower()
        name = name.title()
        self.name = name
        self.type_ = CHARACTERS[name]['Type']
        self.HP = CHARACTERS[name]['HP']
        self.moves = CHARACTERS[name]['Moves']
        self.attack = CHARACTERS[name]['Attack']
        self.defense = CHARACTERS[name]['Defense']
        self.speed = CHARACTERS[name]['Speed']
        self.experience = 0
        self.level = 1

    def calculate_damage(self,defender,move,screen=None):
        '''Calculates the damage from an attack'''
        modifier = self.critical_coeficient(screen)*(random.randint(85,100)/100)*self.type_coeficient(move,defender)
        damage = ((((2*self.level)/5+2)*MOVES_DICTIONARY[move]['power']*(CHARACTERS[self.name]['Attack']/CHARACTERS[defender.name]['Defense']))/50)*modifier
        return damage
    
    def __str__(self):
        moves_ = self.moves
        finalsent = f"{self.name} has moves {moves_} \n"
        for move in moves_:
            finalsent += f"{move} with {MOVES_DICTIONARY[move]['power']} power is super effective against the types {MOVES_DICTIONARY[move]['super effective against']} \n"
            finalsent += f"{move} is not very effective against the types {MOVES_DICTIONARY[move]['not very effective against']} \n"
        return finalsent


    def who_attacks_first(self,enemy): 
        '''Determines which Pokemon attacks first based on their speed'''
        if self.speed >= enemy.speed:
            print("Your Pokemon will attack first.")
            return True
        else:
            print("Your opponent will attack first.")
            return False

    def critical_coeficient(self,screen=None):
        '''Determines whether a hit is critical or not'''
        if random.randint(0,512) < self.speed:
            print("Critical hit!")
            if screen:
                basicFont = pygame.font.SysFont('Monospace',24)
                critical_text = basicFont.render('Critical Hit!!',True,(255,255,255))
                critical_rect = critical_text.get_rect()
                critical_rect.center = (400,550)
                screen.blit(critical_text,critical_rect)
                pygame.display.flip()
            return 2
        else:
            return 1

    def type_coeficient(self,selfmove,enemy):
        '''Determines the type coeeficient used to calculate damage'''
        opptypes = enemy.type_
        selfmove = selfmove.lower()
        selfmove = selfmove.title()
        typecoeff = 1
        for opptype in opptypes:
            if opptype in MOVES_DICTIONARY[selfmove]['super effective against']:
                typecoeff = typecoeff*2
            elif opptype in MOVES_DICTIONARY[selfmove]['not very effective against']:
                typecoeff = typecoeff/2
        return typecoeff

    def update_level(self,enemy_name):
        '''Updates level based on experience. Rounds down.'''
        self.experience = self.experience + CHARACTERS[enemy_name]['Experience']
        newlevel = int(round_down((self.experience)**(1/3)))
        if newlevel > self.level:
            for i in range(newlevel-self.level):
                print("Level up!")
            print(f"Your Pokemon has reached level {newlevel}")
        if newlevel != 0:
            self.level = newlevel

    def choose_move(self,screen=None):
        ''' Allows the user to choose a move for their Pokemon'''
        if screen == None:
            print("-----------------------------------------Please choose a move-------------------------------------")
            for move in self.moves:
                print(move)
            move = input("Enter the move")
            if move in self.moves:
                return MOVES_DICTIONARY[move]
            else:
                print("Please choose a move that is listed.")
                return self.choose_move()
        else:
            pygame.draw.rect(screen,(0,0,0),(50,425,700,150))
            basicFont = pygame.font.SysFont('Monospace',24)
            option_text = basicFont.render("Choose a move",True,(255,255,255))
            option_rect = option_text.get_rect()
            option_rect.center = (400,450)
            screen.blit(option_text,option_rect)
            move_button = []
            current_pos = 150
            ext_pos = 0
            for move in self.moves:
                tmp_text = basicFont.render(move,True,(255,255,255))
                tmp_rect = tmp_text.get_rect()
                tmp_rect.center = (current_pos,475+ext_pos)
                tmp_button = screen.blit(tmp_text,tmp_rect)
                move_button.append((tmp_button,move))
                current_pos += 150
                if current_pos >= 730:
                    current_pos = 150
                    ext_pos += 30
            pygame.display.flip()
            clicked = False
            while not clicked:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        for button,name in move_button:
                            if button.collidepoint(pos):
                                clicked = True
                                return MOVES_DICTIONARY[name]


    def choose_optimal_move(self,defender):
        ''' Chooses the optimal move for the computer(defender) based on damage'''
        moves_tuple = []
        for move in self.moves:
            moves_tuple.append(((MOVES_DICTIONARY[move]['power']*self.type_coeficient(move,defender)),move))
        moves_tuple.sort(reverse=True)
        optimal_move = moves_tuple[0][1]
        return MOVES_DICTIONARY[optimal_move]


    def battle(self,enemy,screen=None):
        ''' Battle until one Pokemon dies'''
        first = self.who_attacks_first(enemy)
        sentences = "" 
        self_full_HP = self.HP
        enemy_full_HP = enemy.HP
        while self.HP > 0 and enemy.HP > 0:
            if first == True:
                user_move = self.choose_move(screen)
            else:
                enemy_move = enemy.choose_optimal_move(self)
            if screen:
                pygame.draw.rect(screen,(0,0,0),(50,425,700,150))
            if first == True:
                damage = self.calculate_damage(enemy,user_move['name'],screen)
                enemy.HP = enemy.HP - damage
                sentences = []
                sentences += [f"After your {self.name}'s {user_move['name']} attack worth {damage :.2f} points:"]
                sentences += [f"Your HP: {self.HP :.2f} Enemy HP: {enemy.HP:.2f}"]
                print("\n".join(sentences))
                first = False
            else:
                damage = enemy.calculate_damage(self,enemy_move['name'],screen)
                self.HP = self.HP - damage
                sentences = []
                sentences += [f"After enemy's {enemy.name}'s {enemy_move['name']} attack worth {damage:.2f} points:"]
                sentences += [f"Your HP: {self.HP:.2f} Enemy HP: {enemy.HP:.2f}"]
                print("\n".join(sentences))
                first = True
            if screen:
                    self_HP_ratio = max(0,self.HP/self_full_HP)
                    enemy_HP_ratio = max(0,enemy.HP/enemy_full_HP)
                    pygame.draw.rect(screen,(255,0,0),(50,50,300,25))
                    pygame.draw.rect(screen,(255,0,0),(450,50,300,25))
                    pygame.draw.rect(screen,(0,255,0),(50,50,self_HP_ratio*300,25))
                    pygame.draw.rect(screen,(0,255,0),(450,50,enemy_HP_ratio*300,25))
                    basicFont = pygame.font.SysFont('Monospace',24)
                    current_pos = 450
                    for sentence in sentences:
                        battle_text = basicFont.render(sentence,True,(255,255,255))
                        battle_rect = battle_text.get_rect()
                        battle_rect.center = (400,current_pos)
                        screen.blit(battle_text,battle_rect)
                        current_pos += 40
                    pygame.display.flip()
                    clicked = False
                    while not clicked:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                exit()
                            if event.type == pygame.KEYDOWN or pygame.mouse.get_pressed()[0]:
                                clicked = True
        if self.HP <= 0:
            sentences = "GAME OVER- Your Pokemon has fainted."
            print(sentences)
        elif enemy.HP <= 0:
            sentences = f"You beat {enemy.name}!"
            print()
            self.update_level(enemy.name)
        if screen:
                pygame.draw.rect(screen,(0,0,0),(50,425,700,150))
                basicFont = pygame.font.SysFont('Monospace',24)
                battle_text = basicFont.render(sentences,True,(255,255,255))
                battle_rect = battle_text.get_rect()
                battle_rect.center = (400,450)
                screen.blit(battle_text,battle_rect)
                pygame.display.flip()
                clicked = False
                while not clicked:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exit()
                        if event.type == pygame.KEYDOWN or pygame.mouse.get_pressed()[0]:
                            clicked = True 
        

string_to_pokemon_class = {'Pikachu' : Pokemon('Pikachu'),
                          'Charizard' : Pokemon('Charizard'),
                           'Squirtle' : Pokemon('Squirtle'),
                          'Jigglypuff' : Pokemon('Jigglypuff'),
                          'Gengar': Pokemon('Gengar'),
                          'Magnemite': Pokemon('Magnemite'),
                          'Bulbasaur': Pokemon('Bulbasaur'),
                          'Charmander': Pokemon('Charmander'),
                          'Beedrill': Pokemon('Beedrill'),
                          'Golem': Pokemon('Golem'),
                          'Dewgong': Pokemon('Dewgong'),
                          'Hypno': Pokemon('Hypno'),
                          'Cleffa': Pokemon('Cleffa'),
                          'Cutiefly': Pokemon('Cutiefly')}
