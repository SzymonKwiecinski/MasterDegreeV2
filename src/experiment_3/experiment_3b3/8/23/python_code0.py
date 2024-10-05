import pulp

# Problem data
data = {
    'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    'strength': [2000, 1500, 1000],
    'lessonewaste': [0.25, 0.2, 0.1],
    'moreonewaste': [0.1, 0.05, 0.05],
    'recruit': [500, 800, 500],
    'costredundancy': [200, 500, 500],
    'num_overman': 150,
    'costoverman': [1500, 2000, 3000],
    'num_shortwork': 50,
    'costshort': [500, 400, 400]
}

K = len(data['strength'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Define problem
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Decision variables
r = pulp.LpVariable.dicts("Recruits", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
o = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
s = pulp.LpVariable.dicts("ShortTime_Workers", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
d = pulp.LpVariable.dicts("Redundant_Workers", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(
    data['costredundancy'][k] * d[k, i] +
    data['costoverman'][k] * o[k, i] +
    data['costshort'][k] * s[k, i]
    for k in range(K) for i in range(I)
)

# Constraints
for k in range(K):
    for i in range(I):
        # Manpower balance constraint
        problem += (
            data['strength'][k] - data['lessonewaste'][k] * r[k, i] - data['moreonewaste'][k] * (1 - d[k, i]) +
            r[k, i] + o[k, i] + s[k, i] >= data['requirement'][k][i], 
            f"Manpower_Balance_{k}_{i}"
        )
        # Recruitment limit
        problem += r[k, i] <= data['recruit'][k], f"Recruitment_Limit_{k}_{i}"
        # Short-time working limit
        problem += s[k, i] <= data['num_shortwork'], f"ShortTime_Working_Limit_{k}_{i}"

# Overmanning constraint
problem += pulp.lpSum(o[k, i] for k in range(K) for i in range(I)) <= data['num_overman'], "Overmanning_Constraint"

# Solve the problem
problem.solve()

# Output results
for k in range(K):
    for i in range(I):
        print(f"Recruitment r_{k}_{i}: {pulp.value(r[k, i])}")
        print(f"Overmanning o_{k}_{i}: {pulp.value(o[k, i])}")
        print(f"ShortTime_Workers s_{k}_{i}: {pulp.value(s[k, i])}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')