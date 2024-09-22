import pulp
import json

# Load data from JSON format
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Extracting data
requirements = data['requirement']
strengths = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit_limits = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

K = len(strengths)  # Number of manpower categories
I = len(requirements[0])  # Number of years

# Create the problem
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Decision Variables
r = pulp.LpVariable.dicts("recruits", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Continuous')
o = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Continuous')
s = pulp.LpVariable.dicts("short_time_workers", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Continuous')

# Objective Function
problem += pulp.lpSum(costredundancy[k] * (o[k, i] + strengths[k] - requirements[k][i]) for k in range(K) for i in range(I)), "Total_Redundancy_Cost"

# Constraints
for k in range(K):
    for i in range(I):
        problem += s[k, i] <= num_shortwork, f"Short_Time_Work_Constraint_{k}_{i}"
        problem += r[k, i] <= recruit_limits[k], f"Recruit_Constraint_{k}_{i}"
        problem += o[k, i] <= num_overman, f"Overmanning_Constraint_{k}_{i}"
        problem += (strengths[k] - lessonewaste[k] * r[k, i] - moreonewaste[k] * (1 - o[k, i]) + s[k, i]/2 == requirements[k][i]), f"Manpower_Requirement_{k}_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')