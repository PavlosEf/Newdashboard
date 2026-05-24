from nicegui import ui

def run():
    # Page Header
    ui.label('Percentage (%) Calculations').classes('text-3xl font-bold text-slate-800 mb-2')
    ui.label('Select your preferred configuration to perform instant math operations.') \
        .classes('text-gray-500 mb-6')

    # Component State Matrix
    state = {
        'option': 'What is X% of Y?',
        'x': 0.0,
        'y': 0.0,
        'result_text': ''
    }

    # Calculation logic switcher
    def perform_calculation():
        opt = state['option']
        x = state['x']
        y = state['y']

        if opt == "What is X% of Y?":
            res = (x / 100) * y
            state['result_text'] = f"{x}% of {y} is <strong>{res:.4f}</strong>"
        elif opt == "X is what percent of Y?" or opt == "X is what % of Y?":
            if y == 0:
                ui.notify("Cannot divide by zero (Y)", type='warning')
                return
            res = (x / y) * 100
            state['result_text'] = f"{x} is <strong>{res:.2f}%</strong> of {y}"
        elif opt == "Percentage increase/decrease from X to Y":
            if x == 0:
                ui.notify("Initial value (X) cannot be zero", type='warning')
                return
            res = ((y - x) / x) * 100
            state['result_text'] = f"The percentage change from {x} to {y} is <strong>{res:.2f}%</strong>"

        results_panel.refresh()

    @ui.refreshable
    def inputs_panel():
        # Adjust label naming parameters dynamically based on selected option state
        opt = state['option']
        if opt == "What is X% of Y?":
            lbl_x, lbl_y = "Enter percentage (X)", "Enter number (Y)"
        elif opt == "Percentage increase/decrease from X to Y":
            lbl_x, lbl_y = "Enter initial number (X)", "Enter final number (Y)"
        else:
            lbl_x, lbl_y = "Enter number (X)", "Enter number (Y)"

        with ui.row().classes('w-full gap-4 mb-4'):
            ui.number(label=lbl_x, value=state['x'], format="%.2f", step=1.0,
                      on_change=lambda e: state.update({'x': e.value or 0.0})).classes('flex-grow')
            ui.number(label=lbl_y, value=state['y'], format="%.2f", step=1.0,
                      on_change=lambda e: state.update({'y': e.value or 0.0})).classes('flex-grow')

    @ui.refreshable
    def results_panel():
        if not state['result_text']:
            return
        with ui.column().classes('w-full mt-4 p-4 bg-green-50 border-b-4 border-green-500 rounded-lg shadow-sm'):
            ui.html(state['result_text']).classes('text-xl text-slate-800 font-medium')

    def menu_selection_changed(e):
        state['option'] = e.value
        state['result_text'] = ''
        inputs_panel.refresh()
        results_panel.refresh()

    # Layout Assembly Structure Mount Point
    with ui.column().classes('w-full max-w-4xl gap-4'):
        ui.select([
            "What is X% of Y?",
            "X is what percent of Y?",
            "X is what % of Y?",
            "Percentage increase/decrease from X to Y"
        ], value=state['option'], on_change=menu_selection_changed).classes('w-full max-w-md mb-2')

        inputs_panel()

        ui.button('Execute Calculation', on_click=perform_calculation) \
            .classes('w-full bg-blue-600 text-white font-bold py-3 rounded-xl shadow-md hover:bg-blue-700 transition-all')

        results_panel()
