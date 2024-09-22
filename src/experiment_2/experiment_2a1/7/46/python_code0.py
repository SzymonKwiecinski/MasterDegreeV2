import pulp
import json

# Input data
data = {'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

# Define the problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Variables
S = len(steel_prices)
A = len(alloy_prices)

# Amount of each alloy used in each type of steel
alloy_use = pulp.LpVariable.dicts("alloy_amount", (range(A), range(S)), lowBound=0)

# Total amount of steel produced
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0)

# Objective function
profit = pulp.lpSum([(total_steel[s] * steel_prices[s]) for s in range(S)]) - pulp.lpSum([(alloy_use[a][s] * alloy_prices[a]) for a in range(A) for s in range(S)])
problem += profit

# Constraints
# Each alloy's availability
for a in range(A):
    problem += pulp.lpSum([alloy_use[a][s] for s in range(S)]) <= available[a], f"Available_Alloy_{a}"

# Carbon percentage constraints
for s in range(S):
    problem += pulp.lpSum([alloy_use[a][s] * carbon[a] for a in range(A)]) >= total_steel[s] * carbon_min[s], f"Carbon_Min_{s}"

# Nickel percentage constraints
for s in range(S):
    problem += pulp.lpSum([alloy_use[a][s] * nickel[a] for a in range(A)]) <= total_steel[s] * nickel_max[s], f"Nickel_Max_{s}"

# Alloy 1 maximum usage constraint
for s in range(S):
    problem += alloy_use[0][s] <= 0.4 * total_steel[s], f"Max_Alloy1_Usage_{s}"

# Solve the problem
problem.solve()

# Prepare the output
alloy_amounts = [[pulp.value(alloy_use[a][s]) for a in range(A)] for s in range(S)]
total_steel_values = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

# Output result
result = {
    "alloy_use": alloy_amounts,
    "total_steel": total_steel_values,
    "total_profit": total_profit
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')