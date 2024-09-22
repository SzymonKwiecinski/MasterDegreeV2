# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- A company produces and sells \var{P} different products. 
- The demand for each product is unlimited, but the company is constrained by cash availability and machine capacity.
- Each unit of the \var{i}-th product requires \var{hour_i} machine hours.
- There are \var{availableHours} machine hours available in the current production period.
- The production costs are \var{cost_i} per unit of the \var{i}-th product.
- The selling prices of the \var{i}-th product is \var{price_i} per unit.
- The available cash is \var{cash}.
- Furthermore, \var{investRate_i} of the sales revenues from the \var{i}-th product will be made available to finance operations during the current period.
- \var{investPercentage_i} is a number between 0 and 1
- The company could increase its available machine hours by \var{upgradeHours}, after spending \var{upgradeCost} for certain repairs. 
- The net income from each product is the revenue we get from selling it minus the production cost and the investment cost.

INPUT FORMAT:

{
    "cash": cash,
    "hour": [hour_i for i in 1, ..., P],
    "cost": [cost_i for i in 1, ..., P],
    "price": [price_i for i in 1, ..., P],
    "investPercentage": [investPercentage_i for i in 1, ..., P],
    "upgradeHours": upgradeHours,   
    "upgradeCost": upgradeCost,
    "availableHours": availableHours,
}

OBJECTIVE: We are aiming at maximizing total net income subject to the cash availability and machine capacity limitations

OUTPUT INFO:

- \var{net_income} shows the net income of the company
- \var{production_i} shows the production quantity of the \var{i}-th product
- \var{upgrade} is a boolean variable that shows whether the company should upgrade its machine capacity or not

OUTPUT FORMAT:

{
    "net_income": net_income,
    "production": [production_i for i in 1, ..., P],
    "upgrade": true/false,
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Production Optimization}

\subsection*{Indices}
\begin{itemize}
    \item \( i \) : Index for products, \( i = 1, 2, \ldots, P \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{cash} \) : Available cash in monetary units
    \item \( \text{hour}_i \) : Machine hours required per unit of product \( i \)
    \item \( \text{cost}_i \) : Production cost per unit of product \( i \)
    \item \( \text{price}_i \) : Selling price per unit of product \( i \)
    \item \( \text{investPercentage}_i \) : Investment percentage of sales revenue for product \( i \)
    \item \( \text{upgradeHours} \) : Additional machine hours available if upgraded
    \item \( \text{upgradeCost} \) : Cost to upgrade the machine capacity
    \item \( \text{availableHours} \) : Available machine hours without upgrade
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{production}_i \) : Number of units to produce for product \( i \)
    \item \( \text{upgrade} \) : Binary variable, 1 if upgrade is chosen, 0 otherwise
\end{itemize}

\subsection*{Objective Function}
Maximize the total net income:
\[
\max \quad \text{net\_income} = \sum_{i=1}^{P} \left( \text{price}_i \times \text{production}_i - \left( \text{cost}_i + \text{investPercentage}_i \times \text{price}_i \right) \times \text{production}_i \right) - \text{upgradeCost} \times \text{upgrade}
\]

\subsection*{Constraints}

\begin{itemize}
    \item Cash constraint:
    \[
    \sum_{i=1}^{P} (\text{production}_i \times \text{cost}_i) \leq \text{cash} + \sum_{i=1}^{P} (\text{investPercentage}_i \times \text{price}_i \times \text{production}_i)
    \]

    \item Machine capacity constraint:
    \[
    \sum_{i=1}^{P} (\text{production}_i \times \text{hour}_i) \leq \text{availableHours} + \text{upgradeHours} \times \text{upgrade}
    \]

    \item Binary constraint for upgrade decision:
    \[
    \text{upgrade} \in \{0, 1\}
    \]

    \item Non-negativity constraint:
    \[
    \text{production}_i \geq 0 \quad \forall i
    \]
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

\section*{Linear Programming Model for Production Optimization}

\subsection*{Indices}
\begin{itemize}
    \item \( i \) : Index for products, \( i = 1, 2, \ldots, P \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{cash} \) : Available cash in monetary units
    \item \( \text{hour}_i \) : Machine hours required per unit of product \( i \)
    \item \( \text{cost}_i \) : Production cost per unit of product \( i \)
    \item \( \text{price}_i \) : Selling price per unit of product \( i \)
    \item \( \text{investPercentage}_i \) : Investment percentage of sales revenue for product \( i \)
    \item \( \text{upgradeHours} \) : Additional machine hours available if upgraded
    \item \( \text{upgradeCost} \) : Cost to upgrade the machine capacity
    \item \( \text{availableHours} \) : Available machine hours without upgrade
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{production}_i \) : Number of units to produce for product \( i \)
    \item \( \text{upgrade} \) : Binary variable, 1 if upgrade is chosen, 0 otherwise
\end{itemize}

\subsection*{Objective Function}
Maximize the total net income:
\[
\max \quad \text{net\_income} = \sum_{i=1}^{P} \left( \text{price}_i \times \text{production}_i - \left( \text{cost}_i + \text{investPercentage}_i \times \text{price}_i \right) \times \text{production}_i \right) - \text{upgradeCost} \times \text{upgrade}
\]

\subsection*{Constraints}

\begin{itemize}
    \item Cash constraint:
    \[
    \sum_{i=1}^{P} (\text{production}_i \times \text{cost}_i) \leq \text{cash} + \sum_{i=1}^{P} (\text{investPercentage}_i \times \text{price}_i \times \text{production}_i)
    \]

    \item Machine capacity constraint:
    \[
    \sum_{i=1}^{P} (\text{production}_i \times \text{hour}_i) \leq \text{availableHours} + \text{upgradeHours} \times \text{upgrade}
    \]

    \item Binary constraint for upgrade decision:
    \[
    \text{upgrade} \in \{0, 1\}
    \]

    \item Non-negativity constraint:
    \[
    \text{production}_i \geq 0 \quad \forall i
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'P': 2,
    'Cash': 3000,
    'Hour': [2, 6],
    'Cost': [3, 2],
    'Price': [6, 5],
    'InvestPercentage': [0.4, 0.3],
    'UpgradeHours': 2000,
    'UpgradeCost': 400,
    'AvailableHours': 2000
}

#### Initialize the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

#### Decision Variables
production = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Continuous') for i in range(data['P'])]
upgrade = pulp.LpVariable('upgrade', cat='Binary')

#### Objective Function
net_income = pulp.lpSum((data['Price'][i] * production[i] - 
                         (data['Cost'][i] + data['InvestPercentage'][i] * data['Price'][i]) * production[i]) 
                         for i in range(data['P'])) - data['UpgradeCost'] * upgrade
problem += net_income

#### Constraints

#### Cash constraint
cash_constraint = pulp.lpSum(production[i] * data['Cost'][i] for i in range(data['P'])) <= (
    data['Cash'] + pulp.lpSum(data['InvestPercentage'][i] * data['Price'][i] * production[i] for i in range(data['P'])))
problem += cash_constraint

#### Machine capacity constraint
machine_capacity_constraint = pulp.lpSum(production[i] * data['Hour'][i] for i in range(data['P'])) <= (
    data['AvailableHours'] + data['UpgradeHours'] * upgrade)
problem += machine_capacity_constraint

#### Non-negativity constraints are automatically handled by `lowBound=0` in `LpVariable`.

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

