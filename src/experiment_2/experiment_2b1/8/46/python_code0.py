import pulp
import json

# Input data
data = {'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 
        'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 
        'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}

# Parameters
A = len(data['available'])  # Number of alloys
S = len(data['steel_prices'])  # Number of steel types

# Create problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", 
                                       ((a, s) for a in range(A) for s in range(S)), 
                                       lowBound=0)

total_steel = pulp.LpVariable.dicts("total_steel", 
                                     (s for s in range(S)), 
                                     lowBound=0)

# Objective function
profit = pulp.lpSum(data['steel_prices'][s] * total_steel[s] - 
                    pulp.lpSum(data['alloy_prices'][a] * alloy_amount[a, s] for a in range(A)) 
                    for s in range(S))

problem += profit

# Constraints
# Carbon and Nickel constraints
for s in range(S):
    problem += pulp.lpSum(data['carbon'][a] * alloy_amount[a, s] for a in range(A)) >= data['carbon_min'][s] * total_steel[s]
    problem += pulp.lpSum(data['nickel'][a] * alloy_amount[a, s] for a in range(A)) <= data['nickel_max'][s] * total_steel[s]

# Alloy availability constraints
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a, s] for s in range(S)) <= data['available'][a]

# Alloy 1 production limit
problem += pulp.lpSum(alloy_amount[0, s] for s in range(S)) <= 0.4 * pulp.lpSum(total_steel[s] for s in range(S))

# Solve problem
problem.solve()

# Extract results
alloy_use = [[pulp.value(alloy_amount[a, s]) for a in range(A)] for s in range(S)]
total_steel_values = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

# Output result
result = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_values,
    "total_profit": total_profit
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')