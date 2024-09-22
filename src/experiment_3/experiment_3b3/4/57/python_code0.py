import pulp

# Data
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

# Indices
T = data['T']

# Problem
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("crane", range(T), lowBound=0, cat='Integer')
hold = pulp.LpVariable.dicts("hold", range(T), lowBound=0, upBound=data['MaxContainer'], cat='Continuous')

# Objective Function
total_cost = pulp.lpSum(
    data['UnloadCosts'][t] * amount[t] + 
    data['HoldingCost'] * hold[t] + 
    data['CraneCost'] * crane[t]
    for t in range(T)
)
problem += total_cost

# Constraints
for t in range(T):
    # Constraint 1: amount_t <= unload_capacity_t
    problem += amount[t] <= data['UnloadCapacity'][t]

    # Constraint 2: hold_{t-1} + amount_t - demand_t = hold_t
    if t == 0:
        problem += data['InitContainer'] + amount[t] - data['Demands'][t] == hold[t]
    else:
        problem += hold[t-1] + amount[t] - data['Demands'][t] == hold[t]

    # Constraint 5: crane_t * crane_capacity >= amount_t
    problem += crane[t] * data['CraneCapacity'] >= amount[t]
    
    # Constraint 6: 0 <= crane_t <= num_cranes
    problem += crane[t] <= data['NumCranes']

# Constraint 4: hold_T = 0
problem += hold[T - 1] == 0

# Constraint 7: amount_1 = init_container - hold_1
problem += amount[0] == data['InitContainer'] - hold[0]

# Solve
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')