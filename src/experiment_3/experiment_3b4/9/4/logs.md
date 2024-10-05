# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MILP

PROBLEM INFO: 
- A hospital wants to make a weekly night shift (12pm-8am) schedule for its nurses. 
- The demand for nurses for the night shift on day \var{j} = 1,...,7 is an integer \var{d_j}. 
- Every nurse works \var{period} days in a row on the night shift, followed by (7 - \var{period}) days off.


INPUT FORMAT: 

{
    "period": period,
    "demand": [d_j for j in 1, ...,7]
}

OBJECTIVE: The goal is to find the minimal number of nurses the hospital needs to hire. 

OUTPUT INFO: 

- for each day \var{j} = 1,...,7, \var{start_j} which shows the number of nurses that start their period on day \var{j}.
- the total number of nurses hired.

OUTPUT FORMAT:

{
    "start": [start_j for j in 1, ...,7],
    "total": total
}


</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To create the mathematical model for the given problem, we need to formulate a Mixed Integer Linear Programming (MILP) model. We'll use decision variables to represent the number of nurses starting their shifts on each day and use constraints to ensure the demand for nurses is met each day. Here's the formulation of the MILP model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the total number of nurses hired.

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_j$: Number of nurses who start their shift on day $j$, for $j = 1, \ldots, 7$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $d_j$: Demand for nurses on day $j$, for $j = 1, \ldots, 7$.
    \item \text{period}: Number of consecutive days a nurse works.
\end{itemize}

\textbf{Constraints:}
\begin{align}
    &\sum_{i=0}^{\text{period}-1} x_{(j-i-1) \bmod 7 + 1} \geq d_j, \quad \forall j = 1, \ldots, 7 \\
    &x_j \geq 0 \quad \text{and integer}, \quad \forall j = 1, \ldots, 7
\end{align}

\textbf{Objective Function:}
\begin{align}
    \min \sum_{j=1}^{7} x_j
\end{align}

\textbf{Explanation:} 
\begin{itemize}
    \item Constraint (1) ensures that the total number of nurses working on any given day $j$ meets the demand $d_j$. The summation $\sum_{i=0}^{\text{period}-1} x_{(j-i-1) \bmod 7 + 1}$ represents the number of nurses available each day, accounting for the period they work starting from day $j-i$.
    \item Constraint (2) ensures that the number of nurses starting each day is non-negative and integer.
    \item The objective (3) is to minimize the total number of nurses hired, which is the sum of all nurses starting their shifts on each day.
\end{itemize}

\end{document}
```

This model captures the constraints and objectives described in the problem statement, allowing for the determination of the optimal number of nurses needed to cover the night shifts according to the specified work period. Each nurse works for the specified `period` and then takes the remaining days off within a 7-day week. The modulo operation helps wrap around the week.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the total number of nurses hired.

\textbf{Decision Variables:}
\begin{itemize}
    \item $x_j$: Number of nurses who start their shift on day $j$, for $j = 1, \ldots, 7$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $d_j$: Demand for nurses on day $j$, for $j = 1, \ldots, 7$.
    \item \text{period}: Number of consecutive days a nurse works.
\end{itemize}

\textbf{Constraints:}
\begin{align}
    &\sum_{i=0}^{\text{period}-1} x_{(j-i-1) \bmod 7 + 1} \geq d_j, \quad \forall j = 1, \ldots, 7 \\
    &x_j \geq 0 \quad \text{and integer}, \quad \forall j = 1, \ldots, 7
\end{align}

\textbf{Objective Function:}
\begin{align}
    \min \sum_{j=1}^{7} x_j
\end{align}

\textbf{Explanation:} 
\begin{itemize}
    \item Constraint (1) ensures that the total number of nurses working on any given day $j$ meets the demand $d_j$. The summation $\sum_{i=0}^{\text{period}-1} x_{(j-i-1) \bmod 7 + 1}$ represents the number of nurses available each day, accounting for the period they work starting from day $j-i$.
    \item Constraint (2) ensures that the number of nurses starting each day is non-negative and integer.
    \item The objective (3) is to minimize the total number of nurses hired, which is the sum of all nurses starting their shifts on each day.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
period = data['Period']
demand = data['Demand']

#### Problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{j+1}', lowBound=0, cat='Integer') for j in range(T)]

#### Objective Function
problem += pulp.lpSum(x[j] for j in range(T))

#### Constraints
for j in range(T):
    problem += pulp.lpSum(x[(j-i-1) % T] for i in range(period)) >= demand[j]

#### Solve
problem.solve()

#### Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


