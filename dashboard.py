from nicegui import ui
import os

# Import your other calculators from the local calculators package
import calculators.AlternativeLinesConverter as AlternativeLinesConverter
import calculators.CurrencyConverter as CurrencyConverter
import calculators.MarginsRemoval as MarginsRemoval
import calculators.OffPricesCalculator as OffPricesCalculator
import calculators.PercentageCalculations as PercentageCalculations
import calculators.SurebetCalculator as SurebetCalculator
import calculators.TopPriceBetfairCalculator as TopPriceBetfairCalculator

# =====================================================================
# INLINE SEQUENTIAL ACCA CALCULATOR ENGINE (Secured Layout Pipeline)
# =====================================================================
def run_sequential_acca():
    ui.label('Sequential Acca Calculator').classes('text-3xl font-bold text-slate-800 mb-2')
    ui.label('Generate a complete overall hedging plan for multi-match accumulators with sequential game times.').classes('text-gray-500 mb-6')

    # Component State Configuration - Pre-allocated fixed list to guarantee rendering stability
    state = {
        'num_legs': 3,
        'back_stake': 100.0,
        'acca_boost': 0.0,
        'back_comm': 0.0,
        'lay_comm': 2.0,
        'legs': [
            {'back_odds': 1.30, 'lay_odds': 1.25},
            {'back_odds': 1.65, 'lay_odds': 1.60},
            {'back_odds': 1.80, 'lay_odds': 1.72},
            {'back_odds': 1.95, 'lay_odds': 1.87},
            {'back_odds': 2.00, 'lay_odds': 1.92},
            {'back_odds': 2.00, 'lay_odds': 2.00},
            {'back_odds': 2.00, 'lay_odds': 2.00},
            {'back_odds': 2.00, 'lay_odds': 2.00}
        ],
        'results': None
    }

    def calculate_sequential_acca():
        n = int(state['num_legs'])
        b_stake = float(state['back_stake'])
        boost = float(state['acca_boost']) / 100.0
        b_comm = float(state['back_comm']) / 100.0
        l_comm = float(state['lay_comm']) / 100.0
        
        current_legs = state['legs'][:n]
        
        for idx, leg in enumerate(current_legs):
            if float(leg['back_odds']) <= 1.0 or float(leg['lay_odds']) <= 1.0:
                ui.notify(f"Invalid odds in Match {idx+1}. Values must be greater than 1.00.", type='warning')
                return
        
        total_back_odds = 1.0
        for leg in current_legs:
            total_back_odds *= float(leg['back_odds'])
            
        bookie_gross_return = b_stake * total_back_odds
        bookie_net_win_before_boost = (bookie_gross_return - b_stake) * (1.0 - b_comm)
        bookie_net_win = bookie_net_win_before_boost * (1.0 + boost)
        
        C = 0.0
        D = 0.0
        A_list = []
        B_list = []
        
        for leg in current_legs:
            lay_odd = float(leg['lay_odds'])
            a_k = (1.0 + C) / (1.0 - l_comm)
            b_k = (b_stake + D) / (1.0 - l_comm)
            
            A_list.append(a_k)
            B_list.append(b_k)
            
            C = C + a_k * (lay_odd - 1.0)
            D = D + b_k * (lay_odd - 1.0)
            
        P = (bookie_net_win - D) / (1.0 + C)
        
        legs_results = []
        for i, (a, b, leg) in enumerate(zip(A_list, B_list, current_legs)):
            stk = a * P + b
            liab = stk * (float(leg['lay_odds']) - 1.0)
            
            if i == 0:
                status_txt = "👉 LAY NOW (First Match)"
                status_cls = "bg-green-50 text-green-700 border border-green-200"
            else:
                status_txt = f"⏳ Lay ONLY if Match {i} Wins"
                status_cls = "bg-amber-50 text-amber-700 border border-amber-200"

            legs_results.append({
                'leg_idx': i + 1,
                'lay_stake': round(stk, 2),
                'liability': round(liab, 2),
                'status_text': status_txt,
                'status_class': status_cls
            })
            
        state['results'] = {
            'total_back_odds': round(total_back_odds, 2),
            'bookie_net_win': round(bookie_net_win, 2),
            'guaranteed_profit': round(P, 2),
            'legs': legs_results
        }
        results_panel.refresh()

    def handle_leg_count_change(e):
        val = int(e.value or 3)
        if val < 2: val = 2
        if val > 8: val = 8
        state['num_legs'] = val
        state['results'] = None
        legs_inputs_renderer.refresh()
        results_panel.refresh()

    @ui.refreshable
    def legs_inputs_renderer():
        with ui.column().classes('w-full gap-3 bg-slate-50 p-4 rounded-xl border border-gray-200 shadow-sm mb-4'):
            ui.label('Accumulator Legs Parameters').classes('text-xs font-bold text-slate-400 uppercase tracking-wider')
            
            for i in range(8):
                is_visible = i < state['num_legs']
                row = ui.row().classes('w-full gap-4 items-center wrap')
                row.set_visibility(is_visible)
                
                with row:
                    ui.label(f"Match {i+1}:").classes('font-bold text-slate-700 w-20')
                    ui.number(label='Back Odds', value=state['legs'][i]['back_odds'], format="%.2f", step=0.01,
                              on_change=lambda e, idx=i: state['legs'][idx].update({'back_odds': e.value or 1.01})).classes('flex-grow')
                    ui.number(label='Lay Odds', value=state['legs'][i]['lay_odds'], format="%.2f", step=0.01,
                              on_change=lambda e, idx=i: state['legs'][idx].update({'lay_odds': e.value or 1.01})).classes('flex-grow')

    @ui.refreshable
    def results_panel():
        res = state['results']
        if not res:
            return
            
        profit_color = 'text-green-600' if res['guaranteed_profit'] >= 0 else 'text-red-600'
        
        with ui.column().classes('w-full p-6 bg-slate-50 border border-gray-200 rounded-xl shadow-sm mt-4'):
            ui.label('Guaranteed Overall Plan Metrics').classes('text-xl font-bold text-slate-800 mb-4 underline')
            
            with ui.row().classes('w-full justify-between wrap gap-4 mb-4'):
                ui.label(f"Total Accumulator Odds: {res['total_back_odds']:.2f}").classes('text-sm font-medium text-slate-700')
                ui.label(f"Bookmaker Net Profit (If All Win): {res['bookie_net_win']:.2f}€").classes('text-sm font-medium text-slate-700')
                ui.label(f"Guaranteed Equal Profit: {res['guaranteed_profit']:.2f}€").classes(f'text-lg font-black {profit_color}')
                
            ui.separator().classes('my-4')
            ui.label('Sequential Lay Schedule Action Plan').classes('text-xs font-bold text-gray-400 uppercase tracking-wider mb-3')
            
            for leg in res['legs']:
                status_classes = str(leg['status_class'])
                with ui.row().classes('w-full p-4 bg-white rounded-xl border border-gray-200 items-center justify-between shadow-sm mb-3 wrap gap-2'):
                    with ui.column().classes('gap-0.5'):
                        ui.label(f"Match {leg['leg_idx']}").classes('font-black text-slate-800 text-base')
                        ui.label(leg['status_text']).classes(f"text-[11px] px-2.5 py-0.5 rounded-full font-bold uppercase tracking-wide {status_classes}")
                    
                    with ui.row().classes('gap-6'):
                        with ui.column().classes('items-end'):
                            ui.label('LAY STAKE').classes('text-[10px] text-gray-400 font-bold tracking-widest')
                            ui.label(f"{leg['lay_stake']:.2f}€").classes('text-lg font-bold text-slate-700')
                        with ui.column().classes('items-end'):
                            ui.label('LIABILITY').classes('text-[10px] text-gray-400 font-bold tracking-widest')
                            ui.label(f"{leg['liability']:.2f}€").classes('text-lg font-bold text-red-600')

    with ui.column().classes('w-full max-w-4xl gap-4'):
        with ui.row().classes('w-full items-center gap-4 mb-2'):
            ui.label('Enter Number of Matches (Legs):').classes('font-medium text-slate-700')
            ui.number(value=state['num_legs'], format="%d", step=1, on_change=handle_leg_count_change).classes('w-24')

        legs_inputs_renderer()

        ui.label('Global Parameters Allocation').classes('text-xs font-bold text-slate-400 tracking-wider uppercase mt-2')
        with ui.row().classes('w-full gap-4 wrap items-center mb-4'):
            ui.number('Back Stake (€)', value=state['back_stake'], format="%.2f", step=10.0, on_change=lambda e: state.update({'back_stake': e.value or 0.0})).classes('flex-grow')
            ui.number('Acca Boost (%)', value=state['acca_boost'], format="%.1f", step=1.0, on_change=lambda e: state.update({'acca_boost': e.value or 0.0})).classes('flex-grow')
            ui.number('Bookie Tax/Comm (%)', value=state['back_comm'], format="%.1f", step=0.5, on_change=lambda e: state.update({'back_comm': e.value or 0.0})).classes('flex-grow')
            ui.number('Betfair Comm (%)', value=state['lay_comm'], format="%.1f", step=0.5, on_change=lambda e: state.update({'lay_comm': e.value or 0.0})).classes('flex-grow')

        ui.button('Calculate Sequential Lay Matrix Plan', on_click=calculate_sequential_acca) \
            .classes('w-full bg-blue-600 text-white font-bold py-3 rounded-xl shadow-md hover:bg-blue-700 transition-all')

        results_panel()

# =====================================================================
# DASHBOARD LAYOUT BUILDER & GUIDE CONFIGURATION
# =====================================================================
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

def render_remote_app(title: str, description: str, url: str):
    ui.label(title).classes('text-3xl font-bold text-slate-800 mb-2')
    ui.label(description).classes('text-gray-500 mb-6')
    ui.link('Open ' + title + ' →', url, new_tab=True) \
        .classes('inline-block bg-blue-600 text-white font-bold py-3 px-6 rounded-xl shadow-md hover:bg-blue-700 transition-all no-underline')
    ui.label("Only reachable while the home PC is on. You'll be asked for its password.") \
        .classes('text-xs text-gray-400 mt-3')


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

                ui.label('REMOTE ACCESS').classes('text-xs font-bold text-gray-400 tracking-widest mt-4 mb-1')
                tab_sportsdb = ui.tab('Sports DB')
                tab_polymarket = ui.tab('Polymarket')

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
                    run_sequential_acca() # Executed from inline layout function directly

                with ui.tab_panel(tab_alt_lines):
                    AlternativeLinesConverter.run()

                with ui.tab_panel(tab_percentage):
                    PercentageCalculations.run()
                    
                with ui.tab_panel(tab_currency):
                    CurrencyConverter.run()

                with ui.tab_panel(tab_sportsdb):
                    render_remote_app(
                        'Sports DB',
                        'Sports data warehouse and pricing models, running on the home PC.',
                        'https://pkot.tailf37e23.ts.net',
                    )

                with ui.tab_panel(tab_polymarket):
                    render_remote_app(
                        'Polymarket',
                        'Prediction market tracker, running on the home PC.',
                        'https://pkot.tailf37e23.ts.net:8443',
                    )

# Build and execute app structure
create_dashboard()

# Target configuration bound to Render's container allocation parameters
port_assignment = int(os.environ.get("PORT", 8080))
ui.run(title="Betting Tools Dashboard", host="0.0.0.0", port=port_assignment, reload=False)
