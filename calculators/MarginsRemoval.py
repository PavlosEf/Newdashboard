from nicegui import ui

def run():
    # Page Header Panel
    ui.label('Odds Margin Calculator').classes('text-3xl font-bold text-slate-800 mb-2')
    ui.label('Calculate the margin, implied probabilities, and fair true odds for 2-way or 3-way betting markets.') \
        .classes('text-gray-500 mb-6')

    # Component State Matrix
    state = {
        'market_type': '2-Way Market',
        'odds': [2.00, 2.00, 4.00],  # Holds up to 3 selections
        'results': None
    }

    # Core Mathematical Calculation (Your exact math logic)
    def calculate_margins():
        num_selections = 2 if state['market_type'] == "2-Way Market" else 3
        current_odds = state['odds'][:num_selections]

        # Prevent Division by Zero errors
        if any(odd <= 0 for odd in current_odds):
            ui.notify("Odds must be greater than 0", type='warning')
            return

        probabilities = [100 / odd for odd in current_odds]
        margin = sum(probabilities) - 100
        pseudo_probabilities = [prob / (1 + margin / 100) for prob in probabilities]
        
        # Protect against exact 0% pseudo probability math crash loops
        fair_odds = [100 / pseudo_prob if pseudo_prob > 0 else 0.0 for pseudo_prob in pseudo_probabilities]

        state['results'] = {
            "Margin %": round(margin, 2),
            "Probabilities with Margin": [round(prob, 2) for prob in probabilities],
            "Pseudo-Probabilities": [round(p_prob, 2) for p_prob in pseudo_probabilities],
            "Fair Odds": [round(f_odd, 2) for f_odd in fair_odds],
        }
        results_panel.refresh()

    # Dynamic Odds Entry Rows Block
    @ui.refreshable
    def odds_inputs_renderer():
        num_selections = 2 if state['market_type'] == "2-Way Market" else 3
        with ui.row().classes('w-full gap-4 mb-4'):
            for i in range(num_selections):
                def make_handler(idx):
                    return lambda e: state['odds'].__setitem__(idx, e.value or 1.01)

                ui.number(label=f"Odd {i + 1}", value=state['odds'][i], format="%.2f", step=0.01,
                          on_change=make_handler(i)).classes('flex-grow')

    # Dynamic Results Summary Display Panel
    @ui.refreshable
    def results_panel():
        res = state['results']
        if not res:
            return

        num_selections = 2 if state['market_type'] == "2-Way Market" else 3

        with ui.column().classes('w-full mt-6 p-6 bg-slate-50 border border-gray-200 rounded-xl shadow-sm'):
            with ui.row().classes('w-full justify-between items-center mb-4'):
                ui.label("Calculation Results Matrix").classes('text-xl font-bold text-slate-800 underline')
                ui.label(f"Overround House Margin: {res['Margin %']}%") \
                    .classes('text-lg font-black text-blue-600 bg-blue-50 px-4 py-1 rounded-xl border border-blue-200')

            with ui.grid(columns=num_selections).classes('w-full gap-6 mt-2'):
                for i in range(num_selections):
                    with ui.column().classes('p-4 bg-white rounded-xl border border-gray-100 shadow-sm gap-1'):
                        ui.label(f"SELECTION {i+1}").classes('text-xs font-bold text-slate-400 tracking-wider mb-2')
                        
                        ui.label('Raw Implied Probability:').classes('text-[11px] text-gray-400 font-bold uppercase tracking-wide')
                        ui.label(f"{res['Probabilities with Margin'][i]}%").classes('text-slate-700 font-semibold mb-2')
                        
                        ui.label('Fair True Probability:').classes('text-[11px] text-gray-400 font-bold uppercase tracking-wide')
                        ui.label(f"{res['Pseudo-Probabilities'][i]}%").classes('text-slate-700 font-semibold mb-2')
                        
                        ui.label('Fair Odds (No Margin):').classes('text-[11px] text-gray-400 font-bold uppercase tracking-wide')
                        ui.label(f"{res['Fair Odds'][i]:.2f}").classes('text-xl font-black text-green-600')

    # Selection Toggle Mutation Intercept
    def handle_market_mutation(e):
        state['market_type'] = e.value
        state['results'] = None
        odds_inputs_renderer.refresh()
        results_panel.refresh()

    # Layout Blueprint Wireframes Mounting Structure
    with ui.column().classes('w-full max-w-4xl gap-4'):
        ui.label('Select Market Type Config').classes('text-xs font-bold text-slate-400 tracking-wider uppercase')
        ui.radio(["2-Way Market", "3-Way Market"], value=state['market_type'], on_change=handle_market_mutation) \
            .props('inline') \
            .classes('mb-2')

        ui.label('Enter Observed Bookmaker Odds Selections').classes('text-xs font-bold text-slate-400 tracking-wider uppercase')
        odds_inputs_renderer()

        ui.button('Calculate Clean True Pricing', on_click=calculate_margins) \
            .classes('w-full bg-blue-600 text-white font-bold py-3 rounded-xl shadow-md hover:bg-blue-700 transition-all')

        results_panel()
