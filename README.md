Model1
======

A python implementation of IBM Model 1 for use with the Canadian Parliament minutes (the Hansards.) You can download the correctly formatted files here : https://www.dropbox.com/s/v6rspcdkifsx67q/training.zip
To use, initialize a ConditionalFreqDist (use freqDist = ConditionalFreqDist) and choose a convergence threshold (optimal is 0.01)
Call yourProbabilityDictionary = run(freqDist, convergence_threshol)

To test, call test(yourProbabilityDictionary)

To translate a single word or sentence, wrte the sentence (in French) and call translate(frenchSentence, yourProbabilityDictionary)
