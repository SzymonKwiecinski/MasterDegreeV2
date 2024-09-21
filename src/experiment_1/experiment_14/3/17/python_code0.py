import pulp

# Extract data from JSON format
data = {
    'translators': [
        {'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']},
        {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']},
        {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']},
        {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']},
        {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']},
        {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}
    ],
    'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']
}

# Number of translators
N = len(data['translators'])
# Required languages
required_languages = data['required_languages']
M = len(required_languages)

# Initialize the problem
problem = pulp.LpProblem("Hiring_Translators", pulp.LpMinimize)

# Decision Variables: x_i indicates whether translator i is hired (1) or not (0)
x = pulp.LpVariable.dicts("x", range(1, N + 1), cat='Binary')

# Objective Function: Minimize the total cost of hiring translators
problem += pulp.lpSum(data['translators'][i]['cost'] * x[i+1] for i in range(N)), "Total_Cost"

# Constraints: Each required language must be covered by at least one hired translator
for lang in required_languages:
    problem += pulp.lpSum(x[i+1] for i in range(N) if lang in data['translators'][i]['languages']) >= 1, f"Language_Coverage_{lang}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')