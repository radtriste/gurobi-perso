
import gurobipy as gp

# DATA
# load or import data

categories = {
    'calories',
    'proteins'
}

minNutrition = {
    'calories': 1800,
    'proteins': 91
}

maxNutrition = {
    'calories': 2200,
    'proteins': gp.GRB.INFINITY
}

foods = {
    'salad',
    'ice_cream'
}

cost = {
    'salad': 2.49,
    'ice_cream': 1.59
}

nutritionValues = {
    ('salad', 'calories'): 320,
    ('salad', 'proteins'): 21,
    ('ice_cream', 'calories'): 330,
    ('ice_cream', 'proteins'): 8,
}

# MODEL
# build our model

# define a model object
m = gp.Model('diet')

# introduce the vars
buy = m.addVars(foods, name="buy")

# define the objective
totalCost = gp.quicksum(cost[f] * buy[f] for f in foods)
m.setObjective(totalCost, gp.GRB.MINIMIZE)

# define the constraints
for c in categories:
    categoryTotal = gp.quicksum(buy[f] * nutritionValues[f, c] for f in foods)
    m.addConstr(minNutrition[c] <= categoryTotal, name="total_"+c+"_min")
    m.addConstr(maxNutrition[c] >= categoryTotal, name="total_"+c+"_max")

# optionally, write out the model to a disc
m.write('dietTest.lp')

# SOLVE & POSTPROCESS
# optimize
m.optimize()

# review the results
for f in foods:
    print("purchase {0} units of {1}".format(buy[f].x, f))