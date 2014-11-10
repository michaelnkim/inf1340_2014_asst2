#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import re
import datetime
import json

#Please Remember to check Capitalized/uncapitalized does not matter.
#Please check valid location for quarantine.
def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted.
    First, loads the three files.
    Second, using a For loop, separates list of dictionaries into an individual dictionary.
    Third, using the individual passport,
    Checks the following in order
        1.Should the person be in "Quarantine" ?
        2.Should the person be in "Rejected"?
        3.Should the person be in "Secondary"?
        4.Should the person be in "Accepted" ?

    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """

    with open(input_file, "r") as file_reader:
        file_contents = file_reader.read()
        entries = json.loads(file_contents)

    with open(countries_file, "r") as file_reader:
        file_contents2 = file_reader.read()
        countries = json.loads(file_contents2)

    with open(watchlist_file, "r") as file_reader:
        file_contents3 = file_reader.read()
        watchlist = json.loads(file_contents3)

    Nx = 0
    #Number for For loop

    for entry in entries:
        #For loop allows individual entries to be tested from 0 to end of the entries file.
        individual_entry = entries[Nx]
        #Individual entries
        if (check_quarantine(individual_entry, countries)) == True:
            #Checks Quarantine First, if not move on.
            return ["Quarantine"]
        else:
            if(check_valid_passport(individual_entry)) != True:
             #Checks if passport is valid. if valid, moves on.
                return ["Reject"]
            else:
                if(check_reason(individual_entry)) == False:
                    #If reason for entry and visa has not matched.
                    return ["Reject"]
                else:
                    if(check_watchlist(individual_entry)) == True:
                        return ["Secondary"]
                    else:
                        return ["Accept"]
        Nx+=1

def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes

    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('.{5}-.{5}-.{5}-.{5}-.{5}')

    if passport_format.match(passport_number):
        return True
    else:
        return False

def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :rtype : object
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False



def valid_location(location_place):

    """
    checks whether a location has City, Region, and Country code in right format.
    :param location_place:List
    :return:True if valid.
    """

def valid_visa(visa_number):
    """

    :param visa_number:
    :return:
    """

    """ Attempting to compare the current year, with passports, in order to check validity of visa (ie. less than 2 yrs)
    import datetime
    datetime.date.year().strftime("%Y-%m-%d")
    if valid_date_format(date_string)["%Y"]
    """

def check_quarantine(individual_entry, countries):
    """
    Checks if the traveller should be placed as Quarantine
    :param individual_entry: Traveller's record. Should be list
    :param countries: Countries list.
    :return: True or False
    """

    from_country = (individual_entry.get("from")).get("country")
    #From the dictionary, gets information about the the Country traveller is From.

    if ((countries.get(from_country)).get("medical_advisory")) != "":
        #from country has a Medical Advisory Condition
        return True
        #True means the country has medical condition and should be in Quarantine.
    elif "via" in individual_entry:
        #Checks if the traveler is from a via country that may have a medical advisory condition.
        via_country = ((individual_entry.get("via")).get("country"))
        if ((countries.get(via_country)).get("medical_advisory")) != "":
            #if via country had a medical advisory condition
            return True
    else:
        return False

def check_valid_passport(passport_information):
    """
    Checks if the passport is valid.
    :param passport_information:
    :return: Boolean Value True or False
    """
    if valid_passport_format(passport_information.get("passport")) != True:
        return False
    elif valid_date_format(passport_information.get("birth_date")) != True:
        return False
    elif valid_location(passport_information.get("home")) != True:
        return False
    elif valid_location(passport_information.get("from")) != True:
        return False
    elif valid_location (passport_information.get("via")) != True:
        return False
    return True

def check_reason(passport_information):
    """
    Checks reason for entry and assign whether visa is valid.
    :param passport_information:
    :return:True or False
    """
    if passport_information.get("entry_reason") == "returning":
        return True
    elif passport_information.get("entry_reason") == "transit":
        if valid_visa(passport_information.get("visa")) is True:
            return True
        else:
            return False
    elif passport_information.get("entry_reason") == "visiting":
        if valid_visa(passport_information.get("visa")) is True:
            return True
        else:
            return False
    else:
        return False

def check_watchlist(passport_information, watchlist):
    """
    Checks watchlist and finds if the person holding the passport is indeed inside the watchlist.
    :param passport_information:
    :param watchlist:
    :return: True or False
    """


print(decide("test_returning_citizen.json", "watchlist.json", "countries.json"))