import requests

# import sys
# sys.path.append('E:\\business ideas\\flask_app\count-cough\\userm')

from userm.helper import AIIMSJDPUser, User, CompanyUser, TESTUser, DrAshvendraUser, DrRajkumarHSRUser
from userm.config import API_URL, ACCESS_TOKEN

import random







# a function that will generate a password on length (n) and return it.


def generatePassword(n):
    # defining the list of choices of characters.
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789!@#$%^&*()"

    """
    The random.sample() method returns a list, so we need to convert it into a string before returning it.
    """

    chosenLetter = random.sample(characters, n)

    # finally converting the list into a string
    password = "".join(chosenLetter)

    return password


def create_user(helper: User):
    data = {}
    for attr, v in helper.__dict__.items():
        if  attr.startswith('__'):
            continue
        data[attr] = v
        print(attr, v)
            # attr.value = dict[attr.name]

    if helper.fullName is None:
        data['fullName'] = " ".join([helper.firstName, helper.lastName])
    x = requests.post(API_URL, json=data, headers={'Content-Type': 'application/json'})
    print(x.text)



if __name__ == "__main__":
    # user = AIIMSJDPUser
    # user = CompanyUser
    user = DrRajkumarHSRUser
    user.access_token = ACCESS_TOKEN
    user.firstName = "Dr Rajkumar"
    user.lastName = " "
    user.uniqueName = "drrajkumar"
    user.email = "drrajkumar@airs.com"
    # password = generatePassword(10)
    password = "airs@2024"#"@l7fgesvi1"
    user.password = password
    print('password', password)
    user.isAdmin = True

    create_user(user)
