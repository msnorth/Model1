import re
from nltk import FreqDist, ConditionalFreqDist
#from nltk.util import defaultdict
import string
from collections import OrderedDict, defaultdict

# IBM Model 1 immplementation
#
# to be used with the Hansards https://www.dropbox.com/s/v6rspcdkifsx67q/training.zip


def run(freqDist, convergence_threshold):
    en_corp = []
    fr_corp= []
    for i in range(0,1):

        for j in range(0,1):

            for k in range(1,3):

                print str(i)+str(j)+str(k)

                fr_in = open("hansard.36.1.house.debates."+str(i)+str(j)+str(k)+".f",'r')

                en_in = open("hansard.36.1.house.debates."+str(i)+str(j)+str(k)+".e",'r')

                for line in  en_in.readlines():
                    line = line.translate(string.maketrans("",""), string.punctuation)
                    line = line.lower()
                    en_corp.append(line)

                for line in  fr_in.readlines():
                    line = line.translate(string.maketrans("",""), string.punctuation)
                    line = line.lower()
                    fr_corp.append(line)

                fr_in.close()

                en_in.close()
                
    
    
    counter = 0

    #initialize freqDist uniformly
    while counter < min(len(fr_corp), len(en_corp)):
        French = fr_corp[counter].split()
        English = en_corp[counter].split()
        for frWord in French:
            for enWord in English:
                freqDist[frWord].inc(enWord) 
        counter = counter + 1


    for condition in freqDist.conditions():
            for key in freqDist[condition].keys():
                freqDist[condition][key] = 1.0 / freqDist[condition].B();

    #EM 
    num_converged = 0
    globally_converged = False
    iteration_count = 0
    num_probs = len(en_corp) * len(fr_corp)
    print('Training data: ')
    print(min(len(fr_corp), len(en_corp)))
    print('Parallel sentences.')
    while num_converged < num_probs:
        countef = ConditionalFreqDist()
        totalf = FreqDist()
        counter = 0
        while counter < min(len(fr_corp), len(en_corp)):
            total_s = FreqDist()
            French = fr_corp[counter].split()
            English = en_corp[counter].split()
            
            for enWord in English:
                for frWord in French:
                    total_s.inc(enWord, freqDist[frWord][enWord])

            for enWord in English:
                for frWord in French:
                    countef[frWord].inc(enWord, freqDist[frWord][enWord] / total_s[enWord])
                    totalf.inc(frWord, freqDist[frWord][enWord] / total_s[enWord])
            counter = counter + 1
 
        for frWord in freqDist.conditions():
            for enWord in freqDist[frWord].keys():
                new_prob = countef[frWord][enWord] / totalf[frWord]
                delta = abs(freqDist[frWord][enWord] - new_prob)
                if delta < convergence_threshold:
                    num_converged += 1
                freqDist[frWord][enWord] = new_prob
        iteration_count +=1
        if num_converged == num_probs:
            globally_converged = True
            print('Converged with : ')
            print(iteration_count)
            print('iterations')
            
    return freqDist
    
            

def translate(French, prob):
    sentence = []
    for fWord in French:
        try:
          sentence.append(prob[fWord].max())
        except: 
          sentence.append(fWord)
    return sentence


def test(prob):
    en_corp = []
    fr_corp= []
    for i in range(0,1):

        for j in range(0,1):

            for k in range(2,3):

                print str(i)+str(j)+str(k)

                fr_in = open("hansard.36.1.house.debates."+str(i)+str(j)+str(k)+".f",'r')

                en_in = open("hansard.36.1.house.debates."+str(i)+str(j)+str(k)+".e",'r')

                for line in  en_in.readlines():
                    line = line.translate(string.maketrans("",""), string.punctuation)
                    line = line.lower()
                    en_corp.append(line)

                for line in  fr_in.readlines():
                    line = line.translate(string.maketrans("",""), string.punctuation)
                    line = line.lower()
                    fr_corp.append(line)

                fr_in.close()

                en_in.close()
    correct = 0
    wrong = 0
    counter = 0
    while counter < min(len(fr_corp), len(en_corp)):
        French = fr_corp[counter].split()
        English = en_corp[counter].split()
        s = translate (French,prob)
        if s == English:
            correct += 1
        else:
            wrong += 1

        counter += 1

    print('correct: ')
    print(correct)
    print('wrong: ')
    print(wrong)
    print('Tested on:')
    print(correct + wrong)
        

