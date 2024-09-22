import pulp

# Data from JSON
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

# Sets and Parameters
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

# Initialize the problem
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("Amount", range(1, T+1), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("Crane", range(1, T+1), lowBound=0, cat='Integer')
inventory = pulp.LpVariable.dicts("Inventory", range(1, T+1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(unload_costs[t-1] * amount[t] + holding_cost * inventory[t] + crane_cost * crane[t] for t in range(1, T+1))

# Constraints

# Demand Fulfillment
for t in range(1, T+1):
    if t == 1:
        problem += amount[t] - crane[t] * crane_capacity + init_container == demands[t-1] + inventory[t], f"Demand_Fulfillment_{t}"
    else:
        problem += amount[t] - crane[t] * crane_capacity + inventory[t-1] == demands[t-1] + inventory[t], f"Demand_Fulfillment_{t}"

# Unloading Capacity
for t in range(1, T+1):
    problem += amount[t] <= unload_capacity[t-1], f"Unloading_Capacity_{t}"

# Crane Limit
for t in range(1, T+1):
    problem += crane[t] <= num_cranes, f"Crane_Limit_{t}"

# Inventory Capacity
for t in range(1, T+1):
    problem += inventory[t] <= max_container, f"Inventory_Capacity_{t}"

# Initial Inventory Constraint
problem += inventory[1] == init_container, "Initial_Inventory"

# Final Inventory Constraint
problem += inventory[T] == 0, "Final_Inventory"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')