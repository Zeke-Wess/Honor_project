import pygame, players, time
from Images.image_names import img_dict, selected_img_dict


'''Initiating variables'''
pygame.init()
size = width, height = 1024, 768 #Screen Size
screen = pygame.display.set_mode(size) #Defining the screen
clock = pygame.time.Clock()  #Set clock for refresh rate
fps = 120   #Set the refresh rate
couple_selection = []  #List used when we select couples
couple_num = 0 #The number of couples created
couples = [] # A list of tuples of Person objects
Running = True

class GameObject:   
    '''A class that stores info, and methods for each object in the program'''
    def __init__(self, image_name):
        '''intitialzies variables'''
        self.image_name = image_name  # Saves the initial image url, useful for changing the image
        self.image = pygame.image.load(img_dict[self.image_name]).convert() #The actual image Surface object
        self.rect = self.image.get_rect()  #The rectangle coresponding to the object


class Button(GameObject):
    '''A class that detects when the cursor clicks this object'''




class Draggable(Button):
    '''Allows you to drag an object, also selects it'''

    def __init__(self, image: pygame.Surface):
        super().__init__(image)
        self.dragging = False   # Useful for dragging
        self._rel_x, self._rel_y = 0, 0 # Useful for dragging

    def drag(self):
        '''Makes the image follow the mouse cursor'''
        if not self.dragging: # Defines the distance the image should be away from the cursor
            self._rel_x, self._rel_y = (pygame.mouse.get_pos()[0] - self.rect.left), (pygame.mouse.get_pos()[1] - self.rect.top)
            self.rect.update((pygame.mouse.get_pos()[0] - self._rel_x, pygame.mouse.get_pos()[1] - self._rel_y), (self.rect.width, self.rect.height))
            self.dragging = True

        else: # Moves the image with the mouse
            self.rect.update((pygame.mouse.get_pos()[0] - self._rel_x, pygame.mouse.get_pos()[1] - self._rel_y), (self.rect.width, self.rect.height))

    def stop_dragging(self):
        '''Stops the image from dragging'''
        self.dragging = False 

class Charachter(GameObject):
    '''An object that can be selected and stores a Person object'''

    def __init__(self, image: pygame.Surface, person: players.Person):
        '''Initializes variables'''
        super().__init__(image)
        self.person = person
        self._selected = False

    def toggle_select(self):
        '''Toggles if this object is sleceted or not'''
        if self._selected:
            self.deselect()
        else:
            self.select()

    def select(self):
        '''Changes the image to "Selected_image_url"'''
        self.image = pygame.image.load(selected_img_dict[self.image_name]) # Makes the image the selcted version of it
        self._selected = True
        couple_selection.append(self) # Adds itself to the global list for couple selection

    def deselect(self):
        '''Changes the image to the original image'''
        self.image = pygame.image.load(img_dict[self.image_name]) # Makes the image the unselected version of it
        self._selected = False
        couple_selection.pop()  # Removes itself from the global list for couple selection

    



# def add_couple(people:list):
#     '''Adds a list of '''
#     couples.append(people[0].person, people[1].person)



 
background = GameObject("Start_screen") #Create the background

person_1 = Charachter("Red_stick", players.Person("Red", "Nerd")) #Create people
person_2 = Charachter('Nerd_stick', players.Person("Nerd", "Red"))
person_3 = Charachter("Beard_stick", players.Person("Beard", "Red"))
people = [person_1, person_2, person_3]


for index in range(len(people)): # Place the people 150 pixels apart
    people[index].rect.move_ip(150 + 150*index, 300)



while Running: #Loop the program


    for event in pygame.event.get():  #Loop through the events in the event queue

        if event.type == pygame.MOUSEBUTTONDOWN and event.dict["button"] == 1: #If I left click
            mouse_pos = pygame.mouse.get_pos()
            for person in people:                           
                if person.rect.collidepoint(mouse_pos):  #Then find if I clicked on a person
                    person.toggle_select()               #If I did, select them
                    
                    if len(couple_selection) == 2:   #If two people are selected
                        couples.append((couple_selection[0].person, couple_selection[1].person)) # add thier Person objects to the couples list 
                        couple_num += 1              

                        couple_selection[1].deselect() #Empty the couple slection list
                        couple_selection[0].deselect() #And deselct the people I clicked on 


                        


        if event.type == pygame.QUIT: #When you hit the X, it quits
            Running = False

    pygame.event.clear() #Clear the event que to stop memory leaks

    screen.blit(background.image, background.rect)    #Draw the background
    for person in people:
        screen.blit(person.image, person.rect) #Draw People
    pygame.display.flip()   #Show the next frame
    clock.tick(fps)    #Limit FPS


