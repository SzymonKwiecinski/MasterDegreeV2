# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A foundry receives a specific order for \var{n_steel_quant} tons of steel. 
- This steel must meet the following characteristics: it must contain at least \var{mn_percent} percentage of manganese (Mn) while its percentage of silicon (SI) must be between \var{si_min} and \var{si_max}.
- To cast this steel, the foundry has limited quantities of several types of minerals.
- The contents expressed in percentage per mineral \var{k} are \var{contsi_{k}} for Si and \var{contmn_{k}} for Mn.
- The process for producing steel is such that direct addition of Mn is possible.
- This Manganese is available at a price of \var{mang_price} million euros per ton. 
- As for the minerals, it costs \var{cost_{k}} million euros per thousand tons for mineral \var{k}.
- The foundry plans to sell the steel produced at \var{sell_price} million euros per ton.
- The cost of smelting a ton of mineral is \var{melt_price} million euros.

INPUT FORMAT:

{
	"n_steel_quant": n_steel_quant,
	"mn_percent": mn_percent,
	"si_min": si_min,
	"si_max": si_max,
	"contsi": [contsi_{k} for k in 1,...,K]
	"contmn": [contmn_{k} for k in 1,...,K]
	"mang_price": mang_price,
	"cost": [cost_{k} for k in 1,...,K]
	"sell_price": sell_price,
	"melt_price": melt_price
}

OBJECTIVE: How should the manufacture manage the steel to maximize profit?

OUTPUT INFO:

- \var{amount} represents the amount of each mineral melted
- \var{num_mang} represents the amount of Manganese directly added

OUTPUT FORMAT:

{
	"amount": [amount_{k} for k in 1,...,K]
	"num_mang": [num_mang]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Steel Production}

\subsection*{Parameters}
\begin{itemize}
    \item \( n_{steel\_quant} \): Total tons of steel required
    \item \( mn\_percent \): Minimum percentage of manganese (Mn) required in the steel
    \item \( si_{min} \): Minimum allowable percentage of silicon (Si)
    \item \( si_{max} \): Maximum allowable percentage of silicon (Si)
    \item \( contsi_k \): Percentage of silicon in mineral \( k \)
    \item \( contmn_k \): Percentage of manganese in mineral \( k \)
    \item \( mang\_price \): Price of manganese per ton (in million euros)
    \item \( cost_k \): Cost of mineral \( k \) per thousand tons (in million euros)
    \item \( sell\_price \): Selling price of steel per ton (in million euros)
    \item \( melt\_price \): Cost of melting a ton of mineral (in million euros)
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item \( amount_k \): Amount of mineral \( k \) melted (in tons)
    \item \( num\_mang \): Amount of manganese directly added (in tons)
\end{itemize}

\subsection*{Objective Function}
Maximize profit \( P \):
\[
P = n_{steel\_quant} \times sell\_price - \sum_{k=1}^{K} \left( \frac{cost_k}{1000} \times amount_k + melt\_price \times amount_k \right) - mang\_price \times num\_mang
\]

\subsection*{Constraints}
1. Steel production requirement:
\[
amount_{total} = \sum_{k=1}^{K} amount_k + num\_mang = n_{steel\_quant}
\]

2. Manganese content requirement:
\[
\frac{\sum_{k=1}^{K} amount_k \times contmn_k}{amount_{total}} \geq \frac{mn\_percent}{100} \times n_{steel\_quant}
\]

3. Silicon content constraints:
\[
\frac{si_{min}}{100} \times amount_{total} \leq \frac{\sum_{k=1}^{K} amount_k \times contsi_k}{amount_{total}} \leq \frac{si_{max}}{100} \times amount_{total}
\]

4. Non-negativity constraints:
\[
amount_k \geq 0 \quad \forall k \in \{1, 2, ..., K\}
\]
\[
num\_mang \geq 0
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

\section*{Linear Programming Model for Steel Production}

\subsection*{Parameters}
\begin{itemize}
    \item \( n_{steel\_quant} \): Total tons of steel required
    \item \( mn\_percent \): Minimum percentage of manganese (Mn) required in the steel
    \item \( si_{min} \): Minimum allowable percentage of silicon (Si)
    \item \( si_{max} \): Maximum allowable percentage of silicon (Si)
    \item \( contsi_k \): Percentage of silicon in mineral \( k \)
    \item \( contmn_k \): Percentage of manganese in mineral \( k \)
    \item \( mang\_price \): Price of manganese per ton (in million euros)
    \item \( cost_k \): Cost of mineral \( k \) per thousand tons (in million euros)
    \item \( sell\_price \): Selling price of steel per ton (in million euros)
    \item \( melt\_price \): Cost of melting a ton of mineral (in million euros)
\end{itemize}

\subsection*{Variables}
\begin{itemize}
    \item \( amount_k \): Amount of mineral \( k \) melted (in tons)
    \item \( num\_mang \): Amount of manganese directly added (in tons)
\end{itemize}

\subsection*{Objective Function}
Maximize profit \( P \):
\[
P = n_{steel\_quant} \times sell\_price - \sum_{k=1}^{K} \left( \frac{cost_k}{1000} \times amount_k + melt\_price \times amount_k \right) - mang\_price \times num\_mang
\]

\subsection*{Constraints}
1. Steel production requirement:
\[
amount_{total} = \sum_{k=1}^{K} amount_k + num\_mang = n_{steel\_quant}
\]

2. Manganese content requirement:
\[
\frac{\sum_{k=1}^{K} amount_k \times contmn_k}{amount_{total}} \geq \frac{mn\_percent}{100} \times n_{steel\_quant}
\]

3. Silicon content constraints:
\[
\frac{si_{min}}{100} \times amount_{total} \leq \frac{\sum_{k=1}^{K} amount_k \times contsi_k}{amount_{total}} \leq \frac{si_{max}}{100} \times amount_{total}
\]

4. Non-negativity constraints:
\[
amount_k \geq 0 \quad \forall k \in \{1, 2, ..., K\}
\]
\[
num\_mang \geq 0
\]

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'n_steel_quant': 1000,
    'mn_percent': 0.45,
    'si_min': 3.25,
    'si_max': 5.0,
    'contsi': [4.0, 1.0, 0.6],
    'contmn': [0.45, 0.5, 0.4],
    'mang_price': 8.0,
    'cost': [21, 25, 15],
    'sell_price': 0.45,
    'melt_price': 0.005
}

#### Define the problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

#### Define variables
K = len(data['contsi'])
amount_k = pulp.LpVariable.dicts("amount_k", range(K), lowBound=0)
num_mang = pulp.LpVariable("num_mang", lowBound=0)

#### Objective function
profit = data['n_steel_quant'] * data['sell_price'] - \
         pulp.lpSum((data['cost'][k] / 1000) * amount_k[k] + data['melt_price'] * amount_k[k] for k in range(K)) - \
         data['mang_price'] * num_mang

problem += profit

#### Total amount of steel produced
amount_total = pulp.lpSum(amount_k[k] for k in range(K)) + num_mang

#### Constraints
problem += (amount_total == data['n_steel_quant'], "Steel_Production_Requirement")

#### Manganese content requirement
manganese_content = pulp.lpSum(amount_k[k] * data['contmn'][k] for k in range(K))
problem += (manganese_content >= (data['mn_percent'] / 100) * amount_total, "Manganese_Content_Requirement")

#### Silicon content constraints
silicon_content = pulp.lpSum(amount_k[k] * data['contsi'][k] for k in range(K))
problem += (silicon_content >= (data['si_min'] / 100) * amount_total, "Silicon_Content_Min")
problem += (silicon_content <= (data['si_max'] / 100) * amount_total, "Silicon_Content_Max")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

