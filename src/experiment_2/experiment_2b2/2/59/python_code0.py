from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus
import json

# Load data
data = json.loads('{"translators": [{"id": 1, "cost": 12000, "languages": ["FR", "AR", "IT"]}, {"id": 2, "cost": 16000, "languages": ["GE", "RU", "CH"]}, {"id": 3, "cost": 13000, "languages": ["AR", "CH"]}, {"id": 4, "cost": 15000, "languages": ["FR", "SP", "IT", "PO"]}, {"id": 5, "cost": 9000, "languages": ["FR", "GE", "RU", "SP"]}, {"id": 6, "cost": 7000, "languages": ["GE", "SP", "PO"]}], "required_languages": ["FR", "AR", "GE", "RU", "SP", "CH", "IT", "PO"]}')

translators = data['translators']
required_languages = data['required_languages']

# Set up the problem
problem = LpProblem("Minimize_Translation_Cost", LpMinimize)

# Define variables
translator_vars = LpVariable.dicts("Translator", [t['id'] for t in translators], cat='Binary')

# Objective function
problem += lpSum(translator_vars[t['id']] * t['cost'] for t in translators)

# Constraints to ensure all required languages are covered
for lang in required_languages:
    problem += lpSum(translator_vars[t['id']] for t in translators if lang in t['languages']) >= 1, f"Cover_{lang}"

# Solve the problem
problem.solve()

# Extract results
selected_translators = [t['id'] for t in translators if translator_vars[t['id']].value() == 1]
total_cost = sum(t['cost'] for t in translators if translator_vars[t['id']].value() == 1)

# Output results
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')