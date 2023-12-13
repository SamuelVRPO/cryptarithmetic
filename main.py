# Backtrack algorithm to solve the cryptarithmetic problem
# Samuel Vieira Restrepo
# sv2657@nyu.edu
import os
import copy
import queue
from CSP import CSP
from Variable import Variable


# For the Minimum Remaining Value I use a Priority Queue with MRV as
# the priority. If there is more than 1 item with the same MRV I use
# the get_degree() function to determine the degree heuristic.
def select_unassigned_variable(csp):
    min_queue = queue.PriorityQueue()
    for i in range(len(csp.variables)):
        if not csp.variables[i].is_assigned:
            priority_item = (len(csp.domains[i]), csp.variables[i])
            min_queue.put(priority_item)

    vars_with_m_r_v = []
    m_r_v = float('inf')
    queue_item = min_queue.get()
    vars_with_m_r_v.append(queue_item[1])

    while queue_item[0] <= m_r_v and min_queue.qsize() > 0:
        vars_with_m_r_v.append(queue_item[1])
        m_r_v = queue_item[0]
        queue_item = min_queue.get()

    # If there is only one variable with the MRV, return that, otherwise
    # get the degree heuristic for every var and use that.
    if len(vars_with_m_r_v) == 1:
        return vars_with_m_r_v[0]
    else:
        max_degree = 0
        max_var = None
        for i in vars_with_m_r_v:
            curr_degree = csp.get_degree(i.id)
            if curr_degree > max_degree:
                max_degree = curr_degree
                max_var = i
    return max_var


# This is the main Backtrack algorithm with some modifications
def backtrack(csp, assignment):
    if csp.assignment_is_complete():
        return assignment

    var = select_unassigned_variable(csp)

    for value in csp.domains[var.id]:
        if csp.is_consistent(var.id, value, assignment):
            assignment[var.letter] = value
            prev_state = copy.deepcopy(csp)
            csp.update_domains(var, value, assignment)
            csp.set_assigned(var)

            result = backtrack(csp, assignment)
            if result != 'failure':
                return result

            assignment.pop(var.letter)
            csp.set_unassigned(var)
            csp = prev_state

    return 'failure'


# In this function I prepare the CSP with the appropriate variables and domains
# from the input file.
def solve_cryptarithmetic(filename):
    variables = []
    # Populate variables array with x0 ... x12
    file = open(filename, 'r')
    iden = 0
    for char in file.read():
        if char != '\n':
            new_var = Variable(letter=char, iden=iden)
            variables.append(new_var)
            iden += 1

    # Append auxiliary variables c0 ... c3 to variables
    variables.append(Variable(letter='c0', iden=13))
    variables.append(Variable(letter='c1', iden=14))
    variables.append(Variable(letter='c2', iden=15))
    variables.append(Variable(letter='c3', iden=16))

    domains = []
    for i in range(len(variables)):
        if i > 12:
            domains.append({0, 1})
        elif i == 8:
            domains.append({1})
        elif i == 0 or i == 4:
            domains.append({1, 2, 3, 4, 5, 6, 7, 8, 9})
        else:
            domains.append({0, 1, 2, 3, 4, 5, 6, 7, 8, 9})

    csp = CSP(variables, domains, [])

    # We call the Backtrack algorithm and store the solution
    solved = backtrack(csp, {})
    if solved != 'failure':
        word1, word2, word3 = '', '', ''
        for i in range(4):
            word1 = word1 + str(solved[csp.variables[i].letter])

        for i in range(4, 8):
            word2 = word2 + str(solved[csp.variables[i].letter])

        for i in range(8, 13):
            word3 = word3 + str(solved[csp.variables[i].letter])

        if os.path.exists('result.txt'):
            os.remove('result.txt')
        result_file = open('result.txt', 'x')
        result_file.write(word1 + '\n')
        result_file.write(word2 + '\n')
        result_file.write(word3 + '\n')

    else:
        if os.path.exists('result.txt'):
            os.remove('result.txt')
        result_file = open('result.txt', 'x')
        result_file.write('failure')
    return


if __name__ == '__main__':
    solve_cryptarithmetic('test.txt')

