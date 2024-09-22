import pulp
import json

# Input data
data = {'T': 4, 
        'Demands': [450, 700, 500, 750], 
        'UnloadCosts': [75, 100, 105, 130], 
        'UnloadCapacity': [800, 500, 450, 700], 
        'HoldingCost': 20, 
        'MaxContainer': 500, 
        'InitContainer': 200, 
        'NumCranes': 4, 
        'CraneCapacity': 200, 
        'CraneCost': 1000}

# Problem parameters
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

# Define the problem
problem = pulp.LpProblem("Seaport_Cost_Minimization", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Integer')
cranes = pulp.LpVariable.dicts("cranes", range(T), lowBound=0, upBound=num_cranes, cat='Integer')
containers_in_yard = pulp.LpVariable.dicts("containers_in_yard", range(T), lowBound=0, upBound=max_container, cat='Integer')

# Objective Function
total_cost = pulp.lpSum([unload_costs[t] * amount[t] for t in range(T)]) + \
             pulp.lpSum([holding_cost * containers_in_yard[t] for t in range(T)]) + \
             pulp.lpSum([crane_cost * cranes[t] for t in range(T)])

problem += total_cost, "Total_Cost"

# Constraints

# Initial container setup
problem += (containers_in_yard[0] == init_container + amount[0] - demands[0], "Initial_Container_Constraint")

# Monthly balance constraints
for t in range(1, T):
    problem += (containers_in_yard[t] == containers_in_yard[t-1] + amount[t] - demands[t], f"Container_Balance_Constraint_{t}")

# Unloading capacity constraint
for t in range(T):
    problem += (amount[t] <= unload_capacity[t], f"Unloading_Capacity_Constraint_{t}")

# Crane rental constraint
for t in range(T):
    problem += (cranes[t] * crane_capacity >= demands[t] - (containers_in_yard[t-1] if t > 0 else init_container), f"Cranes_Capacity_Constraint_{t}")

# Maximum containers in yard constraint
for t in range(T):
    problem += (containers_in_yard[t] <= max_container, f"Max_Container_Constraint_{t}")

# Final condition that no containers should remain in the yard
problem += (containers_in_yard[T-1] == 0, "Final_Container_Zero_Constraint")

# Solve the problem
problem.solve()

# Output results
amounts = [pulp.value(amount[t]) for t in range(T)]
cranes_rented = [pulp.value(cranes[t]) for t in range(T)]
total_cost_value = pulp.value(problem.objective)

output = {
    "containers_unloaded": amounts,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')