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
To solve this Linear Programming problem, we will define the decision variables, objective function, and constraints. Here is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Sets}
\begin{itemize}
    \item \( A \): Set of alloys, indexed by \( a \)
    \item \( S \): Set of steel types, indexed by \( s \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{available}_{a} \): Tons of alloy \( a \) available
    \item \( \text{carbon}_{a} \): Percent of carbon in alloy \( a \)
    \item \( \text{nickel}_{a} \): Percent of nickel in alloy \( a \)
    \item \( \text{alloy\_price}_{a} \): Cost per ton of alloy \( a \)
    \item \( \text{steel\_price}_{s} \): Selling price per ton of steel \( s \)
    \item \( \text{carbon\_min}_{s} \): Minimum percent of carbon required in steel \( s \)
    \item \( \text{nickel\_max}_{s} \): Maximum percent of nickel allowed in steel \( s \)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{alloy\_amount}_{a,s} \): Amount of alloy \( a \) used in steel \( s \)
    \item \( \text{total\_steel}_{s} \): Total amount of steel type \( s \) produced
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{total\_profit} = \sum_{s \in S} \left( \text{steel\_price}_{s} \times \text{total\_steel}_{s} \right) - \sum_{a \in A} \sum_{s \in S} \left( \text{alloy\_price}_{a} \times \text{alloy\_amount}_{a,s} \right)
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Material Balance for Each Steel Type:
    \[
    \text{total\_steel}_{s} = \sum_{a \in A} \text{alloy\_amount}_{a,s} \quad \forall s \in S
    \]
    
    \item Carbon Requirement for Each Steel Type:
    \[
    \sum_{a \in A} \left( \text{carbon}_{a} \times \text{alloy\_amount}_{a,s} \right) \geq \text{carbon\_min}_{s} \times \text{total\_steel}_{s} \quad \forall s \in S
    \]
    
    \item Nickel Limitation for Each Steel Type:
    \[
    \sum_{a \in A} \left( \text{nickel}_{a} \times \text{alloy\_amount}_{a,s} \right) \leq \text{nickel\_max}_{s} \times \text{total\_steel}_{s} \quad \forall s \in S
    \]
    
    \item Alloy Availability:
    \[
    \sum_{s \in S} \text{alloy\_amount}_{a,s} \leq \text{available}_{a} \quad \forall a \in A
    \]
    
    \item Alloy 1 Usage Limitation:
    \[
    \text{alloy\_amount}_{1,s} \leq 0.4 \times \text{total\_steel}_{s} \quad \forall s \in S
    \]
    
    \item Non-negativity:
    \[
    \text{alloy\_amount}_{a,s} \geq 0, \quad \text{total\_steel}_{s} \geq 0 \quad \forall a \in A, s \in S
    \]
\end{enumerate}

\end{document}
``` 

This model maximizes the total profit by determining how much of each alloy should be used in each type of steel while satisfying the material, carbon, nickel, and availability constraints.

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

\subsection*{Sets}
\begin{itemize}
    \item \( A \): Set of alloys, indexed by \( a \)
    \item \( S \): Set of steel types, indexed by \( s \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{available}_{a} \): Tons of alloy \( a \) available
    \item \( \text{carbon}_{a} \): Percent of carbon in alloy \( a \)
    \item \( \text{nickel}_{a} \): Percent of nickel in alloy \( a \)
    \item \( \text{alloy\_price}_{a} \): Cost per ton of alloy \( a \)
    \item \( \text{steel\_price}_{s} \): Selling price per ton of steel \( s \)
    \item \( \text{carbon\_min}_{s} \): Minimum percent of carbon required in steel \( s \)
    \item \( \text{nickel\_max}_{s} \): Maximum percent of nickel allowed in steel \( s \)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{alloy\_amount}_{a,s} \): Amount of alloy \( a \) used in steel \( s \)
    \item \( \text{total\_steel}_{s} \): Total amount of steel type \( s \) produced
\end{itemize}

\subsection*{Objective Function}
Maximize total profit:
\[
\text{total\_profit} = \sum_{s \in S} \left( \text{steel\_price}_{s} \times \text{total\_steel}_{s} \right) - \sum_{a \in A} \sum_{s \in S} \left( \text{alloy\_price}_{a} \times \text{alloy\_amount}_{a,s} \right)
\]

\subsection*{Constraints}
\begin{enumerate}
    \item Material Balance for Each Steel Type:
    \[
    \text{total\_steel}_{s} = \sum_{a \in A} \text{alloy\_amount}_{a,s} \quad \forall s \in S
    \]
    
    \item Carbon Requirement for Each Steel Type:
    \[
    \sum_{a \in A} \left( \text{carbon}_{a} \times \text{alloy\_amount}_{a,s} \right) \geq \text{carbon\_min}_{s} \times \text{total\_steel}_{s} \quad \forall s \in S
    \]
    
    \item Nickel Limitation for Each Steel Type:
    \[
    \sum_{a \in A} \left( \text{nickel}_{a} \times \text{alloy\_amount}_{a,s} \right) \leq \text{nickel\_max}_{s} \times \text{total\_steel}_{s} \quad \forall s \in S
    \]
    
    \item Alloy Availability:
    \[
    \sum_{s \in S} \text{alloy\_amount}_{a,s} \leq \text{available}_{a} \quad \forall a \in A
    \]
    
    \item Alloy 1 Usage Limitation:
    \[
    \text{alloy\_amount}_{1,s} \leq 0.4 \times \text{total\_steel}_{s} \quad \forall s \in S
    \]
    
    \item Non-negativity:
    \[
    \text{alloy\_amount}_{a,s} \geq 0, \quad \text{total\_steel}_{s} \geq 0 \quad \forall a \in A, s \in S
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Problem data
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

#### Sets
alloys = range(len(data['available']))
steel_types = range(len(data['steel_prices']))

#### Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision Variables
alloy_amount = pulp.LpVariable.dicts("AlloyAmount", (alloys, steel_types), 0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("TotalSteel", steel_types, 0, cat='Continuous')

#### Objective Function
problem += (
    pulp.lpSum(data['steel_prices'][s] * total_steel[s] for s in steel_types) -
    pulp.lpSum(data['alloy_prices'][a] * alloy_amount[a][s] for a in alloys for s in steel_types)
), "Total Profit"

#### Constraints
#### Material Balance
for s in steel_types:
    problem += (total_steel[s] == pulp.lpSum(alloy_amount[a][s] for a in alloys)), f"MaterialBalance_Steel_{s}"

#### Carbon Requirement
for s in steel_types:
    problem += (
        pulp.lpSum(data['carbon'][a] * alloy_amount[a][s] for a in alloys) >= 
        data['carbon_min'][s] * total_steel[s]
    ), f"CarbonRequirement_Steel_{s}"

#### Nickel Limitation
for s in steel_types:
    problem += (
        pulp.lpSum(data['nickel'][a] * alloy_amount[a][s] for a in alloys) <= 
        data['nickel_max'][s] * total_steel[s]
    ), f"NickelLimitation_Steel_{s}"

#### Alloy Availability
for a in alloys:
    problem += (
        pulp.lpSum(alloy_amount[a][s] for s in steel_types) <= data['available'][a]
    ), f"AlloyAvailability_Alloy_{a}"

#### Alloy 1 Usage Limitation
for s in steel_types:
    problem += (
        alloy_amount[0][s] <= 0.4 * total_steel[s]
    ), f"Alloy1UsageLimitation_Steel_{s}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

