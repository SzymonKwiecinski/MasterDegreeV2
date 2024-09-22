# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- A division of an auto parts manufacturer produces \var{P} different parts using \var{M} different machines.
- Batch of 100 part \var{p} requires \var{time_{m,p}} hours on machine \var{m}.
- The division incurs a charge of \var{cost_{m}} per hour for using machine \var{m}.
- Machine \var{m} has an availability of up to \var{available_{m}} hours per month.
- The division sells part \var{p} in batches of 100 at price of \var{price_{p}} per batch.
- The division must produce at least \var{min_batches_{p}} batches of part \var{p} each month to fulfill a contract.
- Extra available time for machine \var{m} can be acquired at $\var{extra_costs_{m}}/hour. 
- Up to \var{max_extra_{m}} hours can be purchased for each machine \var{m}.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P],
    "extra_costs": [extra_cost_{m} for m in 1, ..., M],
    "max_extra": [max_extra_{m} for m in 1, ..., M]
}

OBJECTIVE: How many batches of each part should the manufacturer produce each month to maximize profit?

OUTPUT INFO:

- the number of batches of each part produced \var{batches_{p}}.
- \var{extra_time} denotes the additional hours purchased for each machine \var{m}.
- \var{total_profit} represents the total profit obtained for the month.

OUTPUT FORMAT:

{
    "batches": [batches_{p} for p in 1, ..., P],
    "extra_time": [extra_time_{p} for p in 1, ..., P],
    "total_profit": total_profit
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To formulate the linear programming model for the given problem, we need to define decision variables, constraints, and the objective function. Here is the problem modeled in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Linear Programming Model for Auto Parts Manufacturer}
\author{}
\date{}
\maketitle

\section*{Model Description}

We are tasked with determining the optimal number of batches of each part to be produced each month in order to maximize profit while considering machine constraints and contractual obligations.

\subsection*{Decision Variables}

Let:
\begin{itemize}
    \item \(x_p\) be the number of batches of part \(p\) produced, where \(p = 1, \ldots, P\).
    \item \(e_m\) be the extra hours purchased for machine \(m\), where \(m = 1, \ldots, M\).
\end{itemize}

\subsection*{Objective Function}

The objective is to maximize the total profit, calculated as the revenue from selling the parts minus the machine operation costs and the costs for extra machine hours.

\begin{align*}
\text{Maximize } & \sum_{p=1}^{P} \text{price}_p \cdot x_p - \sum_{m=1}^{M} \text{cost}_m \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \right) - \sum_{m=1}^{M} \text{extra\_cost}_m \cdot e_m
\end{align*}

\subsection*{Constraints}

The model is subject to the following constraints:

\begin{enumerate}
    \item \textbf{Demand Constraints:}
    \begin{align*}
    x_p &\geq \text{min\_batches}_p \quad \forall p = 1, \ldots, P
    \end{align*}
    
    \item \textbf{Machine Time Constraints:}
    \begin{align*}
    \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p &\leq \text{available}_m + e_m \quad \forall m = 1, \ldots, M
    \end{align*}
    
    \item \textbf{Extra Time Constraints:}
    \begin{align*}
    0 \leq e_m &\leq \text{max\_extra}_m \quad \forall m = 1, \ldots, M
    \end{align*}
    
    \item \textbf{Non-negativity Constraints:}
    \begin{align*}
    x_p &\geq 0 \quad \forall p = 1, \ldots, P \\
    e_m &\geq 0 \quad \forall m = 1, \ldots, M
    \end{align*}
\end{enumerate}

\end{document}
```

This LaTeX code establishes a complete linear programming model where the goal is to maximize the profit by determining the optimal production batches for each part subject to machine availability and contractual obligations. The decision variables, constraints, and objective function are clearly defined for the problem context.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Linear Programming Model for Auto Parts Manufacturer}
\author{}
\date{}
\maketitle

\section*{Model Description}

We are tasked with determining the optimal number of batches of each part to be produced each month in order to maximize profit while considering machine constraints and contractual obligations.

\subsection*{Decision Variables}

Let:
\begin{itemize}
    \item \(x_p\) be the number of batches of part \(p\) produced, where \(p = 1, \ldots, P\).
    \item \(e_m\) be the extra hours purchased for machine \(m\), where \(m = 1, \ldots, M\).
\end{itemize}

\subsection*{Objective Function}

The objective is to maximize the total profit, calculated as the revenue from selling the parts minus the machine operation costs and the costs for extra machine hours.

\begin{align*}
\text{Maximize } & \sum_{p=1}^{P} \text{price}_p \cdot x_p - \sum_{m=1}^{M} \text{cost}_m \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \right) - \sum_{m=1}^{M} \text{extra\_cost}_m \cdot e_m
\end{align*}

\subsection*{Constraints}

The model is subject to the following constraints:

\begin{enumerate}
    \item \textbf{Demand Constraints:}
    \begin{align*}
    x_p &\geq \text{min\_batches}_p \quad \forall p = 1, \ldots, P
    \end{align*}
    
    \item \textbf{Machine Time Constraints:}
    \begin{align*}
    \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p &\leq \text{available}_m + e_m \quad \forall m = 1, \ldots, M
    \end{align*}
    
    \item \textbf{Extra Time Constraints:}
    \begin{align*}
    0 \leq e_m &\leq \text{max\_extra}_m \quad \forall m = 1, \ldots, M
    \end{align*}
    
    \item \textbf{Non-negativity Constraints:}
    \begin{align*}
    x_p &\geq 0 \quad \forall p = 1, \ldots, P \\
    e_m &\geq 0 \quad \forall m = 1, \ldots, M
    \end{align*}
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extract the data from the JSON format provided
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

#### Number of parts and machines
P = len(data['prices'])
M = len(data['availability'])

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables for the number of batches of each part
x = pulp.LpVariable.dicts("x", range(P), lowBound=0, cat='Continuous')

#### Decision variables for extra machine hours
e = pulp.LpVariable.dicts("e", range(M), lowBound=0, cat='Continuous')

#### Objective function
revenue = pulp.lpSum([data['prices'][p] * x[p] for p in range(P)])
machine_cost = pulp.lpSum([data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) for m in range(M)])
extra_hours_cost = pulp.lpSum([data['extra_costs'][m] * e[m] for m in range(M)])

problem += revenue - machine_cost - extra_hours_cost

#### Demand constraints
for p in range(P):
    problem += x[p] >= data['min_batches'][p]

#### Machine time constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(P)) <= data['availability'][m] + e[m]

#### Extra time constraints
for m in range(M):
    problem += e[m] <= data['max_extra'][m]

#### Solve the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

