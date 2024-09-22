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
To formulate the given problem as a Mixed-Integer Linear Programming (MILP) model, we define the necessary decision variables, objective function, and constraints. Here's how the problem can be modeled in LaTeX using optimal notation:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{MILP Model for Nurse Scheduling}

\textbf{Parameters:}
\begin{align*}
\text{period} & : \text{ Number of consecutive days a nurse works on night shifts.} \\
d_j & : \text{ Demand for nurses on night shift for day } j \in \{1, \ldots, 7\}.
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
\text{Let } start_j & \text{ be the number of nurses starting their period on day } j \in \{1, \ldots, 7\}. \\
\text{Let } total & \text{ be the total number of nurses hired.}
\end{align*}

\textbf{Objective:}
\[
\min \; total
\]

\textbf{Constraints:}
\begin{align*}
\text{Total Nurses Hired: } \\
total & = \sum_{j=1}^{7} start_j \\

\text{Demand Satisfaction: } \\
\sum_{k=0}^{\text{period}-1} start_{(j-k-1) \mod 7 + 1} & \geq d_j \quad \forall j \in \{1, \ldots, 7\} \\

\text{Non-negativity and Integer Constraints: } \\
start_j & \geq 0 \quad \text{and integer} \quad \forall j \in \{1, \ldots, 7\}
\end{align*}

\textbf{Explanation:}
\begin{itemize}
    \item The objective is to minimize the total number of nurses hired.
    \item The constraint ensures that for each day \( j \), the number of nurses currently on shift meets the demand \( d_j \). 
    \item Nurses work for a consecutive number of \text{period} days, hence for each day \( j \), the supply of nurses comes from those who started their shift up to \text{period} days prior.
    \item The modulo operation accommodates the weekly cycle, ensuring that day indices wrap around from 7 back to 1.
\end{itemize}

\end{document}
```

This LaTeX document outlines the MILP model for determining an optimal nurse scheduling pattern that minimizes the number of nurses while satisfying daily demand constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{MILP Model for Nurse Scheduling}

\textbf{Parameters:}
\begin{align*}
\text{period} & : \text{ Number of consecutive days a nurse works on night shifts.} \\
d_j & : \text{ Demand for nurses on night shift for day } j \in \{1, \ldots, 7\}.
\end{align*}

\textbf{Decision Variables:}
\begin{align*}
\text{Let } start_j & \text{ be the number of nurses starting their period on day } j \in \{1, \ldots, 7\}. \\
\text{Let } total & \text{ be the total number of nurses hired.}
\end{align*}

\textbf{Objective:}
\[
\min \; total
\]

\textbf{Constraints:}
\begin{align*}
\text{Total Nurses Hired: } \\
total & = \sum_{j=1}^{7} start_j \\

\text{Demand Satisfaction: } \\
\sum_{k=0}^{\text{period}-1} start_{(j-k-1) \mod 7 + 1} & \geq d_j \quad \forall j \in \{1, \ldots, 7\} \\

\text{Non-negativity and Integer Constraints: } \\
start_j & \geq 0 \quad \text{and integer} \quad \forall j \in \{1, \ldots, 7\}
\end{align*}

\textbf{Explanation:}
\begin{itemize}
    \item The objective is to minimize the total number of nurses hired.
    \item The constraint ensures that for each day \( j \), the number of nurses currently on shift meets the demand \( d_j \). 
    \item Nurses work for a consecutive number of \text{period} days, hence for each day \( j \), the supply of nurses comes from those who started their shift up to \text{period} days prior.
    \item The modulo operation accommodates the weekly cycle, ensuring that day indices wrap around from 7 back to 1.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = '{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}'
params = json.loads(data)

#### Parameters
T = params['T']
period = params['Period']
demand = params['Demand']

#### Create the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

#### Decision Variables
start = pulp.LpVariable.dicts("start", range(1, T + 1), lowBound=0, cat='Integer')
total = pulp.LpVariable("total", lowBound=0, cat='Integer')

#### Objective Function
problem += total, "Total_Nurses_Hired"

#### Total Nurses Hired Constraint
problem += total == pulp.lpSum(start[j] for j in range(1, T + 1)), "Total_Nurses_Constraint"

#### Demand Satisfaction Constraints
for j in range(1, T + 1):
    problem += (
        pulp.lpSum(start[(j - k - 1) % T + 1] for k in range(period)) >= demand[j - 1],
        f"Demand_Constraint_Day_{j}"
    )

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

