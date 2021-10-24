#!/usr/bin/env python3

users = [
    {'username': 'walter', 'pin': '0001', 'balance': { 'KSh':2000, 'USD':0 }},
    {'username': 'elaine', 'pin': '0002', 'balance': { 'KSh':1000, 'USD':200 }},
    {'username': 'collins', 'pin': '0003', 'balance': { 'KSh':-500, 'USD':2000 }},
    {'username': 'juma', 'pin': '0004', 'balance': { 'KSh':140, 'USD':200 }},
]

ksh_notes = [50, 100, 200, 500, 1000]
usd_notes = [1, 5, 20, 50, 100]
transactions = []

def promptString(prompt):
    print(prompt + ':')
    result = input()
    return result

def promptNumber(prompt):
    return int(promptString(prompt))

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

def promptAmmount(min, balance):
    print('Your balance is:', balance)

    # Make sure there is a balance we can withdraw
    if (balance < min):
        return 0

    ammount = promptNumber('How much would you like to withdraw (x' + str(min) + ')')

    # Make sure ammount is greater than or equal to min and
    # Make sure ammount is divisible by min exactly
    if (ammount < min or ammount % min > 0):
        print('Please enter a number that is a multiple of:', min)
        return 0

    # Make sure ammount is in balance
    if (ammount > balance):
        print('Not enough funds. Balance:', balance)
        return 0

    return ammount

def withdrawKSH(user):
    min = ksh_notes[3]
    balance = user.get('balance', {}).get('KSh')
    ammount = promptAmmount(min, balance)

    # Check for error
    if (ammount > 0):
        user.get('balance', {}).update({ 'KSh': balance - ammount })
        transactions.append({ 'ACTION': 'WITHDRAW', 'AMMOUNT': ammount, 'CURRENCY': 'KSH' })

def withdrawUSD(user):
    min = usd_notes[2]
    balance = user.get('balance').get('USD')
    ammount = promptAmmount(min, balance)

    # Check for error
    if (ammount > 0):
        user.get('balance').update({ 'USD': balance - ammount })
        transactions.append({ 'ACTION': 'WITHDRAW', 'AMMOUNT': ammount, 'CURRENCY': 'USD' })

def withdraw(user):
    currency = promptString('What would you like to withdraw (Ksh/USD)').upper()

    if (currency == 'KSH'):
        withdrawKSH(user)
    elif (currency == 'USD'):
        withdrawUSD(user)
    else:
        print('Invalid currency')

def balance(user):
    pass

def menu(user):
    print('--------------------------')
    print('MENU')
    print('--------------------------')
    print('A: WITHDRAW')
    print('B: CHECK BALANCE')
    print('Q: QUIT')

    command = promptString('What would you like to do (A/B/Q)').upper()

    if command == 'A':
        withdraw(user)
        return True
    elif command == 'B':
        balance(user)
        return True
    elif command == 'Q':
        return False

        return True

user = login()

while (menu(user)):
    pass
