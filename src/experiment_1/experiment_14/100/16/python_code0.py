import pulp

# Data input
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [
        [14, 22],
        [18, 12],
        [10, 16]
    ]
}

# Number of power plants and cities
num_power_plants = len(data['supply'])
num_cities = len(data['demand'])

# Create problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((p, c) for p in range(num_power_plants) for c in range(num_cities)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[(p, c)] for p in range(num_power_plants) for c in range(num_cities))

# Constraints
# Supply constraints
for p in range(num_power_plants):
    problem += pulp.lpSum(x[(p, c)] for c in range(num_cities)) <= data['supply'][p], f"Supply_Constraint_{p}"

# Demand constraints
for c in range(num_cities):
    problem += pulp.lpSum(x[(p, c)] for p in range(num_power_plants)) == data['demand'][c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')