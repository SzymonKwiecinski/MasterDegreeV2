# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- A company produces \var{S} different types of steel using \var{A} different alloys.
- The company has \var{available_{a}} tons of alloy \var{a} available.
- Steel \var{s} requires a certain percentage of carbon \var{carbon_min_{s}}.
- Steel \var{s} has a maximum allowable percentage for nickel \var{nickel_max_{s}}.
- Alloy \var{a} contains \var{carbon_{a}} percent of carbon and \var{nickel_{a}} percent of nickel.
- Alloy \var{a} has a purchase price of \var{alloy_price_{a}} per ton.
- Steel \var{s} has a selling price of \var{steel_price_{s}} per ton.
- All steel must have at most 40% of alloy 1.

INPUT FORMAT: 

{
"available": [available_{a} for a in 1, ..., A],
"carbon": [carbon_{a} for a in 1, ..., A],
"nickel": [nickel_{a} for a in 1, ..., A],
"alloy_prices": [alloy_price_{a} for a in 1, ..., A],
"steel_prices": [steel_price_{s} for s in 1, ..., S],
"carbon_min": [carbon_min_{s} for s in 1, ..., S],
"nickel_max": [nickel_min_{s} for s in 1, ..., S]
}

OBJECTIVE: How much of each alloy should the company use in each type of steel, and how much of each steel type should be produced to maximize profit?

OUTPUT INFO:

- The amount of each alloy used in each type of steel \var{alloy_amount_{a,s}}.
- \var{total_steel_{s}} shows the total amount of steel type \var{s} produced.
- \var{total_profit} represents the total profit.

OUTPUT FORMAT:

{
    "alloy_use": [[alloy_amount_{a,s} for a in 1, ..., A] for s in 1, ..., S],
    "total_steel": [total_steel_{s} for s in 1, ..., S],
    "total_profit": total_profit
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To create a mathematical model for the given problem, we need to set up an optimization problem that maximizes the profit for the company by deciding how much of each alloy to use in each type of steel and how much of each type of steel to produce, subject to the given constraints. Here is the Linear Programming model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Sets and Indices}
\begin{itemize}
    \item Let \( A \) be the set of alloys, indexed by \( a \).
    \item Let \( S \) be the set of steel types, indexed by \( s \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{available}_a \): Availability of alloy \( a \) in tons.
    \item \( \text{carbon}_a \): Percentage of carbon in alloy \( a \).
    \item \( \text{nickel}_a \): Percentage of nickel in alloy \( a \).
    \item \( \text{alloy\_price}_a \): Purchase price per ton of alloy \( a \).
    \item \( \text{steel\_price}_s \): Selling price per ton of steel \( s \).
    \item \( \text{carbon\_min}_s \): Minimum required percentage of carbon in steel \( s \).
    \item \( \text{nickel\_max}_s \): Maximum allowable percentage of nickel in steel \( s \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{alloy\_amount}_{a,s} \): Amount of alloy \( a \) used in steel \( s \) in tons.
    \item \( \text{total\_steel}_s \): Total production of steel type \( s \) in tons.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\max \sum_{s \in S} \left( \text{steel\_price}_s \cdot \text{total\_steel}_s \right) - \sum_{a \in A} \sum_{s \in S} \left( \text{alloy\_price}_a \cdot \text{alloy\_amount}_{a,s} \right)
\]

\subsection*{Constraints}
\begin{align}
& \text{Material balance for steel production:} \notag \\
& \text{total\_steel}_s = \sum_{a \in A} \text{alloy\_amount}_{a,s}, \quad \forall s \in S \\
& \text{Availability of alloy:} \notag \\
& \sum_{s \in S} \text{alloy\_amount}_{a,s} \leq \text{available}_a, \quad \forall a \in A \\
& \text{Carbon content constraint:} \notag \\
& \sum_{a \in A} \frac{\text{carbon}_a}{100} \times \text{alloy\_amount}_{a,s} \geq \frac{\text{carbon\_min}_s}{100} \times \text{total\_steel}_s, \quad \forall s \in S \\
& \text{Nickel content constraint:} \notag \\
& \sum_{a \in A} \frac{\text{nickel}_a}{100} \times \text{alloy\_amount}_{a,s} \leq \frac{\text{nickel\_max}_s}{100} \times \text{total\_steel}_s, \quad \forall s \in S \\
& \text{Maximum 40\% of alloy 1 in any steel:} \notag \\
& \text{alloy\_amount}_{1,s} \leq 0.4 \times \text{total\_steel}_s, \quad \forall s \in S \\
& \text{Non-negativity:} \notag \\
& \text{alloy\_amount}_{a,s} \geq 0, \quad \forall a \in A, s \in S \\
& \text{total\_steel}_s \geq 0, \quad \forall s \in S
\end{align}

\end{document}
```

The above model represents a Linear Programming problem that can be solved using optimization software to obtain the optimal production plan that maximizes profit for the company. The constraints ensure that the production adheres to material availability, content requirements for carbon and nickel, and the restriction on the use of alloy 1.

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

\subsection*{Sets and Indices}
\begin{itemize}
    \item Let \( A \) be the set of alloys, indexed by \( a \).
    \item Let \( S \) be the set of steel types, indexed by \( s \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{available}_a \): Availability of alloy \( a \) in tons.
    \item \( \text{carbon}_a \): Percentage of carbon in alloy \( a \).
    \item \( \text{nickel}_a \): Percentage of nickel in alloy \( a \).
    \item \( \text{alloy\_price}_a \): Purchase price per ton of alloy \( a \).
    \item \( \text{steel\_price}_s \): Selling price per ton of steel \( s \).
    \item \( \text{carbon\_min}_s \): Minimum required percentage of carbon in steel \( s \).
    \item \( \text{nickel\_max}_s \): Maximum allowable percentage of nickel in steel \( s \).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{alloy\_amount}_{a,s} \): Amount of alloy \( a \) used in steel \( s \) in tons.
    \item \( \text{total\_steel}_s \): Total production of steel type \( s \) in tons.
\end{itemize}

\subsection*{Objective Function}
Maximize the total profit:
\[
\max \sum_{s \in S} \left( \text{steel\_price}_s \cdot \text{total\_steel}_s \right) - \sum_{a \in A} \sum_{s \in S} \left( \text{alloy\_price}_a \cdot \text{alloy\_amount}_{a,s} \right)
\]

\subsection*{Constraints}
\begin{align}
& \text{Material balance for steel production:} \notag \\
& \text{total\_steel}_s = \sum_{a \in A} \text{alloy\_amount}_{a,s}, \quad \forall s \in S \\
& \text{Availability of alloy:} \notag \\
& \sum_{s \in S} \text{alloy\_amount}_{a,s} \leq \text{available}_a, \quad \forall a \in A \\
& \text{Carbon content constraint:} \notag \\
& \sum_{a \in A} \frac{\text{carbon}_a}{100} \times \text{alloy\_amount}_{a,s} \geq \frac{\text{carbon\_min}_s}{100} \times \text{total\_steel}_s, \quad \forall s \in S \\
& \text{Nickel content constraint:} \notag \\
& \sum_{a \in A} \frac{\text{nickel}_a}{100} \times \text{alloy\_amount}_{a,s} \leq \frac{\text{nickel\_max}_s}{100} \times \text{total\_steel}_s, \quad \forall s \in S \\
& \text{Maximum 40\% of alloy 1 in any steel:} \notag \\
& \text{alloy\_amount}_{1,s} \leq 0.4 \times \text{total\_steel}_s, \quad \forall s \in S \\
& \text{Non-negativity:} \notag \\
& \text{alloy\_amount}_{a,s} \geq 0, \quad \forall a \in A, s \in S \\
& \text{total\_steel}_s \geq 0, \quad \forall s \in S
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

#### Set indices
A = range(len(data['available']))  #### Alloys
S = range(len(data['steel_prices']))  #### Steel types

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", (A, S), lowBound=0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("total_steel", S, lowBound=0, cat='Continuous')

#### Objective Function
profit = pulp.lpSum(data['steel_prices'][s] * total_steel[s] for s in S) - \
         pulp.lpSum(data['alloy_prices'][a] * alloy_amount[a][s] for a in A for s in S)
problem += profit

#### Constraints

#### Material balance for steel production
for s in S:
    problem += total_steel[s] == pulp.lpSum(alloy_amount[a][s] for a in A), f"Material_Balance_{s}"

#### Availability of alloy
for a in A:
    problem += pulp.lpSum(alloy_amount[a][s] for s in S) <= data['available'][a], f"Alloy_Availability_{a}"

#### Carbon content constraint
for s in S:
    problem += pulp.lpSum((data['carbon'][a] / 100) * alloy_amount[a][s] for a in A) >= \
               (data['carbon_min'][s] / 100) * total_steel[s], f"Carbon_Content_{s}"

#### Nickel content constraint
for s in S:
    problem += pulp.lpSum((data['nickel'][a] / 100) * alloy_amount[a][s] for a in A) <= \
               (data['nickel_max'][s] / 100) * total_steel[s], f"Nickel_Content_{s}"

#### Maximum 40% of alloy 1 in any steel
for s in S:
    problem += alloy_amount[0][s] <= 0.4 * total_steel[s], f"Max_Alloy1_{s}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

