import pulp

# Problem data
data = {
    'T': 4,
    'Demands': [450, 700, 500, 750],
    'UnloadCosts': [75, 100, 105, 130],
    'UnloadCapacity': [800, 500, 450, 700],
    'HoldingCost': 20,
    'MaxContainer': 500,
    'InitContainer': 200,
    'NumCranes': 4,
    'CraneCapacity': 200,
    'CraneCost': 1000
}

# Unpack the data
T = data['T']
demands = data['Demands']
unload_costs = data['UnloadCosts']
unload_capacity = data['UnloadCapacity']
holding_cost = data['HoldingCost']
max_container = data['MaxContainer']
init_container = data['InitContainer']
num_cranes = data['NumCranes']
crane_capacity = data['CraneCapacity']
crane_cost = data['CraneCost']

# Define the LP problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Containers_Unloaded",
                          range(1, T + 1),
                          lowBound=0,
                          cat=pulp.LpInteger)
y = pulp.LpVariable.dicts("Cranes_Rented",
                          range(1, T + 1),
                          lowBound=0,
                          cat=pulp.LpInteger)
h = pulp.LpVariable.dicts("Containers_Held",
                          range(T + 1),  # including h_0
                          lowBound=0,
                          cat=pulp.LpContinuous)

# Initial inventory constraint
problem += (h[0] == init_container, "Initial_Inventory")

# Objective function
problem += pulp.lpSum(unload_costs[t-1] * x[t] + crane_cost * y[t] + holding_cost * h[t]
                      for t in range(1, T + 1))

# Constraints
for t in range(1, T + 1):
    # Unloading capacity constraint
    problem += (x[t] <= unload_capacity[t-1], f"Unload_Capacity_Constraint_{t}")

    # Crane capacity constraint
    problem += (crane_capacity * y[t] >= demands[t-1], f"Crane_Capacity_Constraint_{t}")

    # Crane rental limit
    problem += (y[t] <= num_cranes, f"Crane_Rental_Limit_{t}")

    # Inventory balance constraint
    problem += (h[t] == h[t-1] + x[t] - demands[t-1], f"Inventory_Balance_{t}")

    # Inventory limit constraint
    problem += (h[t] <= max_container, f"Inventory_Limit_{t}")

# Final inventory constraint
problem += (h[T] == 0, "Final_Inventory_Constraint")

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')