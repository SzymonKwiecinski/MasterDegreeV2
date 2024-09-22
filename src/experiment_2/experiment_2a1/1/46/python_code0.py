import pulp
import json

# Input data
data = {'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 
        'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 
        'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 
        'nickel_max': [1.5, 1.7]}

available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

A = len(available)  # Number of alloys
S = len(steel_prices)  # Number of steel types

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", (range(S), range(A)), lowBound=0)
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0)

# Objective function
profit = pulp.lpSum((total_steel[s] * steel_prices[s]) - 
                    pulp.lpSum(alloy_amount[s][a] * alloy_prices[a] for a in range(A)) for s in range(S))
problem += profit

# Constraints
# Total alloy usage for each steel must not exceed available amount
for a in range(A):
    problem += pulp.lpSum(alloy_amount[s][a] for s in range(S)) <= available[a]

# Carbon and nickel constraints for each type of steel
for s in range(S):
    problem += (pulp.lpSum(alloy_amount[s][a] * carbon[a] for a in range(A)) / 
                 total_steel[s]) >= carbon_min[s]
    problem += (pulp.lpSum(alloy_amount[s][a] * nickel[a] for a in range(A)) / 
                 total_steel[s]) <= nickel_max[s]

# Additional constraint for alloy usage
for s in range(S):
    problem += pulp.lpSum(alloy_amount[s][0] for s in range(S)) <= 0.4 * total_steel[s]

# Solve the problem
problem.solve()

# Prepare output
alloy_use = [[pulp.value(alloy_amount[s][a]) for a in range(A)] for s in range(S)]
total_steel_output = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

# Print objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')

# Output formatted
output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_output,
    "total_profit": total_profit
}

print(json.dumps(output, indent=4))