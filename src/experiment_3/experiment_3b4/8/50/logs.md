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
To create a mathematical model for the given linear programming problem, we need to maximize the profit while adhering to the availability constraints and fulfilling the minimum batch requirements. We will define the decision variables, objective function, and constraints in this linear programming model.

Let's denote:
- \( x_p \) as the number of batches of part \( p \) to be produced.
- \( \text{extra}_{m} \) as the extra hours purchased for machine \( m \).

We will utilize the inputs provided to construct the model.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\textbf{Decision Variables:}
\begin{align*}
x_p & : \text{Number of batches of part } p \text{ produced, for } p = 1, ..., P \\
\text{extra}_m & : \text{Extra hours purchased for machine } m, \text{ for } m = 1, ..., M
\end{align*}

\textbf{Objective Function:}

Maximize total profit:
\[
\text{Profit} = \sum_{p=1}^{P} \left( \text{price}_p \cdot x_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \right) + \text{extra}_m \cdot \text{extra\_cost}_m \right)
\]

\textbf{Constraints:}

1. Machine availability including extra hours:
\[
\sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{availability}_m + \text{extra}_m, \quad \forall m = 1, ..., M
\]

2. Minimum batch production requirements:
\[
x_p \geq \text{min\_batches}_p, \quad \forall p = 1, ..., P
\]

3. Limit on extra hours purchased:
\[
0 \leq \text{extra}_m \leq \text{max\_extra}_m, \quad \forall m = 1, ..., M
\]

4. Non-negativity of decision variables:
\[
x_p \geq 0, \quad \text{extra}_m \geq 0, \quad \forall p = 1, ..., P, \ \forall m = 1, ..., M
\]

\end{document}
```

This linear programming model aims to determine the optimal number of batches for each part and any additional machine time required to maximize profits while satisfying constraints such as machine availability, minimum production requirements, and limits on extra hours. Adjustments can be made to the input parameters to reflect real-world scenarios within the model.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Formulation}

\textbf{Decision Variables:}
\begin{align*}
x_p & : \text{Number of batches of part } p \text{ produced, for } p = 1, ..., P \\
\text{extra}_m & : \text{Extra hours purchased for machine } m, \text{ for } m = 1, ..., M
\end{align*}

\textbf{Objective Function:}

Maximize total profit:
\[
\text{Profit} = \sum_{p=1}^{P} \left( \text{price}_p \cdot x_p \right) - \sum_{m=1}^{M} \left( \text{cost}_m \cdot \left( \sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \right) + \text{extra}_m \cdot \text{extra\_cost}_m \right)
\]

\textbf{Constraints:}

1. Machine availability including extra hours:
\[
\sum_{p=1}^{P} \text{time}_{m,p} \cdot x_p \leq \text{availability}_m + \text{extra}_m, \quad \forall m = 1, ..., M
\]

2. Minimum batch production requirements:
\[
x_p \geq \text{min\_batches}_p, \quad \forall p = 1, ..., P
\]

3. Limit on extra hours purchased:
\[
0 \leq \text{extra}_m \leq \text{max\_extra}_m, \quad \forall m = 1, ..., M
\]

4. Non-negativity of decision variables:
\[
x_p \geq 0, \quad \text{extra}_m \geq 0, \quad \forall p = 1, ..., P, \ \forall m = 1, ..., M
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

#### Initialize problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
num_parts = len(data['prices'])
num_machines = len(data['machine_costs'])

x = [pulp.LpVariable(f'x_{p}', lowBound=0) for p in range(num_parts)]
extra = [pulp.LpVariable(f'extra_{m}', lowBound=0, upBound=data['max_extra'][m]) for m in range(num_machines)]

#### Objective function
profit = (
    pulp.lpSum(data['prices'][p] * x[p] for p in range(num_parts)) 
    - pulp.lpSum(
        data['machine_costs'][m] * (
            pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(num_parts))
        ) + extra[m] * data['extra_costs'][m] 
        for m in range(num_machines)
    )
)
problem += profit

#### Constraints

#### Machine availability including extra hours
for m in range(num_machines):
    problem += (
        pulp.lpSum(data['time_required'][m][p] * x[p] for p in range(num_parts)) 
        <= data['availability'][m] + extra[m]
    )

#### Minimum batch production requirements
for p in range(num_parts):
    problem += x[p] >= data['min_batches'][p]

#### Solve problem
problem.solve()

#### Print objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

