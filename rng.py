#!/usr/bin/python3

import random

def rng(body):
    d = int(body.split(' ')[1])

    roll = random.randint(1, d)
    return "Your roll is: {roll}".format(roll = roll)

    # idea:  log your rolls in a spreadsheet for some weird reason!
