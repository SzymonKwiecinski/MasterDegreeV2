import pulp
import json

# Data provided
data_json = '{"available": [40, 50, 80], "carbon": [3, 4, 3.5], "nickel": [1, 1.5, 1.8], "alloy_prices": [380, 400, 440], "steel_prices": [650, 600], "carbon_min": [3.6, 3.4], "nickel_max": [1.5, 1.7]}'
data = json.loads(data_json)

# Sets
A = range(len(data['available']))  # Alloys
S = range(len(data['steel_prices']))  # Steel types

# Create the linear programming problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (A, S), lowBound=0)  # Amount of alloy a used in steel type s
y = pulp.LpVariable.dicts("y", S, lowBound=0)       # Total amount of steel type s produced

# Objective Function
total_profit = pulp.lpSum(data['steel_prices'][s] * y[s] - pulp.lpSum(data['alloy_prices'][a] * x[a][s] for a in A) for s in S)
problem += total_profit, "Total_Profit"

# Constraints
# Alloy availability
for a in A:
    problem += pulp.lpSum(x[a][s] for s in S) <= data['available'][a], f"Alloy_Availability_{a}"

# Carbon requirement
for s in S:
    problem += (pulp.lpSum(x[a][s] * data['carbon'][a] for a in A) / y[s] >= data['carbon_min'][s]), f"Carbon_Requirement_{s}"

# Nickel limit
for s in S:
    problem += (pulp.lpSum(x[a][s] * data['nickel'][a] for a in A) / y[s] <= data['nickel_max'][s]), f"Nickel_Limit_{s}"

# Alloy 1 constraint
problem += (pulp.lpSum(x[0][s] for s in S) <= 0.4 * pulp.lpSum(y[s] for s in S)), "Alloy_1_Constraint"

# Solve the problem
problem.solve()

# Output results
alloy_use = [[pulp.value(x[a][s]) for s in S] for a in A]
total_steel = [pulp.value(y[s]) for s in S]
total_profit_value = pulp.value(problem.objective)

print(f'Alloy Use: {alloy_use}')
print(f'Total Steel Produced: {total_steel}')
print(f'(Objective Value): <OBJ>{total_profit_value}</OBJ>')