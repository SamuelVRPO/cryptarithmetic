# This class contains all the methods used in the algorithm:
# - assignment_is_complete(): Returns whether an assignment is complete
# - get_degree(): Returns the degree of a variable v by going through every constraint
#   and seeing how many unassigned variables there are in the constraints shared with v
# - is_consistent(): Returns whether the new assignment is consistent in a similar manner
#   to get_degree(), by going through all the constraints and verifying that they are met.
#   It differs from get_degree() because if multiple variables have the same letter, it must
#   go through every variable and check its constraints as well.
# - set_assigned(): When a letter is assigned a value, goes through every variable with that
#   letter and sets it as assigned.
# - set_unassigned(): Does the opposite of set_assigned().
# - update_domains(): Similar to get_degree() and is_consistent(), it goes through all the
#   constraints, and tries all the values for the variable. Every value that does not satisfy
#   the constraint is removed from the domain list of CSP.
class CSP:
    def __init__(self, variables, domains, _constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = _constraints

    # If every variable is assigned, return true, otherwise return false
    def assignment_is_complete(self):
        complete = True
        for x in self.variables:
            if not x.is_assigned:
                complete = False

        return complete

    def get_degree(self, id_var):
        degree = 0
        counted = []

        # Constraint: All letters must be different
        if id_var in range(13):
            counted_letters = []
            for i in range(13):
                if self.variables[i].letter == self.variables[id_var].letter:
                    continue

                if not self.variables[i].is_assigned and self.variables[i].letter not in counted_letters:
                    counted_letters.append(self.variables[i].letter)
                    degree += 1
        # Constraint: x3 + x7 = x12 + 10 * c0
        if id_var in [3, 7, 12, 13]:
            for i in [3, 7, 12, 13]:
                if i == id_var:
                    continue
                if not self.variables[i].is_assigned and i not in counted:
                    degree += 1
                    counted.append(i)
        # Constraint: c0 + x2 + x6 = x11 + 14 + 10 * c1
        if id_var in [13, 2, 6, 11, 14]:
            for i in [13, 2, 6, 11, 14]:
                if i == id_var:
                    continue
                if not self.variables[i].is_assigned and i not in counted:
                    degree += 1
                    counted.append(i)
        # Constraint: c1 + x1 + x5 = x10 + 15 + 10 * c2
        if id_var in [14, 1, 5, 10, 15]:
            for i in [14, 1, 5, 10, 15]:
                if i == id_var:
                    continue
                if not self.variables[i].is_assigned and i not in counted:
                    degree += 1
                    counted.append(i)
        # Constraint: c2 + x0 + x4 = x4 + 9 + 10 * c3
        if id_var in [15, 0, 4, 9, 16]:
            for i in [15, 0, 4, 9, 16]:
                if i == id_var:
                    continue
                if not self.variables[i].is_assigned and i not in counted:
                    degree += 1
                    counted.append(i)
        # Constraint: c3 = x8
        if id_var in [16, 8]:
            for i in [16, 8]:
                if i == id_var:
                    continue
                if not self.variables[i].is_assigned and i not in counted:
                    degree += 1
                    counted.append(i)

        return degree

    def is_consistent(self, id_var, value, assignment):
        # Constraint: All letters must be different
        shared_letters = []

        if id_var in range(13):
            assigned_letters = []
            for i in range(13):
                if self.variables[i].letter == self.variables[id_var].letter:
                    shared_letters.append(i)
                if self.variables[i].letter not in assigned_letters and self.variables[i].is_assigned:
                    assigned_letters.append(self.variables[i].letter)

            for letter in assigned_letters:
                if assignment[letter] == value:
                    return False

        for index in shared_letters:
            # Constraint: x3 + x7 = x12 + 10 * c0
            constraint_list = [3, 7, 12, 13]
            if index in constraint_list:
                cl = constraint_list.copy()
                cl.remove(index)
                missing_assigned_var = False
                for i in cl:
                    if not self.variables[i].is_assigned:
                        missing_assigned_var = True
                        break

                if not missing_assigned_var:
                    x3, x7, x12, c0 = 0, 0, 0, 0

                    if index == 3:
                        x3 = value
                        x7 = assignment[self.variables[7].letter]
                        x12 = assignment[self.variables[12].letter]
                        c0 = assignment[self.variables[13].letter]
                    elif index == 7:
                        x7 = value
                        x3 = assignment[self.variables[3].letter]
                        x12 = assignment[self.variables[12].letter]
                        c0 = assignment[self.variables[13].letter]
                    elif index == 12:
                        x12 = value
                        x3 = assignment[self.variables[3].letter]
                        x7 = assignment[self.variables[7].letter]
                        c0 = assignment[self.variables[13].letter]
                    elif index == 13:
                        c0 = value
                        x3 = assignment[self.variables[3].letter]
                        x7 = assignment[self.variables[7].letter]
                        x12 = assignment[self.variables[12].letter]

                    if x3 + x7 != x12 + 10 * c0:
                        return False
            # Constraint: c0 + x2 + x6 = x11 + 10 * c1
            constraint_list = [13, 2, 6, 11, 14]
            if index in constraint_list:
                cl = constraint_list.copy()
                cl.remove(index)
                missing_assigned_var = False
                for i in cl:
                    if not self.variables[i].is_assigned:
                        missing_assigned_var = True
                        break

                if not missing_assigned_var:
                    c0, x2, x6, x11, c1 = 0, 0, 0, 0, 0

                    if index == 13:
                        c0 = value
                        x2 = assignment[self.variables[2].letter]
                        x6 = assignment[self.variables[6].letter]
                        x11 = assignment[self.variables[11].letter]
                        c1 = assignment[self.variables[14].letter]
                    elif index == 2:
                        x2 = value
                        c0 = assignment[self.variables[13].letter]
                        x6 = assignment[self.variables[6].letter]
                        x11 = assignment[self.variables[11].letter]
                        c1 = assignment[self.variables[14].letter]
                    elif index == 6:
                        x6 = value
                        x2 = assignment[self.variables[2].letter]
                        c0 = assignment[self.variables[13].letter]
                        x11 = assignment[self.variables[11].letter]
                        c1 = assignment[self.variables[14].letter]
                    elif index == 11:
                        x11 = value
                        x2 = assignment[self.variables[2].letter]
                        x6 = assignment[self.variables[6].letter]
                        c0 = assignment[self.variables[13].letter]
                        c1 = assignment[self.variables[14].letter]
                    elif index == 14:
                        c1 = value
                        x2 = assignment[self.variables[2].letter]
                        x6 = assignment[self.variables[6].letter]
                        x11 = assignment[self.variables[11].letter]
                        c0 = assignment[self.variables[13].letter]

                    if c0 + x2 + x6 != x11 + 10 * c1:
                        return False

            # Constraint: c1 + x1 + x5 = x10 + 10 * c2
            constraint_list = [14, 1, 5, 10, 15]
            if index in constraint_list:
                cl = constraint_list.copy()
                cl.remove(index)
                missing_assigned_var = False
                for i in cl:
                    if not self.variables[i].is_assigned:
                        missing_assigned_var = True
                        break

                if not missing_assigned_var:
                    c1, x1, x5, x10, c2 = 0, 0, 0, 0, 0

                    if index == 14:
                        c1 = value
                        x1 = assignment[self.variables[1].letter]
                        x5 = assignment[self.variables[5].letter]
                        x10 = assignment[self.variables[10].letter]
                        c2 = assignment[self.variables[15].letter]
                    elif index == 1:
                        x1 = value
                        c1 = assignment[self.variables[14].letter]
                        x5 = assignment[self.variables[5].letter]
                        x10 = assignment[self.variables[10].letter]
                        c2 = assignment[self.variables[15].letter]
                    elif index == 5:
                        x5 = value
                        x1 = assignment[self.variables[1].letter]
                        c1 = assignment[self.variables[14].letter]
                        x10 = assignment[self.variables[10].letter]
                        c2 = assignment[self.variables[15].letter]
                    elif index == 10:
                        x10 = value
                        x1 = assignment[self.variables[1].letter]
                        x5 = assignment[self.variables[5].letter]
                        c1 = assignment[self.variables[14].letter]
                        c2 = assignment[self.variables[15].letter]
                    elif index == 15:
                        c2 = value
                        x1 = assignment[self.variables[1].letter]
                        x5 = assignment[self.variables[5].letter]
                        x10 = assignment[self.variables[10].letter]
                        c1 = assignment[self.variables[14].letter]

                    if c1 + x1 + x5 != x10 + 10 * c2:
                        return False

            # Constraint: c2 + x0 + x4 = x9 + 10 * c3
            constraint_list = [15, 0, 4, 9, 16]
            if index in constraint_list:
                cl = constraint_list.copy()
                cl.remove(index)
                missing_assigned_var = False
                for i in cl:
                    if not self.variables[i].is_assigned:
                        missing_assigned_var = True
                        break

                if not missing_assigned_var:
                    c2, x0, x4, x9, c3 = 0, 0, 0, 0, 0

                    if index == 15:
                        c2 = value
                        x0 = assignment[self.variables[0].letter]
                        x4 = assignment[self.variables[4].letter]
                        x9 = assignment[self.variables[9].letter]
                        c3 = assignment[self.variables[16].letter]
                    elif index == 0:
                        x0 = value
                        c2 = assignment[self.variables[15].letter]
                        x4 = assignment[self.variables[4].letter]
                        x9 = assignment[self.variables[9].letter]
                        c3 = assignment[self.variables[16].letter]
                    elif index == 4:
                        x4 = value
                        x0 = assignment[self.variables[0].letter]
                        c2 = assignment[self.variables[15].letter]
                        x9 = assignment[self.variables[9].letter]
                        c3 = assignment[self.variables[16].letter]
                    elif index == 9:
                        x9 = value
                        x0 = assignment[self.variables[0].letter]
                        x4 = assignment[self.variables[4].letter]
                        c2 = assignment[self.variables[15].letter]
                        c3 = assignment[self.variables[16].letter]
                    elif index == 16:
                        c3 = value
                        x0 = assignment[self.variables[0].letter]
                        x4 = assignment[self.variables[4].letter]
                        x9 = assignment[self.variables[9].letter]
                        c2 = assignment[self.variables[15].letter]

                    if c2 + x0 + x4 != x9 + 10 * c3:
                        return False

            # Constraint: c3 = x8
            constraint_list = [16, 8]
            if index in constraint_list:
                cl = constraint_list.copy()
                cl.remove(index)
                missing_assigned_var = False
                for i in cl:
                    if not self.variables[i].is_assigned:
                        missing_assigned_var = True
                        break

                if not missing_assigned_var:
                    c3, x8 = 0, 0

                    if index == 16:
                        c3 = value
                        x8 = assignment[self.variables[8].letter]
                    elif index == 8:
                        x8 = value
                        c3 = assignment[self.variables[16].letter]

                    if c3 != x8:
                        return False
        return True

    def set_assigned(self, assigned_var):
        if assigned_var.id < 13:
            for i in range(13):
                if self.variables[i].letter == assigned_var.letter:
                    self.variables[i].is_assigned = True

        else:
            self.variables[assigned_var.id].is_assigned = True

    def set_unassigned(self, unassigned_var):
        if unassigned_var.id < 13:
            for i in range(13):
                if self.variables[i].letter == unassigned_var.letter:
                    self.variables[i].is_assigned = False

        else:
            self.variables[unassigned_var.id].is_assigned = False

    def update_domains(self, var, value, assignment):
        if var.id in range(13):
            for i in range(13):
                if self.variables[i].letter == var.letter or self.variables[i].is_assigned:
                    continue

                if value in self.domains[i]:
                    self.domains[i].remove(value)

        constraint_list = [3, 7, 12, 13]
        if var.id in constraint_list:
            cl = constraint_list.copy()
            cl.remove(var.id)
            unassigned_vars = 0
            var_to_assign = None
            for el in cl:
                if not self.variables[el].is_assigned:
                    unassigned_vars += 1
                    var_to_assign = self.variables[el]

            if unassigned_vars == 1:
                if var_to_assign.id == 3:
                    new_domain = self.domains[3].copy()
                    for val in self.domains[3]:
                        x3 = val
                        x7 = assignment[self.variables[7].letter]
                        x12 = assignment[self.variables[12].letter]
                        c0 = assignment[self.variables[13].letter]

                        if x3 + x7 != x12 + 10 * c0:
                            new_domain.remove(val)

                    self.domains[3] = new_domain

                elif var_to_assign.id == 7:
                    new_domain = self.domains[7].copy()
                    for val in self.domains[7]:
                        x7 = val
                        x3 = assignment[self.variables[3].letter]
                        x12 = assignment[self.variables[12].letter]
                        c0 = assignment[self.variables[13].letter]

                        if x3 + x7 != x12 + 10 * c0:
                            new_domain.remove(val)

                    self.domains[7] = new_domain
                elif var_to_assign.id == 12:
                    new_domain = self.domains[12].copy()
                    for val in self.domains[12]:
                        x12 = val
                        x3 = assignment[self.variables[3].letter]
                        x7 = assignment[self.variables[7].letter]
                        c0 = assignment[self.variables[13].letter]

                        if x3 + x7 != x12 + 10 * c0:
                            new_domain.remove(val)

                    self.domains[12] = new_domain
                elif var_to_assign.id == 13:
                    new_domain = self.domains[13].copy()
                    for val in self.domains[13]:
                        c0 = val
                        x3 = assignment[self.variables[3].letter]
                        x7 = assignment[self.variables[7].letter]
                        x12 = assignment[self.variables[12].letter]

                        if x3 + x7 != x12 + 10 * c0:
                            new_domain.remove(val)

                    self.domains[13] = new_domain

        constraint_list = [13, 2, 6, 11, 14]
        if var.id in constraint_list:
            cl = constraint_list.copy()
            cl.remove(var.id)
            unassigned_vars = 0
            var_to_assign = None
            for el in cl:
                if not self.variables[el].is_assigned:
                    unassigned_vars += 1
                    var_to_assign = self.variables[el]

            if unassigned_vars == 1:
                if var_to_assign.id == 13:
                    new_domain = self.domains[13].copy()
                    for val in self.domains[13]:
                        c0 = val
                        x2 = assignment[self.variables[2].letter]
                        x6 = assignment[self.variables[6].letter]
                        x11 = assignment[self.variables[11].letter]
                        c1 = assignment[self.variables[14].letter]

                        if c0 + x2 + x6 != x11 + 10 * c1:
                            new_domain.remove(val)

                    self.domains[13] = new_domain

                elif var_to_assign.id == 2:
                    new_domain = self.domains[2].copy()
                    for val in self.domains[2]:
                        x2 = val
                        c0 = assignment[self.variables[13].letter]
                        x6 = assignment[self.variables[6].letter]
                        x11 = assignment[self.variables[11].letter]
                        c1 = assignment[self.variables[14].letter]

                        if c0 + x2 + x6 != x11 + 10 * c1:
                            new_domain.remove(val)

                    self.domains[2] = new_domain
                elif var_to_assign.id == 6:
                    new_domain = self.domains[6].copy()
                    for val in self.domains[6]:
                        x6 = val
                        x2 = assignment[self.variables[2].letter]
                        c0 = assignment[self.variables[13].letter]
                        x11 = assignment[self.variables[11].letter]
                        c1 = assignment[self.variables[14].letter]

                        if c0 + x2 + x6 != x11 + 10 * c1:
                            new_domain.remove(val)

                    self.domains[6] = new_domain
                elif var_to_assign.id == 11:
                    new_domain = self.domains[11].copy()
                    for val in self.domains[11]:
                        x11 = val
                        x2 = assignment[self.variables[2].letter]
                        x6 = assignment[self.variables[6].letter]
                        c0 = assignment[self.variables[13].letter]
                        c1 = assignment[self.variables[14].letter]

                        if c0 + x2 + x6 != x11 + 10 * c1:
                            new_domain.remove(val)

                    self.domains[11] = new_domain
                elif var_to_assign.id == 14:
                    new_domain = self.domains[14].copy()
                    for val in self.domains[14]:
                        c1 = val
                        x2 = assignment[self.variables[2].letter]
                        x6 = assignment[self.variables[6].letter]
                        x11 = assignment[self.variables[11].letter]
                        c0 = assignment[self.variables[13].letter]

                        if c0 + x2 + x6 != x11 + 10 * c1:
                            new_domain.remove(val)

                    self.domains[14] = new_domain

        constraint_list = [14, 1, 5, 10, 15]
        if var.id in constraint_list:
            cl = constraint_list.copy()
            cl.remove(var.id)
            unassigned_vars = 0
            var_to_assign = None
            for el in cl:
                if not self.variables[el].is_assigned:
                    unassigned_vars += 1
                    var_to_assign = self.variables[el]

            if unassigned_vars == 1:
                if var_to_assign.id == 14:
                    new_domain = self.domains[14].copy()
                    for val in self.domains[14]:
                        c1 = val
                        x1 = assignment[self.variables[1].letter]
                        x5 = assignment[self.variables[5].letter]
                        x10 = assignment[self.variables[10].letter]
                        c2 = assignment[self.variables[15].letter]

                        if c1 + x1 + x5 != x10 + 10 * c2:
                            new_domain.remove(val)

                    self.domains[14] = new_domain
                elif var_to_assign.id == 1:
                    new_domain = self.domains[1].copy()
                    for val in self.domains[1]:
                        x1 = val
                        c1 = assignment[self.variables[14].letter]
                        x5 = assignment[self.variables[5].letter]
                        x10 = assignment[self.variables[10].letter]
                        c2 = assignment[self.variables[15].letter]

                        if c1 + x1 + x5 != x10 + 10 * c2:
                            new_domain.remove(val)

                    self.domains[1] = new_domain
                elif var_to_assign.id == 5:
                    new_domain = self.domains[5].copy()
                    for val in self.domains[5]:
                        x5 = val
                        x1 = assignment[self.variables[1].letter]
                        c1 = assignment[self.variables[14].letter]
                        x10 = assignment[self.variables[10].letter]
                        c2 = assignment[self.variables[15].letter]

                        if c1 + x1 + x5 != x10 + 10 * c2:
                            new_domain.remove(val)

                    self.domains[5] = new_domain
                elif var_to_assign.id == 10:
                    new_domain = self.domains[10].copy()
                    for val in self.domains[10]:
                        x10 = val
                        x1 = assignment[self.variables[1].letter]
                        x5 = assignment[self.variables[5].letter]
                        c1 = assignment[self.variables[14].letter]
                        c2 = assignment[self.variables[15].letter]

                        if c1 + x1 + x5 != x10 + 10 * c2:
                            new_domain.remove(val)

                    self.domains[10] = new_domain
                elif var_to_assign.id == 15:
                    new_domain = self.domains[15].copy()
                    for val in self.domains[15]:
                        c2 = val
                        x1 = assignment[self.variables[1].letter]
                        x5 = assignment[self.variables[5].letter]
                        x10 = assignment[self.variables[10].letter]
                        c1 = assignment[self.variables[14].letter]

                        if c1 + x1 + x5 != x10 + 10 * c2:
                            new_domain.remove(val)

                    self.domains[15] = new_domain

        constraint_list = [15, 0, 4, 9, 16]
        if var.id in constraint_list:
            cl = constraint_list.copy()
            cl.remove(var.id)
            unassigned_vars = 0
            var_to_assign = None
            for el in cl:
                if not self.variables[el].is_assigned:
                    unassigned_vars += 1
                    var_to_assign = self.variables[el]

            if unassigned_vars == 1:
                if var_to_assign.id == 15:
                    new_domain = self.domains[15].copy()
                    for val in self.domains[15]:
                        c2 = val
                        x0 = assignment[self.variables[0].letter]
                        x4 = assignment[self.variables[4].letter]
                        x9 = assignment[self.variables[9].letter]
                        c3 = assignment[self.variables[16].letter]

                        if c2 + x0 + x4 != x9 + 10 * c3:
                            new_domain.remove(val)

                    self.domains[15] = new_domain
                elif var_to_assign.id == 0:
                    new_domain = self.domains[0].copy()
                    for val in self.domains[0]:
                        x0 = val
                        c2 = assignment[self.variables[15].letter]
                        x4 = assignment[self.variables[4].letter]
                        x9 = assignment[self.variables[9].letter]
                        c3 = assignment[self.variables[16].letter]

                        if c2 + x0 + x4 != x9 + 10 * c3:
                            new_domain.remove(val)

                    self.domains[0] = new_domain
                elif var_to_assign.id == 4:
                    new_domain = self.domains[4].copy()
                    for val in self.domains[4]:
                        x4 = val
                        x0 = assignment[self.variables[0].letter]
                        c2 = assignment[self.variables[15].letter]
                        x9 = assignment[self.variables[9].letter]
                        c3 = assignment[self.variables[16].letter]

                        if c2 + x0 + x4 != x9 + 10 * c3:
                            new_domain.remove(val)

                    self.domains[4] = new_domain
                elif var_to_assign.id == 9:
                    new_domain = self.domains[9].copy()
                    for val in self.domains[9]:
                        x9 = val
                        x0 = assignment[self.variables[0].letter]
                        x4 = assignment[self.variables[4].letter]
                        c2 = assignment[self.variables[15].letter]
                        c3 = assignment[self.variables[16].letter]

                        if c2 + x0 + x4 != x9 + 10 * c3:
                            new_domain.remove(val)

                    self.domains[9] = new_domain
                elif var_to_assign.id == 16:
                    new_domain = self.domains[16].copy()
                    for val in self.domains[16]:
                        c3 = val
                        x0 = assignment[self.variables[0].letter]
                        x4 = assignment[self.variables[4].letter]
                        x9 = assignment[self.variables[9].letter]
                        c2 = assignment[self.variables[15].letter]

                        if c2 + x0 + x4 != x9 + 10 * c3:
                            new_domain.remove(val)

                    self.domains[16] = new_domain

        constraint_list = [16, 8]
        if var.id in constraint_list:
            cl = constraint_list.copy()
            cl.remove(var.id)
            unassigned_vars = 0
            var_to_assign = None
            for el in cl:
                if not self.variables[el].is_assigned:
                    unassigned_vars += 1
                    var_to_assign = self.variables[el]

            if unassigned_vars == 1:
                if var_to_assign.id == 16:
                    new_domain = self.domains[16].copy()
                    for val in self.domains[16]:
                        c3 = val
                        x8 = assignment[self.variables[8].letter]

                        if c3 != x8:
                            new_domain.remove(val)

                    self.domains[16] = new_domain
                elif var_to_assign.id == 8:
                    new_domain = self.domains[8].copy()
                    for val in self.domains[8]:
                        x8 = val
                        c3 = assignment[self.variables[16].letter]

                        if c3 != x8:
                            new_domain.remove(val)

                    self.domains[8] = new_domain
