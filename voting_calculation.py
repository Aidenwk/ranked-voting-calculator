"""
This file is used in the counting of votes for a 
ranked preferential style voting system as implemented
in the Modelling Weekly Group Build process
written by Aiden Kennedy
"""

import csv
import random

FILENAME="./MWCDSGB VI Mastersheets - Voting.csv" #Place filename for voting calculation here
CATEGORY_DICTIONARY={}
VOTER_LIST=[]
VOTES_DICTIONARY={}

class Voter():
    """
    This class is the voter class and contains all the information for an
    individual voter
    """
    __slots__=["__current_vote","__vote_number","__name","__rankings","__is_valid"]
    def __init__(self,name):
        self.__name=name
        self.__vote_number=1
        self.__current_vote=""
        self.__rankings={}
        self.__is_valid=True

    def set_rankings(self,category,rank):
        """
        Sets the rankings of each category that a voter 
        voted for, the slicing is used to counter
        the st/nd/rd/th 's
        """
        if len(rank)==4:
            self.__rankings[int(rank[:2])]=category
        elif len(rank)==3:
            self.__rankings[int(rank[:1])]=category

    def set_current_vote(self):
        """
        Sets the current vote for the voter,
        if the voter has exceeded their rankings
        then the voter will be set to invalid and
        not be counted
        """
        if self.__vote_number in self.__rankings:
            self.__current_vote=self.__rankings[self.__vote_number]
        else:
            self.__is_valid=False

    def set_vote_number(self):
        """
        Advances the voters vote number, used when 
        the current vote has been eliminated
        """
        if self.__vote_number<len(CATEGORY_DICTIONARY):
            self.__vote_number+=1
        else:
            self.__is_valid=False

    def get_current_vote(self):
        """
        Returns the voters current vote
        """
        return self.__current_vote

    def get_name(self):
        """
        Returns the voters name
        """
        return self.__name

    def get_is_valid(self):
        """
        Returns the validity of the
        voter (if all their votes have been eliminated)
        """
        return self.__is_valid

    def __repr__(self):
        """
        Stringifies the voter by returning 
        all the current values
        """
        return self.__name + "\n" + str(self.__vote_number) + "\n" + self.__current_vote + "\n" + str(self.__rankings) + "\n" + str(self.__is_valid)

def initialize_voters():
    """
    Sets up the list of voter objects given a CSV
    file
    """
    with open(FILENAME) as csv_file:
        csv_reader=csv.reader(csv_file)
        for lines in csv_reader:
            if csv_reader.line_num==1:
                for i in range(1,len(lines)-1):
                    CATEGORY_DICTIONARY[i]=lines[i]
            else:
                VOTER_LIST.append(Voter(lines[len(lines)-1]))
                for i in range(1,len(lines)-1):
                    VOTER_LIST[len(VOTER_LIST)-1].set_rankings(CATEGORY_DICTIONARY[i],lines[i])
                VOTER_LIST[len(VOTER_LIST)-1].set_current_vote()

def calculate_votes():
    """
    Calculates the votes using the intialized
    voter list
    """
    setup=False
    min_value=0
    for keys in CATEGORY_DICTIONARY:
        #Sets up the votes dictionary with the categories in the CSV file
        VOTES_DICTIONARY[CATEGORY_DICTIONARY[keys]]=0
    while len(VOTES_DICTIONARY)>1:
        voter_index=0
        for voters in VOTER_LIST:
            if voters.get_current_vote() not in VOTES_DICTIONARY or setup==False:
                #Adds voter's current vote on the first loop or if their current vote has been eliminated
                while not voters.get_current_vote() in VOTES_DICTIONARY and voters.get_is_valid()==True:
                    #Updates a voter's current vote until it is a category that has not been eliminated or all the voter's votes have been eliminated
                    voters.set_vote_number()
                    voters.set_current_vote()
                if voters.get_is_valid()==False:
                    #Removes a voter if all their votes have been eliminated
                    VOTER_LIST.pop(voter_index)
                    continue
                VOTES_DICTIONARY[voters.get_current_vote()]+=1
            voter_index+=1
        setup=True
        to_be_popped=[]
        print(VOTES_DICTIONARY)
        for keys in VOTES_DICTIONARY:
            #checks what the minimum votes for a category is
            if VOTES_DICTIONARY[keys]<min_value:
                min_value=VOTES_DICTIONARY[keys]
        for keys in VOTES_DICTIONARY:
            #Stages the lowest voted for categories to be eliminated
            if VOTES_DICTIONARY[keys]==min_value:
                to_be_popped.append(keys)
        if not len(to_be_popped)==len(VOTES_DICTIONARY):
            #Pops all staged categories from the voted dictionary if there will be any remaining categories
            for keys in to_be_popped:
                print("Eliminated: ",keys)
                VOTES_DICTIONARY.pop(keys)
        elif len(to_be_popped)==len(VOTES_DICTIONARY):
            #If all of the staged pops will empty the votes dictionary then one of the categories will be randomly removed before a recount
            VOTES_DICTIONARY.pop(to_be_popped[random.randint(0,len(to_be_popped))])
        min_value+=1
    print("Winner: "+str(VOTES_DICTIONARY))
    

def main():
    initialize_voters()
    calculate_votes()

if __name__=="__main__":
    main()