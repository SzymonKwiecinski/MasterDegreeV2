import pulp

# Data
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

# Indexes
categories = range(len(data['strength']))
years = range(len(data['requirement'][0]))

# LP problem
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("Recruit", (categories, years), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("Overmanning", (categories, years), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("Short", (categories, years), lowBound=0, cat='Continuous')
redundancy = pulp.LpVariable.dicts("Redundancy", (categories, years), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(redundancy[k][i] for k in categories for i in years), "Total Redundancy"

# Constraints
for k in categories:
    # Initial strength setting
    current_strength = data['strength'][k]
    
    for i in years:
        # Redundancy calculation
        problem += redundancy[k][i] >= current_strength - data['requirement'][k][i] + overmanning[k][i] - short[k][i]
        
        if i < len(years) - 1:
            # Workforce Balance
            next_strength = current_strength * (1 - data['moreonewaste'][k]) + recruit[k][i] * (1 - data['lessonewaste'][k]) - redundancy[k][i]
            current_strength = next_strength
        
        # Recruitment Limits
        problem += recruit[k][i] <= data['recruit'][k]
        
        # Short-time Work Limit
        problem += short[k][i] <= data['num_shortwork']
        
        # Production Requirement
        problem += data['requirement'][k][i] <= current_strength + overmanning[k][i] - 0.5 * short[k][i]

# Overmanning Limits - Constraints across all categories
for i in years:
    problem += pulp.lpSum(overmanning[k][i] for k in categories) <= data['num_overman']

# Solve the problem
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')