import pulp

# Data provided from the input
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

# Creating the optimization problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(1, data['T'] + 1), lowBound=0)
crane = pulp.LpVariable.dicts("crane", range(1, data['T'] + 1), lowBound=0, cat='Integer')
store = pulp.LpVariable.dicts("store", range(1, data['T'] + 1), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t-1] * amount[t] +
                       data['HoldingCost'] * store[t] +
                       data['CraneCost'] * crane[t]
                       for t in range(1, data['T'] + 1))

# Constraints
for t in range(1, data['T'] + 1):
    problem += amount[t] <= data['UnloadCapacity'][t-1], f"Capacity_Constraint_{t}"
    
for t in range(1, data['T'] + 1):
    if t == 1:
        problem += store[t] == data['InitContainer'] + amount[t] - data['Demands'][t-1], f"Initial_Store_Constraint"
    else:
        problem += store[t] == store[t-1] + amount[t] - data['Demands'][t-1], f"Store_Constraint_{t}"

for t in range(1, data['T'] + 1):
    problem += store[t] <= data['MaxContainer'], f"Max_Container_Constraint_{t}"

problem += store[data['T']] == 0, "End_Empty_Yard_Constraint"

for t in range(1, data['T'] + 1):
    problem += data['Demands'][t-1] <= crane[t] * data['CraneCapacity'], f"Demand_Crane_Constraint_{t}"
    
for t in range(1, data['T'] + 1):
    problem += crane[t] <= data['NumCranes'], f"Max_Crane_Constraint_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')