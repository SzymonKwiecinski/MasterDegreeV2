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
To solve this problem using an integer linear programming (ILP) approach, we must determine the minimum number of employees required to meet the daily demand while respecting the working and resting schedule constraints. The problem involves setting up a schedule for a series of employees to ensure that on each day, the required number of employees is present, given the working/resting cycle stipulated.

Here’s how we can model this problem in a mathematical form and transform it into a Latex document:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Total number of days in the planning horizon.
    \item $n\_working\_days$: Number of consecutive working days for each employee.
    \item $n\_resting\_days$: Number of consecutive resting days for each employee.
    \item $\text{num}_n$: Required number of employees on day $n$ for all $n \in \{1, \dots, N\}$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Binary variable indicating if employee $i$ is employed (1 if employed, 0 otherwise).
    \item $y_{n, i}$: Binary variable indicating if employee $i$ is working on day $n$ (1 if working, 0 otherwise).
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees hired:
\[
\text{Minimize} \quad \sum_{i=1}^{M} x_i
\]
where \( M \) is a sufficiently large number representing a potential upper bound for the number of employees.

\subsection*{Constraints}
1. Demand satisfaction:
   \[
   \sum_{i=1}^{M} y_{n, i} \geq \text{num}_n \quad \forall n \in \{1, \dots, N\}
   \]
2. Working and resting cycle:
   \[
   y_{n, i} \leq x_i \quad \forall n \in \{1, \dots, N\}, \forall i
   \]
   \[
   \sum_{k=0}^{n\_working\_days-1} y_{n+k, i} = n\_working\_days \cdot z_{n, i} \quad \forall n, \forall i
   \]
   \[
   \sum_{k=0}^{n\_resting\_days-1} (1-y_{n\_working\_days+n+k, i}) = n\_resting\_days \cdot (1-z_{n, i}) \quad \forall n, \forall i
   \]
   Here, $z_{n, i}$ is an auxiliary binary variable indicating the start of a new working cycle.

3. Non-negativity and binary constraints:
   \[
   x_i \in \{0, 1\}, \quad y_{n, i} \in \{0, 1\}, \quad z_{n, i} \in \{0, 1\}
   \]

\end{document}
```

This formulation helps calculate the minimum number of employees needed to satisfy the demand while ensuring that employees work for a certain number of days and take specific days off. The binary decision variables account for the scheduling and presence of each employee on any given day.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{itemize}
    \item $N$: Total number of days in the planning horizon.
    \item $n\_working\_days$: Number of consecutive working days for each employee.
    \item $n\_resting\_days$: Number of consecutive resting days for each employee.
    \item $\text{num}_n$: Required number of employees on day $n$ for all $n \in \{1, \dots, N\}$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_i$: Binary variable indicating if employee $i$ is employed (1 if employed, 0 otherwise).
    \item $y_{n, i}$: Binary variable indicating if employee $i$ is working on day $n$ (1 if working, 0 otherwise).
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees hired:
\[
\text{Minimize} \quad \sum_{i=1}^{M} x_i
\]
where \( M \) is a sufficiently large number representing a potential upper bound for the number of employees.

\subsection*{Constraints}
1. Demand satisfaction:
   \[
   \sum_{i=1}^{M} y_{n, i} \geq \text{num}_n \quad \forall n \in \{1, \dots, N\}
   \]
2. Working and resting cycle:
   \[
   y_{n, i} \leq x_i \quad \forall n \in \{1, \dots, N\}, \forall i
   \]
   \[
   \sum_{k=0}^{n\_working\_days-1} y_{n+k, i} = n\_working\_days \cdot z_{n, i} \quad \forall n, \forall i
   \]
   \[
   \sum_{k=0}^{n\_resting\_days-1} (1-y_{n\_working\_days+n+k, i}) = n\_resting\_days \cdot (1-z_{n, i}) \quad \forall n, \forall i
   \]
   Here, $z_{n, i}$ is an auxiliary binary variable indicating the start of a new working cycle.

3. Non-negativity and binary constraints:
   \[
   x_i \in \{0, 1\}, \quad y_{n, i} \in \{0, 1\}, \quad z_{n, i} \in \{0, 1\}
   \]

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num_demand = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

#### Parameters
N = len(num_demand)
M = sum(num_demand)  #### an upper bound on the number of employees

#### Create the problem
problem = pulp.LpProblem("Employee_Scheduling", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(M), cat='Binary')
y = pulp.LpVariable.dicts("y", ((n, i) for n in range(N) for i in range(M)), cat='Binary')
z = pulp.LpVariable.dicts("z", ((n, i) for n in range(N) for i in range(M)), cat='Binary')

#### Objective Function
problem += pulp.lpSum(x[i] for i in range(M))

#### Constraints

#### 1. Demand satisfaction
for n in range(N):
    problem += pulp.lpSum(y[n, i] for i in range(M)) >= num_demand[n]

#### 2. Working and resting cycle
for n in range(N):
    for i in range(M):
        problem += y[n, i] <= x[i]
        
        #### Consistent working days for working cycle
        if n <= N - n_working_days:
            problem += pulp.lpSum(y[n+k, i] for k in range(n_working_days)) == n_working_days * z[n, i]
        
        #### Consistent resting days for resting cycle
        if n <= N - (n_working_days + n_resting_days):
            problem += pulp.lpSum(1 - y[n_working_days+n+k, i] for k in range(n_resting_days)) == n_resting_days * (1 - z[n, i])

#### Solve the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

