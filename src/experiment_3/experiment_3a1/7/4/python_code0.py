import pulp
import json

# Data provided in the JSON format
data = json.loads("{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}")

# Extracting data
T = data['T']
period = data['Period']
demand = data['Demand']

# Create the problem variable
problem = pulp.LpProblem("Night_Shift_Nurse_Scheduling", pulp.LpMinimize)

# Decision variables x_j
x = pulp.LpVariable.dicts("NursesStart", range(T), lowBound=0, cat='Integer')

# Objective Function: Minimize total number of nurses hired
problem += pulp.lpSum([x[j] for j in range(T)]), "TotalNursesHired"

# Constraints to ensure demand is met
for j in range(T):
    problem += (pulp.lpSum([x[(j-i) % T] for i in range(period)]) >= demand[j]), f"Demand_Satisfaction_{j+1}"

# Solve the problem
problem.solve()

# Extract results
start = [int(x[j].value()) for j in range(T)]
total_nurses_hired = pulp.value(problem.objective)

# Output the results
print(f'Start: {start}, Total Nurses Hired: {total_nurses_hired}')
print(f' (Objective Value): <OBJ>{total_nurses_hired}</OBJ>')