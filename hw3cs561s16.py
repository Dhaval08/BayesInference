import sys

filename = sys.argv[-1]                 #accepting input file name via the command line
f = open(filename)

#---------------------------------Creating the Bayesian Network from the i/p file as a Dictionary-----------------------------------

bayesNetwork = {}                       #creating an empty dictionary for storing the network

queryList = []

nextLine = f.readline().strip()
i = 0

while nextLine[0]!='*':

    queryList.append(nextLine)
    nextLine = f.readline().strip()

print(queryList)

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

                bayesNetwork[next.strip('\n')] = {'Parents': [], 'Probability':decision.strip('\n'), 'ConditionalProb':[], 'Type':'Normal'}
                bayesNetwork[next.strip('\n')]['Children'] = []

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


for i in range (0, len(queryList)):
    query = queryList[i]

    if query[0] == 'P':

        splitQuery = query.split('(')
        function = splitQuery[0]                    #It can be 'P', 'EU' or 'MEU'
        print(function)

        values = splitQuery[1]                      #The part of the query after the opening bracket

        observedVariables = []
        observedValues = []
        observedDictionary = {}
        variables = []
        value = []

        if values.count('|')==1:                    #Extract the query variable appearing before the '|'

            b = values[:values.index('|')]
            X = b[:b.index(' ')]

            variables.append(X)                     #Query variable. eg. P(X|e)

            if b.count('+')==1:
                value.append('True')
            else:
                value.append('False')

            d = values[values.index('| ')+2:]      #'d' will store the part after the '|'


        else:                                       #If '|' is not present in the given query
            d = values                              #In this case, 'd' will be the entire query itself

        e = d.split(', ')

        for i in range(0, len(e)):                  #Check for each variable whose value is already given in the query
                variables.append((e[i][:e[i].index(' =')]))
                if e[i].count('+') == 1:
                    value.append('True')
                else:
                    value.append('False')


        for i in range (0, len(variables)):
                observedDictionary[variables[i]] = value[i]

        print(observedDictionary)




