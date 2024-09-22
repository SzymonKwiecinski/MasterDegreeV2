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
To model this problem as a Linear Programming (LP) problem, we need to define the decision variables, the objective function, and the constraints.

**Decision Variables:**
- \( x_p \): Number of batches of part \( p \) produced, for \( p = 1, \ldots, P \).
- \( e_m \): Additional hours purchased for machine \( m \), for \( m = 1, \ldots, M \).

**Objective:**
Maximize profit, which is calculated as:
\[ 
\text{Profit} = \sum_{p=1}^{P} (\text{price}_p \times x_p) - \sum_{m=1}^{M} (\text{cost}_m \times \text{used hours}_m + \text{extra\_cost}_m \times e_m)
\]
Where, 
\(\text{used hours}_m = \sum_{p=1}^{P} (\text{time}_{m,p} \times x_p)\).

**Constraints:**
1. Demand fulfillment constraint:
   \[
   x_p \geq \text{min\_batches}_p \quad \forall p = 1, \ldots, P
   \]
2. Machine availability constraint:
   \[
   \sum_{p=1}^{P} (\text{time}_{m,p} \times x_p) \leq \text{available}_m + e_m \quad \forall m = 1, \ldots, M
   \]
3. Additional hours constraint:
   \[
   0 \leq e_m \leq \text{max\_extra}_m \quad \forall m = 1, \ldots, M
   \]
4. Non-negativity constraints:
   \[
   x_p \geq 0 \quad \forall p = 1, \ldots, P
   \]
   \[
   e_m \geq 0 \quad \forall m = 1, \ldots, M
   \]

Here is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables:}
\begin{align*}
x_p & : \text{Number of batches of part } p \text{ produced}, \quad \forall p = 1, \ldots, P. \\
e_m & : \text{Additional hours purchased for machine } m, \quad \forall m = 1, \ldots, M.
\end{align*}

\subsection*{Objective:}
Maximize the profit:
\begin{align*}
\text{Maximize} \quad \sum_{p=1}^{P} (\text{price}_p \times x_p) - \sum_{m=1}^{M} \left(\text{cost}_m \sum_{p=1}^{P} (\text{time}_{m,p} \times x_p) + \text{extra\_cost}_m \times e_m \right)
\end{align*}

\subsection*{Constraints:}
1. Demand fulfillment:
\begin{align*}
x_p \geq \text{min\_batches}_p \quad \forall p = 1, \ldots, P
\end{align*}

2. Machine availability:
\begin{align*}
\sum_{p=1}^{P} (\text{time}_{m,p} \times x_p) \leq \text{available}_m + e_m \quad \forall m = 1, \ldots, M
\end{align*}

3. Additional hours constraints:
\begin{align*}
0 \leq e_m \leq \text{max\_extra}_m \quad \forall m = 1, \ldots, M
\end{align*}

4. Non-negativity:
\begin{align*}
x_p & \geq 0 \quad \forall p = 1, \ldots, P \\
e_m & \geq 0 \quad \forall m = 1, \ldots, M
\end{align*}

\end{document}
```

This linear programming model will help determine the optimal number of batches of each part to produce, and the additional machine hours to purchase to maximize the total profit while meeting the given constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables:}
\begin{align*}
x_p & : \text{Number of batches of part } p \text{ produced}, \quad \forall p = 1, \ldots, P. \\
e_m & : \text{Additional hours purchased for machine } m, \quad \forall m = 1, \ldots, M.
\end{align*}

\subsection*{Objective:}
Maximize the profit:
\begin{align*}
\text{Maximize} \quad \sum_{p=1}^{P} (\text{price}_p \times x_p) - \sum_{m=1}^{M} \left(\text{cost}_m \sum_{p=1}^{P} (\text{time}_{m,p} \times x_p) + \text{extra\_cost}_m \times e_m \right)
\end{align*}

\subsection*{Constraints:}
1. Demand fulfillment:
\begin{align*}
x_p \geq \text{min\_batches}_p \quad \forall p = 1, \ldots, P
\end{align*}

2. Machine availability:
\begin{align*}
\sum_{p=1}^{P} (\text{time}_{m,p} \times x_p) \leq \text{available}_m + e_m \quad \forall m = 1, \ldots, M
\end{align*}

3. Additional hours constraints:
\begin{align*}
0 \leq e_m \leq \text{max\_extra}_m \quad \forall m = 1, \ldots, M
\end{align*}

4. Non-negativity:
\begin{align*}
x_p & \geq 0 \quad \forall p = 1, \ldots, P \\
e_m & \geq 0 \quad \forall m = 1, \ldots, M
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10], 
    'extra_costs': [0, 15, 22.5], 
    'max_extra': [0, 80, 80]
}

#### Decision Variables
P = len(data['prices'])  #### number of products
M = len(data['machine_costs'])  #### number of machines

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variable for batches produced
x = pulp.LpVariable.dicts("Batches_Produced", range(P), lowBound=0)

#### Decision variable for additional hours purchased
e = pulp.LpVariable.dicts("Extra_Hours", range(M), lowBound=0)

#### Objective function
problem += pulp.lpSum([data['prices'][p] * x[p] for p in range(P)]) - \
           pulp.lpSum([data['machine_costs'][m] * 
                        pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(P)]) + 
                        data['extra_costs'][m] * e[m] for m in range(M)])

#### Constraints
#### Demand fulfillment
for p in range(P):
    problem += x[p] >= data['min_batches'][p]

#### Machine availability
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(P)]) <= data['availability'][m] + e[m]

#### Additional hours constraints
for m in range(M):
    problem += e[m] <= data['max_extra'][m]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

