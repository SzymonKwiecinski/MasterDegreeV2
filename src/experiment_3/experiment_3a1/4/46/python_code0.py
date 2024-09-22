import pulp
import json

# Data input
data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')

# Number of alloys and steel types
A = len(data['available'])
S = len(data['steel_prices'])

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", [(a, s) for a in range(A) for s in range(S)], lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", range(S), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(y[s] * data['steel_prices'][s] for s in range(S)) - \
           pulp.lpSum(x[(a, s)] * data['alloy_prices'][a] for a in range(A) for s in range(S)), "Total_Profit"

# Constraints
# Alloy availability constraints
for a in range(A):
    problem += pulp.lpSum(x[(a, s)] for s in range(S)) <= data['available'][a], f"Available_Alloy_{a}"

# Carbon content constraint for each steel type
for s in range(S):
    problem += pulp.lpSum(x[(a, s)] * (data['carbon'][a] / 100) for a in range(A)) >= data['carbon_min'][s] * y[s], f"Carbon_Content_{s}"

# Nickel content constraint for each steel type
for s in range(S):
    problem += pulp.lpSum(x[(a, s)] * (data['nickel'][a] / 100) for a in range(A)) <= data['nickel_max'][s] * y[s], f"Nickel_Content_{s}"

# Maximum alloy usage constraint
for s in range(S):
    problem += pulp.lpSum(x[(0, s)]) <= 0.4 * y[s], f"Max_Alloy_Usage_{s}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')