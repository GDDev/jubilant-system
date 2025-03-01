from random import choice, randint
from datetime import date

from numpy import random as rd

real_people = [
    'Albert Einstein',
    'Cleopatra',
    'Sun Tzu',
    'Gordon Ramsay',
    'Mother Teresa',
    'Julius Caesar'
]
characters = [
    'Batman',
    'Yoda',
    'Shaggy Rogers',
    'Captain America',
    'SpongeBob SquarePants',
    'Optimus Prime'
]
real_quotes = [
    'Imagination is more important than knowledge.',
    'To be or not to be.',
    'The only thing we have to fear is fear itself.'
]
funny_quotes = [
    'I am vengeance!',
    'I\'m Pickle Rick!',
    'It\'s over, Anakin! I have the high ground!',
    'I am the danger.',
    'It\'s a-me, Mario!',
    'I am inevitable.'
]


def random_year():
    year = randint(-3200, date.today().year)
    return f'{abs(year)} BC' if year < 0 else year


def choose_real_person_funny_quote() -> dict:
    return {
        'quote': rd.choice(funny_quotes, replace=False),
        'author': choice(real_people),
        'year': random_year()
    }


def choose_character_real_quote() -> dict:
    return {
        'quote': rd.choice(real_quotes, replace=False),
        'author': choice(characters),
        'year': random_year()
    }


def choose_quote() -> dict:
    functions = [
        choose_real_person_funny_quote,
        choose_character_real_quote
    ]

    return choice(functions)()
