import random
import time


def myticket():
    a = 'abcdefghijklmnopqrstuvwxyz0123456789'
    ticket = ''
    for i in range(15):
        ticket += random.choice(a)
    now_time = str(int(time.time()))
    ticket += now_time
    ticket = 'TK-' + ticket
    return ticket