import pulp
import json

# Load data
data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')

# Constants
A = len(data['available'])  # Number of alloys
S = len(data['steel_prices'])  # Number of steel types

# Create a linear programming problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(A), range(S)), lowBound=0)  # amount of alloy a in steel s
y = pulp.LpVariable.dicts("y", range(S), lowBound=0)  # amount of steel s produced

# Objective Function
problem += pulp.lpSum(data['steel_prices'][s] * y[s] for s in range(S)) - \
           pulp.lpSum(data['alloy_prices'][a] * pulp.lpSum(x[a][s] for s in range(S)) for a in range(A))

# Constraints

# Alloy Availability Constraints
for a in range(A):
    problem += pulp.lpSum(x[a][s] for s in range(S)) <= data['available'][a]

# Carbon Content Constraints
for s in range(S):
    problem += (pulp.lpSum(data['carbon'][a] * x[a][s] for a in range(A)) >= data['carbon_min'][s] * y[s]) 

# Nickel Content Constraints
for s in range(S):
    problem += (pulp.lpSum(data['nickel'][a] * x[a][s] for a in range(A)) <= data['nickel_max'][s] * y[s])

# Alloy 1 Constraint
problem += pulp.lpSum(x[0][s] for s in range(S)) <= 0.4 * pulp.lpSum(y[s] for s in range(S))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')