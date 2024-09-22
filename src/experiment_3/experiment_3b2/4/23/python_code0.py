import pulp
import json

# Given data in JSON format
data_json = '''{
    "requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    "strength": [2000, 1500, 1000],
    "lessonewaste": [0.25, 0.2, 0.1],
    "moreonewaste": [0.1, 0.05, 0.05],
    "recruit": [500, 800, 500],
    "costredundancy": [200, 500, 500],
    "num_overman": 150,
    "costoverman": [1500, 2000, 3000],
    "num_shortwork": 50,
    "costshort": [500, 400, 400]
}'''

# Load data
data = json.loads(data_json)

# Constants
K = len(data['strength'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Create the problem instance
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
redundancy = pulp.LpVariable.dicts("redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(
    data['costredundancy'][k] * redundancy[k, i] +
    data['costoverman'][k] * overmanning[k, i] +
    data['costshort'][k] * short[k, i]
    for k in range(K) for i in range(I)
), "Total_Cost"

# Constraints
for k in range(K):
    for i in range(I):
        problem += (
            data['strength'][k] +
            pulp.lpSum(recruit[k, j] * (1 - data['lessonewaste'][k])**(j) for j in range(i + 1)) -
            redundancy[k, i] >= 
            data['requirement'][k][i] - short[k, i] * 0.5 + overmanning[k, i],
            f"Manpower_Balance_{k}_{i}"
        )

for k in range(K):
    for i in range(I):
        problem += (
            recruit[k, i] <= data['recruit'][k],
            f"Recruitment_Limit_{k}_{i}"
        )

for i in range(I):
    problem += (
        pulp.lpSum(overmanning[k, i] for k in range(K)) <= data['num_overman'],
        f"Overmanning_Limit_{i}"
    )

for k in range(K):
    for i in range(I):
        problem += (
            short[k, i] <= data['num_shortwork'],
            f"Short_Time_Working_Limit_{k}_{i}"
        )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')