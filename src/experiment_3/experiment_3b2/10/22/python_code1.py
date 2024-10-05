import pulp
import json

# Load data from the provided JSON
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Extracting data from the loaded JSON
requirements = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

# Initialize the problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Indices
K = range(len(strength))
I = range(len(requirements[0]))

# Decision Variables
x = pulp.LpVariable.dicts("x", (K, I), lowBound=0, cat='Continuous')  # Recruits
y = pulp.LpVariable.dicts("y", (K, I), lowBound=0, cat='Continuous')  # Redundant employees
z = pulp.LpVariable.dicts("z", (K, I), lowBound=0, cat='Continuous')  # Overmanned employees
s = pulp.LpVariable.dicts("s", (K, I), lowBound=0, cat='Continuous')  # Short-time employees

# Objective Function
problem += pulp.lpSum(costredundancy[k] * y[k][i] for k in K for i in I), "Total_Redundancy_Cost"

# Constraints

# Manpower Balance Constraints
for k in K:
    for i in I:
        if i == 0:  # First year
            problem += (strength[k] * (1 - moreonewaste[k]) + x[k][i] * (1 - lessonewaste[k] ) 
                         == requirements[k][i] + z[k][i] + s[k][i] / 2 - y[k][i]), f"Manpower_Balance_Year_{i}_Category_{k}")
        else:  # Subsequent years
            problem += ((pulp.lpSum(x[k_prime][i - 1] * (1 - lessonewaste[k_prime]) for k_prime in K) 
                            - y[k][i - 1]) * (1 - moreonewaste[k]) + x[k][i] * (1 - lessonewaste[k]) 
                         == requirements[k][i] + z[k][i] + s[k][i] / 2 - y[k][i]), 
                         f"Manpower_Balance_Year_{i}_Category_{k}")

# Recruitment Limits
for k in K:
    for i in I:
        problem += x[k][i] <= recruit[k], f"Recruitment_Limit_Category_{k}_Year_{i}"
        problem += x[k][i] >= 0, f"Recruitment_Nonnegativity_Category_{k}_Year_{i}"

# Overmanning Limits
for i in I:
    problem += pulp.lpSum(z[k][i] for k in K) <= num_overman, f"Overmanning_Limit_Year_{i}"

# Short-time Working Limits
for k in K:
    for i in I:
        problem += s[k][i] <= num_shortwork, f"Short_time_Working_Limit_Category_{k}_Year_{i}"
        problem += s[k][i] >= 0, f"Short_time_Working_Nonnegativity_Category_{k}_Year_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')