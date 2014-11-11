#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import pytest
from papers import decide

"""
Assumption
1. Passport, Country code, First and Last Name, Visa code in upper case letters.
2. reason for entry in lower case letters.
"""

def test_basic():
    assert decide("test_returning_citizen.json", "watchlist.json", "countries.json") == ["Accept", "Accept"]
    assert decide("test_watchlist.json", "watchlist.json", "countries.json") == ["Secondary"]

#    assert decide("test_watchlist2.json", "watchlist.json", "countries.json") == ["Secondary"]
    assert decide("test_quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]


    #Tested 4 cases just containing all 3 conditions to test whether priority is set.
    assert decide("test_Priority_Quarantine.json", "watchlist.json", "countries.json") == ["Quarantine"]
    #Via Country ELE = Quarantine
    assert decide("test_Priority_Reject.json", "watchlist.json", "countries.json") == ["Reject"]
    #Doesn't have Visa field
    assert decide("test_Priority_Secondary.json", "watchlist.json", "countries.json") == ["Secondary"]
    #In the Watchlist for Passport Number
    assert decide("test_Priority_Accept.json", "watchlist.json", "countries.json") == ["Accept"]

    assert decide("test_reject0.json", "watchlist.json", "countries.json") == ["Reject"]
    #Doesn't have Last name, should be rejected
    assert decide("test_invalid_visa.json", "watchlist.json", "countries.json") == ["Accept"]
    #Expired Visa of 1999



def test_files():
    with pytest.raises(FileNotFoundError):
        decide("test_returning_citizen.json", "", "countries.json")


