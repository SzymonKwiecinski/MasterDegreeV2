# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP or MILP

PROBLEM INFO:

- The town has \var{S} different shifts for the police officers during the day.
- During each shift \var{s}, the town requires \var{officers_needed_{s}} police officers on duty.
- Each police officer works for two consecutive shifts.
- The cost for the town when starting a shift at \var{s} is \var{shift_cost_{s}}.

INPUT FORMAT: 

{
    "officers_needed": [officers_needed_{s} for s in 1, ..., S],
    "shift_costs": [shift_cost_{s} for s in 1, ..., S]
}

OBJECTIVE: How many officers should the town assign to each shift in order to minimize the total cost?

OUTPUT INFO:

- The number of officers assigned to each shift \var{officers_assigned_{s}}.
- \var{total_cost} indicates the total cost for the town.

OUTPUT FORMAT:

{
    "officers_assigned": [officers_assigned_{s} for s in 1, ..., S],
    "total_cost": total_cost
}
</DESCRIPTION>
<DATA>
{'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

#### Extracting data
NumShifts = data['NumShifts']
OfficersNeeded = data['OfficersNeeded']
ShiftCosts = data['ShiftCosts']

#### Defining the Linear Programming problem
problem = pulp.LpProblem("Minimize_Shift_Cost", pulp.LpMinimize)

#### Decision variables: Number of officers starting at each shift
officers_starting = [pulp.LpVariable(f"officers_starting_{s}", lowBound=0, cat='Integer') for s in range(NumShifts)]

#### Objective function: Minimize the total cost of assigning officers
problem += pulp.lpSum([ShiftCosts[s] * officers_starting[s] for s in range(NumShifts)])

#### Constraints: Ensure that for each shift the required number of officers is on duty
for s in range(NumShifts):
    problem += (officers_starting[s] + officers_starting[(s + 1) % NumShifts] >= OfficersNeeded[s])

#### Solve the problem
problem.solve()

#### Gather the results
officers_assigned = [int(officers_starting[s].varValue) for s in range(NumShifts)]
total_cost = pulp.value(problem.objective)

#### Output the results
output = {
    "officers_assigned": officers_assigned,
    "total_cost": total_cost
}

print(f'Result: {output} (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

