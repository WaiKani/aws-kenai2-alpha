#!/usr/bin/env python3
from datetime import date
import os

#Dict serving as the database of the atm
users = [
    {'username': 'walter', 'pin': '0001', 'balance': { 'KSh':2000, 'USD':0 }},
    {'username': 'elaine', 'pin': '0002', 'balance': { 'KSh':1000, 'USD':200 }},
    {'username': 'collins', 'pin': '0003', 'balance': { 'KSh':-500, 'USD':2000 }},
    {'username': 'juma', 'pin': '0004', 'balance': { 'KSh':140, 'USD':200 }},
]


#A list denoting the dominations for each currency
ksh_notes = [50, 100, 200, 500, 1000]
usd_notes = [1, 5, 20, 50, 100]

#A history of transaction histpry
transactions = []

########
#Stream Handler Functions
########

#This group of functions serve as the standard iostream handlers
#Takes in the prompt to be displayed on stdout
#Returns the user input in the format expected
def promptString(prompt):
    print(prompt + ':')
    result = input()
    return result

def promptNumber(prompt):
    return int(promptString(prompt))



########
#Logging In Functions
########

#Screen Clearing Function
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

#Searches the database for a username and pin match
#If the user if not found or the pin is incorrect returns None
def findUser(username, pin):
    for user in users:
        if (user.get('username') == username and user.get('pin') == pin):
            return user
    
    return None

#Login Subproces
#Logs in a user by verifying the user and corresponding pin
#A maximum of 3 attempts is allowed
def login():
    counter = 0
    while (counter < 3):
        username = promptString('Enter user name')

        if (username):
            pin = promptString('Enter your PIN number')

            counter = counter + 1
            clearConsole()

            print('Logging in...')
            user = findUser(username, pin)

            if (user):
                return user
    promptString("You have made to may attempts. Try again later")
    exit()




########
#Withdrawal Functions
########

#Prompts the user on the amount to withdraw while ensuring no over draft
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

#Withdraw Ksh from account
def withdrawKSH(user):
    min = ksh_notes[3]
    balance = user.get('balance', {}).get('KSh')
    ammount = promptAmmount(min, balance)

    # Check for error
    if ammount > 0:
        command = promptString('Withdraw ' + str(ammount) + ' KSH').upper()

        if command == 'Y':
            user.get('balance', {}).update({ 'KSh': balance - ammount })
            transactions.append({ 'ACTION': 'WITHDRAW', 'AMMOUNT': ammount, 'CURRENCY': 'KSH' })

#Withdraw USD from account
def withdrawUSD(user):
    min = usd_notes[2]
    balance = user.get('balance').get('USD')
    ammount = promptAmmount(min, balance)

    # Check for error
    if (ammount > 0):
        command = promptString('Withdraw ' + str(ammount) + ' USD').upper()

        if command == 'Y':
            user.get('balance').update({ 'USD': balance - ammount })
            transactions.append({ 'ACTION': 'WITHDRAW', 'AMMOUNT': ammount, 'CURRENCY': 'USD' })

#Widthrawl suprocess
#Allows user to either USD or KSH
def withdraw(user):
    print('--------------------------')
    print('WITHDRAW')
    print('--------------------------')
    currency = promptString('What would you like to withdraw (Ksh/USD)').upper()

    if (currency == 'KSH'):
        withdrawKSH(user)
    elif (currency == 'USD'):
        withdrawUSD(user)
    else:
        print('Invalid currency')



########
#Deposit Functions
########

#Cash Deposit Subprocess
#Allows the user to deposit Ksh into their account in multiples of 500
def deposit(user):
    print('--------------------------')
    print('DEPOSIT')
    print('--------------------------')

    currency = promptString('What would you like to deposit (Ksh/USD)').upper()

    if (currency != 'KSH'):
        print('Invalid currency')
        return

    min = ksh_notes[3]
    balance = user.get('balance').get('KSh')
    ammount = promptNumber('How much would you like to deposit (x' + str(min) + ' Ksh)')

    # Check for error
    if (ammount <= 0 or ammount % min > 0):
        print('Please enter a number that is a multiple of:', min)
        return

    command = promptString('Deposit ' + str(ammount) + ' KSH').upper()

    if command == 'Y':
        user.get('balance', {}).update({ 'KSh': balance + ammount })
        transactions.append({ 'ACTION': 'DEPOSIT', 'AMMOUNT': ammount, 'CURRENCY': 'KSH' })



########
#Balance Function
########

#Acount Balance Display Subprocess
#Allows user to view the amount in thier account of each currency
def balance(user):
    print('--------------------------')
    print('BALANCE')
    print('--------------------------')
    print('You have Ksh:', user.get('balance', {}).get('KSh'))
    print('You have USD:', user.get('balance', {}).get('USD'))
    print('--------------------------')
    promptString('Press enter to continue')



########
#Recipt Display Function
########

#Reciept Printing Function
#Allows the user to print out a copy of all transactions carried out
#while interacting with the ATM
def receipt(user):
    while (True):
        printReceipt = promptString('Do you want a receipt (y/n)').upper()

        if printReceipt == 'N':
            return
        elif printReceipt == 'Y':
            break

    print('--------------------------')
    print('RECEIPT')
    print('--------------------------')
    
    for transaction in transactions:
        if transaction.get('ACTION') == 'DEPOSIT':
            print('+', str(transaction.get('AMMOUNT')).rjust(12), transaction.get('CURRENCY'))
        elif transaction.get('ACTION') == 'WITHDRAW':
            print('-', str(transaction.get('AMMOUNT')).rjust(12), transaction.get('CURRENCY'))

    print('--------------------------')
    print('Ksh', str(user.get('balance', {}).get('KSh')).rjust(10))
    print('USD', str(user.get('balance', {}).get('USD')).rjust(10))
    print('--------------------------')
    print(date.today())



########
#Central Menu Function
########

#Menu Displaying function
#Once a user logs in this function displays and the possible actions
#the user can do and calls the appropriate subprocess
def menu(user):
    print('--------------------------')
    print('MENU')
    print('--------------------------')
    print('A: WITHDRAW')
    print('B: CHECK BALANCE')
    print('C: DEPOSIT')
    print('Q: QUIT')

    command = promptString('What would you like to do (A/B/Q)').upper()

    if command == 'A':
        withdraw(user)
    elif command == 'B':
        balance(user)
    elif command == 'C':
        deposit(user)
    elif command == 'Q':
        return False

    return True


if __name__ == '__main__':
    #Attempt to login the user
    user = login()

    #display the menu
    while (menu(user)):
        pass

    #on quiting prompt the user if they want a reciept
    receipt(user)
