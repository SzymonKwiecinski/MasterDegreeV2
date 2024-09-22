import pulp
import json

# Load data from the provided JSON format
data = json.loads('{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}')

# Parameters
A = len(data['available'])  # Number of alloys
S = len(data['steel_prices'])  # Number of steel types

# Create the problem variable
problem = pulp.LpProblem("Maximize_Steel_Production", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(A), range(S)), lowBound=0)  # Alloy usage in steel production
y = pulp.LpVariable.dicts("y", range(S), lowBound=0)  # Amount of steel produced

# Objective Function
profit = pulp.lpSum([y[s] * data['steel_prices'][s] for s in range(S)]) - \
         pulp.lpSum([pulp.lpSum([x[a][s] * data['alloy_prices'][a] for s in range(S)]) for a in range(A)])

problem += profit, "Total_Profit"

# Constraints
# 1. Alloy availability
for a in range(A):
    problem += pulp.lpSum([x[a][s] for s in range(S)]) <= data['available'][a], f"Available_Alloy_{a}"

# 2. Carbon requirement
for s in range(S):
    problem += pulp.lpSum([x[a][s] * data['carbon'][a] for a in range(A)]) >= data['carbon_min'][s] * y[s], f"Carbon_Min_{s}"

# 3. Nickel limit
for s in range(S):
    problem += pulp.lpSum([x[a][s] * data['nickel'][a] for a in range(A)]) <= data['nickel_max'][s] * y[s], f"Nickel_Max_{s}"

# 4. Alloy 1 usage limit for all steel types
for s in range(S):
    problem += x[0][s] <= 0.4 * y[s], f"Alloy_1_Usage_Limit_{s}"

# Solve the problem
problem.solve()

# Output results
for a in range(A):
    for s in range(S):
        print(f"x[{a},{s}] = {x[a][s].varValue}")

for s in range(S):
    print(f"y[{s}] = {y[s].varValue}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')