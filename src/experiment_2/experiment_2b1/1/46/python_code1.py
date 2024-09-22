import pulp
import json

data = {'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}

# Parameters from the input data
available = data['available']
carbon = data['carbon']
nickel = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

A = len(available)  # Number of alloys
S = len(steel_prices)  # Number of steel types

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", (range(A), range(S)), lowBound=0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
profit = pulp.lpSum(
    [(steel_prices[s] * total_steel[s] - pulp.lpSum(alloy_amount[a][s] * alloy_prices[a] for a in range(A))) for s in range(S)]
)
problem += pulp.lpSum(profit)

# Constraints for each type of steel
for s in range(S):
    problem += pulp.lpSum(alloy_amount[a][s] for a in range(A)) == total_steel[s]  # Total steel produced
    for a in range(A):
        problem += alloy_amount[a][s] <= available[a]  # Cannot use more than available

# Carbon and nickel constraints
for s in range(S):
    problem += pulp.lpSum(alloy_amount[a][s] * carbon[a] for a in range(A)) >= carbon_min[s] * total_steel[s]  # Carbon min constraint
    problem += pulp.lpSum(alloy_amount[a][s] * nickel[a] for a in range(A)) <= nickel_max[s] * total_steel[s]  # Nickel max constraint

# Constraint for alloy 1 usage
for s in range(S):
    problem += alloy_amount[0][s] <= 0.4 * total_steel[s]  # At most 40% of alloy 1

# Solve the problem
problem.solve()

# Extracting results
alloy_use = [[pulp.value(alloy_amount[a][s]) for a in range(A)] for s in range(S)]
total_steel_output = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

# Final results
results = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_output,
    "total_profit": total_profit
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')