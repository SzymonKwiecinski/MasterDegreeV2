import pulp
import json

# Data
data = json.loads('{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}')
T = data['T']
period = data['Period']
demand = data['Demand']

# Problem definition
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
start = {j: pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(T)}
total = pulp.LpVariable('total', lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(start[j] for j in range(T)), "Total_Nurses_Hired"

# Constraints
for j in range(T):
    problem += (
        pulp.lpSum(start[(j - i) % T] for i in range(period)) >= demand[j],
        f"Demand_Constraint_{j}"
    )

# Constraint for total nurses hired
problem += total == pulp.lpSum(start[j] for j in range(T)), "Total_Hired_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')