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

\section*{Mathematical Model for Cafeteria Staffing}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( N \) be the total number of days.
    \item Let \( \text{num}_{n} \) be the number of required employees on day \( n \) for \( n = 1, \ldots, N \).
    \item Let \( n_{\text{working}} \) be the number of consecutive working days for each employee.
    \item Let \( n_{\text{resting}} \) be the number of consecutive resting days for each employee.
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item Let \( total\_number \) be the total number of employees to hire.
    \item Let \( is\_work_{n,i} \) be a binary variable that equals 1 if employee \( i \) is working on day \( n \), and 0 otherwise, for \( n = 1, \ldots, N \) and \( i = 1, \ldots, total\_number \).
\end{itemize}

\subsection*{Objective}
Minimize the total number of employees:
\[
\text{Minimize} \quad total\_number
\]

\subsection*{Constraints}
For each day \( n \):
\[
\sum_{i=1}^{total\_number} is\_work_{n,i} \geq \text{num}_{n} \quad \forall n = 1, \ldots, N
\]

Each employee \( i \) can work for \( n_{\text{working}} \) days and must rest for \( n_{\text{resting}} \) days:
\[
is\_work_{n,i} + is\_work_{n+1,i} + \ldots + is\_work_{n+n_{\text{working}}-1,i} \leq n_{\text{working}} \quad \forall n = 1, \ldots, N - n_{\text{working}} + 1
\]
\[
is\_work_{n+n_{\text{working}},i} + is\_work_{n+n_{\text{working}}+1,i} + \ldots + is\_work_{n+n_{\text{working}}+n_{\text{resting}}-1,i} = 0 \quad \forall n = 1, \ldots, N - n_{\text{working}} - n_{\text{resting}} + 1
\]

\subsection*{Output}
The output will consist of:
\begin{itemize}
    \item \( total\_number \): the total number of employees hired.
    \item \( is\_work \): a matrix where each entry \( is\_work_{n,i} \) indicates whether employee \( i \) works on day \( n \).
\end{itemize}

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

\section*{Mathematical Model for Cafeteria Staffing}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( N \) be the total number of days.
    \item Let \( \text{num}_{n} \) be the number of required employees on day \( n \) for \( n = 1, \ldots, N \).
    \item Let \( n_{\text{working}} \) be the number of consecutive working days for each employee.
    \item Let \( n_{\text{resting}} \) be the number of consecutive resting days for each employee.
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item Let \( total\_number \) be the total number of employees to hire.
    \item Let \( is\_work_{n,i} \) be a binary variable that equals 1 if employee \( i \) is working on day \( n \), and 0 otherwise, for \( n = 1, \ldots, N \) and \( i = 1, \ldots, total\_number \).
\end{itemize}

\subsection*{Objective}
Minimize the total number of employees:
\[
\text{Minimize} \quad total\_number
\]

\subsection*{Constraints}
For each day \( n \):
\[
\sum_{i=1}^{total\_number} is\_work_{n,i} \geq \text{num}_{n} \quad \forall n = 1, \ldots, N
\]

Each employee \( i \) can work for \( n_{\text{working}} \) days and must rest for \( n_{\text{resting}} \) days:
\[
is\_work_{n,i} + is\_work_{n+1,i} + \ldots + is\_work_{n+n_{\text{working}}-1,i} \leq n_{\text{working}} \quad \forall n = 1, \ldots, N - n_{\text{working}} + 1
\]
\[
is\_work_{n+n_{\text{working}},i} + is\_work_{n+n_{\text{working}}+1,i} + \ldots + is\_work_{n+n_{\text{working}}+n_{\text{resting}}-1,i} = 0 \quad \forall n = 1, \ldots, N - n_{\text{working}} - n_{\text{resting}} + 1
\]

\subsection*{Output}
The output will consist of:
\begin{itemize}
    \item \( total\_number \): the total number of employees hired.
    \item \( is\_work \): a matrix where each entry \( is\_work_{n,i} \) indicates whether employee \( i \) works on day \( n \).
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Given data in JSON format
data = json.loads("{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}")

#### Extracting data
num_required = data['num']
n_working = data['n_working_days']
n_resting = data['n_resting_days']
N = len(num_required)

#### Problem definition
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

#### Decision variable
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(total_number)), cat='Binary')

#### Objective function
problem += total_number, "Minimize_Total_Employees"

#### Constraints for required employees on each day
for n in range(N):
    problem += pulp.lpSum(is_work[(n, i)] for i in range(total_number)) >= num_required[n], f"Min_Employees_Day_{n+1}"

#### Constraints for working days
for i in range(total_number):
    for n in range(N - n_working + 1):
        problem += pulp.lpSum(is_work[(n + d, i)] for d in range(n_working)) <= n_working, f"Working_Days_Limit_{i}_{n+1}"

    #### Constraints for resting days
    for n in range(N - n_working - n_resting + 1):
        problem += pulp.lpSum(is_work[(n + d + n_working, i)] for d in range(n_resting)) == 0, f"Resting_Days_Requirement_{i}_{n+1}"

#### Add a constraint to link total_number with the total hired employees
problem += total_number >= pulp.lpSum(1 for i in range(total_number) if pulp.lpSum(is_work[(n, i)] for n in range(N)) > 0), "Total_Number_Constraint"

#### Solve the problem
problem.solve()

#### Output results
hired_employees = pulp.value(total_number)
print(f' (Objective Value): <OBJ>{hired_employees}</OBJ>')

is_work_matrix = [[pulp.value(is_work[(n, i)]) for i in range(int(hired_employees))] for n in range(N)]
print("Work Schedule (is_work matrix):")
for row in is_work_matrix:
    print(row)
```

