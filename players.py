import random

class Person():
    '''Every person is stored in a player object'''
    def __init__(self, name, partner):
        '''Initializes varaibles'''
        self.name = name
        self.partner = partner

    def __repr__(self):
        '''Returns Person(name, partner)'''
        return f'Person({self.name}, {self.partner})'

def setup(players=16):  #Takes the number of individual popele, NOT couples
    '''Creates a list of a set number of player objects'''
    people = []
    match_list = []
    for i in range((int(players/2)), players): 
        match_list.append(i)
    random.shuffle(match_list)  #Randomizes a list of the second half of the names of people

    for index, name in enumerate(range(int(players/2))):  #Looks rough now, change it when we have the name_list
        people.append(Person(name, match_list[index]))   #Creates the first half, assigning a name and choosing a coresponding partner name

    for index, name in enumerate(match_list):             #Does the same thing as previous, just backwords
        people.append(Person(name, people[index].name))

    return people

def check(couple):
    '''Returns True if the couple is correct, otherwise returns False'''
    return couple[0].partner == couple[1].name  #If the first person's match is the other person

def bulk_check(Couples):
    '''Takes a list of touple couples and returns the number that are correct'''
    correct_couples = 0
    for couple in Couples: #Checks each couple
        if check(couple):
            correct_couples += 1
    return correct_couples
            

if __name__ == "__main__":  #Testing stuff
    setup()

    