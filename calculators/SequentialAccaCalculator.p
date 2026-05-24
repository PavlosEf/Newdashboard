from nicegui import ui

def run():
    ui.label('Sequential Acca Calculator').classes('text-3xl font-bold text-slate-800 mb-2')
    ui.label('Lock in equal guaranteed profits for multi-match accumulators when games are played at different times.').classes('text-gray-500 mb-6')

    # Component State Configuration
    state = {
        'num_legs': 3,
        'back_stake': 100.0,
        'acca_boost': 0.0,
        'back_comm': 0.0,
        'lay_comm': 2.0,
        'legs': [
            {'back_odds': 1.5, 'lay_odds': 1.55},
            {'back_odds': 1.8, 'lay_odds': 1.85},
            {'back_odds': 2.0, 'lay_odds': 2.05},
        ] + [{'back_odds': 2.0, 'lay_odds': 2.05} for _ in range(17)],
        'results': None
    }

    def calculate_sequential_acca():
        n = state['num_legs']
        b_stake = state['back_stake']
        boost = state['acca_boost'] / 100.0
        b_comm = state['back_comm'] / 100.0
        l_comm = state['lay_comm'] / 100.0
        
        current_legs = state['legs'][:n]
        
        # Calculate total combined back odds
        total_back_odds = 1.0
        for leg in current_legs:
            total_back_odds *= leg['back_odds']
            
        bookie_gross_return = b_stake * total_back_odds
        bookie_net_win_before_boost = (bookie_gross_return - b_stake) * (1.0 - b_comm)
        bookie_net_win = bookie_net_win_before_boost * (1.0 + boost)
        
        # Sequential matrix algebra solving for Equal Profit P
        C = 0.0
        D = 0.0
        A_list = []
        B_list = []
        
        for leg in current_legs:
            lay_odd = leg['lay_odds']
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
            liab = stk * (leg['lay_odds'] - 1.0)
            legs_results.append({
                'leg_idx': i + 1,
                'lay_stake': round(stk, 2),
                'liability': round(liab, 2),
            })
            
        state['results'] = {
            'total_back_odds': round(total_back_odds, 2),
            'bookie_net_win': round(bookie_net_win, 2),
            'guaranteed_profit': round(P, 2),
            'legs': legs_results
        }
        results_panel.refresh()

    @ui.refreshable
    def legs_inputs_renderer():
        with ui.column().classes('w-full gap-3 bg-slate-50 p-4 rounded-xl border border-gray-200 shadow-sm mb-4'):
            ui.label('Accumulator Legs Parameters').classes('text-xs font-bold text-slate-400 uppercase tracking-wider')
            for i in range(state['num_legs']):
                with ui.row().classes('w-full gap-4 items-center wrap'):
                    ui.label(f"Match {i+1}:").classes('font-bold text-slate-700 w-20')
                    
                    def make_back_handler(idx):
                        return lambda e: state['legs'][idx].update({'back_odds': e.value or 1.01})
                    def make_lay_handler(idx):
                        return lambda e: state['legs'][idx].update({'lay_odds': e.value or 1.01})
                        
                    ui.number(label='Back Odds', value=state['legs'][i]['back_odds'], format="%.2f", step=0.01, on_change=make_back_handler(i)).classes('flex-grow')
                    ui.number(label='Lay Odds', value=state['legs'][i]['lay_odds'], format="%.2f", step=0.01, on_change=make_lay_handler(i)).classes('flex-grow')

    @ui.refreshable
    def results_panel():
        res = state['results']
        if not res:
            return
            
        profit_color = 'text-green-600' if res['guaranteed_profit'] >= 0 else 'text-red-600'
        
        with ui.column().classes('w-full p-6 bg-slate-50 border border-gray-200 rounded-xl shadow-sm mt-4'):
            ui.label('Guaranteed Matrix Outputs').classes('text-xl font-bold text-slate-800 mb-4 underline')
            
            with ui.row().classes('w-full justify-between wrap gap-4 mb-4'):
                ui.label(f"Total Accumulator Odds: {res['total_back_odds']:.2f}").classes('text-sm font-medium text-slate-700')
                ui.label(f"Bookmaker Net Profit (If All Win): {res['bookie_net_win']:.2f}€").classes('text-sm font-medium text-slate-700')
                ui.label(f"Guaranteed Equal Profit: {res['guaranteed_profit']:.2f}€").classes(f'text-lg font-black {profit_color}')
                
            ui.separator().classes('my-2')
            ui.label('Step-by-Step Lay Schedule Instructions').classes('text-xs font-bold text-gray-400 uppercase tracking-wider mb-2')
            
            for leg in res['legs']:
                with ui.row().classes('w-full p-3 bg-white rounded-lg border border-gray-100 items-center justify-between shadow-sm mb-2'):
                    ui.label(f"Match {leg['leg_idx']}").classes('font-bold text-slate-800')
                    ui.label(f"Lay Stake: {leg['lay_stake']:.2f}€").classes('text-slate-700 font-medium')
                    ui.label(f"Betfair Liability: {leg['liability']:.2f}€").classes('text-slate-700 font-medium')
                    ui.label('Action if Reached').classes('text-[10px] text-blue-600 bg-blue-50 px-2 py-0.5 rounded font-bold uppercase tracking-wide')

    def adjust_leg_count(e):
        val = int(e.value or 3)
        if val < 2:
            val = 2
        state['num_legs'] = val
        state['results'] = None
        legs_inputs_renderer.refresh()
        results_panel.refresh()

    with ui.column().classes('w-full max-w-4xl gap-4'):
        with ui.row().classes('w-full items-center gap-4 mb-2'):
            ui.label('Enter Number of Matches (Legs):').classes('font-medium text-slate-700')
            ui.number(value=state['num_legs'], format="%d", step=1, on_change=adjust_leg_count).classes('w-24')

        legs_inputs_renderer()

        ui.label('Global Parameters Allocation').classes('text-xs font-bold text-slate-400 tracking-wider uppercase mt-2')
        with ui.row().classes('w-full gap-4 wrap items-center mb-4'):
            ui.number('Back Stake (€)', value=state['back_stake'], format="%.2f", step=10.0, on_change=lambda e: state.update({'back_stake': e.value or 0.0})).classes('flex-grow')
            ui.number('Acca Boost (%)', value=state['acca_boost'], format="%.1f", step=1.0, on_change=lambda e: state.update({'acca_boost': e.value or 0.0})).classes('flex-grow')
            ui.number('Bookie Tax/Comm (%)', value=state['back_comm'], format="%.1f", step=0.5, on_change=lambda e: state.update({'back_comm': e.value or 0.0})).classes('flex-grow')
            ui.number('Betfair Comm (%)', value=state['lay_comm'], format="%.1f", step=0.5, on_change=lambda e: state.update({'lay_comm': e.value or 0.0})).classes('flex-grow')

        ui.button('Calculate Sequential Lay Matrix', on_click=calculate_sequential_acca) \
            .classes('w-full bg-blue-600 text-white font-bold py-3 rounded-xl shadow-md hover:bg-blue-700 transition-all')

        results_panel()
