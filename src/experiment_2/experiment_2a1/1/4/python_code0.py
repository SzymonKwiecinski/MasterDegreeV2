import pulp
import json

# Load data from the JSON format provided
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Create a linear programming problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables: number of nurses starting on each day
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

# Objective function: minimize the total number of nurses hired
problem += pulp.lpSum(start[j] for j in range(T)), "Total_Nurses"

# Constraints: ensure demand is met for each day
for j in range(T):
    # Calculate the total number of nurses available on day j
    availability = pulp.lpSum(start[(j - k) % T] for k in range(period))
    problem += availability >= demand[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare output
start_nurses = [int(start[j].varValue) for j in range(T)]
total_nurses = int(pulp.value(problem.objective))

# Output the result
result = {
    "start": start_nurses,
    "total": total_nurses
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')