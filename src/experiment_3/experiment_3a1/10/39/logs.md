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
To model the cafeteria staffing problem as a linear programming (LP) problem, we will define the decision variables, objective function, and constraints based on the given information. Below is the LaTeX representation of the mathematical model.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Cafeteria Staffing Problem}

\textbf{Parameters:}
\begin{itemize}
    \item $N$: Total number of days.
    \item $num_n$: Required number of employees on day $n$, where $n = 1, 2, \ldots, N$.
    \item $n_{working}$: Number of consecutive working days for each employee.
    \item $n_{resting}$: Number of consecutive days off for each employee.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $total\_number$: Total number of employees to hire.
    \item $is\_work_{n,i}$: Binary variable where $is\_work_{n,i} = 1$ if employee $i$ is working on day $n$, and $is\_work_{n,i} = 0$ otherwise, for $i = 1, 2, \ldots, total\_number$ and $n = 1, 2, \ldots, N$.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } total\_number
\]

\textbf{Constraints:}
For each day $n$, ensure that the required number of employees is met:
\[
\sum_{i=1}^{total\_number} is\_work_{n,i} \geq num_n \quad \forall n \in \{1, 2, \ldots, N\}
\]

Incorporate the working and resting constraint for each employee. For each employee $i$:
\[
is\_work_{n,i} = 1 \quad \text{for } n = j \text{ to } j+n_{working}-1
\]
\[
is\_work_{j+n_{working},i} = 0 \quad \text{for } j+n_{working} \text{ to } j+n_{working}+n_{resting}-1
\]

\textbf{Binary Constraints:}
\[
is\_work_{n,i} \in \{0, 1\} \quad \forall n \in \{1, 2, \ldots, N\}, i \in \{1, 2, \ldots, total\_number\}
\]

\end{document}
``` 

This model captures the staffing requirements based on the days employees work and rest, while aiming to minimize the number of employees hired. Adjustments might be necessary for specific implementation details or if additional constraints arise.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Cafeteria Staffing Problem}

\textbf{Parameters:}
\begin{itemize}
    \item $N$: Total number of days.
    \item $num_n$: Required number of employees on day $n$, where $n = 1, 2, \ldots, N$.
    \item $n_{working}$: Number of consecutive working days for each employee.
    \item $n_{resting}$: Number of consecutive days off for each employee.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $total\_number$: Total number of employees to hire.
    \item $is\_work_{n,i}$: Binary variable where $is\_work_{n,i} = 1$ if employee $i$ is working on day $n$, and $is\_work_{n,i} = 0$ otherwise, for $i = 1, 2, \ldots, total\_number$ and $n = 1, 2, \ldots, N$.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } total\_number
\]

\textbf{Constraints:}
For each day $n$, ensure that the required number of employees is met:
\[
\sum_{i=1}^{total\_number} is\_work_{n,i} \geq num_n \quad \forall n \in \{1, 2, \ldots, N\}
\]

Incorporate the working and resting constraint for each employee. For each employee $i$:
\[
is\_work_{n,i} = 1 \quad \text{for } n = j \text{ to } j+n_{working}-1
\]
\[
is\_work_{j+n_{working},i} = 0 \quad \text{for } j+n_{working} \text{ to } j+n_{working}+n_{resting}-1
\]

\textbf{Binary Constraints:}
\[
is\_work_{n,i} \in \{0, 1\} \quad \forall n \in \{1, 2, \ldots, N\}, i \in \{1, 2, \ldots, total\_number\}
\]

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data
data = json.loads('{"num": [5, 10, 2, 3, 2, 10], "n_working_days": 5, "n_resting_days": 2}')
num_n = data['num']
n_working = data['n_working_days']
n_resting = data['n_resting_days']
N = len(num_n)

#### Create the problem
problem = pulp.LpProblem("CafeteriaStaffingProblem", pulp.LpMinimize)

#### Decision Variables
total_number = pulp.LpVariable('total_number', lowBound=1, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(int(total_number))), cat='Binary')

#### Objective Function
problem += total_number, "Minimize Total Employees"

#### Constraints for required number of employees
for n in range(N):
    problem += pulp.lpSum(is_work[n, i] for i in range(int(total_number))) >= num_n[n], f"MinEmployees_day_{n}"

#### Constraints for working and resting days for each employee
for i in range(int(total_number)):
    for n in range(N - n_working - n_resting + 1):
        #### Working days
        for j in range(n_working):
            problem += is_work[n + j, i] == 1, f"Work_days_{i}_from_day_{n + j}"
        #### Resting days
        for j in range(n_resting):
            problem += is_work[n + n_working + j, i] == 0, f"Rest_days_{i}_after_work_{n + j + n_working}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

