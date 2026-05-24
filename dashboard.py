from nicegui import ui
import os

# Import your calculators from the local calculators package
import calculators.AlternativeLinesConverter as AlternativeLinesConverter
import calculators.CurrencyConverter as CurrencyConverter
import calculators.MarginsRemoval as MarginsRemoval
import calculators.OffPricesCalculator as OffPricesCalculator
import calculators.PercentageCalculations as PercentageCalculations
import calculators.SurebetCalculator as SurebetCalculator
import calculators.TopPriceBetfairCalculator as TopPriceBetfairCalculator
import calculators.SequentialAccaCalculator as SequentialAccaCalculator

def render_guide():
    """Renders the simple, step-by-step English manual approved by the user."""
    ui.label('📋 Dashboard User Manual').classes('text-3xl font-bold text-slate-800 mb-2')
    ui.label('Welcome! Follow this simple step-by-step guide to understand how every tool works.') \
        .classes('text-gray-500 mb-6')
    
    with ui.column().classes('w-full max-w-4xl gap-6'):
        
        # 1. Off Prices Calculator
        with ui.card().classes('w-full p-5 bg-slate-50 border-l-4 border-blue-500 shadow-sm'):
            ui.label('1. Off Prices Calculator').classes('text-lg font-bold text-slate-800 mb-2')
            ui.markdown('''
            * **What it is:** A tool to check if your bookmaker's odds are safe or if they are heavily mispriced compared to the competition.
            * **What to do:**
              1. Go to any row you want to use.
              2. Type your bookmaker's odds in the **Our Odds** box.
              3. Type the rival bookmaker's odds in the **Competition Odds** box.
            * **What you see:**
              * **Difference:** The exact percentage mathematical gap between the two odds.
              * **Status Badge:**
                * `OK` (Green): The price gap is safe and normal.
                * `OFF 2` (Purple) or `OFF 1` (Red): Your odds are way out of line and need attention.
            ''')

        # 2. Surebet Calculator
        with ui.card().classes('w-full p-5 bg-slate-50 border-l-4 border-blue-500 shadow-sm'):
            ui.label('2. Surebet Calculator').classes('text-lg font-bold text-slate-800 mb-2')
            ui.markdown('''
            * **What it is:** A tool that calculates exactly how much money to bet on different outcomes of the same match to secure a guaranteed profit, no matter who wins.
            * **What to do:**
              1. Enter the total number of market outcomes in the **Number of Market Outcomes** box (e.g., type 2 for two way markets, 3 for threeway markets etc).
              2. Type the odds for each outcome in the boxes that appear below.
              3. Enter your stakes using one of these two options:
                 * **Basic Bookmaker Stake:** Use this if you have a specific, fixed amount of money you *must* bet on Outcome 1.
                 * **Equally splitted stake:** Use this if you have a total overall budget you want to split across all outcomes.
              4. Click the **Run Market Surebet Calculation** button.
            * **What you see:**
              * **Target Outcome Stakes:** The exact amount of money you need to bet on each separate choice.
              * **Net Profit Breakdown:** Your expected profit for each outcome (shown in Green if positive, Red if negative).
              * **Arbitrage Percentage:** If this number is green (above 0%), it means you have locked in a guaranteed winning bet.
            ''')

        # 3. Margins Removal
        with ui.card().classes('w-full p-5 bg-slate-50 border-l-4 border-blue-500 shadow-sm'):
            ui.label('3. Margins Removal').classes('text-lg font-bold text-slate-800 mb-2')
            ui.markdown('''
            * **What it is:** A tool that strips away the bookmaker's hidden fee ("house edge" or commission) to reveal the real, true mathematical probability of an event.
            * **What to do:**
              1. Select whether your market is a **2-Way** market (like Tennis or Over/Under) or a **3-Way** market (like Football 1X2).
              2. Type the odds offered by the bookmaker into the empty boxes.
            * **What you see:**
              * **True Probability (%):** The actual mathematical percentage chance of each outcome happening.
              * **Fair Odds:** What the odds *should* be if the bookmaker wasn't taking a commission cut. This helps you spot if a price offers real value.
            ''')

        # 4. Lay Bet Calculator
        with ui.card().classes('w-full p-5 bg-slate-50 border-l-4 border-blue-500 shadow-sm'):
            ui.label('4. Lay Bet Calculator').classes('text-lg font-bold text-slate-800 mb-2')
            ui.markdown('''
            * **What it is:** A tool used when you want to back an outcome at a bookmaker and lay it (bet against it) on an exchange like Betfair to hedge your risk or unlock bonuses.
            * **What to do:**
              1. Type the bookmaker's odds in the **Back Odds** box.
              2. Type the exchange's odds in the **Lay Odds** box.
              3. Enter the money you want to risk at the bookmaker in the **Back Stake (€)** box.
              4. Click the **Calculate Lay Matrix Outputs** button.
            * **What you see:**
              * **Equal Profit Strategy:** Shows you the exact **Bookmaker Stake** and **Betfair Stake (Lay)** needed if you want to make the exact same profit regardless of who wins the match.
              * **One-Way Strategy:** Shows you the stakes needed if you want to completely clear your risk on one side of the bet.
              * **Net Market Profit:** Shows your final net returns for both scenarios so you can easily compare your options.
            ''')

        # 5. Sequential Acca Calculator
        with ui.card().classes('w-full p-5 bg-slate-50 border-l-4 border-blue-500 shadow-sm'):
            ui.label('5. Sequential Acca Calculator').classes('text-lg font-bold text-slate-800 mb-2')
            ui.markdown('''
            * **What it is:** A specialized tool for hedging accumulator bets (paroli) when the matches are played at different times (sequentially). It locks in a guaranteed equal profit regardless of when or where the accumulator wins or breaks.
            * **What to do:**
              1. Select the number of matches (legs) in your accumulator.
              2. Enter the **Back Odds** from the bookmaker and the current **Lay Odds** from Betfair for each match.
              3. Enter your **Back Stake**, any **Acca Boost (%)** bonus, and the exchange commission rate.
              4. Click **Calculate Sequential Lay Matrix**.
            * **What you see:**
              * A step-by-step guide for each match. It tells you exactly how much to lay on Betfair for Match 1. If Match 1 wins at the bookmaker, you proceed to Match 2 and lay the next specified amount. If any match loses at the bookmaker, the acca is broken, you stop, and you walk away with the exact same guaranteed net profit.
            ''')

        # 6. Alternative Lines Converter
        with ui.card().classes('w-full p-5 bg-slate-50 border-l-4 border-slate-500 shadow-sm'):
            ui.label('6. Alternative Lines Converter').classes('text-lg font-bold text-slate-800 mb-2')
            ui.markdown('''
            * **⚠️ Important Note:** This tool is experimental. Because different bookmakers apply different margins to different markets, the actual outcome in the real market may differ, but it will stay close to the results shown here.
            * **What it is:** A utility that allows you to translate a betting line from one bookmaker to match a different line from another bookmaker (for example, converting odds for Over 2.5 goals to see what the fair odds would be for Over 3.5 goals).
            * **What to do:**
              1. Select the market type from the choices provided (e.g., Over/Under lines).
              2. Enter your baseline reference odds into the input boxes.
              3. Enter the alternative line you want to compare against.
            * **What you see:**
              * **Converted Fair Odds:** The calculated fair price for the alternative line. This lets you immediately check if a competitor's alternative line is giving you good value or if it is priced too low.
            ''')

        # 7. Percentage Calculations
        with ui.card().classes('w-full p-5 bg-slate-50 border-l-4 border-slate-500 shadow-sm'):
            ui.label('7. Percentage (%) Calculations').classes('text-lg font-bold text-slate-800 mb-2')
            ui.markdown('''
            * **What it is:** A quick, everyday math toolbox designed to handle rapid percentage calculations for your stakes, bankroll, or profits.
            * **What to do:**
              1. Click on the drop-down menu to select the specific math question you want to solve (e.g., "What is X% of Y?", "X is what % of Y?", or "Percentage increase/decrease").
              2. Type your numbers into the input boxes that open up.
              3. Click the **Calculate** button.
            * **What you see:**
              * **Result:** A simple, direct text answer displaying the exact mathematical calculation instantly.
            ''')

        # 8. Currency Converter
        with ui.card().classes('w-full p-5 bg-slate-50 border-l-4 border-slate-500 shadow-sm'):
            ui.label('8. Currency Converter').classes('text-lg font-bold text-slate-800 mb-2')
            ui.markdown('''
            * **What it is:** A tool that converts money values between different global currencies using live, real-time exchange rates. This is ideal if you are tracking balances or placing bets across bookmakers that use different currencies (like Euros, Dollars, or Pounds).
            * **What to do:**
              1. Type the amount of money you want to convert into the input box.
              2. Select your starting currency flag from the first drop-down menu.
              3. Select your target currency flag from the second drop-down menu.
            * **What you see:**
              * **Converted Value:** The exact value of your money in the new currency based on today's live global market rates.
              * **Exchange Rate:** The exact conversion multiplier currently being used.
            ''')

def create_dashboard():
    # 1. Top Application Bar
    with ui.header().classes('bg-slate-900 text-white items-center justify-between px-6 py-4 shadow-md'):
        ui.label('⚡ Pro Betting Tools Dashboard').classes('text-2xl font-bold tracking-wide')
    
    # 2. Main Structural Grid Layout
    with ui.row().classes('w-full h-screen no-wrap'):
        
        # Left Side Navigation Menu Panel
        with ui.column().classes('w-72 bg-slate-50 h-full p-4 border-r border-gray-200 shadow-sm shrink-0'):
            ui.label('MAIN').classes('text-xs font-bold text-gray-400 tracking-widest mb-1')
            
            with ui.tabs().classes('w-full items-start').props('vertical') as tabs:
                tab_guide = ui.tab('📋 User Guide & Manual')
                
                ui.label('CALCULATORS').classes('text-xs font-bold text-gray-400 tracking-widest mt-4 mb-1')
                tab_off_prices = ui.tab('Off Prices Calculator')
                tab_surebet = ui.tab('Surebet Calculator')
                tab_margins = ui.tab('Margins Removal')
                tab_topprice = ui.tab('Lay Bet Calculator')
                tab_sequential = ui.tab('Sequential Acca Calculator')
                
                ui.label('UTILITIES').classes('text-xs font-bold text-gray-400 tracking-widest mt-4 mb-1')
                tab_alt_lines = ui.tab('Alternative Lines Converter')
                tab_percentage = ui.tab('Percentage (%) Calculations')
                tab_currency = ui.tab('Currency Converter')
                
        # Right Side Content Container Area
        with ui.column().classes('flex-grow p-8 bg-white h-full overflow-y-auto'):
            with ui.tab_panels(tabs, value=tab_guide).classes('w-full h-full'):
                
                with ui.tab_panel(tab_guide):
                    render_guide()
                
                with ui.tab_panel(tab_off_prices):
                    OffPricesCalculator.run()
                    
                with ui.tab_panel(tab_surebet):
                    SurebetCalculator.run()
                    
                with ui.tab_panel(tab_margins):
                    MarginsRemoval.run()

                with ui.tab_panel(tab_topprice):
                    TopPriceBetfairCalculator.run()

                with ui.tab_panel(tab_sequential):
                    SequentialAccaCalculator.run()

                with ui.tab_panel(tab_alt_lines):
                    AlternativeLinesConverter.run()

                with ui.tab_panel(tab_percentage):
                    PercentageCalculations.run()
                    
                with ui.tab_panel(tab_currency):
                    CurrencyConverter.run()

# Build and execute app structure
create_dashboard()

# Target configuration bound to Render's container allocation parameters
port_assignment = int(os.environ.get("PORT", 8080))
ui.run(title="Betting Tools Dashboard", host="0.0.0.0", port=port_assignment, reload=False)
