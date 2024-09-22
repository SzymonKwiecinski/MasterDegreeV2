import pulp

# Data from JSON
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

# Create the problem
problem = pulp.LpProblem("Production_and_Inventory_Scheduling", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Production", range(T), lowBound=0)  # Production variables
I = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0)   # Inventory variables

# Objective Function
problem += pulp.lpSum(storage_cost * I[i] + switch_cost * (pulp.lpAbs(x[i] - x[i-1]) if i > 0 else 0)
                      for i in range(T)), "Total_Cost"

# Constraints
problem += (I[0] == 0, "Initial_Inventory")

for i in range(1, T):
    problem += (I[i] == I[i-1] + x[i] - deliver[i], f"Inventory_Constraint_{i}")
    problem += (I[i] >= 0, f"Non_Negative_Inventory_{i}")

for i in range(T):
    problem += (x[i] >= 0, f"Non_Negative_Production_{i}")

# Solve the problem
problem.solve()

# Output the results
production_schedule = [x[i].varValue for i in range(T)]
total_cost = pulp.value(problem.objective)

print(f'Production Schedule: {production_schedule}')
print(f'Total Cost incurred: <OBJ>{total_cost}</OBJ>')