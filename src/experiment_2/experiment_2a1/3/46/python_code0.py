import pulp
import json

# Input data
data = {'available': [40, 50, 80], 
        'carbon': [3, 4, 3.5], 
        'nickel': [1, 1.5, 1.8], 
        'alloy_prices': [380, 400, 440], 
        'steel_prices': [650, 600], 
        'carbon_min': [3.6, 3.4], 
        'nickel_max': [1.5, 1.7]}

# Problem parameters
A = len(data['available'])  # Number of alloys
S = len(data['steel_prices'])  # Number of steel types

# Create a linear programming problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", 
                                       (range(A), range(S)), 
                                       lowBound=0, 
                                       cat='Continuous')
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
problem += pulp.lpSum(data['steel_prices'][s] * total_steel[s] for s in range(S)) - \
            pulp.lpSum(data['alloy_prices'][a] * pulp.lpSum(alloy_amount[a][s] for s in range(S)) for a in range(A))

# Constraints
# Alloy availability
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a][s] for s in range(S)) <= data['available'][a]

# Carbon content constraint
for s in range(S):
    problem += pulp.lpSum(alloy_amount[a][s] * data['carbon'][a] for a in range(A)) >= total_steel[s] * data['carbon_min'][s]

# Nickel content constraint
for s in range(S):
    problem += pulp.lpSum(alloy_amount[a][s] * data['nickel'][a] for a in range(A)) <= total_steel[s] * data['nickel_max'][s]

# Limit on the amount of alloy 1
for s in range(S):
    problem += alloy_amount[0][s] <= 0.4 * total_steel[s]

# Total steel production from alloys
for s in range(S):
    problem += total_steel[s] == pulp.lpSum(alloy_amount[a][s] for a in range(A))

# Solve the problem
problem.solve()

# Prepare output
alloy_use = [[pulp.value(alloy_amount[a][s]) for a in range(A)] for s in range(S)]
total_steel_output = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

# Print results
output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_output,
    "total_profit": total_profit
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')