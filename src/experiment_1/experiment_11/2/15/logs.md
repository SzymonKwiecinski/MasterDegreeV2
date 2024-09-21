# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model}

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of parts
    \item $M$: Number of machines
    \item $TimeRequired_{m,p}$: Time required to produce one batch of part $p$ on machine $m$
    \item $MachineCosts_m$: Cost associated with using machine $m$
    \item $Availability_m$: Availability of machine $m$ per month
    \item $Prices_p$: Selling price of one batch of part $p$
    \item $MinBatches_p$: Minimum number of batches of part $p$ to be produced
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $x_p$: Number of batches of part $p$ to be produced
\end{itemize}

\subsection*{Objective Function}
Maximize the profit, which is the total sales minus the costs of using the machines:
\[
\text{Maximize } Z = \sum_{p=1}^{P} Prices_p \cdot x_p - \sum_{m=1}^{M} MachineCosts_m \cdot \sum_{p=1}^{P} TimeRequired_{m,p} \cdot x_p
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Non-negativity constraint for the number of batches:
    \[
    x_p \geq 0 \quad \forall p = 1, 2, \ldots, P
    \]
    \item Machine time availability constraint:
    \[
    \sum_{p=1}^{P} TimeRequired_{m,p} \cdot x_p \leq Availability_m \quad \forall m = 1, 2, \ldots, M
    \]
    \item Minimum production requirement:
    \[
    x_p \geq MinBatches_p \quad \forall p = 1, 2, \ldots, P
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data_json = '''{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    "machine_costs": [160, 10, 15], 
    "availability": [200, 300, 500], 
    "prices": [570, 250, 585, 430], 
    "min_batches": [10, 10, 10, 10]
}'''

#### Load data
data = json.loads(data_json)

#### Parameters
P = len(data['prices'])  #### Number of parts
M = len(data['machine_costs'])  #### Number of machines
TimeRequired = data['time_required']  #### Time required for each machine-part combination
MachineCosts = data['machine_costs']  #### Costs associated with each machine
Availability = data['availability']  #### Availability of each machine
Prices = data['prices']  #### Selling prices of each part
MinBatches = data['min_batches']  #### Minimum batches required for each part

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(P), lowBound=0, cat='Continuous')

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Objective Function
problem += pulp.lpSum([Prices[p] * x[p] for p in range(P)]) - \
           pulp.lpSum([MachineCosts[m] * pulp.lpSum([TimeRequired[m][p] * x[p] for p in range(P)]) for m in range(M)])

#### Constraints
#### Machine time availability constraint
for m in range(M):
    problem += pulp.lpSum([TimeRequired[m][p] * x[p] for p in range(P)]) <= Availability[m]

#### Minimum production requirement
for p in range(P):
    problem += x[p] >= MinBatches[p]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

