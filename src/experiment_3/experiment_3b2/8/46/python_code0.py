import pulp
import json

# Data input
data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')

# Constants
S = len(data['steel_prices'])  # number of steel types
A = len(data['available'])      # number of alloys

# Create the problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(A), range(S)), lowBound=0)  # Amount of each alloy for each steel type
y = pulp.LpVariable.dicts("y", range(S), lowBound=0)               # Amount of each steel type produced

# Objective Function
problem += pulp.lpSum(data['steel_prices'][s] * y[s] for s in range(S)) - pulp.lpSum(data['alloy_prices'][a] * x[a][s] for a in range(A) for s in range(S))

# Constraints
# Alloy availability
for a in range(A):
    problem += pulp.lpSum(x[a][s] for s in range(S)) <= data['available'][a]

# Steel production
for s in range(S):
    problem += pulp.lpSum(x[a][s] for a in range(A)) == y[s]

# Carbon requirement
for s in range(S):
    problem += pulp.lpSum(data['carbon'][a] / 100 * x[a][s] for a in range(A)) >= data['carbon_min'][s] * y[s]

# Nickel constraint
for s in range(S):
    problem += pulp.lpSum(data['nickel'][a] / 100 * x[a][s] for a in range(A)) <= data['nickel_max'][s] * y[s]

# Alloy 1 constraint
for s in range(S):
    problem += x[0][s] <= 0.4 * y[s]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')