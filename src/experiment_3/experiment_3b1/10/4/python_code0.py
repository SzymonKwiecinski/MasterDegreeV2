import pulp
import json

# Data
data = json.loads('{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}')
T = data['T']
period = data['Period']
demand = data['Demand']

# Problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(start[j] for j in range(T)), "Total_Nurses_Hired"

# Constraints
for j in range(T):
    problem += (pulp.lpSum(start[(j - i) % T] for i in range(period)) >= demand[j]), f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')