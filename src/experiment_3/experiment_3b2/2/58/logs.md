# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MIP

PROBLEM INFO:

- A division of an auto parts manufacturer produces \var{P} different parts using \var{M} different machines.
- Batch of 100 part \var{p} requires \var{time_{m,p}} hours on machine \var{m}.
- The division incurs a charge of \var{cost_{m}} per hour for using machine \var{m}.
- Machine \var{m} has an availability of up to \var{available_{m}} hours per month.
- The division sells part \var{p} in batches of 100 at price of \var{price_{p}} per batch.
- Machine \var{1} requires a setup time of \var{setup_time_{p}} hours before it can be used for each part \var{p}.
- Other machines do not require a setup time.
- There are no minimum production quantities for any part.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "setup_time": [setup_time_{p} for p in 1, ..., P]
}

OBJECTIVE: How many batches of each part should the manufacturer produce each month to maximize profit?

OUTPUT INFO:

- the number of batches of each part produced \var{batches_{p}}.
- \var{setup_flags_{p}} indicates whether \var{part_{p}} is set up or not.
- \var{total_profit} represents the total profit obtained for the month.

OUTPUT FORMAT:

{
    "batches": [batches_{p} for p in 1, ..., P],
    "setup_flags": [setup_flag_{p} for p in 1, ..., P],
    "total_profit": total_profit
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve the given Mixed Integer Programming problem using linear programming, we will formulate the problem in LaTeX using the appropriate mathematical notation. The formulation will involve defining decision variables, the objective function, and constraints.

Here is the LaTeX code for the problem formulation:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model}

\textbf{Sets and Indices:}
\begin{itemize}
    \item $P$: Set of parts, indexed by $p = 1, \ldots, P$
    \item $M$: Set of machines, indexed by $m = 1, \ldots, M$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $time_{m,p}$: Hours required on machine $m$ to produce a batch of part $p$
    \item $cost_{m}$: Cost per hour for using machine $m$
    \item $available_{m}$: Availability of machine $m$ in hours per month
    \item $price_{p}$: Selling price of a batch of part $p$
    \item $setup\_time_{p}$: Setup time required on machine 1 for part $p$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $batches_{p}$: Number of batches of part $p$ to produce (integer)
    \item $setup\_flag_{p}$: Binary variable indicating whether part $p$ is set up on machine 1 (0 or 1)
\end{itemize}

\textbf{Objective Function:}
\[
\max \sum_{p=1}^{P} \left( price_{p} \cdot batches_{p} \right) - \sum_{m=1}^{M} \sum_{p=1}^{P} \left( cost_{m} \cdot time_{m,p} \cdot batches_{p} \right) - \sum_{p=1}^{P} \left( cost_{1} \cdot setup\_time_{p} \cdot setup\_flag_{p} \right)
\]

\textbf{Constraints:}

\begin{itemize}
    \item \textbf{Availability constraints for each machine:}
    \[
    \sum_{p=1}^{P} \left( time_{m,p} \cdot batches_{p} \right) + \begin{cases} 
    \sum_{p=1}^{P} \left( setup\_time_{p} \cdot setup\_flag_{p} \right), & \text{if } m = 1 \\
    0, & \text{otherwise}
    \end{cases} \leq available_{m}, \quad \forall m = 1, \ldots, M
    \]

    \item \textbf{Binary setup indicator constraint:}
    \[
    batches_{p} \leq \text{Large} \cdot setup\_flag_{p}, \quad \forall p = 1, \ldots, P
    \]

    \item \textbf{Non-negativity and integrality constraints:}
    \[
    batches_{p} \geq 0, \quad batches_{p} \in \mathbb{Z}, \quad \forall p = 1, \ldots, P
    \]
    \[
    setup\_flag_{p} \in \{0, 1\}, \quad \forall p = 1, \ldots, P
    \]
\end{itemize}

\end{document}
```

This LaTeX code represents the mathematical model for the Mixed Integer Programming (MIP) problem. The model includes the objective function that aims to maximize the total profit, accounting for sales revenue and costs, including machine operation and setup. Constraints ensure machine availability and the logical relation between the number of batches produced and the setup requirement.

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

\textbf{Sets and Indices:}
\begin{itemize}
    \item $P$: Set of parts, indexed by $p = 1, \ldots, P$
    \item $M$: Set of machines, indexed by $m = 1, \ldots, M$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $time_{m,p}$: Hours required on machine $m$ to produce a batch of part $p$
    \item $cost_{m}$: Cost per hour for using machine $m$
    \item $available_{m}$: Availability of machine $m$ in hours per month
    \item $price_{p}$: Selling price of a batch of part $p$
    \item $setup\_time_{p}$: Setup time required on machine 1 for part $p$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $batches_{p}$: Number of batches of part $p$ to produce (integer)
    \item $setup\_flag_{p}$: Binary variable indicating whether part $p$ is set up on machine 1 (0 or 1)
\end{itemize}

\textbf{Objective Function:}
\[
\max \sum_{p=1}^{P} \left( price_{p} \cdot batches_{p} \right) - \sum_{m=1}^{M} \sum_{p=1}^{P} \left( cost_{m} \cdot time_{m,p} \cdot batches_{p} \right) - \sum_{p=1}^{P} \left( cost_{1} \cdot setup\_time_{p} \cdot setup\_flag_{p} \right)
\]

\textbf{Constraints:}

\begin{itemize}
    \item \textbf{Availability constraints for each machine:}
    \[
    \sum_{p=1}^{P} \left( time_{m,p} \cdot batches_{p} \right) + \begin{cases} 
    \sum_{p=1}^{P} \left( setup\_time_{p} \cdot setup\_flag_{p} \right), & \text{if } m = 1 \\
    0, & \text{otherwise}
    \end{cases} \leq available_{m}, \quad \forall m = 1, \ldots, M
    \]

    \item \textbf{Binary setup indicator constraint:}
    \[
    batches_{p} \leq \text{Large} \cdot setup\_flag_{p}, \quad \forall p = 1, \ldots, P
    \]

    \item \textbf{Non-negativity and integrality constraints:}
    \[
    batches_{p} \geq 0, \quad batches_{p} \in \mathbb{Z}, \quad \forall p = 1, \ldots, P
    \]
    \[
    setup\_flag_{p} \in \{0, 1\}, \quad \forall p = 1, \ldots, P
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'setup_time': [12, 8, 4, 0]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data provided in JSON format
data = '{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "setup_time": [12, 8, 4, 0]}'
data = json.loads(data)

#### Extracting data from the loaded JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

#### Define sets and indices
P = len(prices)  #### Number of parts
M = len(machine_costs)  #### Number of machines
Large = max(availability)  #### A large number for binary constraints

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flag = pulp.LpVariable.dicts("setup_flag", range(P), cat='Binary')

#### Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * time_required[m][p] * batches[p] for m in range(M) for p in range(P)) - \
         pulp.lpSum(machine_costs[0] * setup_time[p] * setup_flag[p] for p in range(P))

problem += profit

#### Constraints
#### Availability constraints for each machine
for m in range(M):
    if m == 0:
        problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + 
                     pulp.lpSum(setup_time[p] * setup_flag[p] for p in range(P))) <= availability[m]
    else:
        problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m])

#### Binary setup indicator constraint
for p in range(P):
    problem += batches[p] <= Large * setup_flag[p]

#### Solve the problem
problem.solve()

#### Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

