import pulp

# Data provided
data = {
    'NumTerminals': 3, 
    'NumDestinations': 4, 
    'Cost': [
        [34, 49, 17, 26], 
        [52, 64, 23, 14], 
        [20, 28, 12, 17]
    ],
    'Demand': [65, 70, 50, 45], 
    'Supply': [150, 100, 100]
}

num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Initialize the problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Define the decision variables
amount = pulp.LpVariable.dicts(
    "amount",
    ((i, j) for i in range(num_terminals) for j in range(num_destinations)),
    lowBound=0,
    cat=pulp.LpContinuous
)

# Objective Function
problem += pulp.lpSum(cost[i][j] * amount[i, j]
                      for i in range(num_terminals)
                      for j in range(num_destinations)), "Total_Transportation_Cost"

# Constraints
# Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum(amount[i, j] for j in range(num_destinations)) <= supply[i], f"Supply_Constraint_{i}"

# Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum(amount[i, j] for i in range(num_terminals)) >= demand[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Collect the output
distribution = [{
    "from": i,
    "to": j,
    "amount": amount[i, j].varValue
} for i in range(num_terminals) for j in range(num_destinations)]

total_cost = pulp.value(problem.objective)

output = {
    "distribution": distribution,
    "total_cost": total_cost
}

# Print the results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')