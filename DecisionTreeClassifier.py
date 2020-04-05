
from load_data import *


class Ques:
    def __init__(self, about, detail):
        self.about = about
        self.detail = detail
        self.arr = None

    def compre(self, case):
        if case[self.about] >= self.detail:
            return True
        else:
            return False

    def crate_arr(self):
        self.arr = [self.about, self.detail]


class Pick:
    def __init__(self, is_ques, index):
        self.is_ques = is_ques
        self.index = index


class Node:
    def __init__(self, data, ques=None, left=None, right=None, guess=None, chances=None):
        self.data = data
        self.ques = ques
        self.left = left
        self.right = right
        self.guess = guess
        self.chances = chances
        self.arr = None

    def crate_arr(self):
        self.arr = [len(self.data), self.guess, self.chances]

    def display(self, clf, lst_of_pickers):
        lines, _, _, _ = self._display_aux(clf, lst_of_pickers)
        for line in lines:
            print(line)

    def _display_aux(self, clf, lst_of_pickers):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        if self.arr is None:
            self.crate_arr()
        if self.ques != None and self.ques.arr is None:
            self.ques.crate_arr()

        lst = []
        for item in lst_of_pickers:
            if item.is_ques:
                if self.ques is None:
                    lst.append(None)
                else:
                    lst.append(dict_ques_title[item.index])
                    if item.index == 0:
                        # about
                        lst[-1] += classes[self.ques.about]
                    else:
                        lst[-1] += dict_ques_detail[self.ques.detail]

            else:
                lst.append(dict_title[item.index])
                if item.index == 1:
                    lst[-1] += dict_guess[self.arr[item.index]]
                elif item.index == 2 and self.arr[item.index] is not None:
                    lst[-1] += str(self.arr[item.index] * 100)
                    lst[-1] += "%"
                else:
                    lst[-1] += str(self.arr[item.index])

        # No child.
        if self.right is None and self.left is None:
            line = str(lst)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux(clf, lst_of_pickers)
            s = str(lst)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux(clf, lst_of_pickers)
            s = str(lst)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux(clf, lst_of_pickers)
        right, m, q, y = self.right._display_aux(clf, lst_of_pickers)
        s = str(lst)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


class TreeClassifier:
    def __init__(self):
        self.is_raedy = False
        self.opstions = None
        self.tree = None

    def fit(self, x_train, y):
        self.is_raedy = True

        def find_options(train_y):
            unique = set()
            for l in train_y:
                unique.add(l)
            return unique

        opstions_to_anser = find_options(y)
        self.opstions = opstions_to_anser

        def cuc_impurity(lst_of_index):
            if len(lst_of_index) == 0:
                return 0, None
            if len(lst_of_index) == 1:
                return 0, y[lst_of_index[0]]
            best_num = -1
            best_guess = None
            for guess in opstions_to_anser:
                num = 0
                for i in lst_of_index:
                    if y[i] == guess:
                        num += 1
                if best_num < num:
                    best_num = num
                    best_guess = guess
            score = 1 - (best_num / len(lst_of_index))
            return score, best_guess

        def split(ques, lst_of_index):
            t = []
            f = []
            for i in lst_of_index:
                if ques.compre(x_train[i]):
                    t.append(i)
                else:
                    f.append(i)
            return f, t

        def find_best_split(lst_of_index):
            if len(lst_of_index) == 0:
                return None, None, None
            befor_score, g = cuc_impurity(lst_of_index)
            max = 0
            best_q = None
            rem_f, rem_t = None, None
            for index in lst_of_index:
                case = x_train[index]
                for i in range(len(case)):
                    ques = Ques(i, case[i])
                    f, t = split(ques, lst_of_index)
                    score1, g1 = cuc_impurity(f)
                    score2, g2 = cuc_impurity(t)
                    avg_impurity = ((len(f) / len(lst_of_index)) * score1) + ((len(t) / len(lst_of_index)) * score2)
                    gain = befor_score - avg_impurity
                    if gain > max:
                        max = gain
                        best_q = ques
                        rem_f, rem_t = f, t
            return best_q, rem_f, rem_t

        def make_tree(lst_of_index):
            q, f, t = find_best_split(lst_of_index)
            if q is None:
                impurity, guess = cuc_impurity(lst_of_index)
                return Node(lst_of_index, guess=guess, chances=1 - impurity)
            return Node(lst_of_index, q, make_tree(f), make_tree(t))

        self.tree = make_tree(range(len(x_train)))

    def pracdict(self, x_test):
        if not self.is_raedy:
            raise NotImplementedError
        else:
            def pridct(row, node):
                if node.ques is None:
                    return node.guess, node.chances

                if node.ques.compre(row):
                    return pridct(row, node.right)
                else:
                    return pridct(row, node.left)

            pridcttions = []
            for i in range(len(x_test)):
                g, ch = pridct(x_test[i], self.tree)
                pridcttions.append(g)
            return pridcttions


def accuracy_score(y_test, pridcttions):
    t = 0
    f = 0
    for i in range(len(y_test)):
        if y_test[i] == pridcttions[i]:
            t += 1
        else:
            f += 1
    return t / (t + f)


