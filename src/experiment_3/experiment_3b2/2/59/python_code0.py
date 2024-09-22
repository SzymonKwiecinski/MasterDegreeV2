import pulp
import json

# Data in JSON format
data = json.loads("""
{
    "translators": [
        {"id": 1, "cost": 12000, "languages": ["FR", "AR", "IT"]},
        {"id": 2, "cost": 16000, "languages": ["GE", "RU", "CH"]},
        {"id": 3, "cost": 13000, "languages": ["AR", "CH"]},
        {"id": 4, "cost": 15000, "languages": ["FR", "SP", "IT", "PO"]},
        {"id": 5, "cost": 9000, "languages": ["FR", "GE", "RU", "SP"]},
        {"id": 6, "cost": 7000, "languages": ["GE", "SP", "PO"]}
    ],
    "required_languages": ["FR", "AR", "GE", "RU", "SP", "CH", "IT", "PO"]
}
""")

# Sets
translators = data['translators']
required_languages = data['required_languages']

# Parameters
costs = {translator['id']: translator['cost'] for translator in translators}
language_capability = {translator['id']: {
    lang: 1 if lang in translator['languages'] else 0 
    for lang in required_languages
} for translator in translators}

num_translators = len(translators)
num_languages = len(required_languages)

# Create the ILP problem
problem = pulp.LpProblem("MinCostTranslatorSelection", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", [translator['id'] for translator in translators], cat='Binary')

# Objective Function
problem += pulp.lpSum(costs[i] * x[i] for i in costs), "Total_Cost"

# Constraints
for j in range(num_languages):
    problem += pulp.lpSum(language_capability[i][required_languages[j]] * x[i] for i in costs) >= 1, f"Lang_{j+1}_Requirement"

# Solve the problem
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')