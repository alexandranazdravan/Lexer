from typing import List

State = str
Conf = (str, str)


class DFA:
    def __init__(self, alpha, token, init, delta, final,check):
        #o chestie pe care am pus-o eu sa nu parsez de doua ori prin acelasi dfa si
        #sa fac split-uri pe tranzitii
        self.check = check
        #alfabetul
        self.alphabet: List[str] = alpha
        #token-ul
        self.token = token
        #multimea totala a starilor
        self.states = List[str]
        #sinkstate-urile
        self.sinkstates = List[str]
        #starea initiala
        self.initialState: State = init
        #multimea tuturor tranzitiilor
        self.delta: List[List[str, str, str]] = delta
        self.deltadict = {}
        #lista starilor finale
        self.finalStates: List[State] = final


    def step(self, conf: Conf) -> Conf:
        next_conf = (str,str)
        if conf[0] in self.deltadict.keys():
            if conf[1][0] in self.deltadict[conf[0]]:
                next_conf = (self.deltadict[conf[0]][conf[1][0]][0], conf[1][1:])
            if conf[1][0] == '\n' and '\\'in self.deltadict[conf[0]]:
                #daca e in skinkstate, s-a terminat
                # print("here")
                if self.deltadict[conf[0]] in self.sinkstates:
                    return -1
                #returnez urmatoarea configuratie
                next_conf = (self.deltadict[conf[0]]['\\'][0], conf[1][1:])
            return next_conf
        return -1




    def accept(self, word: str) -> bool:
        config = (self.initialState, word)
        while config[1]:
            #cat timp nu s-a terminat cuvantul meu, tot aplic step pe el;
            #daca s-a intors -1 la un moment dat, inseamna ca ceva n-a fost in regula, deci
            #returnez false;
            #verific daca sunt in finalStates;
            #daca n am intors true pana la final, returnez false ca inseamna ca nu s in stare
            #finala, chit ca nu s nici in sinkstate
            config = self.step(config)
            if config == -1:
                return False
        if config[0] in self.finalStates:
            return True
        return False


def check(cuvant, dfas, out):
    for dfa in dfas:
        #pentru fiecare dfa din lista verific daca acesta imi accepta cuvantul si il
        #scriu in fisier;
        #fac verificari speciale pt \n ca iar imi dadea batai de cap
        if dfa.accept(cuvant) == True:
            if(cuvant != '\n'):
                # print("cuvantul este:   ", cuvant)
                out.write(dfa.token + " " + cuvant + "\n")
            else:
                out.write(dfa.token + "\\n" + "\n")
            return True
    return False



def prefix(cuvant, dfas, out):
    cuv_aux = cuvant
    leng = len(cuvant)

    while cuv_aux:
        #cat timp am cuvant, verific daca vreun dfa mi-a acceptat vreo parte din el;
        #ca sa vad cat de mare e prefixul, tot sterg de la final, in caz ca nu accepta
        #din prima, cu el intreg
        if check(cuv_aux, dfas):
            cuv_aux = cuvant[leng:]
            leng = len(cuvant)
        else:
            leng = leng - 1
            cuv_aux = cuv_aux[:-1]


def runlexer(fdfas,finput,fout):
    #aici e o citire foarte lunga
    with open(fdfas, "r") as input:
        #lista mea cu toate dfa-urile
        dfas = []
        lines = input.readlines()
        lines_aux = [[]]

        #aici imi portionez dupa fiecare dfa, adica fiecare \n semnifica
        #terminarea citirii datelor pt un dfa
        newList = []
        for el in lines:
            if el != '\n':
                newList.append(el)
            else:
                lines_aux.append(newList)
                newList = []
        lines_aux.append(newList)
        #ii dau pop ca avea mereu lista nula la inceput
        lines_aux.pop(0)

        #aici o iau pe cazuri
        for dfa in lines_aux:
            #daca nu gasesc nici dfa-ul pt space si nici pe cel pt newline,
            #atunci inseamna ca s pe cazul general
            if dfa[1].find("SPACE") == -1 and dfa[1].find("NEWLINE") == -1:
                #creez alpfabetul
                alphabet = dfa[0].split()
                #setez initial state
                initialState = dfa[2]
                #setez token-ul
                token = dfa[1]
                #setez starile finale
                finalStates = dfa[-1].split()
                #dau pop la tot ce am memorat pana acum si raman practic doar cu
                #chestiile din mijloc, adica cu tranzitiile
                dfa.pop(0)
                dfa.pop(0)
                dfa.pop(0)
                dfa.pop(-1)
                transitions = []
                #iau fiecare linie, adica fiecare tranzitie
                for line in dfa:
                    #o verific daca are caracterul spatiu;
                    #din cauza unor probleme cu faptul ca mi salva o stare finala sub forma
                    #"3\n", am fost nevoita pe un caz general sa dau split() ca sa mi taie de la final;
                    #un astfel de split cand am spatiu, imi distruge tot, asa ca iau cazul in particular,
                    #unde ii dau split dupa virgula si fac chestia cu [:-1] ca sa-mi stearga \n
                    aux = line.split(",")
                    if(aux[1] == "' '"):
                        aux[2] = aux[2][:-1]
                        transitions.append(aux)
                        dfas.append(DFA(alphabet, token, initialState, transitions, finalStates, False))
                    else:
                        #daca nu am spatiu ca si caracter, atunci dau split dupa virgula(dupa ce
                        # verific sa nu fi facut asta deja) si initializez sinkstate-urile cu lista
                        # vida si la fel si state-urile totale
                        #else-ul este ca sa mi initializeze si pt cazurile cu spatiu, tratate anterior
                        transitions.append(line.split())
                        dfas.append(DFA(alphabet, token, initialState, transitions, finalStates, False))
                        for dfa in dfas:
                            if dfa.check == False:
                                for i in range(0, len(dfa.delta)):
                                    if len(dfa.delta[i]) == 1:
                                        aux = dfa.delta[i][0].split(',')
                                        dfa.delta[i] = aux
                                        dfa.sinkstates = []
                                        dfa.states = []
                                        dfa.check = True
                                    else:
                                        dfa.sinkstates = []
                                        dfa.states = []
                #aici aveam din nou probleme cu "\n", asa ca am facut din nou chestii cu [:-1]
                for el in dfas:
                    if len(el.initialState) > 1:
                        el.initialState = el.initialState[:-1]
                    if (el.token[-1] == '\n'):
                        el.token = el.token[:-1]
            elif dfa[1].find("SPACE") != -1 and dfa[1].find("NEWLINE") == -1:
                #aici daca gasesc space

                #setez alfabetul
                alphabet = " "
                #setez starea initiala
                initialState = dfa[2]
                #setez token ul
                token = dfa[1]
                #setez lista starilor finale
                finalStates = dfa[-1].split()
                #dau pop la ce nu mi mai trebuie
                dfa.pop(0)
                dfa.pop(0)
                dfa.pop(0)
                dfa.pop(-1)
                transitions = []
                for line in dfa:
                    #imi creez tranzitia si ii dau append
                    transitions.append([line.split()[0][:-2], ' ', line.split()[-1][2:]])
                #adaug in lista de dfa uri dfa-ul format
                dfas.append(DFA(alphabet, token, initialState, transitions, finalStates, True))
                #initializez sinkstates si states
                for dfa in dfas:
                    for i in range(0, len(dfa.delta)):
                        dfa.sinkstates = []
                        dfa.states = []
            elif dfa[1].find("SPACE") == -1 and dfa[1].find("NEWLINE") != -1:
                #aici e daca gasesc \n

                #setez alfabetul
                alphabet = '\n'
                #setez starea initiala
                initialState = dfa[2]
                #setez token ul
                token = dfa[1]
                #setez lista starilor finale
                finalStates = dfa[-1].split()
                #sterg ce nu mi mai trebuie
                dfa.pop(0)
                dfa.pop(0)
                dfa.pop(0)
                dfa.pop(-1)
                transitions = []
                for line in dfa:
                    #aici un split dupa virgula e bine-venit
                    transitions.append(line.split(','))
                #adaug dfa-ul la lista
                dfas.append(DFA(alphabet, token, initialState, transitions, finalStates, False))
                #initiliazez sinkstates si states si mai fac niste "perfectionari" in delta
                for dfa in dfas:
                    dfa.sinkstates = []
                    dfa.states = []
                    if dfa.check == False:
                        for i in range(0, len(dfa.delta)):
                            aux = dfa.delta[i][2]
                            aux = aux[:-1]
                            dfa.delta[i][2] = aux
                            dfa.check = True

        #aici imi creez states si un sinkstate provizoriu
        for dfa in dfas:
            states = []
            sinkstates = []
            for transitions in dfa.delta:
                if transitions[0] not in states:
                    states.append(transitions[0])
                if transitions[2] not in states:
                    states.append(transitions[2])
                if transitions[0] not in dfa.sinkstates:
                    sinkstates.append(transitions[0])
            dfa.states = states
            dfa.sinkstates = sinkstates

        #daca nu gasesc item-ul in lista 2 si el a lista 1, atunci il adaug la diff
        #schimb sinkstates cu diff
        for dfa in dfas:
            list_difference = []
            for item in dfa.states:
                if item not in dfa.sinkstates:
                    list_difference.append(item)
            dfa.sinkstates = list_difference

        #alte probleme de citire pe care am fost nevoita sa le rezolv aici
        #aici era o combinatie ciudata de ghilimele cu apostrof
        for dfa in dfas:
            for transition in dfa.delta:
                if len(transition[1]) > 1:
                    transition[1] = transition[1][1]

        result = {}
        aux = {}
        list_tokens = []
        for dfa in dfas:
            aux = {}
            if dfa.token not in list_tokens:
                list_tokens.append(dfa.token)
                for transition in dfa.delta:
                    if transition[0] in aux.keys():
                        aux[transition[0]][transition[1]] = [transition[2]]
                    else:
                        aux[transition[0]] = {transition[1]: [transition[2]]}
                dfa.deltadict = aux

        #imi iau inputul
        with open(finput, "r") as inputt:
                cuvant = ''.join(inputt.readlines())
        #apelez prefix in care tot scriu out-ul
        with open(fout,"w") as out:
            prefix(cuvant, dfas, out)

