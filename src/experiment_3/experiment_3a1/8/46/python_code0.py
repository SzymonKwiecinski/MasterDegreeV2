import pulp
import json

# Input data
data_json = '{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}'
data = json.loads(data_json)

# Define parameters
A = len(data['available'])  # Number of alloys
S = len(data['steel_prices'])  # Number of steel types

# Create the problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Variables
x = pulp.LpVariable.dicts("x", ((a, s) for a in range(A) for s in range(S)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", range(S), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(y[s] * data['steel_prices'][s] for s in range(S)) - pulp.lpSum(x[a, s] * data['alloy_prices'][a] for a in range(A) for s in range(S))
problem += profit, "Total_Profit"

# Constraints
# Material availability
for a in range(A):
    problem += pulp.lpSum(x[a, s] for s in range(S)) <= data['available'][a], f"Material_Availability_{a}"

# Carbon requirements for each steel type
for s in range(S):
    problem += pulp.lpSum(x[a, s] * (data['carbon'][a] / 100) for a in range(A)) >= data['carbon_min'][s] * y[s], f"Carbon_Requirement_{s}"

# Nickel limitations for each steel type
for s in range(S):
    problem += pulp.lpSum(x[a, s] * (data['nickel'][a] / 100) for a in range(A)) <= data['nickel_max'][s] * y[s], f"Nickel_Limitation_{s}"

# Maximum alloy usage constraint
problem += pulp.lpSum(x[0, s] for s in range(S)) <= 0.4 * pulp.lpSum(y[s] for s in range(S)), "Max_Alloy_Usage"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')