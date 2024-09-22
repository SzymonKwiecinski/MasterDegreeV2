import pulp
import json

# Load data from JSON format
data = json.loads('{"T": 12, "Deliver": [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], "StorageCost": 5, "SwitchCost": 10}')

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Define the decision variables
T = data['T']
Deliver = data['Deliver']
StorageCost = data['StorageCost']
SwitchCost = data['SwitchCost']

I = pulp.LpVariable.dicts('I', range(T + 1), lowBound=0)
x = pulp.LpVariable.dicts('x', range(T), lowBound=0)
y = pulp.LpVariable.dicts('y', range(T - 1), lowBound=0)

# Objective function
problem += pulp.lpSum(StorageCost * I[i] for i in range(T + 1)) + pulp.lpSum(SwitchCost * y[i] for i in range(T - 1))

# Initial inventory
I[0] = 0

# Inventory balance constraints
for i in range(1, T + 1):
    problem += I[i] == I[i - 1] + x[i - 1] - Deliver[i - 1]

# Constraints for auxiliary variables to linearize the absolute value
for i in range(T - 1):
    problem += y[i] >= x[i] - x[i + 1]
    problem += y[i] >= x[i + 1] - x[i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')