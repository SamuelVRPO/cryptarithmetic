# This class is used for all the variables, it contains:
# - ID: index in variables list in CSP
# - Letter: corresponding letter
# - Is_assigned: flag to show variable is assigned a value in the assignment
class Variable:
    def __init__(self, letter, iden):
        self.letter = letter
        self.id = iden
        self.is_assigned = False

    def __lt__(self, other):
        return False

    def __le__(self, other):
        return False
