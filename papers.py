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
#goes under decide
with open("example_entries.json", "r") as file_reader:
    file_contents = file_reader.read()
    entries = json.loads(file_contents)

with open("countries.json", "r") as file_reader:
    file_contents2 = file_reader.read()
    countries = json.loads(file_contents2)
Nx = 0

with open("watchlist.json", "r") as file_reader:
    file_contents3 = file_reader.read()
    watchlist = json.loads(file_contents3)


for entry in entries:
    individual_entry = entries[Nx]
    #Individual entries
    from_country = (individual_entry.get("from")).get("country")
    #print(from_country)
    #print(countries.get(from_country))
    if ((countries.get(from_country)).get("medical_advisory")) != "":
        print ((countries.get(from_country)).get("medical_advisory"))
        #return "Quarantine"

    """if "via" in individual_entry:
        via_country = ((individual_entry.get("via")).get("country"))
        print((individual_entry.get("via")).get("country"))"""

    Nx+=1

def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """

    return ["Reject"]


def valid_passport_format(passport_number):
    """
    Checks whether a pasport number is five sets of five alpha-number characters separated by dashes
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
