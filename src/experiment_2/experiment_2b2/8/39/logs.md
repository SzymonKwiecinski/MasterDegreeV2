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
import pulp

data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

#### Extract data
num_days = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num_days)

#### Create the problem
problem = pulp.LpProblem("Minimize_Employees", pulp.LpMinimize)

#### Decision variables
#### x[i][n]: Employee i works on day n
x = []
for i in range(100):  #### Assume no more than 100 employees as an upper bound
    x.append([pulp.LpVariable(f'x_{i}_{n}', cat='Binary') for n in range(N)])

#### Objective function
problem += pulp.lpSum(x[i][0] for i in range(100)), "Minimize number of employees"

#### Constraints
#### Each day's requirement must be met
for n in range(N):
    problem += pulp.lpSum(x[i][n] for i in range(100)) >= num_days[n], f"Day_{n}_requirement"

#### Each employee works `n_working_days` days at a stretch and then rests `n_resting_days` days
for i in range(100):
    for n in range(N):
        if n + n_working_days + n_resting_days <= N:
            problem += (
                pulp.lpSum(x[i][n + k] for k in range(n_working_days)) <= n_working_days *
                pulp.lpSum(x[i][n + k] for k in range(n_working_days + n_resting_days)),
                f"Working_rest_cycle_{i}_{n}"
            )
        else:
            #### For the ending days where the full cycle can't be completed
            remaining_days = N - n
            problem += (
                pulp.lpSum(x[i][n + k] for k in range(remaining_days)) <= n_working_days *
                pulp.lpSum(x[i][n + k] for k in range(remaining_days)),
                f"End_cycle_{i}_{n}"
            )

#### Solve the problem
problem.solve()

#### Gather results
total_number = sum(1 for i in range(100) if x[i][0].varValue > 0)
is_work = [[int(x[i][n].varValue) for n in range(N)] for i in range(total_number)]

#### Print results
result = {
    "total_number": total_number,
    "is_work": is_work
}
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

