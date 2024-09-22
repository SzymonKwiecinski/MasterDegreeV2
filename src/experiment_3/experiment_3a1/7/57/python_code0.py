import pulp

# Data input from the provided DATA section
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

# Create the linear programming problem
problem = pulp.LpProblem("Seaport Operations", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(1, T + 1), lowBound=0)
crane = pulp.LpVariable.dicts("crane", range(1, T + 1), lowBound=0, upBound=num_cranes)

# Container holding at the end of each month
x = pulp.LpVariable.dicts("x", range(1, T + 1), lowBound=0)

# Objective function
problem += pulp.lpSum(unload_cost[t - 1] * amount[t] + 
                       holding_cost * x[t] + 
                       crane_cost * crane[t] for t in range(1, T + 1))

# Constraints
for t in range(1, T + 1):
    problem += amount[t] <= unload_capacity[t - 1], f"UnloadCapacity_{t}"
    if t > 1:
        problem += amount[t] + x[t - 1] - demand[t - 1] == x[t], f"YardBalance_{t}"
    else:
        problem += amount[t] + init_container - demand[t - 1] == x[t], f"InitialYardBalance_{t}"
    problem += x[t] <= max_container, f"MaxStorage_{t}"
    if t == T:
        problem += x[t] == 0, "EmptyYard"
    problem += crane[t] * crane_capacity >= demand[t - 1], f"LoadingDemand_{t}"
    problem += crane[t] <= num_cranes, f"MaxCranes_{t}"

# Solve the problem
problem.solve()

# Output results
containers_unloaded = [amount[t].varValue for t in range(1, T + 1)]
cranes_rented = [crane[t].varValue for t in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

print(f'Containers Unloaded: {containers_unloaded}')
print(f'Cranes Rented: {cranes_rented}')
print(f'Total Cost: <OBJ>{total_cost}</OBJ>')