import pulp

# Data from JSON
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Parameters
P = len(data['supply'])  # number of power plants
C = len(data['demand'])   # number of cities
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Define the problem
problem = pulp.LpProblem("Electricity_Transmission_Problem", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[p][c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Supply Constraints
for p in range(P):
    problem += (pulp.lpSum(send[p][c] for c in range(C)) <= supply[p]), f"Supply_Constraint_{p}"

# Demand Constraints
for c in range(C):
    problem += (pulp.lpSum(send[p][c] for p in range(P)) >= demand[c]), f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Output the results
for p in range(P):
    for c in range(C):
        print(f"send[{p},{c}] = {send[p][c].varValue}")
        
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')