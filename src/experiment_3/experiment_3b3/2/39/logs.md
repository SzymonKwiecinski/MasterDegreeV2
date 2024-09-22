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
    \item $N$: Total number of days.
    \item $num_n$: Number of employees required on day $n$, where $n = 1, 2, \ldots, N$.
    \item $n_{working\_days}$: Number of consecutive working days for each employee.
    \item $n_{resting\_days}$: Number of consecutive resting days for each employee.
    \item $T = n_{working\_days} + n_{resting\_days}$: Total cycle length of each employee.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $total\_number$: Total number of employees to hire.
    \item $is\_work_{n,i}$: Binary variable indicating whether employee $i$ is working on day $n$ (1 if working, 0 if resting), where $i = 1, 2, \ldots, total\_number$ and $n = 1, 2, \ldots, N$.
\end{itemize}

\subsection*{Objective Function}
\[
\text{Minimize } total\_number
\]

\subsection*{Constraints}
\begin{align}
\sum_{i=1}^{total\_number} is\_work_{n,i} & \geq num_n, \quad \forall n \in \{1, 2, \ldots, N\} \\
is\_work_{n,i} & \in \{0, 1\}, \quad \forall n \in \{1, 2, \ldots, N\}, \forall i \in \{1, 2, \ldots, total\_number\} \\
is\_work_{n,i} & = 1 \text{ for } n \in \{k\cdot T + 1, \ldots, k\cdot T + n_{working\_days}\} \text{ (employee $i$ is working)} \\
is\_work_{n,i} & = 0 \text{ for } n \in \{k\cdot T + n_{working\_days} + 1, \ldots, (k+1)\cdot T\} \text{ (employee $i$ is resting)}
\end{align}
where $k$ is a non-negative integer representing the cycle of each employee.

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
    \item $N$: Total number of days.
    \item $num_n$: Number of employees required on day $n$, where $n = 1, 2, \ldots, N$.
    \item $n_{working\_days}$: Number of consecutive working days for each employee.
    \item $n_{resting\_days}$: Number of consecutive resting days for each employee.
    \item $T = n_{working\_days} + n_{resting\_days}$: Total cycle length of each employee.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $total\_number$: Total number of employees to hire.
    \item $is\_work_{n,i}$: Binary variable indicating whether employee $i$ is working on day $n$ (1 if working, 0 if resting), where $i = 1, 2, \ldots, total\_number$ and $n = 1, 2, \ldots, N$.
\end{itemize}

\subsection*{Objective Function}
\[
\text{Minimize } total\_number
\]

\subsection*{Constraints}
\begin{align}
\sum_{i=1}^{total\_number} is\_work_{n,i} & \geq num_n, \quad \forall n \in \{1, 2, \ldots, N\} \\
is\_work_{n,i} & \in \{0, 1\}, \quad \forall n \in \{1, 2, \ldots, N\}, \forall i \in \{1, 2, \ldots, total\_number\} \\
is\_work_{n,i} & = 1 \text{ for } n \in \{k\cdot T + 1, \ldots, k\cdot T + n_{working\_days}\} \text{ (employee $i$ is working)} \\
is\_work_{n,i} & = 0 \text{ for } n \in \{k\cdot T + n_{working\_days} + 1, \ldots, (k+1)\cdot T\} \text{ (employee $i$ is resting)}
\end{align}
where $k$ is a non-negative integer representing the cycle of each employee.

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'num': [5, 10, 2, 3, 2, 10],
    'n_working_days': 5,
    'n_resting_days': 2
}

#### Parameters
N = len(data['num'])  #### Total number of days
num_n = data['num']  #### Number of employees required each day
n_working_days = data['n_working_days'] 
n_resting_days = data['n_resting_days'] 
T = n_working_days + n_resting_days  #### Total cycle length

#### Problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

#### Decision Variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts(
    'is_work', 
    ((n, i) for n in range(N) for i in range(100)), 
    cat='Binary'
)

#### Objective Function
problem += total_number, "Minimize Total Number of Employees"

#### Constraints
for n in range(N):
    problem += (
        pulp.lpSum(is_work[(n, i)] for i in range(100)) >= num_n[n],
        f"Minimum_Workers_Day_{n}"
    )

#### Initial constraints setup in cycles
for i in range(100):
    for k in range((N + T - 1) // T):  #### Ensuring all days are covered
        for day in range(n_working_days):
            if k * T + day < N:
                problem += (
                    is_work[(k * T + day, i)] == 1,
                    f"Work_Employee_{i}_Day_{k * T + day}"
                )
        for day in range(n_working_days, T):
            if k * T + day < N:
                problem += (
                    is_work[(k * T + day, i)] == 0,
                    f"Rest_Employee_{i}_Day_{k * T + day}"
                )

#### Solve
problem.solve()

#### Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


