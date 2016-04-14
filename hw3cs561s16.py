# @author Dhaval Shah

import sys
import copy

# topologicalSort will sort the given network in a top down fashion
# a node is added to the list only after we have added all its parents

def topologicalSort(networkDictionary):
    var = networkDictionary.keys()
    l =[]

    while len(l) < len(var):
        for v in var:
            if v not in l and all(x in l for x in networkDictionary[v]['Parents']):
                   l.append(v)
    return l

# selectNodes will only select those nodes that are either present in the query
# or whose eventual child/children are in the query. Other nodes are not to be considered

def selectNodes(sortedVariables, networkDictionary, observedVariables):

    x = observedVariables.keys()
    newNetwork = []

    bnPresence = [True if a in x else False for a in sortedVariables]

    for i in range (0, pow(len(sortedVariables), 2)):
        for v in sortedVariables:
            if bnPresence[sortedVariables.index(v)]!=True and any(bnPresence[sortedVariables.index(c)]==True for c in networkDictionary[v]['Children']):
                index = sortedVariables.index(v)
                bnPresence[index] = True

    for eachNode in sortedVariables:
        if bnPresence[sortedVariables.index(eachNode)] == True:
            newNetwork.append(eachNode)

    return newNetwork

def calculateProbability(Y, e, bayesNetwork):
    if len(bayesNetwork[Y]['Parents']) == 0:
        if e[Y] == True:
            prob = float(bayesNetwork[Y]['Probability'])
            return float(bayesNetwork[Y]['Probability'])
        else:
            return 1.0-float(bayesNetwork[Y]['Probability'])
        # Y has at least 1 parent
    else:
        # get the value of parents of Y
        parents = tuple(e[p] for p in bayesNetwork[Y]['Parents'])

        # query for prob of Y = y
        if e[Y] == True:
            return float(bayesNetwork[Y]['ConditionalProbability'][parents])
        else:
            return 1.0-float(bayesNetwork[Y]['ConditionalProbability'][parents])


# enumerateAll will calculate probability for each variable in the given evidence 'e'

def enumerateAll(X, vars, e, bayesNetwork):
    if not vars:
        return 1.0

    Y = vars[0]
    if Y in e:
        returnValue = calculateProbability(Y, e, bayesNetwork) * enumerateAll(X,vars[1:], e, bayesNetwork)

    else:
        prob = []
        e2 = copy.deepcopy(e)
        for eachValue in [True, False]:
            e2[Y] = eachValue
            prob.append(calculateProbability(Y, e2, bayesNetwork) * enumerateAll(X,vars[1:], e2, bayesNetwork))

        returnValue = sum(prob)

    return returnValue

#---------------------------------------accepting and manipulating the input file---------------------------------------------

#filename = sys.argv[-1]
f = open('sample04.txt')

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
                bayesNetwork[next.strip('\n')] = {'Parents': [], 'Probability':decision.strip('\n'), 'ConditionalProbability':[], 'Type':'Decision'}
                bayesNetwork[next.strip('\n')]['Children'] = []
            else:

                bayesNetwork[next.strip('\n')] = {'Parents': [], 'Probability':decision.strip('\n'), 'ConditionalProbability':[], 'Type':'Normal'}
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
sortedVariables = topologicalSort(bayesNetwork)


#-------------------------------------------------Bayesian Network Created---------------------------------------------------

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
        evidenceObservedDictionary = {}
        evidenceVariables = []
        evidenceValue = []
        variables = []
        value = []
        X = ''
        flag = False

        if values.count('|')==1:                    #Extract the query variable appearing before the '|'

            flag = True

            b = values[:values.index('|')]
            X = b[:b.index(' ')]

            variables.append(X)                     #Query variable. eg. P(X|e)

            if b.count('+')==1:
                value.append(True)
            else:
                value.append(False)

            d = values[values.index('| ')+2:]       #'d' will store the part after the '|'

            print X
            print sortedVariables.index(X)

        else:                                       #If '|' is not present in the given query
            d = values                              #In this case, 'd' will be the entire query itself


        e = d.split(', ')

        for i in range(0, len(e)):                  #Check for each variable whose value is already given in the query
                variables.append((e[i][:e[i].index(' =')]))
                if e[i].count('+') == 1:
                    value.append(True)
                else:
                    value.append(False)


        for i in range (0, len(variables)):
                observedDictionary[variables[i]] = value[i]

        bn = selectNodes(sortedVariables, bayesNetwork, observedDictionary)     #now create a network of only those nodes that we need to calculate the given query

        calculatedProbability = enumerateAll(X, bn, observedDictionary, bayesNetwork)

        # If the query is of the form P(X|e) i.e. flag is true, we have to divide "calculatedProbability" it by P(e).
        # So now we create all the terms and network needed to calculate just P(e) and then perform the division

        if flag == True:
            X2 = ''
            evidenceVariables = variables[1:]
            evidenceValue = value[1:]
            for i in range (0, len(evidenceVariables)):
                evidenceObservedDictionary[evidenceVariables[i]] = evidenceValue[i]
            evidenceBN = selectNodes(sortedVariables, bayesNetwork, evidenceObservedDictionary)

            denominator = enumerateAll(X2, evidenceBN, evidenceObservedDictionary, bayesNetwork)
            print('Probability is', calculatedProbability/denominator)

        else:
            print('Probability is', calculatedProbability)


