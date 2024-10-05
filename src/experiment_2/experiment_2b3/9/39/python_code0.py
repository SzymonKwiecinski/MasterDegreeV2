import pulp

# Parse the data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

N = len(num)

# Create the LP problem
problem = pulp.LpProblem("CafeteriaStaffing", pulp.LpMinimize)

# Calculate the cycle length
cycle_length = n_working_days + n_resting_days

# Define variables
x = pulp.LpVariable.dicts("staff_count", range(N), lowBound=0, cat="Integer")

# Create decision variables for each employee and each day whether they are working
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(cycle_length)), cat="Binary")

# Objective function: minimize the maximum number of employees required on any given day
problem += pulp.lpSum(x), "TotalEmployees"

# Constraints
for n in range(N):
    # Demand constraint for each day
    problem += pulp.lpSum(is_work[(n - i) % N][i % cycle_length] for i in range(N)) >= num[n], f"DemandDay{n}"

for i in range(cycle_length):
    # Relationship between number of employees and working pattern
    problem += pulse.lpSum(is_work[j][i] for j in range(N)) <= x[i % cycle_length], f"WorkRelationDay{i}"

for i in range(N):
    # Enforce the working and resting pattern
    for w in range(cycle_length):
        if w < n_working_days:
            problem += is_work[i][w] == 1, f"WorkingDays{i}_{w}"
        else:
            problem += is_work[i][w] == 0, f"RestingDays{i}_{w}"

# Solve the problem
problem.solve()

total_number = pulp.value(problem.objective)
is_work_result = [[int(is_work[i][w % cycle_length].varValue) for w in range(N)] for i in range(total_number)]

# Format and display the result
solution = {
    "total_number": int(total_number),
    "is_work": is_work_result
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')