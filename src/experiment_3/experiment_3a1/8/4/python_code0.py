import pulp
import json

# Data initialization
data = json.loads('{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}')
T = data['T']
period = data['Period']
demand = data['Demand']

# Problem definition
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Decision Variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(start[j] for j in range(T)), "Minimize_Total_Nurses"

# Constraints
for j in range(T):
    problem += pulp.lpSum(start[(j-i) % T] for i in range(period)) >= demand[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Output the results
start_values = [start[j].varValue for j in range(T)]
total_nurses = pulp.value(problem.objective)

print(f'Start values: {start_values}')
print(f' (Objective Value): <OBJ>{total_nurses}</OBJ>')