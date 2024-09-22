import pulp
import json

# Data input
data = json.loads("{'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}")

# Define parameters
T = data['T']
demand = data['Demands']
unload_cost = data['UnloadCosts']
unload_capacity = data['UnloadCapacity']
holding_cost = data['HoldingCost']
max_container = data['MaxContainer']
init_container = data['InitContainer']
num_cranes = data['NumCranes']
crane_capacity = data['CraneCapacity']
crane_cost = data['CraneCost']

# Create the problem
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(1, T + 1), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("crane", range(1, T + 1), lowBound=0, upBound=num_cranes, cat='Integer')
hold = pulp.LpVariable.dicts("hold", range(1, T + 1), lowBound=0, upBound=max_container, cat='Continuous')
hold[0] = init_container  # Initial containers in the yard

# Objective Function
problem += pulp.lpSum(unload_cost[t - 1] * amount[t] + holding_cost * hold[t] + crane_cost * crane[t] for t in range(1, T + 1))

# Constraints
for t in range(1, T + 1):
    # Demand Fulfillment
    problem += amount[t] + hold[t - 1] - hold[t] == demand[t - 1]
    # Unloading Capacity
    problem += amount[t] <= unload_capacity[t - 1]
    # Crane Loading Capacity
    problem += crane[t] * crane_capacity >= amount[t]

# Maximum Containers in Yard
for t in range(1, T + 1):
    problem += hold[t] <= max_container

# Crane Rental Limit
for t in range(1, T + 1):
    problem += crane[t] <= num_cranes

# No Remaining Containers After Last Month
problem += hold[T] == 0

# Solve the problem
problem.solve()

# Output results
containers_unloaded = [amount[t].varValue for t in range(1, T + 1)]
cranes_rented = [crane[t].varValue for t in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

print(f'Containers Unloaded: {containers_unloaded}')
print(f'Crane Rented: {cranes_rented}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')