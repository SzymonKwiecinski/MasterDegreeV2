import pulp
import json

# Input data
data = {'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 
        'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 
        'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}

# Extract data
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

A = len(available)  # Number of alloys
S = len(steel_prices)  # Number of steel types

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
alloy_use = pulp.LpVariable.dicts("alloy_use", (range(A), range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0)

# Objective Function
profit = pulp.lpSum((steel_prices[s] * total_steel[s] - pulp.lpSum(alloy_prices[a] * alloy_use[a][s] for a in range(A))) for s in range(S))
problem += profit

# Constraints
# Alloy availability constraints
for a in range(A):
    problem += pulp.lpSum(alloy_use[a][s] for s in range(S)) <= available[a]

# Carbon content and Nickel maximum constraints for each steel type
for s in range(S):
    problem += pulp.lpSum((carbon[a] * alloy_use[a][s] for a in range(A))) >= carbon_min[s] * total_steel[s]
    problem += pulp.lpSum((nickel[a] * alloy_use[a][s] for a in range(A))) <= nickel_max[s] * total_steel[s]

# Maximum allowable percentage of alloy 1
for s in range(S):
    problem += alloy_use[0][s] <= 0.4 * total_steel[s]

# Solve the problem
problem.solve()

# Results
alloy_amount = [[pulp.value(alloy_use[a][s]) for a in range(A)] for s in range(S)]
total_steel_amount = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

# Output
result = {
    "alloy_use": alloy_amount,
    "total_steel": total_steel_amount,
    "total_profit": total_profit
}

print(result)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')