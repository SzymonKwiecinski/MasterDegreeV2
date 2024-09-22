import pulp
import json

# Data in JSON format
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Extracting data from JSON
requirements = data['requirement']
strengths = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruits = data['recruit']
cost_redundancy = data['costredundancy']
num_overman = data['num_overman']
num_shortwork = data['num_shortwork']

K = len(requirements)  # Number of manpower categories
I = len(requirements[0])  # Number of years

# Initialize the problem
problem = pulp.LpProblem("Workforce_Management", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(K), range(I)), lowBound=0, upBound=[recruits[k] for k in range(K)], cat='Integer')
y = pulp.LpVariable.dicts("y", (range(K), range(I)), lowBound=0, upBound=num_overman, cat='Integer')
z = pulp.LpVariable.dicts("z", (range(K), range(I)), lowBound=0, upBound=num_shortwork, cat='Integer')
r = pulp.LpVariable.dicts("r", (range(K), range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(cost_redundancy[k] * r[k][i] for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        manpower_balance = strengths[k]
        for j in range(i + 1):
            manpower_balance += x[k][j]
            if j > 0:
                manpower_balance -= (lessonewaste[k] * x[k][j] + moreonewaste[k] * (strengths[k] + pulp.lpSum((x[k][m] - r[k][m]) for m in range(j))))
        
        problem += (manpower_balance == requirements[k][i] + y[k][i] + z[k][i] + r[k][i], f"Manpower_Balance_{k}_{i}")

# Recruitment limits
for k in range(K):
    for i in range(I):
        problem += (x[k][i] >= 0)
        problem += (x[k][i] <= recruits[k])

# Overmanning limits
for k in range(K):
    for i in range(I):
        problem += (y[k][i] >= 0)
        problem += (y[k][i] <= num_overman)

# Short-time working limits
for k in range(K):
    for i in range(I):
        problem += (z[k][i] >= 0)
        problem += (z[k][i] <= num_shortwork)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')