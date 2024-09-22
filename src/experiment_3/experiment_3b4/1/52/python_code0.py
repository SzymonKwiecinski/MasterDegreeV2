import pulp

# Data
data = {'supply': [30, 25, 45], 
        'demand': [40, 60], 
        'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

num_power_plants = len(supply)
num_cities = len(demand)

# Problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Variables
send = pulp.LpVariable.dicts("send", 
                             ((p, c) for p in range(num_power_plants) for c in range(num_cities)), 
                             lowBound=0, 
                             cat=pulp.LpContinuous)

# Objective
problem += pulp.lpSum(transmission_costs[p][c] * send[p, c] 
                      for p in range(num_power_plants) 
                      for c in range(num_cities))

# Supply constraints
for p in range(num_power_plants):
    problem += pulp.lpSum(send[p, c] for c in range(num_cities)) <= supply[p]

# Demand constraints
for c in range(num_cities):
    problem += pulp.lpSum(send[p, c] for p in range(num_power_plants)) == demand[c]

# Solve
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')