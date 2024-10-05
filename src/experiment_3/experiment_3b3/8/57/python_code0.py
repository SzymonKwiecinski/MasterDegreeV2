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

# Unpacking data
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

# Define the problem
problem = pulp.LpProblem("Container_Unloading_Cost_Minimization", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("Amount", range(1, T+1), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("Crane", range(1, T+1), lowBound=0, cat='Integer')
containers = pulp.LpVariable.dicts("Containers", range(1, T+1), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(unload_cost[t-1] * amount[t] + holding_cost * containers[t] + crane_cost * crane[t] for t in range(1, T+1))

# Constraints
for t in range(1, T+1):
    # Demand Fulfillment
    if t == 1:
        problem += amount[t] + init_container - containers[t] == demand[t-1]
    else:
        problem += amount[t] + containers[t-1] - containers[t] == demand[t-1]
    
    # Unloading Capacity
    problem += amount[t] <= unload_capacity[t-1]
    
    # Maximum Storage Capacity
    problem += containers[t] <= max_container
    
    # Crane Loading Constraint
    problem += crane[t] * crane_capacity >= demand[t-1]
    
    # Number of Cranes
    problem += crane[t] <= num_cranes

# Yard Empty After Last Month
problem += containers[T] == 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')