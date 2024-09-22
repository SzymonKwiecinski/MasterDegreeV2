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
- Machine \var{1} is being outsourced so that the manufacturer must pay for the labor.
- The labor costs $\var{standard_cost}/h up to \var{overtime_hour} hours, after which it costs $\var{overtime_cost}/h due to overtime.
- Individual availability conditions for Machine \var{1} can be disregarded.
- The desired profit should surpass \var{min_profit}.

INPUT FORMAT: 

{
    "time_required": [[time_{m,p} for p in 1, ..., P] for m in 1, ..., M],
    "machine_costs": [cost_{m} for m in 1, ..., M],
    "availability": [available_{m} for m in 1, ..., M],
    "prices": [price_{p} for p in 1, ..., P],
    "min_batches": [min_batches_{p} for p in 1, ..., P],
    "standard_cost": standard_cost,
    "overtime_cost": overtime_cost,
    "overtime_hour": overtime_hour,
    "min_profit": min_profit
}

OBJECTIVE: Determine the quantity of batches for each part the manufacturer should produce every month, ensuring all constraints are met.

OUTPUT INFO:

- the number of batches of each part produced \var{batches_{p}}.
- \var{total_profit} represents the total profit obtained for the month.

OUTPUT FORMAT:

{
    "batches": [batches_{p} for p in 1, ..., P],
    "total_profit": total_profit
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Auto Parts Manufacturer}

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of different parts
    \item $M$: Number of different machines
    \item $time_{m,p}$: Time required on machine $m$ to produce a batch of part $p$ (in hours)
    \item $cost_{m}$: Cost per hour for using machine $m$
    \item $available_{m}$: Availability of machine $m$ (in hours per month)
    \item $price_{p}$: Price for selling one batch of part $p$
    \item $min\_batches_{p}$: Minimum number of batches of part $p$ to produce
    \item $standard\_cost$: Standard labor cost per hour (for Machine 1)
    \item $overtime\_cost$: Overtime labor cost per hour (for Machine 1)
    \item $overtime\_hour$: Maximum standard hours before overtime applies
    \item $min\_profit$: Minimum desired profit
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_p$: Number of batches produced for part $p$ (for $p = 1, \ldots, P$)
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} (cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p})) - \text{Labor Cost for Machine 1}
\]

Where the labor cost for Machine 1 can be expressed as:
\[
\text{Labor Cost for Machine 1} =
\begin{cases} 
standard\_cost \cdot hours & \text{if } hours \leq overtime\_hour \\
standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (hours - overtime\_hour) & \text{if } hours > overtime\_hour 
\end{cases}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Time constraints for each machine:
    \[
    \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m} \quad \forall m = 1, \ldots, M
    \]
    
    \item Minimum production requirement for each part:
    \[
    batches_{p} \geq min\_batches_{p} \quad \forall p = 1, \ldots, P
    \]

    \item Minimum profit requirement:
    \[
    Z \geq min\_profit
    \end{itemize}

\subsection*{Non-negativity Constraints}
\[
batches_{p} \geq 0 \quad \forall p = 1, \ldots, P
\]

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

\section*{Linear Programming Model for Auto Parts Manufacturer}

\subsection*{Parameters}
\begin{itemize}
    \item $P$: Number of different parts
    \item $M$: Number of different machines
    \item $time_{m,p}$: Time required on machine $m$ to produce a batch of part $p$ (in hours)
    \item $cost_{m}$: Cost per hour for using machine $m$
    \item $available_{m}$: Availability of machine $m$ (in hours per month)
    \item $price_{p}$: Price for selling one batch of part $p$
    \item $min\_batches_{p}$: Minimum number of batches of part $p$ to produce
    \item $standard\_cost$: Standard labor cost per hour (for Machine 1)
    \item $overtime\_cost$: Overtime labor cost per hour (for Machine 1)
    \item $overtime\_hour$: Maximum standard hours before overtime applies
    \item $min\_profit$: Minimum desired profit
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $batches_p$: Number of batches produced for part $p$ (for $p = 1, \ldots, P$)
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{Maximize } Z = \sum_{p=1}^{P} (price_{p} \cdot batches_{p}) - \sum_{m=1}^{M} (cost_{m} \cdot \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p})) - \text{Labor Cost for Machine 1}
\]

Where the labor cost for Machine 1 can be expressed as:
\[
\text{Labor Cost for Machine 1} =
\begin{cases} 
standard\_cost \cdot hours & \text{if } hours \leq overtime\_hour \\
standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (hours - overtime\_hour) & \text{if } hours > overtime\_hour 
\end{cases}
\]

\subsection*{Constraints}
\begin{itemize}
    \item Time constraints for each machine:
    \[
    \sum_{p=1}^{P} (time_{m,p} \cdot batches_{p}) \leq available_{m} \quad \forall m = 1, \ldots, M
    \]
    
    \item Minimum production requirement for each part:
    \[
    batches_{p} \geq min\_batches_{p} \quad \forall p = 1, \ldots, P
    \]

    \item Minimum profit requirement:
    \[
    Z \geq min\_profit
    \end{itemize}

\subsection*{Non-negativity Constraints}
\[
batches_{p} \geq 0 \quad \forall p = 1, \ldots, P
\]

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'standard_cost': 20,
    'overtime_cost': 30,
    'overtime_hour': 400,
    'min_profit': 5000
}

#### Parameters
P = len(data['prices'])  #### Number of different parts
M = len(data['time_required'])  #### Number of different machines
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

#### Create the LP problem
problem = pulp.LpProblem("AutoPartsManufacturing", pulp.LpMaximize)

#### Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

#### Objective Function
labor_cost_expr = pulp.lpSum(
    (standard_cost * pulp.lpSum(time_required[0][p] * batches[p] for p in range(P)) 
     if pulp.lpSum(time_required[0][p] * batches[p] for p in range(P)) <= overtime_hour
     else standard_cost * overtime_hour + overtime_cost * (pulp.lpSum(time_required[0][p] * batches[p] for p in range(P)) - overtime_hour))
)

profit_expr = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
               pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M)) - labor_cost_expr

problem += profit_expr, "TotalProfit"

#### Constraints
#### Time constraints for each machine
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"MachineAvailability_{m}"

#### Minimum production requirement for each part
for p in range(P):
    problem += batches[p] >= min_batches[p], f"MinBatches_{p}"

#### Minimum profit requirement
problem += profit_expr >= min_profit, "MinProfit"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

