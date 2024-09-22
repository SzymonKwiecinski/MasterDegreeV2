import pulp
import json

# Data input in JSON format
data = {
    'NumTerminals': 3, 
    'NumDestinations': 4, 
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], 
    'Demand': [65, 70, 50, 45], 
    'Supply': [150, 100, 100]
}

num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Create the LP problem
problem = pulp.LpProblem("Soybean_Transport_Problem", pulp.LpMinimize)

# Define decision variables
amount = pulp.LpVariable.dicts("Ship", 
                                ((i, j) for i in range(num_terminals) for j in range(num_destinations)), 
                                lowBound=0, 
                                cat='Continuous')

# Objective function: Minimize total transportation costs
problem += pulp.lpSum(cost[i][j] * amount[i, j] for i in range(num_terminals) for j in range(num_destinations)), "Total_Cost"

# Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum(amount[i, j] for j in range(num_destinations)) <= supply[i], f"Supply_Constraint_{i}"

# Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum(amount[i, j] for i in range(num_terminals)) >= demand[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare output data
distribution = []
for i in range(num_terminals):
    for j in range(num_destinations):
        amount_shipped = amount[i, j].varValue
        if amount_shipped > 0:
            distribution.append({"from": i, "to": j, "amount": amount_shipped})

total_cost = pulp.value(problem.objective)

# Output result in the required format
output = {
    "distribution": distribution,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')