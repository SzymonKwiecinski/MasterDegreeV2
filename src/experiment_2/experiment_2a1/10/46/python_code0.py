import pulp
import json

# Input Data
data = {'available': [40, 50, 80], 
        'carbon': [3, 4, 3.5], 
        'nickel': [1, 1.5, 1.8], 
        'alloy_prices': [380, 400, 440], 
        'steel_prices': [650, 600], 
        'carbon_min': [3.6, 3.4], 
        'nickel_max': [1.5, 1.7]}

# Constants from data
available_alloys = data['available']
carbon_content = data['carbon']
nickel_content = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

# Problem definition
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

# Variables
S = len(steel_prices)  # Number of steel types
A = len(alloy_prices)  # Number of alloys

# Alloy amounts used in each steel type
alloy_amount = pulp.LpVariable.dicts("Alloy_Amount", 
                                      ((a, s) for a in range(A) for s in range(S)), 
                                      lowBound=0)

# Total steel produced for each type
total_steel = pulp.LpVariable.dicts("Total_Steel", range(S), lowBound=0)

# Objective function
problem += pulp.lpSum(steel_prices[s] * total_steel[s] for s in range(S)) - \
           pulp.lpSum(alloy_prices[a] * pulp.lpSum(alloy_amount[a, s] for s in range(S)) for a in range(A))

# Constraints
# Alloy availability constraints
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a, s] for s in range(S)) <= available_alloys[a], f"Alloy_Availability_{a}"

# Carbon percentage constraints
for s in range(S):
    problem += pulp.lpSum(carbon_content[a] * alloy_amount[a, s] for a in range(A)) >= carbon_min[s] * total_steel[s], f"Carbon_Min_{s}"

# Nickel percentage constraints
for s in range(S):
    problem += pulp.lpSum(nickel_content[a] * alloy_amount[a, s] for a in range(A)) <= nickel_max[s] * total_steel[s], f"Nickel_Max_{s}"

# Limit of alloy 1
for s in range(S):
    problem += alloy_amount[0, s] <= 0.4 * total_steel[s], f"Alloy_1_Limit_{s}"

# Solve the problem
problem.solve()

# Prepare the output
alloy_use = [[pulp.value(alloy_amount[a, s]) for a in range(A)] for s in range(S)]
total_steel_production = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

# Print the objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')

# Format and return results
results = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_production,
    "total_profit": total_profit
}

results