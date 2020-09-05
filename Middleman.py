import sys
import fbchat
from fbchat import log, Client
from getpass import getpass
import time


# Functions
def shutdown_exitCancel():
    sys.exit('\n**Cancelled**\nShutting down...')

def shutdown_badInput():
    sys.exit('\n**Invalid selection**\nShutting down...')

def display_menu(user, friend, un, pw):
    type = 0
    print(f'\nDo you wish to transmit a message or receive one?\n')
    print('1. Transmit\n2. Receive');

    type = int(input('\nSelect an option from above [#, -1 to cancel]: '))
    if type == 1:
        msg_send(user, friend, un, pw)
    elif type == 2:
        msg_get(user, friend, un, pw)
    elif type == -1:
        shutdown_exitCancel()
    else:
        shutdown_badInput()

def msg_send(user, friend, un, pw):
    plaintext = list(input(f'\nYou -> {friend.first_name}: ').lower()) #get the user's input
    # perform the algorithm
    index = 0
    charToNum = 27
    for letter in plaintext:
        if letter.isalpha():
            charToNum = ord(letter) - ord('a') + 1
        else:
            charToNum = 27
        plaintext[index] = charToNum
        index += 1
    index = 0

    plaintextBinary = []
    for number in plaintext:
        binaryRep = bin(number)[2:].zfill(5)
        for bit in binaryRep:
            plaintextBinary.append(bit)
    plaintextBinary.reverse()

    for i in range(2):
        plaintextBinary.append(plaintextBinary.pop(0))

    ciphertext = []
    stringBuilder = '0b'
    for bit in plaintextBinary:
        index += 1
        stringBuilder += bit
        if index == 5:
            ciphertext.append(int(stringBuilder, 2))
            index = 0
            stringBuilder = '0b'
    index = 0

    map = {
        0: ' ',
        1: 'A',
        2: 'B',
        3: 'C',
        4: 'D',
        5: 'E',
        6: 'F',
        7: 'G',
        8: 'H',
        9: 'I',
        10: 'J',
        11: 'K',
        12: 'L',
        13: 'M',
        14: 'N',
        15: 'O',
        16: 'P',
        17: 'Q',
        18: 'R',
        19: 'S',
        20: 'T',
        21: 'U',
        22: 'V',
        23: 'W',
        24: 'X',
        25: 'Y',
        26: 'Z',
        27: 'a',
        28: 'b',
        29: 'c',
        30: 'd',
        31: 'e'
    }
    for number in ciphertext:
        ciphertext[index] = map[number]
        index += 1
    index = 0

    t = time.localtime()
    currentTime = int(time.strftime("%H%M", t)) + 2000

    outgoingMsg = ''
    for i in range(len(ciphertext), 0, -1):
        index = currentTime % i
        outgoingMsg += ciphertext.pop(index)

    sent = client.sendMessage(outgoingMsg, thread_id = friend.uid)
    if not sent:
        sys.exit('\n**Error in sending message**\nShutting down...')

    confirmation = input(f'Keep sending messages to {friend.first_name} [Y/n]: ').lower()
    if confirmation == 'y':
        msg_send(user, friend, un, pw)
    elif confirmation == 'n':
        display_menu(user, friend, un, pw)
    else:
        shutdown_badInput()

def msg_get(user, friend, un, pw):
    incomingMsg = ''
    timestampAnalog = 0

    class receiver(Client):
        def onMessage(self, author_id = friend.uid, message_object = None, thread_id = friend.uid, ts = None, **kwargs):
            incomingMsg = message_object.text

            timestampAnalog = int(time.strftime("%H%M", time.localtime(ts / 1000.0)))
            print(f'\n\"{incomingMsg}\" at t = {timestampAnalog}')
            timestampAnalog += 2000

            ciphertext = []
            for i in range(1, len(incomingMsg) + 1):
                ciphertext.insert(timestampAnalog % i, incomingMsg[len(incomingMsg) - i])

            map = {
                ' ': 0,
                'A': 1,
                'B': 2,
                'C': 3,
                'D': 4,
                'E': 5,
                'F': 6,
                'G': 7,
                'H': 8,
                'I': 9,
                'J': 10,
                'K': 11,
                'L': 12,
                'M': 13,
                'N': 14,
                'O': 15,
                'P': 16,
                'Q': 17,
                'R': 18,
                'S': 19,
                'T': 20,
                'U': 21,
                'V': 22,
                'W': 23,
                'X': 24,
                'Y': 25,
                'Z': 26,
                'a': 27,
                'b': 28,
                'c': 29,
                'd': 30,
                'e': 31
            }

            index = 0
            for letter in ciphertext:
                ciphertext[index] = map[letter]
                index += 1
            index = 0

            ciphertextBinary = []
            for number in ciphertext:
                binaryRep = bin(number)[2:].zfill(5)
                for bit in binaryRep:
                    ciphertextBinary.append(bit)

            for i in range(2):
                ciphertextBinary.insert(0, ciphertextBinary.pop(len(ciphertextBinary) - 1))
            ciphertextBinary.reverse()

            plaintext = []
            stringBuilder = '0b'
            for bit in ciphertextBinary:
                index += 1
                stringBuilder += bit
                if index == 5:
                    plaintext.append(int(stringBuilder, 2))
                    index = 0
                    stringBuilder = '0b'
            index = 0

            numToChar = ' '
            for number in plaintext:
                if number != 27:
                    numToChar = chr(plaintext[index] + ord('a') - 1)
                else:
                    numToChar = ' '
                plaintext[index] = numToChar
                index += 1

            incomingMsg = ''
            for i in range(0, len(plaintext)):
                incomingMsg += plaintext[i]

            print(f'\n{friend.first_name} -> You: {incomingMsg}')


    listener = receiver(un, pw)
    try:
        listener.listen()
    except KeyboardInterrupt:
        listener.stopListening()
        display_menu(user, friend, un, pw)


# Login
username = input('Username: ')
password = getpass()
try:
    client = fbchat.Client(username, password, max_tries = 3)
except FBchatException:
    print('\n**Error in Login**\nTrying again...');

# User Search
target_name = input('\nWho will you open a channel with: ')
print()
possible_targets = client.searchForUsers(target_name)

friends = [];
for people in possible_targets:
    if people.is_friend == True:
        friends.append(people)

if len(friends) == 0:
    sys.exit(f'\n**No friend results found for {target_name}**\nShutting down...')

j = 1;
for friend in friends:
    print(f'{j}. {friend.name}')
    j += 1


# Recipent Selection
index = int(input('\nWhich person is the recipient [#, -1 to cancel]: '))

if index == -1:
    shutdown_exitCancel()
elif index > len(friends) or index < -1:
    shutdown_badInput()

recipient = friends[index - 1]

print(f'\nSelected: [{recipient.name}]')
confirmation = input(f'Please confirm that you want to open a channel with {recipient.first_name} [Y/n]: ').lower()

if confirmation == 'n':
    shutdown_exitCancel()
elif confirmation != 'y':
    shutdown_badInput()


# Transmitting vs. Receiving
display_menu(client, recipient, username, password)
