import pulp
import json

# Data provided
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

data = json.loads(data_json)

K = len(data['strength'])
I = len(data['requirement'][0])

# Create the Linear Programming problem
problem = pulp.LpProblem("Minimize_Redundancy_Cost", pulp.LpMinimize)

# Decision Variables
r = pulp.LpVariable.dicts("r", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
o = pulp.LpVariable.dicts("o", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
s = pulp.LpVariable.dicts("s", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * s[k, i] for k in range(K) for i in range(I)) \
           + pulp.lpSum(data['costoverman'][k] * o[k, i] for k in range(K) for i in range(I)) \
           + pulp.lpSum(data['costshort'][k] * s[k, i] for k in range(K) for i in range(I)), "Total_Cost"

# Constraints
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] - data['lessonewaste'][k] * r[k, i] - 
                     data['moreonewaste'][k] * (data['strength'][k] - s[k, i]) + 
                     r[k, i] + o[k, i] + s[k, i] / 2 >= data['requirement'][k][i]), f"Manpower_Balance_k{k}_i{i}"

        problem += r[k, i] <= data['recruit'][k], f"Recruitment_Limit_k{k}_i{i}"
        problem += o[k, i] <= data['num_overman'], f"Overmanning_Limit_k{k}_i{i}"
        problem += s[k, i] <= data['num_shortwork'], f"Short_Working_Limit_k{k}_i{i}"

# Solve the problem
problem.solve()

# Output results
recruit_results = {f"r_{k}_{i}": r[k, i].varValue for k in range(K) for i in range(I)}
overmanning_results = {f"o_{k}_{i}": o[k, i].varValue for k in range(K) for i in range(I)}
short_results = {f"s_{k}_{i}": s[k, i].varValue for k in range(K) for i in range(I)}

print("Recruit:", recruit_results)
print("Overmanning:", overmanning_results)
print("Short-time Working:", short_results)

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')