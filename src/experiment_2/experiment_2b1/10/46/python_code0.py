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

# Extracting data from the JSON-like dictionary
available_alloys = data['available']
carbon_content = data['carbon']
nickel_content = data['nickel']
alloy_prices = data['alloy_prices']
steel_prices = data['steel_prices']
carbon_min = data['carbon_min']
nickel_max = data['nickel_max']

# Parameters
num_alloys = len(available_alloys)
num_steels = len(steel_prices)

# Create the problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

# Decision variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", (range(num_alloys), range(num_steels)), lowBound=0)
total_steel = pulp.LpVariable.dicts("total_steel", range(num_steels), lowBound=0)

# Objective function: Maximize profit
profit = pulp.lpSum((steel_prices[s] * total_steel[s] - pulp.lpSum(alloy_prices[a] * alloy_amount[a][s] for a in range(num_alloys))) for s in range(num_steels)))
problem += profit

# Constraints for carbon and nickel content
for s in range(num_steels):
    problem += pulp.lpSum((carbon_content[a] * alloy_amount[a][s] for a in range(num_alloys))) >= carbon_min[s] * total_steel[s], f"Carbon_Constraint_{s}"
    problem += pulp.lpSum((nickel_content[a] * alloy_amount[a][s] for a in range(num_alloys))) <= nickel_max[s] * total_steel[s], f"Nickel_Constraint_{s}"

# Total production constraint for each steel type
for s in range(num_steels):
    problem += pulp.lpSum(alloy_amount[a][s] for a in range(num_alloys)) == total_steel[s], f"Total_Production_Constraint_{s}"

# Constraints for alloy availability
for a in range(num_alloys):
    problem += pulp.lpSum(alloy_amount[a][s] for s in range(num_steels)) <= available_alloys[a], f"Alloy_Availability_Constraint_{a}"

# Constraint for maximum alloy 1 usage
for s in range(num_steels):
    problem += pulp.lpSum(alloy_amount[0][s] for s in range(num_steels)) <= 0.4 * total_steel[s], f"Max_Alloy1_Usage_Constraint_{s}"

# Solve the problem
problem.solve()

# Extract results
alloy_use = [[pulp.value(alloy_amount[a][s]) for a in range(num_alloys)] for s in range(num_steels)]
total_steel_produced = [pulp.value(total_steel[s]) for s in range(num_steels)]
total_profit = pulp.value(problem.objective)

# Prepare output
output = {
    "alloy_use": alloy_use,
    "total_steel": total_steel_produced,
    "total_profit": total_profit
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')