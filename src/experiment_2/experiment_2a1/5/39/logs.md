# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP or MILP
PROBLEM INFO:

- To operate a cafeteria, the manager must ensure on-call duty based on the statistics on the required staff. 
- In the future days, the number of desired employees on day \var{n} is denoted with \var{num_{n}}.
- Each employee works \var{n_working_days} days in a row and then has \var{n_resting_days} days off.

INPUT FORMAT:

{
	"num": [num_{n} for n in 1,...,N],
	"n_working_days": n_working_days,
	"n_resting_days": n_resting_days
}


OBJECTIVE: Calculate the minimum number of employees to hire

OUTPUT INFO:

- \var{total_number} represents the total number of employees to employ
- \var{is_work} represents whether employee is working a rest on each day. Its length is determined by \var{total_number}

OUTPUT FORMAT:

{
	"total_number": total_number,
	"is_work": [[is_work_{n, i} for n in 1,...,N] for i in 1,...,total_number]
}
</DESCRIPTION>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import json
import pulp

#### Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

#### Parameters
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

#### Create a linear programming problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

#### Decision variable: number of employees to hire
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')

#### Decision variables for each employee and each day
is_work = [[pulp.LpVariable(f'is_work_{n}_{i}', cat='Binary') for i in range(int(total_number) + 1)] for n in range(N)]

#### Objective function: minimize the total number of employees
problem += total_number, "Minimize_Employees"

#### Constraints to ensure required staff is met
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(int(total_number))) >= num[n], f"Staff_Requirement_Day_{n+1}"

#### Constraints to enforce working and resting days
for i in range(int(total_number)):
    for n in range(N):
        working_days = [is_work[(n + d) % N][i] for d in range(n_working_days)]
        resting_days = [is_work[(n + d) % N][i] for d in range(n_working_days, n_working_days + n_resting_days)]
        problem += pulp.lpSum(working_days) <= n_working_days, f"Employee_{i+1}_Working_Days_{n+1}"
        problem += pulp.lpSum(resting_days) == 0, f"Employee_{i+1}_Resting_Days_{n+1}"

#### Solve the problem
problem.solve()

#### Prepare output
result = {
    "total_number": int(pulp.value(total_number)),
    "is_work": [[int(is_work[n][i].value()) for n in range(N)] for i in range(int(pulp.value(total_number)))]
}

#### Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

