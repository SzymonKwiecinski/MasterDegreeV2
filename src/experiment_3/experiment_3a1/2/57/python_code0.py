import pulp
import json

# Data input
data = json.loads('{"T": 4, "Demands": [450, 700, 500, 750], "UnloadCosts": [75, 100, 105, 130], "UnloadCapacity": [800, 500, 450, 700], "HoldingCost": 20, "MaxContainer": 500, "InitContainer": 200, "NumCranes": 4, "CraneCapacity": 200, "CraneCost": 1000}')

# Parameters
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
problem = pulp.LpProblem("Container_Unloading_Problem", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(1, T + 1), lowBound=0)
crane = pulp.LpVariable.dicts("crane", range(1, T + 1), lowBound=0, upBound=num_cranes, cat='Integer')
holding = pulp.LpVariable.dicts("holding", range(1, T + 1), lowBound=0)

# Objective function
problem += pulp.lpSum(unload_cost[t - 1] * amount[t] + holding_cost * holding[t] + crane_cost * crane[t] for t in range(1, T + 1))

# Constraints
for t in range(1, T + 1):
    # Unloading Capacity
    problem += amount[t] <= unload_capacity[t - 1], f"Unload_Capacity_Constraint_{t}"

    # Demand Satisfaction
    if t == 1:
        problem += amount[t] + init_container >= demand[t - 1], f"Demand_Satisfaction_Constraint_{t}"
    else:
        problem += amount[t] + holding[t - 1] >= demand[t - 1], f"Demand_Satisfaction_Constraint_{t}"

    # Max Containers in Storage
    problem += holding[t] <= max_container, f"Max_Storage_Constraint_{t}"

    # Crane Capacity
    problem += crane[t] * crane_capacity >= amount[t], f"Crane_Capacity_Constraint_{t}"

# End of Period Constraint
problem += holding[T] == 0, "End_of_Period_Constraint"

# Solve the problem
problem.solve()

# Output
containers_unloaded = [amount[t].varValue for t in range(1, T + 1)]
cranes_rented = [crane[t].varValue for t in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

print(f'Containers Unloaded: {containers_unloaded}')
print(f'Crane Rented: {cranes_rented}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')