import pulp
import json

data = {'available': [40, 50, 80], 
        'carbon': [3, 4, 3.5], 
        'nickel': [1, 1.5, 1.8], 
        'alloy_prices': [380, 400, 440], 
        'steel_prices': [650, 600], 
        'carbon_min': [3.6, 3.4], 
        'nickel_max': [1.5, 1.7]}

# Define the data
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
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

# Decision variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", 
                                       ((a, s) for a in range(A) for s in range(S)), 
                                       lowBound=0)  # Amount of alloy a used in steel s

total_steel = pulp.LpVariable.dicts("total_steel", 
                                     range(S), 
                                     lowBound=0)  # Total amount of steel type s produced

# Objective function: Maximize total profit
profit = pulp.lpSum((steel_prices[s] * total_steel[s] - 
                     pulp.lpSum(alloy_prices[a] * alloy_amount[a, s] for a in range(A))) 
                     for s in range(S))
problem += profit

# Constraints
# Availability of alloys
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a, s] for s in range(S)) <= available[a], f"AlloyAvailability_{a}"

# Carbon content constraints
for s in range(S):
    problem += (pulp.lpSum(carbon[a] * alloy_amount[a, s] for a in range(A)) / 
                 total_steel[s] >= carbon_min[s]), f"CarbonMin_{s}"

# Nickel content constraints
for s in range(S):
    problem += (pulp.lpSum(nickel[a] * alloy_amount[a, s] for a in range(A)) / 
                 total_steel[s] <= nickel_max[s]), f"NickelMax_{s}"

# Maximum 40% of steel production can be from alloy 1
for s in range(S):
    problem += (alloy_amount[0, s] <= 0.4 * total_steel[s]), f"MaxAlloy1_{s}"

# Solve the problem
problem.solve()

# Prepare output
alloy_use = [[pulp.value(alloy_amount[a, s]) for a in range(A)] for s in range(S)]
total_steel_output = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_output,
    "total_profit": total_profit
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')