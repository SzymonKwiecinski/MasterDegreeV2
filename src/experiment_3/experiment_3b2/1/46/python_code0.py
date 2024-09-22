import pulp
import json

data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Parameters
S = len(data['steel_prices'])  # Number of steel types
A = len(data['alloy_prices'])  # Number of alloy types

# Decision Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", ((a, s) for a in range(A) for s in range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['steel_prices'][s] * total_steel[s] for s in range(S)) - \
           pulp.lpSum(data['alloy_prices'][a] * alloy_amount[(a, s)] for a in range(A) for s in range(S))

# Constraints

# Alloy Availability
for a in range(A):
    problem += pulp.lpSum(alloy_amount[(a, s)] for s in range(S)) <= data['available'][a]

# Steel Production
for s in range(S):
    problem += total_steel[s] == pulp.lpSum(alloy_amount[(a, s)] for a in range(A))

# Carbon Content
for s in range(S):
    problem += pulp.lpSum(data['carbon'][a] * alloy_amount[(a, s)] for a in range(A)) >= data['carbon_min'][s] * total_steel[s]

# Nickel Content
for s in range(S):
    problem += pulp.lpSum(data['nickel'][a] * alloy_amount[(a, s)] for a in range(A)) <= data['nickel_max'][s] * total_steel[s]

# Alloy 1 Usage
for s in range(S):
    problem += alloy_amount[(0, s)] <= 0.4 * total_steel[s]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')