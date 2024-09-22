import pulp
import json

# Data input
data = json.loads("{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}")
T = data['T']
period = data['Period']
demand = data['Demand']

# Create the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')
total = pulp.LpVariable("total", lowBound=0, cat='Integer')

# Objective Function
problem += total == pulp.lpSum(start[j] for j in range(T)), "TotalNurses"
problem += pulp.lpSum(start[j] for j in range(T)), "Minimize Total Nurses"

# Constraints
for j in range(T):
    problem += (pulp.lpSum(start[(j-k) % T] for k in range(period)) >= demand[j]), f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')