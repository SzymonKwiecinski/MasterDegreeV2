import pulp
import json

# Data provided in JSON format
data = '{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}'
data = json.loads(data)

# Parameters
T = data['T']
period = data['Period']
demand = data['Demand']

# Create the problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Decision Variables
start = pulp.LpVariable.dicts("start", range(1, T + 1), lowBound=0, cat='Integer')
total = pulp.LpVariable("total", lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(start[j] for j in range(1, T + 1)), "Total_Nurses_Hired"

# Constraints
for j in range(1, T + 1):
    problem += (
        pulp.lpSum(start[(j - i - 1) % T + 1] for i in range(period)) >= demand[j - 1],
        f"Demand_Constraint_day_{j}"
    )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')