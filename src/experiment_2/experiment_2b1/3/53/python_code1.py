import pulp
import json

# Input data
data = {'NumTerminals': 3, 'NumDestinations': 4, 'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], 'Demand': [65, 70, 50, 45], 'Supply': [150, 100, 100]}

# Extracting data from the input
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
costs = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Create the linear programming problem
problem = pulp.LpProblem("Soybean_Transportation_Problem", pulp.LpMinimize)

# Decision variables for the amount of soybeans shipped from terminal to destination
amount_vars = pulp.LpVariable.dicts("amount", (range(num_terminals), range(num_destinations)), 0)

# Objective function: Minimize total transportation costs
problem += pulp.lpSum(costs[i][j] * amount_vars[i][j] for i in range(num_terminals) for j in range(num_destinations)), "Total_Transportation_Cost"

# Constraints
# Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum(amount_vars[i][j] for j in range(num_destinations)) <= supply[i], f"Supply_Constraint_{i}"

# Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum(amount_vars[i][j] for i in range(num_terminals)) >= demand[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare the output
distribution = [{"from": i, "to": j, "amount": amount_vars[i][j].value()} for i in range(num_terminals) for j in range(num_destinations) if amount_vars[i][j].value() > 0]

# Calculate total cost
total_cost = pulp.value(problem.objective)

# Output in the requested format
output = {
    "distribution": distribution,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')