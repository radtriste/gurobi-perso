# Import packages
import pandas as pd
import gurobipy as gp
from gurobipy import GRB

# DATA

max_value = 336
cards = [5,10,15,20,25,50,75,80,90,100,125,150]
card_values = pd.read_csv('data/card_values.csv', index_col=[0]).squeeze('columns')


def solve(max_value, cards, card_values):

    # MODEL
    m = gp.Model('cards')

    # vars
    nb_cards = m.addVars(cards, vtype=GRB.INTEGER, name = "nb_cards")

    # constraints
    card_total = gp.quicksum(card_values[c]*nb_cards[c] for c in cards)
    m.addConstr(card_total == max_value, name = "total_value")

    m.update()

    m.setObjective(nb_cards.sum(), GRB.MINIMIZE)

    def print_solution():
        if m.status == GRB.OPTIMAL:
            sol = pd.Series(m.getAttr("X", nb_cards), name = "buy_nb_cards", index = cards)
            print(sol[sol > 0])
        else:
            print("No solution")

    # optionally, write out the model to a disc
    m.write('output/card_numbers.lp')

    # SOLVE & POSTPROCESS
    # optimize
    m.optimize()

    print_solution()



solve(max_value, cards, card_values) # Solution => 2*125 + 1*75