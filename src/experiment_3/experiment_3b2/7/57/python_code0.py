import pulp

# Data from the provided JSON
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
    'CraneCost': 1000,
}

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f"x_{t}", lowBound=0, cat='Integer') for t in range(data['T'])]
y = [pulp.LpVariable(f"y_{t}", lowBound=0, upBound=data['NumCranes'], cat='Integer') for t in range(data['T'])]
s = [pulp.LpVariable(f"s_{t}", lowBound=0, upBound=data['MaxContainer'], cat='Integer') for t in range(data['T'] + 1)]

# Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t] * x[t] + data['CraneCost'] * y[t] + data['HoldingCost'] * s[t] for t in range(data['T'])), "Total_Cost"

# Constraints
s[0] = data['InitContainer']  # Initial storage

for t in range(data['T']):
    if t > 0:
        problem += s[t-1] + x[t] - data['Demands'][t] == s[t], f"Balance_Constraint_{t}"
    
    problem += x[t] <= data['UnloadCapacity'][t], f"Unload_Capacity_Constraint_{t}"
    problem += s[t] <= data['MaxContainer'], f"Storage_Capacity_Constraint_{t}"
    if t > 0:
        problem += data['Demands'][t] - s[t-1] <= y[t] * data['CraneCapacity'], f"Cranes_Requirement_Constraint_{t}"

problem += s[data['T'] - 1] == 0, "Final_Condition"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')