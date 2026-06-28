import json
import random
import string
from pathlib import Path

class Bank:
    database = 'data.json'
    data = []
    try :
        if Path(database).exists() :
            with open(database) as fs:
                data = json.loads(fs.read())
        else :
            print("No Such File Exists")
    except Exception as err:
        print(f"An Error Occured As {err}")

    @classmethod
    def __update (cls):
        with open(cls.database , "w") as fs:
            fs.write(json.dumps(cls.data))

    @classmethod
    def __accountnogen(cls):
        alpha = random.choices(string.ascii_letters,k=3)
        num = random.choices(string.digits,k=3)
        spchar = random.choices("!@#$%&",k=1)
        id = alpha + num + spchar
        random.shuffle(id)
        return "".join(id)

    def create_account(self):
       info = {
           "name" : input("Name :- "),
           "age" : int(input("Age :- ")),
           "email" : input("Email :- "),
           "pin" : int(input("Give your Pin :- ")),
           "accountNo" : Bank.__accountnogen(),
           "balance" : 0
       }

       if info["age"] < 18 or len(str(info["pin"])) != 4 :
           print("Sorry You Can Not Create Your Account")
       else :
           print("Account Has Bee Create Successfully")
           for i in info :
               print(f"{i} : {info[i]}")
           print("Please Note Your Account Number")
           Bank.data.append(info)
           Bank.__update()

    def deposite_money(self):
        account_no = input("Please Give Your Account No :- ")
        pin = int(input("Please Give Your Pin No :- "))
        userdata = [i for i in Bank.data if i['accountNo'] == account_no and i['pin'] == pin]
        if userdata == False:
            print("Sorry! No Data Found")
        else :
            amount = int(input("Enter The Amount :- "))
            if amount > 100000 or amount < 0:
                print("Sorry The Amount Is Too Much. You Can Deposite Above 0 And Below 100000 One time")
            else :
                userdata[0]["balance"] += amount
                Bank.__update()
                print(f"Amount {amount} Deposited Successfully")
                print(f"Total Balance : {userdata[0]["balance"]}")

    def withdraw_money(self):
        account_no = input("Please Give Your Account No :- ")
        pin = int(input("Please Give Your Pin No :- "))
        userdata = [i for i in Bank.data if i['accountNo'] == account_no and i['pin'] == pin]
        if userdata == False:
            print("Sorry! No Data Found")
        else :
            amount = int(input("Enter The Amount :- "))
            if userdata[0]["balance"] < amount:
                print("Sorry! Not Enough Balance In Account")
            else :
                userdata[0]["balance"] -= amount
                Bank.__update()
                print(f"Amount {amount} Withdrawn Successfully")
                print(f"Total Balance : {userdata[0]["balance"]}")

    def show_details(self):
        account_no = input("Please Give Your Account No :- ")
        pin = int(input("Please Give Your Pin No :- "))
        userdata = [i for i in Bank.data if i['accountNo'] == account_no and i['pin'] == pin]
        for i in userdata[0]:
            print(f"{i} : {userdata[0][i]}")


    def update_details(self):
        account_no = input("Please Give Your Account No :- ")
        pin = int(input("Please Give Your Pin No :- "))
        userdata = [i for i in Bank.data if i['accountNo'] == account_no and i['pin'] == pin]
        
        print("You Can Not Change The Account Number And Age")
        print("For No Changes Keep The Input Empty")

        newdata = {
            "name" : input("Enter Your Updated Name (Skip If No Changes Required)"),
            "email" : input("Enter Your Updated Email (Skip If No Changes Required)"),
            "pin" : input("Enter Your Updated Pin (Skip If No Changes Required)")
        }
        if newdata["name"] == "":
            newdata["name"] = userdata[0]["name"]

        if newdata["email"] == "":
            newdata["email"] = userdata[0]["email"]

        if newdata["pin"] == "":
            newdata["pin"] = userdata[0]["pin"]

        newdata['age'] = userdata[0]['age']
        newdata['accountNo'] = userdata[0]['accountNo']
        newdata['balance'] = userdata[0]['balance']

        if type(newdata['pin']) == str:
            newdata['pin'] = int(newdata['pin'])

        for i in newdata:

            if newdata[i] == userdata[0][i]:
                continue
            else :
                userdata[0][i] = newdata[i]

        Bank.__update()

        print("Your Details Updated Successfully")

    def delete(self):
        account_no = input("Please Give Your Account No :- ")
        pin = int(input("Please Give Your Pin No :- "))
        userdata = [i for i in Bank.data if i['accountNo'] == account_no and i['pin'] == pin]

        if userdata == False:
            print("There Is No Such Data Exists")
        else :
            print("Are You Sure To Delete Your Account.")
            res = input("y - For sure And n - For stop the process :- ")
            if res == "n" or res == "N":
                print("The Delition Process Stopped Successfully")
            else:
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                Bank.__update()
                print("Account Deleted Successfully")

user = Bank()

print("Press 1 for creating an account")
print("Press 2 for depositing the money in account")
print("Press 3 for withdrawing the money from account")
print("Press 4 for Details")
print("Press 5 for updating details")
print("Press 6 for deleting an account")

check = int(input("Give Your Resoponse :- "))

if check == 1:
    user.create_account()

if check == 2:
    user.deposite_money()

if check == 3:
    user.withdraw_money()

if check == 4:
    user.show_details()

if check == 5:
    user.update_details()

if check == 6:
    user.delete()