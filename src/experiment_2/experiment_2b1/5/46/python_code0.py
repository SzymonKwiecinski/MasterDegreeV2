import pulp
import json

data = json.loads("{'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}")

# Extracting data from input
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
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Variables for the amount of each alloy used in each type of steel
alloy_amount = pulp.LpVariable.dicts("alloy_amount", 
                                      ((a, s) for a in range(A) for s in range(S)), 
                                      lowBound=0)

# Variables for the total amount of each steel produced
total_steel = pulp.LpVariable.dicts("total_steel", range(S), lowBound=0)

# Objective Function: Maximize profit
problem += pulp.lpSum((steel_prices[s] * total_steel[s] - 
                       pulp.lpSum(alloy_prices[a] * alloy_amount[a, s] for a in range(A))) 
                       for s in range(S))

# Constraints for carbon and nickel content per steel type
for s in range(S):
    # Carbon content constraint
    problem += (pulp.lpSum(carbon[a] * alloy_amount[a, s] for a in range(A)) >= 
                 carbon_min[s] * total_steel[s]), f"Carbon_Constraint_{s}"
    
    # Nickel content constraint
    problem += (pulp.lpSum(nickel[a] * alloy_amount[a, s] for a in range(A)) <= 
                 nickel_max[s] * total_steel[s]), f"Nickel_Constraint_{s}"

# Constraints for total amount of each alloy used
for a in range(A):
    problem += (pulp.lpSum(alloy_amount[a, s] for s in range(S)) <= available[a]), f"Available_Alloy_{a}"

# Constraint for alloy 1
problem += (pulp.lpSum(alloy_amount[0, s] for s in range(S)) <= 0.4 * pulp.lpSum(total_steel[s] for s in range(S))), "Alloy_1_Constraint"

# Solve the problem
problem.solve()

# Prepare the output
alloy_use = [[pulp.value(alloy_amount[a, s]) for a in range(A)] for s in range(S)]
total_steel_values = [pulp.value(total_steel[s]) for s in range(S)]
total_profit = pulp.value(problem.objective)

# Output the results
output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_values,
    "total_profit": total_profit
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')