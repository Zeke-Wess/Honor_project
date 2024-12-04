import pygame, players, random
from Images.image_names import *


'''Initiating constants'''
pygame.init()
size = width, height = 1400, 925 #Screen Size
screen = pygame.display.set_mode(size) #Defining the screen
clock = pygame.time.Clock()  #Set clock for refresh rate
fps = 30   #Set the refresh rate
Running = True

'''Initiailizing variables'''
person_selected = False #Used in coupling scene
couple_num = 0 #The number of couples created
couples = [] # A list Couple Objects
couple_list = [] # A list of Person tuples
guessed_couples = 0
scene = None # A string representing the current scene
win = False 
rounds = 1
couple_selected = False
open_pos = [7, 6, 5, 4, 3, 2, 1, 0]
font = pygame.font.Font(None, 100)



class GameObject(pygame.sprite.Sprite):   
    '''A class that stores info, and methods for each object in the program'''
    def __init__(self, image_name):
        '''intitialzies variables'''
        super().__init__()
        self.image_id = image_name  # Saves the initial image url, useful for changing the image
        self.image = pygame.image.load(img_dict[self.image_id]).convert() #The actual image Surface object
        self.rect = self.image.get_rect()  #The rectangle coresponding to the object


class BasicImage(pygame.sprite.Sprite):

    def __init__(self, size):
        super().__init__()
        self.image = pygame.Surface((size))
        self.rect = self.image.get_rect()


class Button(GameObject):
    '''A specialized game object that has transparency for white pixels'''
    
    def __init__(self, image_name):
        super().__init__(image_name)
        pygame.Surface.set_colorkey(self.image, (255, 255, 255))


class Charachter(pygame.sprite.Sprite):
    '''A class for the selectable people during the coupling phase'''
    def __init__(self, image_id, person: players.Person, position):
        '''initiaizes variables'''
        super().__init__()
        self.image_id = image_id
        self.image = pygame.image.load(img_dict[image_id]).convert()
        self.rect = self.image.get_rect()
        self.person = person
        self.pos = position
        self._selected = False
        self._is_option = False

    def toggle_select(self):
        '''Toggles if this object is sleceted or not'''
        if self._selected:
            self.deselect()
        else:
            self.select()

    def select(self):
        '''Changes the image to "Selected_image_url"'''
        self.image = pygame.image.load(selected_img_dict[self.image_id]) # Makes the image the selcted version of it
        self._selected = True

    def deselect(self):
        '''Changes the image to the original image'''
        self.image = pygame.image.load(img_dict[self.image_id]) # Makes the image the unselected version of it
        self._selected = False

    def make_option(self):
        self._is_option = True
        self.image = pygame.image.load(option_img_dict[self.image_id]).convert()

    def make_not_option(self):
        self.image = pygame.image.load(img_dict[self.image_id]).convert()
        self._is_option = False

    def is_selected(self):
        return self._selected
    
    def is_option(self):
        return self._is_option

    def make_correct(self):
        self.image = pygame.image.load(correct_img_dict[self.image_id]).convert()


class Couple(pygame.sprite.Sprite):
    '''A charachter wrapper that stores two charachters, and combines their Rects'''

    def __init__(self, person1:Charachter, person2:Charachter, position):
        '''Initializes variables and creates the image'''

        self.image = pygame.Surface((200, 200)).convert()
        self.rect = self.image.get_rect(width=200)
        self.pos = position
        self.person1 = person1
        self.person2 = person2
        self.correct = False
        #Makes the image both people side by side
        self.image.blits(((self.person1.image, (self.rect.left, self.rect.top)), (self.person2.image, (self.rect.centerx, self.rect.top))))


    def select(self):
        '''Changes the image of the couple to be the selected verion'''
        self.person1.select()
        self.person2.select()
        self.image.blits(((self.person1.image, (0, 0)), (self.person2.image, (100, 0))))


    def deselect(self):
        '''Changes the image of the couple to be the regular version'''
        self.person1.deselect()
        self.person2.deselect()
        self.image.blits(((self.person1.image, (0, 0)), (self.person2.image, (100, 0))))

    def make_correct(self):
        '''Changes the image of the couple to be the correct version'''
        self.correct = True
        self.person1.make_correct()
        self.person2.make_correct()
        self.image.blits(((self.person1.image, (0,0)), (self.person2.image, (100, 0))))

        
def place_player(player:Charachter):
    player.rect.update(100 + (player.pos % 8)*150, 25 + (player.pos>7)*675, player.rect.width, player.rect.height)

def create_players():
    '''Creates the Charahcter objects and returns a sprite group containing them'''
    people_sprites = pygame.sprite.Group()
    player_names = players.setup()
    random.shuffle(player_ids)
    player_ids.pop()
    for i, img_id in enumerate(player_ids):
        player = Charachter(img_id, player_names[i], i)
        place_player(player)
        people_sprites.add(player)
    
    return people_sprites


'''Initialzing Sprites'''
background = BasicImage(size)

people_sprites = create_players()
submit_button = Button("Submit_button")
submit_button.rect.update(650, 800, submit_button.rect.width, submit_button.rect.height)
start_button = Button("Start_button")
start_button.rect.update(650, 800, start_button.rect.width, start_button.rect.height)
split_button = Button("Split_button")
split_button.rect.update(650, 438, split_button.rect.width, split_button.rect.height)
scene_sprites = pygame.sprite.Group(people_sprites)
scene = "Coupling"

while Running: #Loop the program

    for event in pygame.event.get():  #Loop through the events in the event queue

        if event.type == pygame.MOUSEBUTTONDOWN and event.dict["button"] == 1: #If I left click
            mouse_pos = pygame.mouse.get_pos()

            if scene == "Victory":
                scene_sprites.empty()
                couples = []
                scene = None
                if rounds > 1:
                    win_message = font.render(f"You won in {rounds} rounds!", True, (50, 137, 200), (0, 0, 0))
                else:
                    win_message = font.render(f"You won in {rounds} round!", True, (50, 137, 200), (0, 0, 0))
                background.image.blit(win_message, (700 - win_message.get_rect().width//2, 463 - win_message.get_rect().height//2))


            elif scene == "Reset":

                if start_button.rect.collidepoint(mouse_pos):
                    if person_selected and person_selected.correct == False:
                        person_selected.deselect()
                    person_selected = False
                    scene_sprites.remove([start_button, couple_results])
                    couple_results = None
                    rounds += 1


                    new_couples = []
                    couple_list = []
                    guessed_couples = 0
                    for couple in couples:
                        if couple.correct == False:
                            couple_num -= 1
                            scene_sprites.remove(couple)
                            couple.person1.rect.width, couple.person1.rect.height = (100, 200)
                            couple.person2.rect.width, couple.person2.rect.height = (100, 200)
                            people_sprites.add([couple.person1, couple.person2])
                            open_pos.append(couple_num)
                        else:
                            new_couples.append(couple)
                            couple.rect.update((120 + (guessed_couples % 4)*320, 250 + (guessed_couples>3)*225), (couple.rect.size))
                            guessed_couples += 1

                    couples = new_couples

                    scene_sprites.add(people_sprites)
                    scene = "Coupling"


            elif scene == "Truth":


                for couple in couples:
                    if couple.rect.collidepoint(mouse_pos) and couple.correct == False:
                        couple.select()
                        if person_selected:
                            person_selected.deselect()
                        if person_selected == couple:
                            person_selected = False
                            scene_sprites.remove(submit_button)
                        else:
                            person_selected = couple
                            scene_sprites.add(submit_button)

                if submit_button.rect.collidepoint(mouse_pos) and person_selected:
                    truth_result = players.check((person_selected.person1.person, person_selected.person2.person))
                    scene_sprites.remove(submit_button)
                    scene = "Reset"
                    scene_sprites.add(start_button)

                    if truth_result == True:
                        person_selected.make_correct()
                        couple_results.image.fill((0, 255, 0))
                        for i in range(11):
                            couple_results.image.blit(pygame.image.load(img_dict["Check"]).convert(), (25 + i*100, 0))
                        scene_sprites.add(couple_results)

                    else:
                        couple_results.image.fill((255, 0, 0))
                        for i in range(11):
                            couple_results.image.blit(pygame.image.load(img_dict["Cross"]).convert(), (25 + i*100, 0))
                        scene_sprites.add(couple_results)
                        #Make both people not options for each other
                        person_selected.person1.person.options.remove(person_selected.person2.person.number)
                        person_selected.person2.person.options.remove(person_selected.person1.person.number)


            elif scene == "Start_truth":

                if start_button.rect.collidepoint(mouse_pos):

                    scene_sprites.remove(couple_results)
                    scene_sprites.remove(start_button)
                    scene = "Truth"


            elif scene == "Coupling":

                #If the user submits thier couple selection
                if submit_button.rect.collidepoint(mouse_pos) and couple_num == 8:
                    

                    for couple in couples:
                        couple_list.append((couple.person1.person, couple.person2.person))

                    correct_couples = players.bulk_check(couple_list)
                    if correct_couples == 8:
                        win = True
                    couple_results = BasicImage((1100, 50))
                    if correct_couples == guessed_couples:
                        scene = "Reset"
                        for couple in couples[guessed_couples:]:
                            couple.person1.person.options.remove(couple.person2.person.number)
                            couple.person2.person.options.remove(couple.person1.person.number)

                    for i in range(8): #Add a green box for every correct coupple, red for inccorect ones
                        if correct_couples > 0:
                            couple_results.image.blit(pygame.image.load(img_dict["Check"]).convert(), (i*150, 0, 50, 50))
                        else:
                            couple_results.image.blit(pygame.image.load(img_dict["Cross"]).convert(), (i*150, 0, 50, 50))

                        correct_couples -= 1
                        
                    couple_results.rect.update(150, 100, 1100, 50)   
                    scene_sprites.add(couple_results)
                    scene_sprites.remove(submit_button)
                    scene_sprites.add(start_button)
                    if scene == "Coupling": #Needed if we skip right to reset
                        scene = "Start_truth"
                    if win:
                        scene = "Victory"

                if couple_num > 0: #Selecting couples to split
                    for couple in couples:
                        if couple.rect.collidepoint(mouse_pos) and couple.correct == False:
                            couple.select()
                            if couple_selected == False:
                                couple_selected = couple
                                scene_sprites.add(split_button)

                            elif couple_selected == couple:
                                couple.deselect()
                                couple_selected = False
                                scene_sprites.remove(split_button)
                            else:
                                couple_selected.deselect()
                                couple_selected = couple

                if couple_selected and split_button.rect.collidepoint(mouse_pos): #Spliting the couples
                    couple_selected.deselect()
                    if couple_num == 8:
                        submit_button.remove(scene_sprites)
                    couple_num -= 1
                    couples.remove(couple_selected)

                    couple_selected.person1.rect = pygame.Rect(0, 0, 100, 200)
                    couple_selected.person2.rect = pygame.Rect(0, 0, 100, 200)
                    open_pos.append(couple_selected.pos)
                    open_pos.sort(reverse=True)
                    place_player(couple_selected.person1)
                    place_player(couple_selected.person2)
                    scene_sprites.add((couple_selected.person1, couple_selected.person2))
                    people_sprites.add([couple_selected.person1, couple_selected.person2])

                    split_button.remove(scene_sprites)
                    couple_selected = False



                if person_selected == False:

                    for person in people_sprites:  #Find if I clicked anyone

                        if person.rect.collidepoint(mouse_pos):
                            person.select()
                            person_selected = person

                            #Updates all potential matches' image
                            for sprite in people_sprites:
                                if sprite.person.number in person.person.options:
                                    sprite.make_option()

                else: #If I have someone selected, couple them with the next person selected

                    for person in people_sprites: #Coupling

                        #If I clicked on an available person couple them
                        if person.is_option() == True and person.rect.collidepoint(mouse_pos) == True:
                            #Deselect selected people who are selected
                            person_selected.deselect()
                            person.make_not_option()
                            for sprite in people_sprites:
                                if sprite.is_option() == True:
                                    sprite.make_not_option()

                            #Create a new Couple object and add it to the couples list
                            couples.append(Couple(person_selected, person, open_pos.pop()))
                            
                            #Move the Couple into the right spot
                            couple_num = len(couples)
                            couples[-1].rect.update((120 + ((couples[-1].pos) % 4)*320, 250 + (couples[-1].pos > 3)*225), (couples[-1].rect.size))

                            #Remove the hitbox for the person
                            person.rect.update(person.rect.left, person.rect.top, 0, 0)
                            person_selected.rect.update(person_selected.rect.left, person_selected.rect.top, 0, 0)

                            #Remove them from the people sprite group
                            people_sprites.remove((person, person_selected))
                            scene_sprites.remove(person, person_selected)

                            person_selected = False

                            if couple_num == 8:
                                scene_sprites.add(submit_button)


                        #If I click on the selected person, deselect them
                        if person.is_selected() and person.rect.collidepoint(mouse_pos):
                            person.deselect()
                            person_selected = False

                            for sprite in people_sprites:
                                if sprite.is_option() == True:
                                    sprite.make_not_option()

        if event.type == pygame.QUIT: #When you hit the X, it quits
            Running = False

    pygame.event.clear() #Clear the event que to stop memory leaks


    screen.blit(background.image, background.rect, background.rect)
    scene_sprites.draw(screen)
    for couple in couples:
        screen.blit(couple.image, couple.rect)

    pygame.display.flip()   #Show the next frame
    clock.tick(fps)    #Limit FPS
