import pulp

# Data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

num_power_plants = len(data['supply'])
num_cities = len(data['demand'])

# Problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((p, c) for p in range(num_power_plants) for c in range(num_cities)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[p, c] for p in range(num_power_plants) for c in range(num_cities))

# Constraints
# 1. Supply constraints for each power plant
for p in range(num_power_plants):
    problem += pulp.lpSum(x[p, c] for c in range(num_cities)) <= data['supply'][p]

# 2. Demand constraints for each city
for c in range(num_cities):
    problem += pulp.lpSum(x[p, c] for p in range(num_power_plants)) == data['demand'][c]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')