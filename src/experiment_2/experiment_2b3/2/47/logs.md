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

#### Data input
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

#### Define the LP problem
problem = pulp.LpProblem("Police_Shift_Allocation", pulp.LpMinimize)

#### Decision variables
officers_assigned = pulp.LpVariable.dicts("Officers_Assigned", range(num_shifts), lowBound=0, cat=pulp.LpInteger)

#### Objective function
problem += pulp.lpSum([shift_costs[s] * officers_assigned[s] for s in range(num_shifts)])

#### Constraints
for s in range(num_shifts):
    problem += (officers_assigned[s] + officers_assigned[(s+1) % num_shifts] >= officers_needed[s], f"Requirement_{s}")

#### Solve the problem
problem.solve()

#### Extract the results
officers_assigned_result = [pulp.value(officers_assigned[s]) for s in range(num_shifts)]
total_cost = pulp.value(problem.objective)

#### Prepare the output
output = {
    "officers_assigned": officers_assigned_result,
    "total_cost": total_cost
}

#### Print the results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

