from nicegui import ui

def run():
    # Header Section
    ui.label('Single-Bet Multi-Outcome Surebet Calculator').classes('text-3xl font-bold text-slate-800 mb-2')
    ui.label('Dynamically add up to 6 outcomes to calculate individual single-market stakes and arbitrage profits.') \
        .classes('text-gray-500 mb-6')

    # State Schema
    state = {
        'num_outcomes': 2,
        'odds': [2.00, 2.50, 3.00, 4.00, 5.00, 6.00],
        'labels': ["Outcome 1 (Kaizen)", "Outcome 2 (Comp)", "Outcome 3", "Outcome 4", "Outcome 5", "Outcome 6"],
        'kaizen_stake': 0.0,
        'total_stake': 100.0,
        'stakes': [],
        'profits': [],
        'calculated_total_stake': 0.0,
        'arbitrage_pct': 0.0,
        'results_ready': False
    }

    # Core Mathematical Formulas (Your exact calculation logic)
    def calculate_surebet():
        n = state['num_outcomes']
        current_odds = state['odds'][:n]
        
        k_stake = state['kaizen_stake']
        t_stake = state['total_stake']
        
        probabilities = [1 / odd if odd > 0 else 0 for odd in current_odds]
        total_probability = sum(probabilities)

        if total_probability == 0:
            return

        # 1. Base stake distribution logic loops
        if k_stake > 0 and t_stake == 0:
            stakes = [k_stake * (prob / probabilities[0]) for prob in probabilities]
            t_stake = sum(stakes)
        elif t_stake > 0 and k_stake == 0:
            stakes = [t_stake * (prob / total_probability) for prob in probabilities]
        elif k_stake > 0 and t_stake > 0:
            stakes = [k_stake * (prob / probabilities[0]) for prob in probabilities]
            stakes[0] = k_stake  # Fixed target
            remaining_stake = t_stake - k_stake
            if remaining_stake > 0 and len(probabilities) > 1:
                sub_prob_sum = sum(probabilities[1:])
                for i in range(1, len(stakes)):
                    if sub_prob_sum > 0:
                        stakes[i] += remaining_stake * (probabilities[i] / sub_prob_sum)
        else:
            stakes = [0] * n

        # 2. Output parameter valuation mapping
        profits = [(current_odds[i] * stakes[i]) - t_stake for i in range(len(current_odds))]
        arbitrage_percentage = (1 - total_probability) * 100

        state['stakes'] = [round(stake, 2) for stake in stakes]
        state['profits'] = [round(profit, 2) for profit in profits]
        state['calculated_total_stake'] = round(t_stake, 2)
        state['arbitrage_pct'] = round(arbitrage_percentage, 2)
        state['results_ready'] = True
        
        results_renderer.refresh()

    # Dynamic Odds Inputs Block
    @ui.refreshable
    def odds_fields_renderer():
        with ui.column().classes('w-full gap-3 bg-slate-50 p-4 rounded-xl border border-gray-200 shadow-sm mb-6'):
            ui.label('Market Odds Elements').classes('text-xs font-bold text-slate-400 uppercase tracking-wider')
            
            # Form grid columns structure mapping
            with ui.row().classes('w-full gap-4 wrap items-center'):
                for i in range(state['num_outcomes']):
                    def build_change_handler(idx):
                        return lambda e: state['odds'].__setitem__(idx, e.value or 1.01)
                    
                    ui.number(label=state['labels'][i], value=state['odds'][i], format="%.2f", step=0.01,
                              on_change=build_change_handler(i)).classes('w-40 flex-grow')

    # Dynamic Results Summary Display Block
    @ui.refreshable
    def results_renderer():
        if not state['results_ready']:
            return

        arb_color = 'text-green-600' if state['arbitrage_pct'] > 0 else 'text-red-600'

        with ui.column().classes('w-full mt-6 p-6 bg-slate-50 border border-gray-200 rounded-xl shadow-sm'):
            ui.label("Calculation Matrix Matrix Summary").classes('text-xl font-bold text-slate-800 mb-4 underline')
            
            with ui.row().classes('w-full justify-between gap-6 wrap'):
                with ui.column().classes('flex-grow min-w-[200px] gap-1'):
                    ui.label("Target Outcome Stakes").classes('font-bold text-gray-400 text-xs tracking-wider uppercase mb-1')
                    for i in range(state['num_outcomes']):
                        ui.label(f"{state['labels'][i]}: {state['stakes'][i]}€").classes('text-base text-slate-700 font-medium')

                with ui.column().classes('flex-grow min-w-[200px] gap-1'):
                    ui.label("Net Profit Breakdown").classes('font-bold text-gray-400 text-xs tracking-wider uppercase mb-1')
                    for i in range(state['num_outcomes']):
                        p_val = state['profits'][i]
                        p_color = 'text-green-600' if p_val >= 0 else 'text-red-600'
                        ui.label(f"Profit {i+1}: {p_val}€").classes(f'text-base font-bold {p_color}')
            
            ui.separator().classes('my-4')
            
            with ui.row().classes('w-full justify-between items-center'):
                ui.label(f"Total Cumulative Stake: {state['calculated_total_stake']}€").classes('text-lg font-bold text-slate-800')
                ui.label(f"Arbitrage Percentage: {state['arbitrage_pct']}%").classes(f'text-xl font-black {arb_color}')

    # Dropdown change event intercept
    def adjust_outcome_count(e):
        state['num_outcomes'] = int(e.value)
        state['results_ready'] = False
        odds_fields_renderer.refresh()
        results_renderer.refresh()

    # Layout Controls Configuration Panel
    with ui.column().classes('w-full max-w-4xl gap-4'):
        with ui.row().classes('w-full items-center gap-4 mb-2'):
            ui.label('Select Number of Market Outcomes:').classes('font-medium text-slate-700')
            ui.select([2, 3, 4, 5, 6], value=state['num_outcomes'], on_change=adjust_outcome_count).classes('w-24')

        # Generate inputs
        odds_fields_renderer()

        ui.label('Enter Specific Stake Allocations').classes('text-xs font-bold text-slate-400 tracking-wider uppercase mt-2')
        with ui.row().classes('w-full gap-4 mb-6'):
            ui.number('Kaizen Fixed Stake (€)', value=state['kaizen_stake'], format="%.2f", step=1.0,
                      on_change=lambda e: state.update({'kaizen_stake': e.value or 0.0})).classes('flex-grow')
            ui.number('Global Total Stake (€)', value=state['total_stake'], format="%.2f", step=1.0,
                      on_change=lambda e: state.update({'total_stake': e.value or 0.0})).classes('flex-grow')

        # Action Execution Link Block
        ui.button('Run Market Surebet Calculation', on_click=calculate_surebet) \
            .classes('w-full bg-blue-600 text-white font-bold py-3 rounded-xl shadow-md hover:bg-blue-700 transition-all')

        # Mounting component reference node link hook
        results_renderer()
