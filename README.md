# Carbon Credit Price Simulator for Amazon Forest Conservation

A Monte Carlo simulation tool that determines the equilibrium carbon credit prices needed to make forest conservation economically competitive with conventional land use (timber extraction, cattle ranching, and soybean farming) in the Brazilian Amazon rainforest.
Available at https://forest-forever.streamlit.app/

<img width="607" height="608" alt="image" src="https://github.com/user-attachments/assets/1c89fd58-46d7-4dd3-b53c-ea2f0e61f68a" />


## Overview

This application helps answer a critical question in environmental economics: **What price per ton of CO2 would make preserving Amazon rainforest more profitable than clearing it for agriculture?**

The simulator uses financial modeling to compare the Net Present Value (NPV) of:
- **Conventional land use**: Timber extraction + alternating cattle ranching and soybean farming
- **Conservation**: Carbon credit payments for existing forest carbon stock + annual sequestration

## Key Features

- **Monte Carlo Simulation**: Runs thousands of scenarios to account for revenue uncertainty
- **Dual Currency Support**: Display values in Brazilian Reais (R$) or US Dollars (US$)
- **Interactive Parameters**: Adjust discount rates, time horizons, and revenue assumptions
- **Visual Analytics**: Interactive charts showing NPV distributions and viable price combinations
- **Financial Analysis**: Detailed breakdown of annual equivalent values and trade-offs

## Scientific Basis

The model incorporates realistic Amazon rainforest parameters:
- **Carbon Stock**: 569 tons CO2/hectare (existing forest carbon)
- **Annual Absorption**: 9.5 tons CO2/hectare/year (sequestration rate)
- **Time Horizon**: 10-50 years (default: 30 years)
- **Discount Rate**: 1-20% (default: 8%)

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Dependencies
```bash
pip install streamlit numpy pandas plotly
```

### Quick Start
```bash
# Clone the repository
git clone <repository-url>
cd carbon-credit-simulator

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run Carlos.py
```

The application will open in your default web browser at `http://localhost:8501`

## How It Works

### 1. Conventional Land Use Simulation
The simulator models typical Amazon land exploitation:
- **Timber Extraction**: One-time revenue from logging (optional)
- **Cattle Ranching**: Annual revenue with variability
- **Soybean Farming**: Alternating with cattle, includes price volatility
- **Monte Carlo Approach**: Generates thousands of revenue scenarios

### 2. Carbon Credit Equilibrium Analysis
For each conventional use scenario, the tool calculates:
- **Stock Credits**: Payment for existing forest carbon (155 tCO2/ha)
- **Flow Credits**: Annual payments for carbon sequestration (0.5 tCO2/ha/year)
- **Viable Combinations**: Price pairs that make conservation competitive

### 3. Financial Metrics
- **Net Present Value (NPV)**: Discounted future cash flows
- **75th Percentile Target**: Carbon prices must beat 75% of conventional scenarios
- **Annual Equivalents**: Converts lump-sum payments to annual values

## User Interface

### Input Parameters

**Financial Settings:**
- Discount rate (1-20%)
- Time horizon (10-50 years)
- Currency display (R$ or US$)

**Conventional Use Parameters:**
- Timber value per hectare (optional)
- Cattle revenue (mean and standard deviation)
- Soybean revenue (mean and standard deviation)
- Number of Monte Carlo simulations

### Output Analysis

**Key Metrics:**
- Recommended stock credit price (total and annualized)
- Recommended flow credit price (annual)
- Conventional land use NPV statistics

**Visualizations:**
- NPV distribution histogram
- Viable price combination scatter plot
- Financial summary table

## Example Results

For typical Amazon parameters:
- **Stock Credit Price**: R$ 150-300 per tCO2 (total payment)
- **Flow Credit Price**: R$ 100-200 per tCO2/year (annual payment)
- **Break-even**: Conservation becomes competitive at these price levels

*Note: Actual results depend on local economic conditions and input parameters*

## Use Cases

### Policy Makers
- Determine minimum carbon credit prices for REDD+ programs
- Analyze cost-effectiveness of conservation incentives
- Model different economic scenarios and assumptions

### Researchers
- Study land-use economics in tropical forests
- Validate carbon pricing mechanisms
- Conduct sensitivity analysis on key parameters

### Conservation Organizations
- Develop funding strategies for forest protection
- Justify carbon credit pricing to investors
- Design payment schemes for landowners

### Carbon Market Participants
- Price carbon credits from forest conservation
- Evaluate investment opportunities in REDD+ projects
- Assess market demand at different price levels

## Technical Details

### Model Structure
```python
class CarbonCreditSimulation:
    - generate_price_scenarios()  # Monte Carlo price generation
    - calculate_npv()            # Net Present Value calculation
    - simulate_conventional_use() # Agriculture/timber scenarios
    - find_equilibrium_carbon_prices() # Break-even analysis
```

### Key Assumptions
- Normal distribution for revenue variability
- Simplified crop rotation (cattle/soy alternating)
- Constant carbon sequestration rate
- No transaction costs or market frictions

### Data Export
Results can be downloaded as CSV files for further analysis in Excel, R, or other tools.

## Limitations and Considerations

- **Simplified Model**: Real land use decisions involve many factors not captured
- **Price Distributions**: Assumes normal distributions for agricultural revenues  
- **Market Dynamics**: Doesn't account for carbon market liquidity or price volatility
- **Regulatory Framework**: Assumes stable carbon credit mechanisms
- **Regional Variation**: Parameters may need adjustment for different Amazon regions

## Contributing

Contributions are welcome! Areas for improvement:
- Additional land use scenarios (e.g., selective logging, agroforestry)
- More sophisticated price modeling (e.g., mean reversion, seasonality)
- Integration with real market data APIs
- Sensitivity analysis tools
- Batch processing capabilities

## License

[Add your chosen license here]

## Citation

If you use this tool in research, please cite:
```
[Add appropriate citation format]
```

## Contact

[Add contact information for questions and support]

## Acknowledgments

- Amazon rainforest carbon stock data based on scientific literature
- Economic modeling approaches adapted from environmental economics research
- Built with Streamlit for interactive web applications
