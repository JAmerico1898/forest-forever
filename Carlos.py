import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class CarbonCreditSimulation:
    def __init__(self, num_simulations=100000, discount_rate=0.08, time_horizon=30):
        self.num_simulations = num_simulations
        
        # Constants
        self.CARBON_STOCK = 569  # tons/hectare
        self.ANNUAL_ABSORPTION = 9.5  # tons/hectare/year
        self.DISCOUNT_RATE = discount_rate
        self.TIME_HORIZON = time_horizon
        
    def generate_price_scenarios(self, mean_price, std_dev):
        """Generate price scenarios using normal distribution"""
        return np.random.normal(mean_price, std_dev, self.num_simulations)
    
    def calculate_npv(self, cash_flows, discount_rate=None):
        """Calculate Net Present Value of cash flows"""
        if discount_rate is None:
            discount_rate = self.DISCOUNT_RATE
        
        years = np.arange(len(cash_flows))
        discount_factors = 1 / (1 + discount_rate) ** years
        return np.sum(cash_flows * discount_factors)
    
    def simulate_conventional_use(self, timber_value, cattle_mean, cattle_std, 
                                soy_mean, soy_std):
        """Simulate NPV of conventional land use (timber + agriculture)"""
        # Generate annual revenues for cattle and soy
        cattle_revenues = self.generate_price_scenarios(cattle_mean, cattle_std)
        soy_revenues = self.generate_price_scenarios(soy_mean, soy_std)
        
        # Calculate NPV for each simulation
        conventional_npvs = []
        for i in range(self.num_simulations):
            # Initialize cash flows
            cash_flows = np.zeros(self.TIME_HORIZON)
            
            # Add timber revenue if applicable
            if timber_value > 0:
                cash_flows[0] = timber_value
            
            # Alternate between cattle and soy (simplified rotation)
            for year in range(self.TIME_HORIZON):
                if year % 2 == 0:
                    cash_flows[year] += cattle_revenues[i]
                else:
                    cash_flows[year] += soy_revenues[i]
            
            npv = self.calculate_npv(cash_flows)
            conventional_npvs.append(npv)
            
        return np.array(conventional_npvs)
    
    def find_equilibrium_carbon_prices(self, conventional_npvs):
        """Find carbon credit prices that make conservation competitive"""
        # Calculate required annual carbon credit revenue
        stock_credit_prices = np.linspace(0, 1000, 100)  # Test range for stock credits
        flow_credit_prices = np.linspace(0, 1000, 100)   # Test range for flow credits
        
        equilibrium_prices = []
        
        for stock_price in stock_credit_prices:
            for flow_price in flow_credit_prices:
                # Calculate conservation NPV
                conservation_cash_flows = np.zeros(self.TIME_HORIZON)
                
                # One-time payment for existing carbon stock
                conservation_cash_flows[0] = self.CARBON_STOCK * stock_price
                
                # Annual payments for carbon absorption
                annual_credit_revenue = self.ANNUAL_ABSORPTION * flow_price
                conservation_cash_flows[1:] = annual_credit_revenue
                
                conservation_npv = self.calculate_npv(conservation_cash_flows)
                
                # Check if this price combination makes conservation competitive
                if conservation_npv >= np.percentile(conventional_npvs, 75):
                    equilibrium_prices.append({
                        'stock_price': stock_price,
                        'flow_price': flow_price,
                        'conservation_npv': conservation_npv
                    })
        
        return pd.DataFrame(equilibrium_prices)
    
    def run_simulation(self, timber_value, cattle_mean, cattle_std, 
                      soy_mean, soy_std):
        """Run full simulation and return results"""
        # Simulate conventional use NPVs
        conventional_npvs = self.simulate_conventional_use(
            timber_value, cattle_mean, cattle_std, soy_mean, soy_std
        )
        
        # Find equilibrium carbon credit prices
        equilibrium_prices = self.find_equilibrium_carbon_prices(conventional_npvs)
        
        # Calculate summary statistics
        results = {
            'conventional_npv_mean': np.mean(conventional_npvs),
            'conventional_npv_p75': np.percentile(conventional_npvs, 75),
            'min_stock_price': equilibrium_prices['stock_price'].min(),
            'min_flow_price': equilibrium_prices['flow_price'].min(),
            'recommended_stock_price': equilibrium_prices['stock_price'].median(),
            'recommended_flow_price': equilibrium_prices['flow_price'].median()
        }
        
        return results, equilibrium_prices, conventional_npvs

def main():
    st.set_page_config(page_title="Carbon Credit Price Simulator", layout="wide")
    
    st.title("Carbon Credit Price Simulator for Forest Conservation")
    
    st.markdown("""
    This simulator helps determine the equilibrium carbon credit prices needed to make forest 
    conservation competitive with conventional land use (timber extraction, cattle ranching, 
    and soybean farming) in the Amazon rainforest.
    """)
    
    # Currency selection
    use_usd = st.toggle(
        "Show values in US Dollars",
        value=False,
        help="Toggle between Brazilian Reais (R$) and US Dollars (US$)"
    )
    
    exchange_rate = 6.00  # Default exchange rate
    if use_usd:
        exchange_rate = st.slider(
            "Exchange Rate (R$/US$)",
            min_value=1.00,
            max_value=10.00,
            value=5.50,
            step=0.05,
            help="Exchange rate for converting Brazilian Reais to US Dollars"
        )
    
    # Function to format currency values
    def format_currency(value):
        if use_usd:
            return f"US$ {value/exchange_rate:,.2f}"
        return f"R$ {value:,.2f}"
    
    st.divider()
    
    # Create three columns for financial inputs
    st.subheader("Financial Parameters")
    fin_col1, fin_col2 = st.columns(2)
    
    with fin_col1:
        discount_rate = st.slider(
            "Discount Rate (%)",
            min_value=1.0,
            max_value=20.0,
            value=8.0,
            step=0.5,
            help="Annual discount rate used for NPV calculations"
        ) / 100  # Convert percentage to decimal
        
    with fin_col2:
        time_horizon = st.slider(
            "Time Horizon (Years)",
            min_value=10,
            max_value=50,
            value=30,
            step=5,
            help="Number of years to consider in the analysis"
        )
    
    st.divider()
    
    # Create two columns for conventional use inputs
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Conventional Use Parameters")
        
        include_timber = st.toggle(
            "Include Timber Extraction",
            value=True,
            help="Toggle whether to include one-time timber revenue in the analysis"
        )
        
        timber_value = 0
        if include_timber:
            timber_value = st.slider(
                f"Timber Value ({format_currency(1000)[0:3]}/hectare)",
                min_value=1000 if not use_usd else 1000/exchange_rate,
                max_value=10000 if not use_usd else 10000/exchange_rate,
                value=5000 if not use_usd else 5000/exchange_rate,
                step=100 if not use_usd else 100/exchange_rate,
                help="One-time revenue from timber extraction"
            )
            if use_usd:
                timber_value *= exchange_rate  # Convert back to BRL for calculations
        
        cattle_mean = st.slider(
            f"Average Cattle Revenue ({format_currency(1000)[0:3]}/hectare/year)",
            min_value=200 if not use_usd else 200/exchange_rate,
            max_value=2000 if not use_usd else 2000/exchange_rate,
            value=800 if not use_usd else 800/exchange_rate,
            step=50 if not use_usd else 50/exchange_rate,
            help="Mean annual revenue from cattle ranching"
        )
        if use_usd:
            cattle_mean *= exchange_rate
        
        cattle_std = st.slider(
            f"Cattle Revenue Std Dev ({format_currency(1000)[0:3]}/hectare/year)",
            min_value=50 if not use_usd else 50/exchange_rate,
            max_value=500 if not use_usd else 500/exchange_rate,
            value=200 if not use_usd else 200/exchange_rate,
            step=25 if not use_usd else 25/exchange_rate,
            help="Standard deviation of annual cattle revenues"
        )
        if use_usd:
            cattle_std *= exchange_rate
    
    with col2:
        soy_mean = st.slider(
            f"Average Soybean Revenue ({format_currency(1000)[0:3]}/hectare/year)",
            min_value=3000 if not use_usd else 500/exchange_rate,
            max_value=10000 if not use_usd else 3000/exchange_rate,
            value=6100 if not use_usd else 1200/exchange_rate,
            step=50 if not use_usd else 50/exchange_rate,
            help="Mean annual revenue from soybean farming"
        )
        if use_usd:
            soy_mean *= exchange_rate
        
        soy_std = st.slider(
            f"Soybean Revenue Std Dev ({format_currency(1000)[0:3]}/hectare/year)",
            min_value=100 if not use_usd else 100/exchange_rate,
            max_value=1000 if not use_usd else 1000/exchange_rate,
            value=300 if not use_usd else 300/exchange_rate,
            step=25 if not use_usd else 25/exchange_rate,
            help="Standard deviation of annual soybean revenues"
        )
        if use_usd:
            soy_std *= exchange_rate
        
        num_simulations = st.slider(
            "Number of Simulations",
            min_value=1000,
            max_value=200000,
            value=100000,
            step=1000,
            help="More simulations increase accuracy but take longer"
        )
    
    # Initialize and run simulation
    sim = CarbonCreditSimulation(
        num_simulations=num_simulations,
        discount_rate=discount_rate,
        time_horizon=time_horizon
    )
    
    results, equilibrium_prices, conventional_npvs = sim.run_simulation(
        timber_value, cattle_mean, cattle_std, soy_mean, soy_std
    )
    
    # Display results in cards
    st.subheader("Simulation Results")
    
    # Calculate annual equivalents using the discount rate
    annual_factor = sim.DISCOUNT_RATE * (1 + sim.DISCOUNT_RATE) ** sim.TIME_HORIZON / ((1 + sim.DISCOUNT_RATE) ** sim.TIME_HORIZON - 1)
    
    annual_stock_price = results['recommended_stock_price'] * annual_factor
    annual_flow_price = results['recommended_flow_price']  # Flow price is already annual
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Conventional Use NPV (Mean)",
            value=format_currency(results['conventional_npv_mean']) + "/ha"
        )
    
    with col2:
        st.metric(
            label="Stock Credit Price (Total)",
            value=format_currency(results['recommended_stock_price']) + "/tCO2-ha",
            delta=format_currency(annual_stock_price) + "/tCO2-ha-year",
            delta_color="off",
            help="Total price and annualized equivalent over 30 years"
        )
    
    with col3:
        st.metric(
            label="Flow Credit Price (Annual)",
            value=format_currency(annual_flow_price) + "/tCO2-ha-year",
            help="Price for annually sequestered carbon"
        )
    
    # Additional explanation
    currency_symbol = "US$" if use_usd else "R$"
    st.info(f"""
        💡 The Stock Credit Price shows both the total upfront payment needed per tCO2 and its annual equivalent 
        (calculated using a {discount_rate*100:.1f}% discount rate over {time_horizon} years). The Flow Credit Price is already an annual value 
        for each ton of CO2 sequestered per year. All values in {currency_symbol}.
    """)
    
    # Create visualizations
    st.subheader("Detailed Analysis")
    
    # Distribution of Conventional NPVs
    fig1 = go.Figure()
    fig1.add_trace(go.Histogram(
        x=conventional_npvs if not use_usd else conventional_npvs/exchange_rate,
        nbinsx=50,
        name="NPV Distribution"
    ))
    fig1.add_vline(
        x=results['conventional_npv_p75'] if not use_usd else results['conventional_npv_p75']/exchange_rate,
        line_dash="dash",
        annotation_text="75th Percentile"
    )
    fig1.update_layout(
        title="Distribution of Conventional Land Use NPVs",
        xaxis_title=f"Net Present Value ({currency_symbol}/ha)",
        yaxis_title="Frequency"
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Equilibrium Price Combinations
    fig2 = go.Figure()
    
    # Add the main scatter plot
    fig2.add_trace(go.Scatter(
        x=equilibrium_prices['stock_price'] if not use_usd else equilibrium_prices['stock_price']/exchange_rate,
        y=equilibrium_prices['flow_price'] if not use_usd else equilibrium_prices['flow_price']/exchange_rate,
        mode='markers',
        marker=dict(
            size=8,
            color=equilibrium_prices['conservation_npv'] if not use_usd else equilibrium_prices['conservation_npv']/exchange_rate,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title=f"Conservation NPV ({currency_symbol}/ha)")
        ),
        name='Viable Combinations'
    ))
    
    # Add recommended point
    fig2.add_trace(go.Scatter(
        x=[results['recommended_stock_price'] if not use_usd else results['recommended_stock_price']/exchange_rate],
        y=[results['recommended_flow_price'] if not use_usd else results['recommended_flow_price']/exchange_rate],
        mode='markers',
        marker=dict(
            size=15,
            color='red',
            symbol='star'
        ),
        name='Recommended Combination'
    ))
    
    # Update layout
    fig2.update_layout(
        title="Viable Carbon Credit Price Combinations",
        xaxis_title=f"Stock Credit Price ({currency_symbol}/tCO2)",
        yaxis_title=f"Flow Credit Price ({currency_symbol}/tCO2)",
        hovermode='closest',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="Black",
            borderwidth=1
        ),
        margin=dict(l=60, r=40, t=60, b=60),
        coloraxis_colorbar=dict(
            title=f"Conservation NPV ({currency_symbol}/ha)",
            x=1.15
        )
    )
    
    # Add annotation explaining the trade-off
    fig2.add_annotation(
        text="Each point represents a combination of prices<br>that makes conservation competitive",
        xref="paper", yref="paper",
        x=0.02, y=0.98,
        showarrow=False,
        bgcolor="white",
        bordercolor="black",
        borderwidth=1
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Additional Analysis
    st.subheader("Financial Summary")
    
    # Calculate annual equivalent values
    conservation_annual = results['recommended_stock_price'] * sim.CARBON_STOCK / time_horizon + \
                        results['recommended_flow_price'] * sim.ANNUAL_ABSORPTION
    
    conventional_annual = results['conventional_npv_mean'] * discount_rate * \
                        (1 + discount_rate) ** time_horizon / ((1 + discount_rate) ** time_horizon - 1)
    
    summary_data = pd.DataFrame({
        'Metric': [
            'Total Carbon Stock Value per Hectare',
            'Annual Carbon Absorption Value per Hectare',
            'Equivalent Annual Conservation Revenue',
            f"Average Annual Conventional Revenue {'(inc. Timber)' if include_timber else '(excl. Timber)'}"
        ],
        'Value': [
            format_currency(results['recommended_stock_price'] * sim.CARBON_STOCK),
            format_currency(results['recommended_flow_price'] * sim.ANNUAL_ABSORPTION),
            format_currency(conservation_annual),
            format_currency(conventional_annual)
        ]
    })
    
    st.table(summary_data)
    
    # Download results
    csv = pd.DataFrame(results, index=[0]).to_csv(index=False)
    st.download_button(
        label="Download Results CSV",
        data=csv,
        file_name="carbon_credit_simulation_results.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()