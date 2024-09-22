import pulp

# Data from JSON format
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
problem = pulp.LpProblem("Container_Unloading_Optimization", pulp.LpMinimize)

# Variables
amount = pulp.LpVariable.dicts("amount", range(1, T + 1), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("crane", range(1, T + 1), lowBound=0, upBound=num_cranes, cat='Integer')
containers_in_yard = pulp.LpVariable.dicts("containers_in_yard", range(1, T + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(unload_costs[t - 1] * amount[t] + holding_cost * containers_in_yard[t] + crane_cost * crane[t] for t in range(1, T + 1)), "Total_Cost"

# Constraints
problem += containers_in_yard[1] == init_container - amount[1] + demands[0], "Initial_Containers_Yard"
for t in range(2, T + 1):
    problem += containers_in_yard[t] == containers_in_yard[t - 1] - amount[t] + demands[t - 1], f"Containers_Yard_{t}"
    problem += containers_in_yard[t] <= max_container, f"Max_Containers_Yard_{t}"
    problem += amount[t] <= unload_capacities[t - 1], f"Unload_Capacity_{t}"
    problem += amount[t] >= demands[t - 1], f"Demand_Satisfaction_{t}"
    problem += crane[t] * crane_capacity >= amount[t], f"Crane_Capacity_{t}"
    
problem += containers_in_yard[T] == 0, "Final_Containers_Yard"

# Solve the problem
problem.solve()

# Output results
containers_unloaded = [amount[t].varValue for t in range(1, T + 1)]
cranes_rented = [crane[t].varValue for t in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

print(f'Containers Unloaded: {containers_unloaded}')
print(f'Crane Rented: {cranes_rented}')
print(f'Total Cost: <OBJ>{total_cost}</OBJ>')