import pulp
import json

# Input Data
data = {'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

# Define the problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Define variables
S = len(steel_prices)
A = len(available)
alloy_amount = pulp.LpVariable.dicts("alloy_amount", ((a, s) for a in range(A) for s in range(S)), lowBound=0)
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0)

# Objective function
total_profit = pulp.lpSum((steel_prices[s] * total_steel[s]) - (pulp.lpSum(alloy_prices[a] * alloy_amount[(a, s)] for a in range(A)) for s in range(S)))
problem += total_profit

# Constraints for alloy usage
for a in range(A):
    problem += pulp.lpSum(alloy_amount[(a, s)] for s in range(S)) <= available[a]

# Carbon and Nickel content constraints for each steel
for s in range(S):
    problem += (pulp.lpSum(carbon[a] * (alloy_amount[(a, s)] / total_steel[s]) for a in range(A)) >= carbon_min[s])
    problem += (pulp.lpSum(nickel[a] * (alloy_amount[(a, s)] / total_steel[s]) for a in range(A)) <= nickel_max[s])

# Total steel production
for s in range(S):
    problem += pulp.lpSum(alloy_amount[(a, s)] for a in range(A)) == total_steel[s]

# Additional constraint for Alloy 1
problem += pulp.lpSum(alloy_amount[(0, s)] for s in range(S)) <= 0.4 * pulp.lpSum(total_steel[s] for s in range(S))

# Solve the problem
problem.solve()

# Collecting results
alloy_use = [[pulp.value(alloy_amount[(a, s)]) for a in range(A)] for s in range(S)]
total_steel_results = [pulp.value(total_steel[s]) for s in range(S)]
total_profit_value = pulp.value(problem.objective)

# Output results
output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_results,
    "total_profit": total_profit_value
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')