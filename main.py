from typing import List
import sys


State = str
Conf = (str, str)


class NFA:
    def __init__(self, alpha, token, init, delta, final):
        #alfabetul
        self.alphabet: List[str] = alpha
        #token-ul
        self.token = token
        #multimea totala a starilor
        self.states = List[str]
        #starea initiala
        self.initialState: State = init
        #multimea tuturor tranzitiilor
        self.delta: List[List[str, str, str]] = delta
        self.deltadict = {}
        #lista starilor finale
        self.finalStates: State = final

    def e_closure_aux(self, v, visited, e_closure_states):
        if v not in visited:
            visited.append(v)
            e_closure_states.append(v)
            if v in self.deltadict:
                if "ep" in self.deltadict[v]:
                    for el in self.deltadict[v]["ep"]:
                        if self.deltadict[v]["ep"] not in visited:
                            self.e_closure_aux(el ,visited,e_closure_states)

    def e_closure(self, v):
        visited = list()
        e_closure_states = list()
        self.e_closure_aux(v, visited, e_closure_states)
        return e_closure_states


    def not_e_closure_aux(self, closure, visited, new_tranz):
        list_closure = self.e_closure(closure)
        dict = {}
        for letter in self.alphabet:
            aux1 = []
            final = []
            for el in list_closure:
                if el in self.deltadict and letter in self.deltadict[el]:
                    aux1.append(self.deltadict[el][letter][0])

            aux1 = list(dict.fromkeys(aux1))
            aux2 = list(dict.fromkeys(aux1))
            final.extend(aux1)
            dict[letter] = aux1

        new_tranz[str(list_closure)] = dict
        if str(list_closure) not in visited:
            visited.append(str(list_closure))
            for k, v in dict.items():
                if v != []:
                    for i in v:
                        self.not_e_closure_aux(i, visited, new_tranz)



    def not_e_closure(self, v, tranz):
        visited = list()
        tranz_aux = {}
        if v not in visited:
            visited.append(v)
            tranz_aux = self.not_e_closure_aux(v, visited, tranz)
        tranz[v] = tranz_aux
        return tranz

def listToString(s):

    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1


class DFA:
    def __init__(self, alpha, init, final):
        #alfabetul
        self.alphabet: List[str] = alpha
        #multimea totala a starilor
        self.states = List[str]
        #sinkstate-urile
        self.sinkstates = State
        #starea initiala
        self.initialState: State = init
        #multimea tuturor tranzitiilor
        # self.delta: dict{dict[]} = delta
        self.delta = {}
        #lista starilor finale
        self.finalStates: List[State] = final



def print_nfa(nfa):
    print("Name: " + nfa.token)
    print("Alfabet: " + str(nfa.alphabet))
    print("All states: " + str(nfa.states))
    print("Initial state: " + str(nfa.initialState))
    print("Final state: " + str(nfa.finalStates))
    print("Delta: " + str(nfa.delta))
    print()

def print_dfa(nfa):
    print("Alfabet: " + str(nfa.alphabet))
    print("All states: " + str(nfa.states))
    print("Initial state: " + str(nfa.initialState))
    print("Final state: " + str(nfa.finalStates))
    print("Sink state: " + str(nfa.sinkstates))
    print("Delta: " + str(nfa.delta))
    print()

def main(fin,fout):


    with open(fin, "r") as inputt:
        inputt = open(fin, "r")
        word = ''.join(inputt.readlines())
        inputt.close()

    new_word = word.split(" ")
    new_word.reverse()
    alphabet = []

    nfas = []
    nr_states = 0
    it_is_character = 0

    for token in new_word:
        if ((token.isalpha() and len(token) == 1) or (token.isnumeric() and len(token) == 1)):
            nfas.append(NFA(token,"caracter",str(nr_states),[str(nr_states),token,str(nr_states + 1)],str(nr_states + 1)))
            nr_states = nr_states + 2
            it_is_character = 1
            if token not in alphabet:
                alphabet.append(token)

        if(token == "STAR"):
            it_is_character = 0
            new_delta = []
            new_tranz = []
            ceva = nfas.pop()
            new_tranz.append(str(nr_states))
            new_tranz.append("ep")
            new_tranz.append(str(ceva.initialState))
            new_delta.append(new_tranz)
            new_tranz = []
            new_tranz.append(str(ceva.finalStates))
            new_tranz.append("ep")
            new_tranz.append(str(ceva.initialState))
            new_delta.append(new_tranz)
            new_tranz = []
            new_tranz.append(str(nr_states))
            new_tranz.append("ep")
            new_tranz.append(str(nr_states + 1))
            new_delta.append(new_tranz)
            new_tranz = []
            new_tranz.append(str(ceva.finalStates))
            new_tranz.append("ep")
            new_tranz.append(str(nr_states + 1))
            new_delta.append(new_tranz)

            if (len(ceva.delta) != 3):
                for tranz in ceva.delta:
                    new_delta.append(tranz)
            else:
                if(len(ceva.delta[0]) == 3):
                    for tranz in ceva.delta:
                        new_delta.append(tranz)
                else:
                    new_delta.append(ceva.delta)
            nfas.append(NFA(token, "STAR", str(nr_states), new_delta, str(nr_states + 1)))
            nr_states = nr_states + 2


        if(token == "CONCAT"):
            it_is_character = 0

            new_delta = []
            new_tranz = []
            ceva1 = nfas.pop()
            ceva2 = nfas.pop()

            new_tranz.append(str(ceva1.finalStates))
            new_tranz.append("ep")
            new_tranz.append(str(ceva2.initialState))
            new_delta.append(new_tranz)
            if(len(ceva1.delta) != 3):
                for tranz in ceva1.delta:
                    new_delta.append(tranz)
            else:
                new_delta.append(ceva1.delta)
            if (len(ceva2.delta) != 3):
                for tranz in ceva2.delta:
                    new_delta.append(tranz)
            else:
                new_delta.append(ceva2.delta)

            nfas.append(NFA(token,"concat",ceva1.initialState,new_delta,ceva2.finalStates))

        if(token == "PLUS"):
            it_is_character = 0

            new_delta = []
            new_tranz = []
            ceva = nfas.pop()
            new_tranz.append(str(nr_states))
            new_tranz.append("ep")
            new_tranz.append(str(ceva.initialState))
            new_delta.append(new_tranz)
            new_tranz = []
            new_tranz.append(str(ceva.finalStates))
            new_tranz.append("ep")
            new_tranz.append(str(ceva.initialState))
            new_delta.append(new_tranz)
            new_tranz = []
            new_tranz.append(str(ceva.finalStates))
            new_tranz.append("ep")
            new_tranz.append(str(nr_states + 1))
            new_delta.append(new_tranz)

            if (len(ceva.delta) != 3):
                for tranz in ceva.delta:
                    new_delta.append(tranz)
            else:
                if (len(ceva.delta[0]) == 3):
                    for tranz in ceva.delta:
                        new_delta.append(tranz)
                else:
                    new_delta.append(ceva.delta)
            nfas.append(NFA(token, "plus", str(nr_states), new_delta, str(nr_states + 1)))
            nr_states = nr_states + 2

        if(token == "UNION"):
            it_is_character = 0

            new_delta = []
            new_tranz = []
            ceva1 = nfas.pop()
            ceva2 = nfas.pop()

            state1 = str(nr_states)
            state2 = ceva2.initialState
            state3 = ceva2.finalStates
            state4 = ceva1.initialState
            state5 = ceva1.finalStates
            state6 = str(nr_states + 1)

            new_tranz.append(str(state1))
            new_tranz.append("ep")
            new_tranz.append(str(state2))
            new_delta.append(new_tranz)
            new_tranz = []
            new_tranz.append(str(state1))
            new_tranz.append("ep")
            new_tranz.append(str(state4))
            new_delta.append(new_tranz)
            new_tranz = []
            new_tranz.append(str(state3))
            new_tranz.append("ep")
            new_tranz.append(str(state6))
            new_delta.append(new_tranz)
            new_tranz = []
            new_tranz.append(str(state5))
            new_tranz.append("ep")
            new_tranz.append(str(state6))
            new_delta.append(new_tranz)
            if (len(ceva1.delta) != 3):
                for tranz in ceva1.delta:
                    new_delta.append(tranz)
            else:
                if (len(ceva1.delta[0]) == 3):
                    for tranz in ceva1.delta:
                        new_delta.append(tranz)
                else:
                    new_delta.append(ceva1.delta)
            if (len(ceva2.delta) != 3):
                for tranz in ceva2.delta:
                    new_delta.append(tranz)
            else:

                if(len(ceva2.delta[0]) == 3):
                    for tranz in ceva2.delta:
                        new_delta.append(tranz)
                else:
                    new_delta.append(ceva2.delta)
            nfas.append(NFA(token, "union", state1, new_delta, state6))
            nr_states = nr_states + 2

    # if(it_is_character == 0):
    #     for nfa in nfas:
    #         states = []
    #         for transitions in nfa.delta:
    #
    #             if transitions[0] not in states:
    #                 states.append(transitions[0])
    #             if transitions[2] not in states:
    #                 states.append(transitions[2])
    #         nfa.states = states
    # else:
    #     states = []
    #     states.append(nfas[0].initialState)
    #     states.append(nfas[0].finalStates)
    #     nfas[0].states = states
    #     print(nfas[0].states)

    if it_is_character == 0:
        aux = {}
        for transition in nfas[0].delta:
            if transition[0] in aux.keys():
                aux[transition[0]][transition[1]].append(transition[2])
            else:
                aux[transition[0]] = {transition[1]: [transition[2]]}
        nfas[0].deltadict = aux

        alpha = []
        for key,value in nfas[0].deltadict.items():
            if list(value.keys())[0] not in alpha and list(value.keys())[0] != "ep":
                alpha.append(list(value.keys())[0])

        nfas[0].alphabet = alpha
        res = {}
        res = nfas[0].not_e_closure(nfas[0].initialState,res)
        res.popitem()
        new_res = {}
        initial_state_for_dfas = ""
        final_states_for_dfas = list()
        for k,v in res.items():
            for letter in nfas[0].alphabet:
                for el in  res[k][letter]:
                    l = nfas[0].e_closure(el)
                    res[k][letter] = (str(l))
                    if nfas[0].finalStates in l:
                        if listToString(l) not in final_states_for_dfas:
                            l.append(listToString(l))

        final_states = list()
        for k,v in res.items():
            s = k[1:][:-1]
            l = s.split(",")
            ll = []
            for el in l:
                el1 = el[1:][:-1]
                for elem in el1:
                    if elem == "'":
                        el1 = el1[1:]
                ll.append(el1)
            key = listToString(ll)
            aux_dict = {}
            for letter in nfas[0].alphabet:
                if res[k][letter] != []:
                    s = res[k][letter][1:][:-1]
                    s = s.split(",")
                    lll = []
                    for element in s:
                        element1 = element[1:][:-1]
                        element1 = element1.replace("'", "")
                        lll.append(element1)
                        aux_dict[letter] = listToString(lll)
                else:
                    aux_dict[letter] = ' '
                new_res[key] = aux_dict
            if nfas[0].initialState in ll:
                initial_state_for_dfas = listToString(ll)
            if nfas[0].finalStates in ll:
                final_states_for_dfas.append(listToString(ll))

        list_of_states_for_dfa = list()
        touple_for_dfa = list()
        index = 0
        initial_state = "nimic"
        sinkstate = ""
        for k, v in new_res.items():
            if k not in list_of_states_for_dfa:
                list_of_states_for_dfa.append(k)
                touple_for_dfa.append((k,index))
                index += 1
            for letter in nfas[0].alphabet:
                if v[letter] not in list_of_states_for_dfa:
                    list_of_states_for_dfa.append(v[letter])
                    touple_for_dfa.append((v[letter], index))
                    index += 1
        deltadict = {}

        for k,v in new_res.items():
            delta_aux = {}
            for letter in nfas[0].alphabet:
                for pereche in touple_for_dfa:
                    if k == pereche[0]:
                        if pereche[0] == initial_state_for_dfas:
                            initial_state = pereche[1]
                        if pereche[0] in final_states_for_dfas:
                            if pereche[0] not in final_states:
                                final_states.append(pereche[1])
                        for perechee in touple_for_dfa:
                            if perechee[0] == new_res[k][letter]:
                                if new_res[k][letter] in final_states_for_dfas:
                                    if perechee[1] not in final_states:
                                        final_states.append(perechee[1])
                                if new_res[k][letter] == ' ':
                                    sinkstate = perechee[1]
                                delta_aux[letter] = perechee[1]
                        deltadict[pereche[1]] = delta_aux


        states = []
        for i in range(0,index):
            states.append((str(i)))

        delta_aux = {}
        for letter in nfas[0].alphabet:
            for elem in states:
                if elem == str(sinkstate):
                    delta_aux[letter] = elem
                    deltadict[elem] = delta_aux

        final_states = list(dict.fromkeys(final_states))
        dfa = DFA(nfas[0].alphabet,initial_state,final_states)
        dfa.delta = deltadict
        dfa.states = states
        dfa.sinkstates = sinkstate
    else:
        print_nfa(nfas[0])
        dfa = DFA(nfas[0].alphabet, nfas[0].initialState, nfas[0].finalStates)
        dfa.sinkstates = str(int(nfas[0].finalStates) + 1)
        delta_aux = {}
        delta_aux[dfa.alphabet] = dfa.finalStates
        dfa.delta[dfa.initialState] = delta_aux
        delta_aux = {}
        delta_aux[dfa.alphabet] = str(dfa.sinkstates)
        dfa.delta[dfa.finalStates] = delta_aux
        delta_aux = {}
        delta_aux[dfa.alphabet] = str(dfa.sinkstates)
        dfa.delta[str(dfa.sinkstates)] = delta_aux
        states = []
        states.append(dfa.initialState)
        states.append(dfa.finalStates)
        states.append(dfa.sinkstates)
        dfa.states = states

    # de scris in fisier dupa
    index = 0
    for k in dfa.delta:
        for letter in dfa.alphabet:
            index += 1
    count = 0
    with open(fout, "a") as out:
        for elem in dfa.alphabet:
            out.write(elem)
        out.write("\n")
        out.write(str(len(dfa.states)) + "\n")
        out.write(str(dfa.initialState)+ "\n")
        for i in range(0,len(dfa.finalStates)):
            elem = dfa.finalStates[i]
            if i < len(dfa.finalStates) - 1:
                out.write(str(elem) + " ")
            else:
                out.write(str(elem))
        out.write("\n")
        for k in dfa.delta:
            for letter in dfa.alphabet:
                out.write(str(k) + ",'" + letter + "'," + str(dfa.delta[k][letter]))
                if count < index - 1:
                    count += 1
                    out.write("\n")
    out.close()


if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])
    # main("tests/T2/in/T2.1.in", "tests/T2/out/01.txt")

