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

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( b_p \) be the number of batches produced for part \( p \) where \( p = 1, 2, \ldots, P \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( time_{m,p} \): hours required on machine \( m \) to produce a batch of part \( p \).
    \item \( cost_m \): cost per hour of using machine \( m \).
    \item \( available_m \): total available hours of machine \( m \) per month.
    \item \( price_p \): selling price per batch of part \( p \).
    \item \( min\_batches_p \): minimum batches that must be produced for part \( p \).
    \item \( standard\_cost \): cost per hour for standard labor.
    \item \( overtime\_cost \): cost per hour for overtime labor.
    \item \( overtime\_hour \): threshold hours for paying overtime.
    \item \( min\_profit \): minimum desired profit for the month.
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
    \text{Maximize} \quad Z &= \sum_{p=1}^P \left( price_p \cdot b_p \right) - \sum_{m=1}^M \left( cost_m \cdot \sum_{p=1}^P \left( time_{m,p} \cdot b_p \right) \right) - \text{Labor Costs}
\end{align*}

\textbf{Labor Costs:}
\begin{align*}
    \text{Labor Costs} &= \begin{cases} 
    standard\_cost \cdot \text{Total Hours} & \text{if Total Hours} \leq overtime\_hour \\
    standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (\text{Total Hours} - overtime\_hour) & \text{if Total Hours} > overtime\_hour 
    \end{cases}
\end{align*}

Where Total Hours is the total time spent on machine 1, calculated as:
\[
\text{Total Hours} = \sum_{p=1}^P (time_{1,p} \cdot b_p)
\]

\textbf{Constraints:}
\begin{align*}
    1. & \quad b_p \geq min\_batches_p, \quad \forall p = 1, \ldots, P \\
    2. & \quad \sum_{p=1}^P (time_{m,p} \cdot b_p) \leq available_m, \quad \forall m = 1, \ldots, M \\
    3. & \quad Z \geq min\_profit
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item \( batches = [b_1, b_2, \ldots, b_P] \)
    \item \( total\_profit = Z \)
\end{itemize}

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

\textbf{Decision Variables:}
\begin{itemize}
    \item Let \( b_p \) be the number of batches produced for part \( p \) where \( p = 1, 2, \ldots, P \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( time_{m,p} \): hours required on machine \( m \) to produce a batch of part \( p \).
    \item \( cost_m \): cost per hour of using machine \( m \).
    \item \( available_m \): total available hours of machine \( m \) per month.
    \item \( price_p \): selling price per batch of part \( p \).
    \item \( min\_batches_p \): minimum batches that must be produced for part \( p \).
    \item \( standard\_cost \): cost per hour for standard labor.
    \item \( overtime\_cost \): cost per hour for overtime labor.
    \item \( overtime\_hour \): threshold hours for paying overtime.
    \item \( min\_profit \): minimum desired profit for the month.
\end{itemize}

\textbf{Objective Function:}
\begin{align*}
    \text{Maximize} \quad Z &= \sum_{p=1}^P \left( price_p \cdot b_p \right) - \sum_{m=1}^M \left( cost_m \cdot \sum_{p=1}^P \left( time_{m,p} \cdot b_p \right) \right) - \text{Labor Costs}
\end{align*}

\textbf{Labor Costs:}
\begin{align*}
    \text{Labor Costs} &= \begin{cases} 
    standard\_cost \cdot \text{Total Hours} & \text{if Total Hours} \leq overtime\_hour \\
    standard\_cost \cdot overtime\_hour + overtime\_cost \cdot (\text{Total Hours} - overtime\_hour) & \text{if Total Hours} > overtime\_hour 
    \end{cases}
\end{align*}

Where Total Hours is the total time spent on machine 1, calculated as:
\[
\text{Total Hours} = \sum_{p=1}^P (time_{1,p} \cdot b_p)
\]

\textbf{Constraints:}
\begin{align*}
    1. & \quad b_p \geq min\_batches_p, \quad \forall p = 1, \ldots, P \\
    2. & \quad \sum_{p=1}^P (time_{m,p} \cdot b_p) \leq available_m, \quad \forall m = 1, \ldots, M \\
    3. & \quad Z \geq min\_profit
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item \( batches = [b_1, b_2, \ldots, b_P] \)
    \item \( total\_profit = Z \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'standard_cost': 20, 'overtime_cost': 30, 'overtime_hour': 400, 'min_profit': 5000}</DATA>


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
    'standard_cost': 20,
    'overtime_cost': 30,
    'overtime_hour': 400,
    'min_profit': 5000
}

#### Define the problem
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

#### Decision variables
P = len(data['prices'])  #### Number of parts
batches = pulp.LpVariable.dicts("b", range(P), lowBound=0, cat='Integer')

#### Objective function
total_profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
machine_costs = pulp.lpSum(data['machine_costs'][m] * (
    pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P))
) for m in range(len(data['machine_costs'])))
total_hours = pulp.lpSum(data['time_required'][0][p] * batches[p] for p in range(P))

#### Labor Costs
labor_costs = pulp.lpIf(total_hours <= data['overtime_hour'],
                        data['standard_cost'] * total_hours,
                        data['standard_cost'] * data['overtime_hour'] + 
                        data['overtime_cost'] * (total_hours - data['overtime_hour']))

#### Full objective function
profit_equation = total_profit - machine_costs - labor_costs
problem += profit_equation, "Total_Profit"

#### Constraints
#### Minimum batches
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_Batches_{p}"

#### Machine availability constraints
for m in range(len(data['availability'])):
    problem += (
        pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) 
        <= data['availability'][m], f"Availability_{m}"
    )

#### Minimum profit constraint
problem += profit_equation >= data['min_profit'], "Min_Profit"

#### Solve the problem
problem.solve()

#### Output results
batches_output = [pulp.value(batches[p]) for p in range(P)]
total_profit_value = pulp.value(problem.objective)
print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')
```

