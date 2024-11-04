
import gurobipy as gp
import pandas as pd
from gurobipy import GRB

# DATA
# load or import data

categories, minNutrition, maxNutrition = gp.multidict({
    'calories': [1800, 2200],
    'proteins': [91, GRB.INFINITY],
    'fat': [0, 65],
    'sodium': [0, 1779],
})

foods, cost = gp.multidict({
    'hamburger': 2.49,
    'chicken': 2.89,
    'hot_dog': 1.50,
    'fries': 1.89,
    'macaroni': 2.09,
    'pizza': 1.99,
    'salad': 2.49,
    'milk': 0.89,
    'ice_cream': 1.59
})

nutrition = pd.read_csv('data/nutritionValues.csv', index_col=[0,1]).squeeze('columns')
# nutrition = nutrition.to_dict()

def solve(categories, minNutrition, maxNutrition, foods, cost, nutritionValues):

    # MODEL
    # build our model

    # define a model object
    m = gp.Model('diet')

    # introduce the vars
    buy = m.addVars(foods, name="buy")

    # define the objective
    # totalCost = gp.quicksum(cost[f] * buy[f] for f in foods)
    # m.setObjective(totalCost, GRB.MINIMIZE)
    m.setObjective(buy.prod(cost), GRB.MINIMIZE)

    # define the constraints
    # for c in categories:
    #     categoryTotal = gp.quicksum(buy[f] * nutritionValues[f, c] for f in foods)
    #     m.addConstr(minNutrition[c] <= categoryTotal, name="total_"+c+"_min")
    #     m.addConstr(maxNutrition[c] >= categoryTotal, name="total_"+c+"_max")
    m.addConstrs((gp.quicksum(buy[f] * nutritionValues[f, c] for f in foods) ==
                  [minNutrition[c], maxNutrition[c]] for c in categories), name="nutrition_req")

    def print_solution():
        if m.status == GRB.OPTIMAL:
            sol = pd.Series(m.getAttr("X", buy), name = "food_bought", index = foods)
            print(sol[sol > 0])

            nutrition = {}
            print(f"\nCost: {round(m.ObjVal, 4)}")
            print("\nBuy:")
            for f in foods:
                print(f"\t{f}: {round(buy[f].x, 4)}")
            print("\nNutrition values:")
            for c in categories:
                nutrition[c] = sum(buy[f].x * nutritionValues[f, c]
                                   for f in foods)
                print(f"\t{c}: {round(nutrition[c], 4)}")
        else:
            print("No solution")

    # optionally, write out the model to a disc
    m.write('dietTest.lp')

    # SOLVE & POSTPROCESS
    # optimize
    m.optimize()

    print_solution()


solve(categories, minNutrition, maxNutrition, foods, cost, nutrition)


# CHANGE DATA and solve again
categories, minNutrition, maxNutrition = gp.multidict({
    'calories': [1500, 1800],
    'proteins': [100, GRB.INFINITY],
    'fat': [0, 65],
    'sodium': [0, 1779],
})

solve(categories, minNutrition, maxNutrition, foods, cost, nutrition)