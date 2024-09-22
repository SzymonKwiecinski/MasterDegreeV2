# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
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


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Cafeteria Staffing Problem}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( N \) be the total number of days.
    \item Let \( num_n \) denote the required number of employees on day \( n \) for \( n = 1, 2, \ldots, N \).
    \item Let \( n_{\text{working}} \) be the number of consecutive working days an employee has.
    \item Let \( n_{\text{resting}} \) be the number of consecutive resting days an employee has.
    \item Let \( total\_number \) be the total number of employees to hire.
    \item Let \( is\_work_{n,i} \) be a binary decision variable indicating whether employee \( i \) is working on day \( n \) (1 if working, 0 if resting).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( total\_number \): total number of employees to hire.
    \item \( is\_work_{n,i} \) for \( n = 1, \ldots, N \) and \( i = 1, \ldots, total\_number \).
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees:
\[
\text{Minimize } total\_number
\]

\subsection*{Constraints}
For each day \( n \), the sum of employees working must meet the requirement:
\[
\sum_{i=1}^{total\_number} is\_work_{n,i} \geq num_n, \quad \forall n = 1, \ldots, N
\]

Additionally, for each employee \( i \), the working and resting schedule must follow the constraints:
\[
is\_work_{n,i} = 1 \quad \text{for } n \in [k, k+n_{\text{working}} - 1] \text{ and } 0 \text{ for } n \in [k+n_{\text{working}}, k+n_{\text{working}} + n_{\text{resting}} - 1]
\]
for \( k \) indicating any starting day where employee \( i \) starts their cycle.

This implies that the pattern of work and rest for each employee is cyclic with a length of \( n_{\text{working}} + n_{\text{resting}} \).

\subsection*{Output}
The output format will be:
\[
\{ 
  "total\_number": total\_number, 
  "is\_work": [[is\_work_{n,i} \text{ for } n = 1,\ldots,N] \text{ for } i = 1,\ldots,total\_number] 
\}
\]

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Cafeteria Staffing Problem}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( N \) be the total number of days.
    \item Let \( num_n \) denote the required number of employees on day \( n \) for \( n = 1, 2, \ldots, N \).
    \item Let \( n_{\text{working}} \) be the number of consecutive working days an employee has.
    \item Let \( n_{\text{resting}} \) be the number of consecutive resting days an employee has.
    \item Let \( total\_number \) be the total number of employees to hire.
    \item Let \( is\_work_{n,i} \) be a binary decision variable indicating whether employee \( i \) is working on day \( n \) (1 if working, 0 if resting).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( total\_number \): total number of employees to hire.
    \item \( is\_work_{n,i} \) for \( n = 1, \ldots, N \) and \( i = 1, \ldots, total\_number \).
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees:
\[
\text{Minimize } total\_number
\]

\subsection*{Constraints}
For each day \( n \), the sum of employees working must meet the requirement:
\[
\sum_{i=1}^{total\_number} is\_work_{n,i} \geq num_n, \quad \forall n = 1, \ldots, N
\]

Additionally, for each employee \( i \), the working and resting schedule must follow the constraints:
\[
is\_work_{n,i} = 1 \quad \text{for } n \in [k, k+n_{\text{working}} - 1] \text{ and } 0 \text{ for } n \in [k+n_{\text{working}}, k+n_{\text{working}} + n_{\text{resting}} - 1]
\]
for \( k \) indicating any starting day where employee \( i \) starts their cycle.

This implies that the pattern of work and rest for each employee is cyclic with a length of \( n_{\text{working}} + n_{\text{resting}} \).

\subsection*{Output}
The output format will be:
\[
\{ 
  "total\_number": total\_number, 
  "is\_work": [[is\_work_{n,i} \text{ for } n = 1,\ldots,N] \text{ for } i = 1,\ldots,total\_number] 
\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON format
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

#### Parameters
N = len(data['num'])  #### total number of days
num_n = data['num']  #### required number of employees on each day
n_working = data['n_working_days']  #### number of consecutive working days
n_resting = data['n_resting_days']  #### number of consecutive resting days

#### Create the LP problem
problem = pulp.LpProblem("Cafeteria Staffing Problem", pulp.LpMinimize)

#### Decision variables
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  #### assuming maximum of 100 employees

#### Objective function
problem += total_number, "Minimize total number of employees"

#### Constraints for the number of employees working each day
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(100)) >= num_n[n], f"Day_{n+1}_requirement"

#### Working and resting schedule for each employee
for i in range(100):
    for k in range(N):
        if k + n_working <= N:
            #### Working days
            problem += pulp.lpSum(is_work[n][i] for n in range(k, k + n_working)) == n_working, f"Employee_{i}_work_days_from_{k+1}"
        if k + n_working + n_resting <= N:
            #### Resting days
            problem += pulp.lpSum(is_work[n][i] for n in range(k + n_working, k + n_working + n_resting)) == 0, f"Employee_{i}_rest_days_from_{k+1}"

#### Additional constraint to ensure total_number is equal to the number of employees used
for i in range(100):
    problem += pulp.lpSum(is_work[n][i] for n in range(N)) <= total_number, f"Employee_{i}_usage"

#### Solve the problem
problem.solve()

#### Output results
solution = {
    "total_number": pulp.value(total_number),
    "is_work": [[int(is_work[n][i].varValue) for n in range(N)] for i in range(100)]
}

print(json.dumps(solution))

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

