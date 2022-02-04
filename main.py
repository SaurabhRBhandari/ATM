import sys
import logging
import os
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


class Card:
    def __init__(self, number, account):
        self.account = account
        self.number = number

    def __str__(self):
        return(self.number)


class User:
    def __init__(self, acccount, card):
        self.account = acccount
        self.card = card


class Account:
    def __init__(self, account, balance=0):
        self.account = account
        self.balance = balance

    def add(self, addend):
        self.balance = int(self.balance)+int(addend)

    def withdraw(self, subtrahend):
        balance = int(self.balance)-int(subtrahend)
        if(balance >= 0):
            self.balance = balance
        else:
            logging.error("Insufficient Balance")
            raise Exception("Insufficient Balance")

    def get_balance(self):
        return self.balance

    def __str__(self):
        return self.account


class ATM:
    def register(card_number):
        Pin = input("Create pin:")
        Pin1 = input("Confirm pin:")
        if Pin != Pin1:
            logging.error("Pins don't match,restart")
            ATM.register(card_number)
        else:
            db = open("ATM_database.txt", "a")
            db.write(card_number+","+Pin+"\n")
            logging.info(
                "Your pin has been saved successfully,please reinsert your card to continue")
            sys.exit()

    def authenticate(card_number):
        pin = input("Enter 4 digit pin(first time users press enter)")
        if not len(card_number or pin) < 1:
            try:
                if card_number in ATM.card_list:
                    try:
                        if pin == ATM.cards[card_number]:
                            account = Account(
                                ATM.db[card_number], ATM.accounts[ATM.db[card_number]])
                            card = Card(card_number, account)
                            user = User(account, card)
                            logging.info('User verified!')
                            return user
                        else:
                            logging.error("Pin incorrect,try again")
                            return ATM.authenticate(card_number)

                    except:
                        ATM.register(card_number)
                        return True
                else:
                    logging.error("Invalid card")
            except:
                pass

    def load_bank_db():
        db = open("bank_database.txt", 'r')
        ac_list = []
        card_list = []
        balance = []
        for i in db:
            a, b, c = i.split(',')
            b = b.strip()
            c = c.strip()
            ac_list.append(a)
            card_list.append(b)
            balance.append(c)
        accounts = dict(zip(ac_list, balance))

        return accounts, card_list

    def load_atm_db():
        db = open("ATM_database.txt", 'r')
        card_list = []
        pin = []
        for i in db:
            a, b = i.split(',')
            b = b.strip()
            card_list.append(a)
            pin.append(b)
        cards = dict(zip(card_list, pin))

        return cards

    def deposit_money(user):
        account = user.account
        # Would be replaced by depositing money
        deposit = input("Please enter money to be added")
        account.add(deposit)
        balance = account.get_balance()
        data = ''
        db = open("bank_database.txt", 'r')
        for i in db:
            a, b, c = i.split(',')
            if(a != str(account)):
                data += f'{a},{b},{c}'
            else:
                data += f'{a},{b}, {balance}\n'
        db.close()
        db = open("bank_database.txt", 'w')
        db.write(data)
        logging.info('Transaction successfull!')

    def withdraw_money(user):
        account = user.account
        withdraw_amount = input("Please enter money to be withdrawn")
        account.withdraw(withdraw_amount)
        balance = account.get_balance()
        data = ''
        db = open("bank_database.txt", 'r')
        for i in db:
            a, b, c = i.split(',')
            if(a != str(account)):
                data += f'{a},{b},{c}'
            else:
                data += f'{a},{b}, {balance}\n'
        db.close()
        db = open("bank_database.txt", 'w')
        db.write(data)
        logging.info('Transaction successfull!')

    accounts, card_list = load_bank_db()
    cards = load_atm_db()
    db = dict(zip(card_list, accounts))

    def display_balance(user):
        logging.info(user.account.get_balance())

    def home():
        card_number = input("Enter your card number")
        try:
            user = ATM.authenticate(card_number)
            if(user):
                print("1.Deposit money")
                print("2.Withdraw money")
                print("3.Display balance")
                ch = input("Enter a number")
                print(ch)
                if(ch == '1'):
                    ATM.deposit_money(user)
                elif(ch == '2'):
                    ATM.withdraw_money(user)
                elif(ch == '3'):
                    ATM.display_balance(user)
                else:
                    logging.error("Invalid choice")
        except:
            logging.error("Something went wrong, please reinsert card")
            sys.exit()


ATM.home()
