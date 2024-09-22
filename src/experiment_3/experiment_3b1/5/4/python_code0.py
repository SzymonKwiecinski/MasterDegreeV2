import pulp
import json

# Data from JSON
data = json.loads('{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}')

# Parameters
T = data['T']
period = data['Period']
demand = data['Demand']

# Create the LP problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
start = pulp.LpVariable.dicts("start", range(1, T + 1), lowBound=0, cat='Integer')
total = pulp.LpVariable("total", lowBound=0, cat='Integer')

# Objective Function
problem += total, "Total_Nurses_Hired"

# Constraints
for j in range(1, T + 1):
    problem += (
        pulp.lpSum(start[(j - k) % T + 1] for k in range(period)) >= demand[j - 1],
        f"Demand_Constraint_Day_{j}"
    )

problem += total == pulp.lpSum(start[j] for j in range(1, T + 1)), "Total_Nurses_Constraint"

# Solve the problem
problem.solve()

# Output the nurse schedule and total nurses hired
for j in range(1, T + 1):
    print(f'start_{j} = {start[j].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')