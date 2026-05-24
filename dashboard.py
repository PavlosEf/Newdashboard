from nicegui import ui

# Import your calculators from the local calculators package
import calculators.AlternativeLinesConverter as AlternativeLinesConverter
import calculators.CurrencyConverter as CurrencyConverter
import calculators.MarginsRemoval as MarginsRemoval
import calculators.OffPricesCalculator as OffPricesCalculator
import calculators.PercentageCalculations as PercentageCalculations
import calculators.SurebetCalculator as SurebetCalculator
import calculators.TopPriceBetfairCalculator as TopPriceBetfairCalculator

def create_dashboard():
    # 1. Top Application Bar
    with ui.header().classes('bg-slate-900 text-white items-center justify-between px-6 py-4 shadow-md'):
        ui.label('⚡ Pro Betting Tools Dashboard').classes('text-2xl font-bold tracking-wide')
    
    # 2. Main Structural Grid Layout
    with ui.row().classes('w-full h-screen no-wrap'):
        
        # Left Side Navigation Menu Panel
        with ui.column().classes('w-72 bg-slate-50 h-full p-4 border-r border-gray-200 shadow-sm shrink-0'):
            ui.label('TOOLS MENU').classes('text-xs font-bold text-gray-500 tracking-widest mb-4')
            
            with ui.tabs().classes('w-full items-start').props('vertical') as tabs:
                tab_off_prices = ui.tab('Off Prices Calculator')
                tab_surebet = ui.tab('Surebet Calculator')
                tab_margins = ui.tab('Margins Removal')
                tab_alt_lines = ui.tab('Alternative Lines Converter')
                tab_percentage = ui.tab('Percentage (%) Calculations')
                tab_currency = ui.tab('Currency Converter')
                tab_topprice = ui.tab('Lay Bet Calculator')
                
        # Right Side Content Container Area
        with ui.column().classes('flex-grow p-8 bg-white h-full overflow-y-auto'):
            with ui.tab_panels(tabs, value=tab_off_prices).classes('w-full h-full'):
                
                with ui.tab_panel(tab_off_prices):
                    OffPricesCalculator.run()
                    
                with ui.tab_panel(tab_surebet):
                    SurebetCalculator.run()
                    
                with ui.tab_panel(tab_margins):
                    MarginsRemoval.run()

                with ui.tab_panel(tab_alt_lines):
                    AlternativeLinesConverter.run()

                with ui.tab_panel(tab_percentage):
                    PercentageCalculations.run()
                    
                with ui.tab_panel(tab_currency):
                    CurrencyConverter.run()

                with ui.tab_panel(tab_topprice):
                    TopPriceBetfairCalculator.run()

# Build and execute app structure
create_dashboard()

# Target configuration bound to Render's container allocation parameters
ui.run(title="Betting Tools Dashboard", port=8080, host="0.0.0.0")
