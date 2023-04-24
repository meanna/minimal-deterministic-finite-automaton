from itertools import count  # used to create a generator to generate an id for each state.
from collections import OrderedDict
import graphviz
import pickle

'''
Create a class MinDict to implement the Daciuk-Algorithm. 
'''


class MinDict():

    @classmethod
    def from_pickle(cls, automat_pkl):
        try:
            with open(automat_pkl, 'rb') as f_in:
                wordlist, delta, final_states, regis, lang = pickle.load(f_in)
                print("=====================Min DEA===================")
                print(f"Sprache: {wordlist} \n")

                for state, targets in delta.items():
                    for label, target_state in targets.items():
                        print(state, "  ", label, "  ", target_state)
            
            min_dict = cls()
            min_dict.word_list = wordlist
            min_dict.char_list = min_dict.get_char_list()
            min_dict.tr = delta
            min_dict.final_states = final_states
            min_dict.language = lang
            min_dict.register = regis

            return min_dict
        except FileNotFoundError as err:
            print(err)
            return


    @classmethod
    def from_wordlist(cls, wordlist):
        min_dict = cls()
        
        min_dict.tarjan = [(), ()]
        min_dict.tarjan_start = []
        min_dict.word_list = wordlist
        min_dict.char_list = min_dict.get_char_list()

        min_dict.final_states: set[int] = set()  # a set used to store all final states
        min_dict.curr_id = count()  # create an id generator: next_id = next(curr_id)
        min_dict.start = next(min_dict.curr_id)  # the start state
        min_dict.register: set[int] = set()  # a set used to store all registered states, which are not equal to each other
        min_dict.tr: dict[int, OrderedDict[str, int]] = {
            min_dict.start: OrderedDict()}  # a dictionary used to store all states and their transitions
        min_dict.language = list()  # init a list used to store the words acquired via traversal
        min_dict.compile(wordlist)  # compile all functions to build the final minimal dictionary.

        return min_dict

    def __init__(self):
        self.tarjan = [(), ()]
        self.tarjan_start = []
        self.word_list = []
        self.char_list = []

        self.final_states: set[int] = set()  # a set used to store all final states
        self.curr_id = count()  # create an id generator: next_id = next(curr_id)
        self.start = next(self.curr_id)  # the start state
        self.register: set[int] = set()  # a set used to store all registered states, which are not equal to each other
        self.tr: dict[int, OrderedDict[str, int]] = {
            self.start: OrderedDict()}  # a dictionary used to store all states and their transitions
        self.language = list()  # init a list used to store the words acquired via traversal


    def get_char_list(self):
        # get char sorted from word list
        chars = {char for word in self.word_list for char in word}
        sorted_chars = sorted(chars)
        return ["_"] + sorted_chars

    def common_prefix(self, word, pre_word):
        """
        Compute the common prefix of two words
        @param word: currently read-in word
        @parm pre_word: previously read-in word
        return: the common prefix of both words
        """
        common_prefix = ''  # init the common prefix

        for i, c in enumerate(word):
            if i < len(pre_word):
                if c == pre_word[i]:
                    common_prefix += c
                else:
                    return common_prefix
            else:
                return common_prefix

    def split_state(self, common_prefix):
        """
        Compute the split state
        @param common_prefix: a substring, the common prefix
        return: the split state
        """
        split_state = self.start
        if common_prefix == '':
            return split_state
        else:
            for i, c in enumerate(common_prefix):
                split_state = self.tr[split_state][c]
            return split_state

    def has_children(self, state):
        """
        Check if a state has children
        @param: state id
        return: boolean value, if the given state has children or not
        """
        # Hint: That self.has_children(state) is true means self.tr[state] is not an empty OrderedDict.
        return self.tr[state]

    def is_equal(self, s1, s2):
        """
        Check if two states are equivalent
        @param: two state ids
        return: boolean value, if the given states are equal
        """
        return (s1 in self.final_states) == (s2 in self.final_states) and self.tr[s1] == self.tr[s2]

    def replace_or_register(self, state):
        """
        Compute replace_or_register
        @param: a state
        """
        last_child = self.tr[state][next(reversed(self.tr[state]))]  # get the last child state from the state transition.
        if self.has_children(last_child):
            self.replace_or_register(last_child)
        # replace and delete the last child state if it has an equal state in the set of the registered states.
        for s in self.register:
            if self.is_equal(last_child, s):
                self.tr[state][next(reversed(self.tr[state]))] = s
                del self.tr[last_child]  # delete the last child state
                return
        # add the last child into the register set if no equal states are found
        self.register.add(last_child)
        self.fill_tarjan_table(last_child)

    def fill_tarjan_table(self, state):
        """
        Fill the Tarjan table while adding states to the registry
        @param: a state
        """

        # fill tarjan table
        status = "F" if state in self.final_states else "N"
        items = []
        for char, next_state in self.tr[state].items():
            item = (self.char_list.index(char), char)
            items.append(item)

        for i in range(1, len(self.tarjan)):

            item_ok = []
            ok = False
            # find cell for tarjan state
            if not self.tarjan[i]:
                # check if tarjan cell is occupied
                if not items:
                    ok = True

                for item in items:
                    char_index, char = item
                    # extend tarjan table for chars
                    if len(self.tarjan) <= i + char_index:
                        extension = [() for _ in range(char_index)]
                        self.tarjan += extension

                    # if cell is empty
                    if not self.tarjan[i + char_index]:
                        item_ok.append(True)
                    else:
                        item_ok.append(False)
                if all(item_ok):
                    ok = True

            else:
                continue

            if ok:
                self.tarjan[i] = (status, state)
                for item in items:
                    char_index, char = item
                    next_state = self.tr[state][char]
                    next_state_status = "F" if next_state in self.final_states else "N"
                    next_state_index = self.tarjan.index((next_state_status, next_state))
                    self.tarjan[i + char_index] = (char, next_state_index)
                    if state == self.start:
                        self.tarjan_start.append((i + char_index, char, next_state_index))
                if len(self.tarjan) == i + 1:
                    self.tarjan += [()]

                break

    def print_tarjan(self):
        print("=====Tarjan Table=====")
        for i, items in enumerate(self.tarjan):
            if items:
                state_status_or_char, state_id_or_line_id = items
                print(f"{i}\t{state_status_or_char}\t{state_id_or_line_id}")
            else:
                print(f"-\t-\t-")
        print("=====================")

    def save_pkl_file(self, data_to_save, file_name):
        """
        :param data_to_save
        :param file_name
        """

        open_file = open(file_name, "wb")
        pickle.dump(data_to_save, open_file)
        open_file.close()

    def save_automat_to_pkl(self, file_name="automat.pkl"):
        data_to_save = self.word_list, self.tr, self.final_states, self.register, self.language
        open_file = open(file_name, "wb")
        pickle.dump(data_to_save, open_file)
        open_file.close()


    def load_tarjan_file(self, file_name):
        """
        :param filename
        """
        open_file = open(file_name, "rb")
        self.tarjan, self.tarjan_start, self.word_list = pickle.load(open_file)
        open_file.close()

    def add_suffix(self, suffix, state):
        """
        This function is used to add the current suffix after the split state
        @param suffix: a substring
        @param state: state id
        """
        for c in suffix:
            next_state = next(self.curr_id)
            if state not in self.tr:
                self.tr[state] = OrderedDict()
            self.tr[state][c] = next_state
            state = next_state

        self.tr[state] = OrderedDict()
        self.final_states.add(state)

    def compile(self, words):
        """
        @param: a sorted list of words
        gather all parts together to implement the Daciuk-Algorithm.
        """
        pre_word = ''
        for word in words:
            common_prefix = self.common_prefix(word, pre_word)
            split_state = self.split_state(common_prefix)
            current_suffix = word[len(common_prefix):]

            if self.has_children(split_state):
                self.replace_or_register(split_state)
            self.add_suffix(current_suffix, split_state)
            pre_word = word

        self.replace_or_register(self.start)
        self.register.add(self.start)
        self.fill_tarjan_table(self.start)

        # remove last empty cells from tarjan
        empty_cell_count = 0
        for elem in reversed(self.tarjan):
            if elem == ():
                empty_cell_count += 1
            else:
                break
        self.tarjan = self.tarjan[:len(self.tarjan) - empty_cell_count]

    def compute_language(self, state=None, word=""):
        """
        Compute the list of words that belong to the automaton and store it
        in self.language.
        :param state
        :param word
        """
        if state is None:
            state = self.start
        for char, next_state in self.tr[state].items():
            word += char
            if next_state in self.final_states:
                self.language.append(word)
            self.compute_language(next_state, word)
            word = word[:-1]


def draw_automaton(states, final_states, initial_state, delta):
    """
    a function with the help of graphviz to draw an automaton.
    :param final_states
    :param initial_state
    :param delta: transition functions
    """
    g = graphviz.Digraph('MinDict')

    for state in states:
        if state in final_states:
            g.attr('node', style='bold')
        if state == initial_state:
            g.node(str(state), labels='->' + str(state))
        else:
            g.node(str(state))
        g.attr('node', style='solid')

    for x, label, z in delta:
        g.edge(str(x), str(z), label=' ' + label + ' ')

    return g


def display_automaton(DEA):
    """
    Draw a graph of the given automaton and save .gv file in graph folder.
    :param DEA: the min DEA
    :return: None
    """
    # retrieve the elements from DEA to formalize a 5-tuple for an automaton.
    start = str(0)  # start state
    states = {str(i) for i in DEA.register}  # set of all states
    final_states = {str(i) for i in DEA.final_states if i in DEA.register}  # set of final states
    delta = set()  # transition function
    for p in DEA.tr:
        if p in DEA.register:
            for c in DEA.tr[p]:
                q = DEA.tr[p][c]
                delta.add((str(p), c, str(q)))

    # draw the minimal dictionary
    g = draw_automaton(states, final_states, start, delta)
    g.render('graph/aut1.gv', view=True)