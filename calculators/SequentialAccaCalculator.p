from nicegui import ui

def run():
    ui.label('Sequential Acca Calculator').classes('text-3xl font-bold text-slate-800 mb-2')
    ui.label('Generate a complete overall hedging plan for multi-match accumulators with sequential game times.').classes('text-gray-500 mb-6')

    # Component State Configuration - Pre-allocated fixed list of 8 maximum slots
    # to maintain a static rendering pipeline structure and eliminate NiceGUI reference errors
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
        
        # Interlocking validation checks
        for idx, leg in enumerate(current_legs):
            if float(leg['back_odds']) <= 1.0 or float(leg['lay_odds']) <= 1.0:
                ui.notify(f"Invalid odds detected in Match {idx+1}. Odds must be greater than 1.00.", type='warning')
                return
        
        # Calculate total combined back odds
        total_back_odds = 1.0
        for leg in current_legs:
            total_back_odds *= float(leg['back_odds'])
            
        bookie_gross_return = b_stake * total_back_odds
        bookie_net_win_before_boost = (bookie_gross_return - b_stake) * (1.0 - b_comm)
        bookie_net_win = bookie_net_win_before_boost * (1.0 + boost)
        
        # Sequential matrix algebra solving for Equal Profit P
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
        if val < 2:
            val = 2
        if val > 8:
            val = 8
        state['num_legs'] = val
        state['results'] = None
        legs_inputs_renderer.refresh()
        results_panel.refresh()

    @ui.refreshable
    def legs_inputs_renderer():
        with ui.column().classes('w-full gap-3 bg-slate-50 p-4 rounded-xl border border-gray-200 shadow-sm mb-4'):
            ui.label('Accumulator Legs Parameters').classes('text-xs font-bold text-slate-400 uppercase tracking-wider')
            
            # Render elements statically from the fixed state buffer and manipulate visibility
            # to guarantee the layout hierarchy stays secure during rendering passes
            for i in range(8):
                is_visible = i < state['num_legs']
                with ui.row().classes('w-full gap-4 items-center wrap' + ('' if is_visible else ' hidden')) as row:
                    if is_visible:
                        ui.label(f"Match {i+1}:").classes('font-bold text-slate-700 w-20')
                        
                        # Closed default parameter scopes (idx=i) to secure values and avoid index bleed traps
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
