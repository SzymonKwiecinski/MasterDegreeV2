import pulp

# Data
data = {
    'T': 12, 
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
    'StorageCost': 5, 
    'SwitchCost': 10
}

# Parameters
T = data['T']
d = data['Deliver']
c_s = data['StorageCost']
c_sw = data['SwitchCost']

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(1, T + 1), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("Inventory", range(1, T + 1), lowBound=0, cat='Continuous')
y_plus = pulp.LpVariable.dicts("y_plus", range(1, T), lowBound=0, cat='Continuous')
y_minus = pulp.LpVariable.dicts("y_minus", range(1, T), lowBound=0, cat='Continuous')

# Objective function
problem += (c_s * pulp.lpSum(I[i] for i in range(1, T + 1)) + 
             c_sw * pulp.lpSum(y_plus[i] + y_minus[i] for i in range(1, T)))

# Constraints
problem += (I[1] == x[1] - d[0], "Flow_Balance_1")
for i in range(2, T + 1):
    problem += (x[i] + I[i - 1] == d[i - 1] + I[i], f"Flow_Balance_{i}")

# Non-negativity of inventory
for i in range(1, T + 1):
    problem += (I[i] >= 0, f"NonNegativity_Inventory_{i}")
    problem += (x[i] >= 0, f"NonNegativity_Production_{i}")

# Absolute value linearization constraints
for i in range(1, T):
    problem += (x[i + 1] - x[i] == y_plus[i] - y_minus[i], f"Linearization_{i}")
    problem += (y_plus[i] >= 0, f"NonNegativity_y_plus_{i}")
    problem += (y_minus[i] >= 0, f"NonNegativity_y_minus_{i}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')