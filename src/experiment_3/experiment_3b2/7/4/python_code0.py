import pulp
import json

# Data in JSON format
data = '{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}'
params = json.loads(data)

# Parameters
T = params['T']
period = params['Period']
demand = params['Demand']

# Create the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
start = pulp.LpVariable.dicts("start", range(1, T + 1), lowBound=0, cat='Integer')
total = pulp.LpVariable("total", lowBound=0, cat='Integer')

# Objective Function
problem += total, "Total_Nurses_Hired"

# Total Nurses Hired Constraint
problem += total == pulp.lpSum(start[j] for j in range(1, T + 1)), "Total_Nurses_Constraint"

# Demand Satisfaction Constraints
for j in range(1, T + 1):
    problem += (
        pulp.lpSum(start[(j - k - 1) % T + 1] for k in range(period)) >= demand[j - 1],
        f"Demand_Constraint_Day_{j}"
    )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')