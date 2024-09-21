# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Nurse Staffing}

\subsection*{Objective}
Minimize the number of nurses that the hospital needs to hire for the planning period.

\subsection*{Parameters}
\begin{itemize}
    \item $T$: Number of days in the planning period.
    \item $Period$: The planning period for nurse staffing.
    \item $Demand_t$: The demand for nurses on day $t$, for $t = 1, 2, \ldots, T$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $N$: The number of nurses to hire.
\end{itemize}

\subsection*{Mathematical Formulation}
\begin{align*}
    \text{Minimize} \quad & N \\
    \text{subject to} \quad & N \geq Demand_t \quad \forall t = 1, 2, \ldots, T \\
    & N \geq 0
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}')
T = data['T']
Demand = data['Demand']

#### Define the problem
problem = pulp.LpProblem("Nurse_Staffing_Problem", pulp.LpMinimize)

#### Decision variable
N = pulp.LpVariable("N", lowBound=0, cat='Integer')

#### Objective function
problem += N, "Minimize the number of nurses"

#### Constraints
for t in range(T):
    problem += N >= Demand[t], f"Demand_constraint_day_{t+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

