from nicegui import ui

def run():
    # Page Header Panel
    ui.label('Lay Bet Calculator').classes('text-3xl font-bold text-slate-800 mb-2')
    ui.label('Calculate lay stakes, liabilities, and profits for betting scenarios on Top Price Market prices.') \
        .classes('text-gray-500 mb-6')

    # Component State Management Architecture
    state = {
        'back_odds': 2.50,
        'lay_odds': 2.40,
        'back_stake': 100.0,
        'results': None
    }

    # Core Mathematical Formulas (Your exact math logic)
    def execute_calculations():
        b_odds = state['back_odds']
        l_odds = state['lay_odds']
        b_stake = state['back_stake']

        if b_odds <= 1 or l_odds <= 1 or b_stake <= 0:
            ui.notify("Please enter valid parameters greater than 0", type='warning')
            return

        # 1. Equal Profit Calculation Logic Path
        eq_lay_stake = (b_stake * b_odds) / l_odds
        eq_liability = eq_lay_stake * (l_odds - 1)
        eq_back_win = b_stake * (b_odds - 1)
        eq_back_lose = -b_stake
        eq_lay_win = -eq_liability
        eq_lay_lose = eq_lay_stake

        # 2. One-Way Calculation Logic Path
        ow_lay_stake = b_stake
        ow_liability = ow_lay_stake * (l_odds - 1)
        ow_back_win = b_stake * (b_odds - 1)
        ow_back_lose = -b_stake
        ow_lay_win = -ow_liability
        ow_lay_lose = b_stake

        state['results'] = {
            'eq_stake': round(eq_lay_stake, 2),
            'eq_liab': round(eq_liability, 2),
            'eq_m_win': round(eq_back_win + eq_lay_win, 2),
            'eq_m_lose': round(eq_back_lose + eq_lay_lose, 2),

            'ow_stake': round(ow_lay_stake, 2),
            'ow_liab': round(ow_liability, 2),
            'ow_m_win': round(ow_back_win - ow_liability, 2),
            'ow_m_lose': round(ow_lay_lose - ow_lay_stake, 2)
        }
        results_panel.refresh()

    @ui.refreshable
    def results_panel():
        res = state['results']
        if not res:
            return

        # Display side-by-side evaluation metrics panels
        with ui.row().classes('w-full gap-6 mt-4 wrap no-wrap-md'):
            
            # --- EQUAL PROFIT RESULTS COLUMN PANEL ---
            with ui.column().classes('flex-grow p-5 bg-slate-50 border border-gray-200 rounded-xl shadow-sm'):
                ui.label('Equal Profit Strategy').classes('text-lg font-bold text-slate-800 underline mb-2')
                ui.label(f"Lay Stake: {res['eq_stake']}€").classes('text-slate-700 font-medium')
                ui.label(f"Liability Risk: {res['eq_liab']}€").classes('text-slate-700 font-medium')
                ui.separator().classes('my-2')
                
                # If selection wins outcomes
                ui.label('IF SELECTION WINS (Back Wins / Lay Loses):').classes('text-[10px] font-bold text-gray-400 tracking-wider uppercase')
                w_color = 'text-green-600' if res['eq_m_win'] >= 0 else 'text-red-600'
                ui.label(f"Net Market Profit: {res['eq_m_win']}€").classes(f'text-lg font-black {w_color} mb-2')
                
                # If selection loses outcomes
                ui.label('IF SELECTION LOSES (Back Loses / Lay Wins):').classes('text-[10px] font-bold text-gray-400 tracking-wider uppercase')
                l_color = 'text-green-600' if res['eq_m_lose'] >= 0 else 'text-red-600'
                ui.label(f"Net Market Profit: {res['eq_m_lose']}€").classes(f'text-lg font-black {l_color}')

            # --- ONE-WAY RESULTS COLUMN PANEL ---
            with ui.column().classes('flex-grow p-5 bg-slate-50 border border-gray-200 rounded-xl shadow-sm'):
                ui.label('One-Way Strategy').classes('text-lg font-bold text-slate-800 underline mb-2')
                ui.label(f"Lay Stake: {res['ow_stake']}€").classes('text-slate-700 font-medium')
                ui.label(f"Liability Risk: {res['ow_liab']}€").classes('text-slate-700 font-medium')
                ui.separator().classes('my-2')
                
                # If selection wins outcomes
                ui.label('IF SELECTION WINS (Back Wins / Lay Loses):').classes('text-[10px] font-bold text-gray-400 tracking-wider uppercase')
                ow_w_color = 'text-green-600' if res['ow_m_win'] >= 0 else 'text-red-600'
                ui.label(f"Net Market Profit: {res['ow_m_win']}€").classes(f'text-lg font-black {ow_w_color} mb-2')
                
                # If selection loses outcomes
                ui.label('IF SELECTION LOSES (Back Loses / Lay Wins):').classes('text-[10px] font-bold text-gray-400 tracking-wider uppercase')
                ow_l_color = 'text-green-600' if res['ow_m_lose'] >= 0 else 'text-red-600'
                ui.label(f"Net Market Profit: {res['ow_m_lose']}€").classes(f'text-lg font-black {ow_l_color}')

    # Main Visual Tree Grid Architecture Layout
    with ui.column().classes('w-full max-w-4xl gap-4'):
        with ui.row().classes('w-full gap-4 items-center wrap'):
            ui.number('Back Odds', value=state['back_odds'], format="%.2f", step=0.01,
                      on_change=lambda e: state.update({'back_odds': e.value or 1.01})).classes('flex-grow')
            ui.number('Lay Odds', value=state['lay_odds'], format="%.2f", step=0.01,
                      on_change=lambda e: state.update({'lay_odds': e.value or 1.01})).classes('flex-grow')
            ui.number('Back Stake (€)', value=state['back_stake'], format="%.2f", step=10.0,
                      on_change=lambda e: state.update({'back_stake': e.value or 0.0})).classes('flex-grow')

        ui.button('Calculate Lay Matrix Outputs', on_click=execute_calculations) \
            .classes('w-full bg-blue-600 text-white font-bold py-3 rounded-xl shadow-md hover:bg-blue-700 transition-all')

        results_panel()
