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

\textbf{Indices:}
\begin{itemize}
    \item $n$: Day index, where $n = 1, 2, \ldots, N$
    \item $i$: Employee index, where $i = 1, 2, \ldots, \text{total\_number}$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $num_n$: Required number of employees on day $n$
    \item $n\_working\_days$: Number of consecutive days an employee works
    \item $n\_resting\_days$: Number of consecutive days an employee rests
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $total\_number$: Total number of employees to hire
    \item $is\_work_{n,i}$: Binary variable indicating if employee $i$ works on day $n$ ($is\_work_{n,i} = 1$ if the employee works on day $n$, and $0$ otherwise)
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } total\_number
\]

\textbf{Constraints:}
\begin{align}
    \sum_{i=1}^{total\_number} is\_work_{n,i} & \geq num_n, \quad \forall n \in \{1, 2, \ldots, N\} \tag{1}\\
    is\_work_{n,i} & = 1 \quad \text{for } n \in \{j, j+1, \ldots, j + n\_working\_days - 1\} \quad \text{if } i \text{ works on day } j \tag{2}\\
    is\_work_{n,i} & = 0 \quad \text{for } n \in \{j + n\_working\_days, \ldots, j + n\_working\_days + n\_resting\_days - 1\} \quad \text{if } i \text{ works on day } j \tag{3}\\
    is\_work_{n,i} & \in \{0, 1\} \quad \forall n \forall i \tag{4}
\end{align}

\textbf{Output:}
\begin{itemize}
    \item $total\_number$: Total number of employees hired
    \item $is\_work$: A matrix representing the work schedule for each employee across the days
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

\textbf{Indices:}
\begin{itemize}
    \item $n$: Day index, where $n = 1, 2, \ldots, N$
    \item $i$: Employee index, where $i = 1, 2, \ldots, \text{total\_number}$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $num_n$: Required number of employees on day $n$
    \item $n\_working\_days$: Number of consecutive days an employee works
    \item $n\_resting\_days$: Number of consecutive days an employee rests
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $total\_number$: Total number of employees to hire
    \item $is\_work_{n,i}$: Binary variable indicating if employee $i$ works on day $n$ ($is\_work_{n,i} = 1$ if the employee works on day $n$, and $0$ otherwise)
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } total\_number
\]

\textbf{Constraints:}
\begin{align}
    \sum_{i=1}^{total\_number} is\_work_{n,i} & \geq num_n, \quad \forall n \in \{1, 2, \ldots, N\} \tag{1}\\
    is\_work_{n,i} & = 1 \quad \text{for } n \in \{j, j+1, \ldots, j + n\_working\_days - 1\} \quad \text{if } i \text{ works on day } j \tag{2}\\
    is\_work_{n,i} & = 0 \quad \text{for } n \in \{j + n\_working\_days, \ldots, j + n\_working\_days + n\_resting\_days - 1\} \quad \text{if } i \text{ works on day } j \tag{3}\\
    is\_work_{n,i} & \in \{0, 1\} \quad \forall n \forall i \tag{4}
\end{align}

\textbf{Output:}
\begin{itemize}
    \item $total\_number$: Total number of employees hired
    \item $is\_work$: A matrix representing the work schedule for each employee across the days
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'num': [5, 10, 2, 3, 2, 10],
    'n_working_days': 5,
    'n_resting_days': 2
}

#### Problem parameters
N = len(data['num'])  #### Total number of days

#### Create the problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

#### Decision variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", ((n, i) for n in range(N) for i in range(1000)),
                                cat='Binary')

#### Objective function
problem += total_number, "Minimize_total_number_of_employees"

#### Constraints
#### (1) Sufficient employees each day
for n in range(N):
    problem += (
        pulp.lpSum(is_work[n, i] for i in range(1000)) >= data['num'][n], 
        f"Constraint_sufficient_employees_day_{n+1}"
    )

#### (2) Working and (3) Resting days constraints
for i in range(1000):
    for j in range(N):
        #### Enforce working days
        if j + data['n_working_days'] <= N:
            problem += (
                pulp.lpSum(is_work[j + k, i] for k in range(data['n_working_days'])) 
                - data['n_working_days'] * is_work[j, i] == 0, 
                f"Constraint_working_days_emp_{i}_from_day_{j+1}"
            )
        
        #### Enforce resting days
        if j + data['n_working_days'] + data['n_resting_days'] <= N:
            problem += (
                pulp.lpSum(is_work[j + data['n_working_days'] + k, i] for k in range(data['n_resting_days']))
                <= data['n_resting_days'] * (1 - is_work[j, i]), 
                f"Constraint_resting_days_emp_{i}_from_day_{j+1}"
            )

#### Solve the problem
problem.solve()

#### Output results
total_employees_needed = sum(
    pulp.value(is_work[0, i]) for i in range(1000)
)

#### Print the total number of employees needed and objective value
print(f"Total Number of Employees Hired: {total_employees_needed}")
print(f"Objective Value: <OBJ>{pulp.value(problem.objective)}</OBJ>")
```
This script sets up and solves a linear programming problem using the Pulp library. The goal is to minimize the number of employees required to fulfill staffing needs while respecting working and resting periods. The decision variable `total_number` is minimized, and the constraints ensure the required number of employees is met each day and enforce the work/rest schedule for each employee.

