import pulp
import json

# Data input in JSON format
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Define the model
problem = pulp.LpProblem("Manpower_Requirements", pulp.LpMinimize)

# Define the indices
K = range(len(data['requirement']))  # categories
I = range(len(data['requirement'][0]))  # years

# Define the decision variables
r = pulp.LpVariable.dicts("recruits", (K, I), lowBound=0, cat='Continuous')
o = pulp.LpVariable.dicts("overmanned", (K, I), lowBound=0, cat='Continuous')
s = pulp.LpVariable.dicts("short_time", (K, I), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * pulp.lpMax(0, (s[k][i] + o[k][i] + data['strength'][k] - data['requirement'][k][i])) for k in K for i in I)

# Constraints
for k in K:
    for i in I:
        problem += (data['strength'][k] - 
                     data['lessonewaste'][k] * r[k][i] - 
                     data['moreonewaste'][k] * (o[k][i] + s[k][i]) >= 
                     data['requirement'][k][i], 
                     f"Manpower_Availability_Constraint_k{k}_i{i}")
        problem += r[k][i] <= data['recruit'][k], f"Recruitment_Limit_k{k}_i{i}"
        problem += o[k][i] <= data['num_overman'], f"Overmanning_Limit_k{k}_i{i}"
        problem += s[k][i] <= data['num_shortwork'], f"Short_time_Limit_k{k}_i{i}"
        problem += s[k][i] <= 0.5 * data['strength'][k], f"Short_time_Capacity_k{k}_i{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')