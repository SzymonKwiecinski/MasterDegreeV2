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

K = len(data['strength'])  # Number of skill categories
I = len(data['requirement'][0])  # Number of years

# Define the problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision variables
r = pulp.LpVariable.dicts("recruits", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
o = pulp.LpVariable.dicts("overmanned", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
s = pulp.LpVariable.dicts("short_time", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - (1 - data['moreonewaste'][k]) * data['strength'][k] - (1 - data['lessonewaste'][k]) * r[(k, i)] + o[(k, i)] - data['requirement'][k][i] - 0.5 * s[(k, i)])
                      for k in range(K) for i in range(I)), "Total_Redundancy_Cost"

# Constraints
for k in range(K):
    for i in range(I):
        # Manpower demand
        problem += (data['strength'][k] - (1 - data['moreonewaste'][k]) * data['strength'][k] - (1 - data['lessonewaste'][k]) * r[(k, i)] + o[(k, i)] + 0.5 * s[(k, i)] >= data['requirement'][k][i]), f"ManpowerDemand_{k}_{i}"
        
        # Recruitment limit
        problem += r[(k, i)] <= data['recruit'][k], f"RecruitmentLimit_{k}_{i}"
        
        # Overmanning limit
        problem += o[(k, i)] <= data['num_overman'], f"OvermanningLimit_{k}_{i}"
        
        # Short-time working limit
        problem += s[(k, i)] <= data['num_shortwork'], f"ShortTimeWorkingLimit_{k}_{i}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for k in range(K):
    for i in range(I):
        print(f"Year {i+1}, Skill {k+1} - Recruits: {pulp.value(r[(k, i)])}, Overmanned: {pulp.value(o[(k, i)])}, Short-time: {pulp.value(s[(k, i)])}")