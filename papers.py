#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Michael Kim and Grant Wheeler'
__email__ = "michaeln.kim@mail.utoronto.ca, grant.wheeler@mail.utoronto.ca"

# imports one per line
import re
import datetime
import json


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

    decision_list = []

    for individual_entry in entries:
        #For loop allows individual entries to be tested.

        if (check_quarantine(individual_entry, countries)) == True:
            #Checks Quarantine First, if not move on.
            decision_list.append("Quarantine")
        else:
            if not (check_valid_passport(individual_entry)):
                #Checks if passport is valid. if valid, moves on.
                decision_list.append("Reject")

            else:
                if not (check_reason(individual_entry)):
                    #Checks reason for entry, and checks if there is valid visa. Moves on if valid.
                    decision_list.append("Reject")
                else:
                    if check_watchlist(individual_entry, watchlist):
                        #Checks if the passport is in watchlist file.
                        decision_list.append("Secondary")
                    else:
                        decision_list.append("Accept")

    return decision_list


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
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def valid_name(name):
    """
    Checks if First or Last name is Valid.
    :param name:String value from the passport, either Last name or First name
    :return:Boolean value. True for valid name.
    """
    if type(name) == str:
        if name != "":
            return True
    else:

        return False


def valid_location(location_place):
    """
    checks whether a location has City, Region, and Country code in right format.
    :param location_place:List
    :return:True if valid.
    """
    if type(location_place.get("city")) == str:
        if type(location_place.get("region")) == str:
            if type(location_place.get("region")) == str:
                return True
    else:
        return False


def valid_visa(passport):
    """
    Checks if the visa is valid format and less than two years old.
    :param visa_information:
    :return:
    """
    visa_information = passport.get("visa")
    visa_format = re.compile('.{5}-.{5}')
    visa_code = (visa_information.get("code"))
    visa_date = datetime.datetime.strptime(visa_information.get("date"), "%Y-%m-%d")
    valid_visa_date = datetime.datetime.strptime("2012-11-10", "%Y-%m-%d")

    if visa_format.match(visa_code):
        if visa_date > valid_visa_date:
            return True
    else:
        return False


def check_quarantine(individual_entry, countries):
    """
    Checks if the traveller should be placed as Quarantine
    :param individual_entry: Traveller's record. Should be list
    :param countries: Countries list.
    :return: True or False
    """

    from_country_raw = (individual_entry.get("from")).get("country")
    from_country = from_country_raw.upper()
    #From the dictionary, gets information about the the Country traveller is From.

    if ((countries.get(from_country)).get("medical_advisory")) != "":
        #from country has a Medical Advisory Condition
        return True
        #True means the country has medical condition and should be in Quarantine.
    elif "via" in individual_entry:
        #Checks if the traveler is from a via country that may have a medical advisory condition.
        via_country_raw = ((individual_entry.get("via")).get("country"))
        via_country = via_country_raw.upper()
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
    if valid_name(passport_information.get("first_name")):
        if valid_name(passport_information.get("last_name")):
            if valid_passport_format(passport_information.get("passport")):
                if valid_date_format(passport_information.get("birth_date")):
                    if valid_location(passport_information.get("home")):
                        if valid_location(passport_information.get("from")):
                            return True
    else:
        return False


def check_reason(passport_information):
    """
    Checks reason for entry and assign whether visa is valid.
    :param passport_information:
    :return:True or False
    """
    if passport_information.get("entry_reason") == "returning":
        return True
    elif passport_information.get("entry_reason") == "transit":
        if "visa" in passport_information:
            if valid_visa(passport_information):
                return True
        else:
            return False
    elif passport_information.get("entry_reason") == "visit":
        if "visa" in passport_information:
            if valid_visa(passport_information):
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
    for entry in watchlist:
        if passport_information.get("last_name") == entry.get("last_name"):
            return True
        elif passport_information.get("passport") == entry.get("passport"):
            return True
    return False