import pulp
import json

# Input data
data = json.loads('{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}')
T = data['T']
Period = data['Period']
Demand = data['Demand']

# Create the linear programming problem
problem = pulp.LpProblem("NurseScheduling", pulp.LpMinimize)

# Decision variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')
total = pulp.LpVariable("total", lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(start[j] for j in range(T)), "MinimizeTotalNurses"

# Constraints for meeting demand
for j in range(T):
    problem += (pulp.lpSum(start[(j - i) % T] for i in range(Period)) >= Demand[j], f"DemandConstraint_{j}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')