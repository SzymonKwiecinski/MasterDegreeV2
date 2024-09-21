import pulp

# Data Input
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Parameters
num_power_plants = len(data['supply'])
num_cities = len(data['demand'])
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Create the Problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(num_power_plants), range(num_cities)), lowBound=0)

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * x[p][c] for p in range(num_power_plants) for c in range(num_cities)), "Total_Transmission_Cost"

# Constraints

# Supply Constraints
for p in range(num_power_plants):
    problem += pulp.lpSum(x[p][c] for c in range(num_cities)) <= supply[p], f"Supply_Constraint_P{p+1}"

# Demand Constraints
for c in range(num_cities):
    problem += pulp.lpSum(x[p][c] for p in range(num_power_plants)) == demand[c], f"Demand_Constraint_C{c+1}"

# Solve the Problem
problem.solve()

# Print the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')