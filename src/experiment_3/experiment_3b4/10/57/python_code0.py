import pulp

# Data provided
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
unload_costs = data['UnloadCosts']
unload_capacity = data['UnloadCapacity']
holding_cost = data['HoldingCost']
max_container = data['MaxContainer']
init_container = data['InitContainer']
num_cranes = data['NumCranes']
crane_capacity = data['CraneCapacity']
crane_cost = data['CraneCost']

# Define the problem
problem = pulp.LpProblem("Container_Unloading_Problem", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat=pulp.LpContinuous)
crane = pulp.LpVariable.dicts("crane", range(T), lowBound=0, cat=pulp.LpInteger)
store = pulp.LpVariable.dicts("store", range(T), lowBound=0, cat=pulp.LpContinuous)

# Objective function
total_cost = (
    pulp.lpSum(unload_costs[t] * amount[t] for t in range(T)) +
    pulp.lpSum(holding_cost * store[t] for t in range(T)) +
    pulp.lpSum(crane_cost * crane[t] for t in range(T))
)
problem += total_cost

# Constraints
for t in range(T):
    problem += amount[t] <= unload_capacity[t], f"Unloading_Capacity_Constraint_{t}"
    problem += crane[t] <= num_cranes, f"Max_Cranes_Constraint_{t}"
    problem += crane[t] * crane_capacity >= demand[t], f"Meet_Demand_Constraint_{t}"
    problem += store[t] <= max_container, f"Storage_Capacity_Constraint_{t}"

# Initial storage calculation
problem += store[0] == init_container + amount[0] - demand[0], "Initial_Storage_Calculation"

# Storage balance constraints
for t in range(1, T):
    problem += store[t] == store[t-1] + amount[t] - demand[t], f"Storage_Balance_{t}"

# End storage requirement
problem += store[T-1] == 0, "End_Storage_Requirement"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')