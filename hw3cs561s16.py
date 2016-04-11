import sys

filename = sys.argv[-1]                 #accepting input file name via the command line
f = open(filename)

#---------------------------------Creating the Bayesian Network from the i/p file as a Dictionary-----------------------------------

bayesNetwork = {}                       #creating an empty dictionary for storing the network

nextLine = f.readline()
i = 0

while nextLine[0]!='*':

    nextLine = f.readline()

first = f.readline().strip()

while first != '':                      #traverse till the end of the input file
    next = first

    countSeparator = next.count('|')    #check if there are any parents for the particular node

    if countSeparator == 0:

            decision = f.readline().strip()
            if decision[0] == 'd':
                bayesNetwork[next.strip('\n')] = {'Parents': [], 'Probability':decision.strip('\n'), 'ConditionalProb':[], 'Type':'Decision'}
                bayesNetwork[next.strip('\n')]['Children'] = []
            else:
                bayesNetwork[next.strip('\n')]['Children'] = []

                bayesNetwork[next.strip('\n')] = {'Parents': [], 'Probability':decision.strip('\n'), 'ConditionalProb':[], 'Type':'Normal'}

    else:

            splitLine = next.split(' | ')
            parentsLine = splitLine[1].split(' ')

            for i in range (0, len(parentsLine)):
                bayesNetwork[parentsLine[i]]['Children'].append(splitLine[0].strip())

            bayesNetwork[splitLine[0].strip('\n')] = {}
            bayesNetwork[splitLine[0].strip('\n')]['Parents'] = parentsLine
            bayesNetwork[splitLine[0].strip('\n')]['Children'] = []


            condprob = {}
            for i in range (0, pow(2, len(parentsLine))):



                conditionalProbability = f.readline().strip()

                splitCondProb = conditionalProbability.split(' ')

                prob = splitCondProb[0]

                truthLine = splitCondProb[1:]

                truth = tuple(True if x == '+' else False for x in truthLine)

                condprob[truth] = prob

            bayesNetwork[splitLine[0].strip('\n')]['ConditionalProbability'] = condprob

            bayesNetwork[splitLine[0].strip('\n')]['Probability'] = []

            bayesNetwork[splitLine[0].strip('\n')]['Type'] = 'Normal'

    first = f.readline()

    first = f.readline().strip()


print(bayesNetwork)


#---------------------------------------Bayesian Network Created------------------------------------------------



