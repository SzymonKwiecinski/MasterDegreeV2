import pulp

# Data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [
        [14, 22],
        [18, 12],
        [10, 16]
    ]
}

supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

num_plants = len(supply)
num_cities = len(demand)

# Problem
problem = pulp.LpProblem("Minimize_Transmission_Costs", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("Send", ((p, c) for p in range(num_plants) for c in range(num_cities)), lowBound=0)

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[p, c] for p in range(num_plants) for c in range(num_cities))

# Supply Constraints
for p in range(num_plants):
    problem += pulp.lpSum(send[p, c] for c in range(num_cities)) <= supply[p]

# Demand Constraints
for c in range(num_cities):
    problem += pulp.lpSum(send[p, c] for p in range(num_plants)) == demand[c]

# Solve
problem.solve()

# Output Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')