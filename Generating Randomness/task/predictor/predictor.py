import re
import random

def ask_string(min_length, learn_mode):
    f_string = ""
    while len(f_string) < min_length:
        if learn_mode:
            print(f'The current data length is {len(f_string)}, {min_length - len(f_string)} symbols left')
        print("Print a random string containing 0 or 1:")
        print()
        input_str = input()
        if not learn_mode and (input_str == "enough"):
            return "enough"
        else:
            input_str = re.sub("[^01]", "", input_str)
            if learn_mode:
                f_string = f_string + input_str
            else:
                f_string = input_str
    return f_string


def collect_stats(data_string, dic):
    for triad in dic.keys():
        pos_match = 0
        counters = dic[triad]
        while (pos_match != -1) and (pos_match < len(data_string)):
            pos_match = data_string.find(triad, pos_match)
            if pos_match != -1:
                if (pos_match+3) < len(data_string):
                    if data_string[pos_match+3] == '0':
                        counters[0] += 1
                    else:
                        counters[1] += 1
                    dic[triad] = counters
                    pos_match += 1
                else:
                    pos_match = -1
#       print(str(triad) + ": " + str(counters[0]) + "," + str(counters[1]))
    return dic


def guess_number(tri, dic):
    countl = dic[tri]
    if countl[0] > countl[1]:
        return '0'
    elif countl[0] < countl[1]:
        return '1'
    else:
        return random.choice(['0', '1'])



print("Please provide AI some data to learn...")
final_string = ask_string(100, True)
print()
print("Final data string:")
print(final_string)
print()
balance = 1000
print("You have $1000. Every time the system successfully predicts your next press, you lose $1.")
print('Otherwise, you earn $1. Print "enough" to leave the game.', "Let's go!")

# generate the possible triads of binary values and count them
dict_ = {bin(i).replace("0b", "").zfill(3): [0, 0] for i in range(8)}
dict_ = collect_stats(final_string, dict_)

random_string = ask_string(4, False)
while random_string != "enough":
    possible_slices = [random_string[symbol:symbol+4] for symbol in range(0, len(random_string))
                       if len(random_string[symbol:symbol+4]) == 4]
    outputs = []
    predicted = []
    guesses = 0
    print(possible_slices)
    for slice_ in possible_slices:
        outputs.append(str(slice_[3]))
        predicted.append(str(guess_number(slice_[0:3], dict_)))
        if outputs[-1] == predicted[-1]:
            guesses += 1
            balance -= 1
        else:
            balance += 1

    print("predictions:")
    print(''.join(predicted))
    print()
    print(f'Computer guessed {guesses} out of {len(possible_slices)} symbols right ({round(guesses/len(possible_slices)*100,2)} %)')
    print(f'Your balance is now ${balance}')
    dict_ = collect_stats(random_string, dict_)
    random_string = ask_string(4, False)
print("Game over!")
