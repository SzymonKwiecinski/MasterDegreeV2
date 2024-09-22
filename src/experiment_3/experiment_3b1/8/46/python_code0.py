import pulp
import json

# Data
data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

# Parameters
A = len(available)
S = len(steel_prices)

# Create the problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(A), range(S)), lowBound=0, cat='Continuous')  # Amount of alloy a used in steel s
y = pulp.LpVariable.dicts("y", range(S), lowBound=0, cat='Continuous')  # Total amount of steel s produced

# Objective Function
problem += pulp.lpSum(steel_prices[s] * y[s] for s in range(S)) - pulp.lpSum(alloy_prices[a] * x[a][s] for a in range(A) for s in range(S))

# Constraints
# Steel Production Constraint
for s in range(S):
    problem += pulp.lpSum(x[a][s] for a in range(A)) == y[s]

# Alloy Availability Constraint
for a in range(A):
    problem += pulp.lpSum(x[a][s] for s in range(S)) <= available[a]

# Carbon Requirement
for s in range(S):
    problem += pulp.lpSum(x[a][s] * carbon[a] for a in range(A)) >= carbon_min[s] * y[s]

# Nickel Constraint
for s in range(S):
    problem += pulp.lpSum(x[a][s] * nickel[a] for a in range(A)) <= nickel_max[s] * y[s]

# Alloy 1 Constraint
for s in range(S):
    problem += x[0][s] <= 0.4 * y[s]

# Solve the problem
problem.solve()

# Output the results
alloy_use = [[pulp.value(x[a][s]) for s in range(S)] for a in range(A)]
total_steel = [pulp.value(y[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

print(f" (Objective Value): <OBJ>{total_profit}</OBJ>")