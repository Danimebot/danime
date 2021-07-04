import discord
from misc.search import searchChar
from misc.run import run_query
from misc.bruh import GetByChar
from misc.clean import *


def charSearch(charName):
    query = searchChar()
    variables = GetByChar(charName)
    if variables:
        result = run_query(query, variables)
        if not result:
            return "None"

        return result 