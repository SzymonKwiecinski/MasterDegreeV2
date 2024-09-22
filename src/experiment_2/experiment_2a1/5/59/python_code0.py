import json
import pulp

data = {'translators': [{'id': 1, 'cost': 12000, 'languages': ['FR', 'AR', 'IT']}, {'id': 2, 'cost': 16000, 'languages': ['GE', 'RU', 'CH']}, {'id': 3, 'cost': 13000, 'languages': ['AR', 'CH']}, {'id': 4, 'cost': 15000, 'languages': ['FR', 'SP', 'IT', 'PO']}, {'id': 5, 'cost': 9000, 'languages': ['FR', 'GE', 'RU', 'SP']}, {'id': 6, 'cost': 7000, 'languages': ['GE', 'SP', 'PO']}], 'required_languages': ['FR', 'AR', 'GE', 'RU', 'SP', 'CH', 'IT', 'PO']}

# Initialize the problem
problem = pulp.LpProblem("Translator_Selection", pulp.LpMinimize)

# Create a decision variable for each translator
translators = data['translators']
translator_vars = {translator['id']: pulp.LpVariable(f"translator_{translator['id']}", cat='Binary') for translator in translators}

# Add the objective function (minimize cost)
problem += pulp.lpSum([translator['cost'] * translator_vars[translator['id']] for translator in translators]), "Total_Cost"

# Add constraints for each required language
for language in data['required_languages']:
    problem += pulp.lpSum([translator_vars[translator['id']] for translator in translators if language in translator['languages']]) >= 1, f"Cover_{language}"

# Solve the problem
problem.solve()

# Collect results
selected_translators = [translator['id'] for translator in translators if translator_vars[translator['id']].value() == 1]
total_cost = pulp.value(problem.objective)

# Output the results
output = {
    "selected_translators": selected_translators,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')