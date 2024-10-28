# Import packages
import pandas as pd
import gurobipy as gp
from gurobipy import GRB

# DATA

max_points = 336
decathlon_card_points = [6,11,16,22,27,53,79,84,94,105,131,157]

# MODEL
m = gp.Model('cards')

# vars
decathlon_nb_cards = m.addVars(decathlon_card_points, vtype=GRB.INTEGER, name = "decathlon_card_points")
# decathlon_total_per_card = m.addVars(decathlon_card_points, vtype=GRB.INTEGER, name = "decathlon_card_points")

# constraints
# decathlon_max_points_per_card = m.addConstrs((v * decathlon_nb_cards[v] == decathlon_total_per_card[v] for v in decathlon_card_points), name = "max_points_per_card")
# decathlon_max_points = m.addConstr((decathlon_total_per_card.sum() == max_points), name = "max_points")
card_total = gp.quicksum(p*decathlon_nb_cards[p] for p in decathlon_card_points)
m.addConstr(card_total == max_points, name = "card_total")

m.update()

# m.setObjective(gp.quicksum(total_per_card[v] for v in card_points), GRB.MAXIMIZE)
m.setObjective(decathlon_nb_cards.sum(), GRB.MINIMIZE)

m.write('card_numbers.lp')

m.optimize()

x_values = pd.Series(m.getAttr('X', decathlon_nb_cards), name = "nb_cards", index = decathlon_card_points)
print(x_values)

# Solution => 2*131 + 2*22