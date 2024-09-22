import pulp
import json

# Given data in JSON format
data = {'NumTerminals': 3, 'NumDestinations': 4, 
        'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], 
        'Demand': [65, 70, 50, 45], 
        'Supply': [150, 100, 100]}

# Extracting information from data
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
costs = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Create a linear programming problem
problem = pulp.LpProblem("Soybean_Transportation_Problem", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", 
                                 ((k, l) for k in range(num_terminals) for l in range(num_destinations)), 
                                 lowBound=0, 
                                 cat='Continuous')

# Objective function
problem += pulp.lpSum(costs[k][l] * amount[k, l] for k in range(num_terminals) for l in range(num_destinations)), "Total_Transportation_Cost"

# Supply constraints
for k in range(num_terminals):
    problem += pulp.lpSum(amount[k, l] for l in range(num_destinations)) <= supply[k], f"Supply_Constraint_{k}"

# Demand constraints
for l in range(num_destinations):
    problem += pulp.lpSum(amount[k, l] for k in range(num_terminals)) >= demand[l], f"Demand_Constraint_{l}"

# Solve the problem
problem.solve()

# Prepare output
distribution = [{"from": k, "to": l, "amount": amount[k, l].varValue} 
                for k in range(num_terminals) for l in range(num_destinations) 
                if amount[k, l].varValue > 0]

total_cost = pulp.value(problem.objective)

# Print the results
output = {
    "distribution": distribution,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')