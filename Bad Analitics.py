"""
This code will go through random words to find correlation between them in Google Trends.
It will return results in a graph along with the correlation.
You can use this to check new random words each time or a random word off of a word you set.

By Mark Brown: mrb5142@rit.edu
"""
from pytrends.request import TrendReq
from random_words import RandomWords
import pandas as pd
import matplotlib.pyplot as plt

# Counter
n = 0

# Set word to check randomly against. Or don't, it still works!
# If you sey one word then it will always check for correlation against that one word
# If you do not set a word then it will check for correlation from 2 new random words each time
quest = input("Would you like to set one word yourself? Otherwise two random words will be used each time. (Y/N): ")
if quest == "Y" or quest == "y":
    custom = input("Type word to set: ")

while True:
    # Counts attempts
    n += 1

    # Selects random word(s) to test
    word = RandomWords().random_words(count=2)
    if quest == "Y" or quest == "y":
        kw_list = [custom, word[1]]
        word[0] = custom
    else:
        kw_list = [word[0], word[1]]

    # Checks Google Trends for the last 5 years on both words
    pyTrends = TrendReq(hl='en-US', tz=360)  # Def "hl='en-US', tz=360"
    pyTrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

    # Creates independent lists for each of the words
    panda = pyTrends.interest_over_time()
    panda1 = pd.DataFrame(panda[panda.columns[0]])
    panda2 = pd.DataFrame(panda[panda.columns[1]])

    # Checks correlation between two lists
    core = panda1.corrwith(panda2[panda2.columns[0]])

    # Passes if correlation greater (or less than negative) of the "cutoff" variable set above
    if core[0] >= .3 or core[0] <= -.3:
        kind = "Weak"
        if core[0] >= .5 or core[0] <= -.5:
            kind = "Moderate"
            if core[0] >= .7 or core[0] <= -.7:
                kind = "Strong"
                if core[0] >= .9 or core[0] <= -.9:
                    kind = "Amazing"
        print(n, word, "%.3f" % core[0], "PASSED")
        print(core)
        plt.title(str(kind) + " correlation: " + str("%.3f" % core[0]))
        plt.plot(panda1, label=word[0])
        plt.plot(panda2, label=word[1])
        plt.legend()
        plt.savefig(str(kind) + " " + str(word[0]) + " & " + str(word[1]) + '.png')
        plt.clf()
    else:
        print(n, word, "%.3f" % core[0], "FAILED")
