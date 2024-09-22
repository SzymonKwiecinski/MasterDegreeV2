import pulp
import json

# Input data
data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 
        'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 
        'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

# Extract data
T = data['T']
demands = data['Demands']
unload_costs = data['UnloadCosts']
unload_capacities = data['UnloadCapacity']
holding_cost = data['HoldingCost']
max_container = data['MaxContainer']
init_container = data['InitContainer']
num_cranes = data['NumCranes']
crane_capacity = data['CraneCapacity']
crane_cost = data['CraneCost']

# Create the optimization problem
problem = pulp.LpProblem("Seaport_Cost_Minimization", pulp.LpMinimize)

# Decision Variables
amounts = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Integer')
cranes = pulp.LpVariable.dicts("crane", range(T), lowBound=0, upBound=num_cranes, cat='Integer')
inventory = pulp.LpVariable.dicts("inventory", range(T+1), lowBound=0, upBound=max_container, cat='Integer')

# Initial inventory
inventory[0] = init_container

# Objective Function: Minimize total costs
total_cost = pulp.lpSum([amounts[t] * unload_costs[t] for t in range(T)]) + \
              pulp.lpSum([inventory[t] * holding_cost for t in range(T)]) + \
              pulp.lpSum([cranes[t] * crane_cost for t in range(T)])

problem += total_cost

# Constraints
for t in range(T):
    # Demand fulfillment
    problem += (amounts[t] - demands[t] + (inventory[t] if t == 0 else inventory[t-1]) <= 0, f"demand_fulfillment_{t}")

    # Unloading capacity
    problem += (amounts[t] <= unload_capacities[t], f"unloading_capacity_{t}")

    # Crane loading capacity
    problem += (cranes[t] * crane_capacity >= demands[t] - (inventory[t] if t == 0 else inventory[t-1]), f"crane_capacity_{t}")

    # Inventory balance
    if t < T - 1:
        problem += (inventory[t+1] == (inventory[t] + amounts[t] - demands[t]), f"inventory_balance_{t}")

# End of last month, inventory must be zero
problem += (inventory[T] == 0, "final_inventory")

# Solve the problem
problem.solve()

# Retrieve results
containers_unloaded = [int(amounts[t].varValue) for t in range(T)]
cranes_rented = [int(cranes[t].varValue) for t in range(T)]
total_cost_value = pulp.value(problem.objective)

# Output
result = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')