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

#### Input data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

#### Number of days
N = len(data['num'])

#### Working and resting days configuration
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
total_cycle_days = n_working_days + n_resting_days

#### Create the problem
problem = pulp.LpProblem("Minimize_Employees", pulp.LpMinimize)

#### Decision variables: is_employee_i_working_on_day_n
max_possible_employees = sum(data['num'])  #### Overestimate
is_work = pulp.LpVariable.dicts("is_work", ((i, n) for i in range(max_possible_employees) for n in range(N)), 
                                cat='Binary')

#### Objective function: Minimize total employees
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
problem += total_number

#### Constraints

#### Ensure enough employees are working each day
for n in range(N):
    problem += pulp.lpSum(is_work[i, n] for i in range(max_possible_employees)) >= data['num'][n]

#### Ensure each employee follows the working/resting cycle
for i in range(max_possible_employees):
    for n in range(N):
        if n + total_cycle_days <= N:
            problem += pulp.lpSum(is_work[i, m] for m in range(n, n + n_working_days)) >= n_working_days * is_work[i, n]

#### Constraint to determine total number of employees used
for i in range(max_possible_employees):
    problem += pulp.lpSum(is_work[i, n] for n in range(N)) <= total_number * N

#### Solve the problem
problem.solve()

#### Extract results
final_total_number = int(pulp.value(total_number))
final_is_work = [[int(pulp.value(is_work[i, n])) for n in range(N)] for i in range(final_total_number)]

#### Prepare output in required format
output = {
    "total_number": final_total_number,
    "is_work": final_is_work
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

