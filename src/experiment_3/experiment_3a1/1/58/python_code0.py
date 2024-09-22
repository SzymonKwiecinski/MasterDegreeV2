import pulp
import json

# Data provided in the JSON format
data = json.loads("""
{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "setup_time": [12, 8, 4, 0]
}
""")

# Defining indices
P = len(data['prices'])  # number of parts
M = len(data['machine_costs'])  # number of machines

# Create a problem variable
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flag = pulp.LpVariable.dicts("setup_flag", range(P), cat='Binary')

# Objective function
total_profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) - \
               pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M))

problem += total_profit, "Total Profit"

# Constraints
# Machine availability constraints
for m in range(M):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) +
                 pulp.lpSum(setup_flag[p] * data['setup_time'][p] for p in range(P)) <= data['availability'][m]), f"Availability_Constraint_{m+1}")

# Setup flag constraints
for p in range(P):
    problem += batches[p] <= M * setup_flag[p], f"Setup_Flag_Constraint_{p+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')