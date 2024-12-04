import random

class Person():
    '''Every person is stored in a player object'''
    def __init__(self, name, partner, number, options):
        '''Initializes varaibles'''
        self.name = name
        self.partner = partner
        self.number = number
        self.options = options

    def __repr__(self):
        '''Returns Person(name, partner)'''
        return f'Person({self.name}, {self.partner})'

def setup(n=16, rand=False):  #Takes the number of individual popele, NOT couples
    '''Creates a list of a set number of player objects'''
    people = [None for _ in range(n)]
    median = n//2
    people2 = [None for _ in range(median)]
    male_names = ["Aaron", "Hudson", "Arlie", "John", "Lambert", "Jerrod", "Claud", "Ryan"]
    female_names = ["Govinda", "Charlene", "Caitlin", "Rhiannon", "Marion", "Evangeline", "Christy", "Monica"]

    #Randomize the order of the list

    for i in range(median):
        partner_index = n-1 -i
        #Create a male Person, and the coresponding Female person
        people[i] = Person(male_names[i], female_names[i], i, [j for j in range(median, n)])
        people2[i] = Person(female_names[i], male_names[i], partner_index, [j for j in range(median)])

    if rand:
        random.shuffle(people2)

    people[median:] = people2

    return people

def check(couple:tuple):
    '''Returns True if the couple is correct, otherwise returns False'''
    return couple[0].partner == couple[1].name  #If the first person's match is the other person

def bulk_check(Couples:list):
    '''Takes a list of touple couples and returns the number that are correct'''
    correct_couples = 0
    for couple in Couples: #Checks each couple
        if check(couple):
            correct_couples += 1
    return correct_couples
            



    