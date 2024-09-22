import pulp

# Load data from JSON format
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

# Parameters
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Storage_and_Switch_Costs", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Production", range(1, T + 1), lowBound=0, cat='Continuous')  # Production variables
I = pulp.LpVariable.dicts("Inventory", range(1, T + 1), lowBound=0, cat='Continuous')   # Inventory variables

# Objective Function
problem += pulp.lpSum(storage_cost * I[i] + switch_cost * pulp.lpSum([pulp.lpAbs(x[i+1] - x[i]) for i in range(1, T)]) for i in range(1, T+1))

# Constraints
I[1] = x[1] - deliver[0]  # Initial inventory constraint
for i in range(2, T + 1):
    problem += I[i] == I[i - 1] + x[i] - deliver[i - 1]  # Inventory balance

problem += I[T] >= 0  # Final inventory must be non-negative

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')