import pulp
import json

# Input Data
data = json.loads("{'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}")

# Parameters
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

# Create the problem
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(1, T+1), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("crane", range(1, T+1), lowBound=0, upBound=num_cranes, cat='Integer')
hold = pulp.LpVariable.dicts("hold", range(0, T+1), lowBound=0, upBound=max_container, cat='Continuous')

# Objective Function
problem += pulp.lpSum(unload_costs[t-1] * amount[t] + holding_cost * hold[t] + crane_cost * crane[t] for t in range(1, T+1)), "Total Cost"

# Constraints
# Unloading capacity constraint
for t in range(1, T+1):
    problem += amount[t] <= unload_capacities[t-1], f"Unload_Capacity_{t}"

# Demand fulfillment constraints
for t in range(1, T+1):
    problem += hold[t-1] + amount[t] - demands[t-1] == hold[t], f"Demand_Fulfillment_{t}"

# Initial condition
problem += hold[0] == init_container, "Initial_Condition"

# Capacity constraint in yard
for t in range(1, T+1):
    problem += hold[t] <= max_container, f"Max_Container_{t}"

# Cranes rented constraint
for t in range(1, T+1):
    problem += crane[t] * crane_capacity >= amount[t], f"Cranes_Capacity_{t}"

# Cranes limit
for t in range(1, T+1):
    problem += crane[t] <= num_cranes, f"Cranes_Limit_{t}"

# Final condition
problem += hold[T] == 0, "Final_Condition"

# Solve the problem
problem.solve()

# Output the results
containers_unloaded = [amount[t].varValue for t in range(1, T+1)]
cranes_rented = [crane[t].varValue for t in range(1, T+1)]
total_cost = pulp.value(problem.objective)

print(f'Containers Unloaded: {containers_unloaded}')
print(f'Crane Rented: {cranes_rented}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')