#!/usr/bin/env python3

users = [
    {'username': 'walter', 'pin': '0001', 'balance': { 'KSh':2000, 'USD':0 }},
    {'username': 'elaine', 'pin': '0002', 'balance': { 'KSh':1000, 'USD':200 }},
    {'username': 'collins', 'pin': '0003', 'balance': { 'KSh':-500, 'USD':2000 }},
    {'username': 'juma', 'pin': '0004', 'balance': { 'KSh':140, 'USD':200 }},
]

def promptString(prompt):
    print(prompt + ':')
    result = input()
    return result

def findUser(username, pin):
    for user in users:
        if (user.get('username') == username and user.get('pin') == pin):
            return user
    
    return None

def login():
    while (True):
        username = promptString('Enter user name')

        if (username):
            pin = promptString('Enter your PIN number')

            print('Logging in...')
            user = findUser(username, pin)

            if (user):
                return user

user = login()

print(user)