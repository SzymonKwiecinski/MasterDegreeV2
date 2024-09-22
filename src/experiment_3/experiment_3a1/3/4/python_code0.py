import pulp

# Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

# Create a linear programming problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')
N = pulp.LpVariable("Total_Nurses", lowBound=0, cat='Integer')

# Objective Function
problem += N

# Constraints for meeting demand
for j in range(T):
    problem += pulp.lpSum(start[(j - k) % T] for k in range(period)) >= demand[j]

# The Total Number of Nurses hired is the sum of nurses starting on each day
problem += N == pulp.lpSum(start[j] for j in range(T))

# Solve the problem
problem.solve()

# Output the results
start_values = [start[j].varValue for j in range(T)]
total_nurses = pulp.value(N)

print(f' (Objective Value): <OBJ>{total_nurses}</OBJ>')
print(f'Start Nurses per Day: {start_values}')