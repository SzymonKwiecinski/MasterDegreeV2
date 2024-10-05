import pulp

# Parse the input data
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Define number of power plants and cities
P = len(supply)
C = len(demand)

# Create a linear programming problem
problem = pulp.LpProblem("Power_Transmission_Problem", pulp.LpMinimize)

# Define decision variables
send_vars = pulp.LpVariable.dicts("Send", ((p, c) for p in range(P) for c in range(C)), 
                                  lowBound=0, cat='Continuous')

# Objective function: Minimize the total transmission cost
problem += pulp.lpSum(send_vars[p, c] * transmission_costs[p][c] for p in range(P) for c in range(C))

# Constraints
# Supply constraints for each power plant
for p in range(P):
    problem += pulp.lpSum(send_vars[p, c] for c in range(C)) <= supply[p], f"Supply_Constraint_{p}"

# Demand constraints for each city
for c in range(C):
    problem += pulp.lpSum(send_vars[p, c] for p in range(P)) >= demand[c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Prepare the output
send = [[send_vars[p, c].varValue for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

# Print the result
result = {
    "send": send,
    "total_cost": total_cost
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')