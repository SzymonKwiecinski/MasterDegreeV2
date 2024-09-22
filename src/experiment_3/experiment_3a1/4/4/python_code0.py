import pulp
import json

# Data provided in JSON format
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
P = data['Period']
demand = data['Demand']

# Create the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum([start[j] for j in range(T)])

# Constraints for meeting demand
for j in range(T):
    problem += (pulp.lpSum([start[(j-k) % T] for k in range(P)]) >= demand[j])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')