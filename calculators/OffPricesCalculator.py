from nicegui import ui

def run():
    # Page Title Block
    ui.label('Off Prices Calculator').classes('text-3xl font-bold text-slate-800 mb-2')
    ui.label('Enter prices below to calculate the percentage difference. Our odds are 1st!') \
        .classes('text-gray-500 mb-6')

    # Data matrix to store the values for 5 rows
    rows_data = []
    for i in range(5):
        rows_data.append({
            'our_odds': 0.0,
            'comp_odds': 0.0,
            'diff_label': None,
            'status_badge': None
        })

    # Core Math Calculation Function
    def calculate_row(index):
        data = rows_data[index]
        a = data['our_odds']
        b = data['comp_odds']

        # Ensure valid inputs before calculating math loops
        if a > 0 and b > 0:
            difference = ((1 / a) - (1 / b)) * 100
            
            # Update the text difference label
            data['diff_label'].set_text(f"{difference:.2f}%")
            
            # Reset badge design properties and clean text
            data['status_badge'].classes(remove='bg-green-500 bg-purple-600 bg-red-500 hidden')
            
            # Evaluation status matrix loops
            if difference > -2:
                data['status_badge'].set_text('OK')
                data['status_badge'].classes('bg-green-500 text-white font-bold px-3 py-1 rounded shadow-sm')
            elif -3 <= difference <= -2:
                data['status_badge'].set_text('OFF 2')
                data['status_badge'].classes('bg-purple-600 text-white font-bold px-3 py-1 rounded shadow-sm')
            else:
                data['status_badge'].set_text('OFF 1')
                data['status_badge'].classes('bg-red-500 text-white font-bold px-3 py-1 rounded shadow-sm')
        else:
            data['diff_label'].set_text('—')
            data['status_badge'].classes('hidden')

    # Helper to generate structural change handling variables safely
    def make_change_handler(idx, field_ref):
        return lambda e: [
            rows_data[idx].update({field_ref: e.value or 0.0}),
            calculate_row(idx)
        ]

    # Render Grid Panels for the 5 Input Rows
    for i in range(5):
        with ui.row().classes('w-full items-center gap-6 mb-4 p-3 bg-slate-50 rounded-xl border border-gray-100 shadow-sm'):
            
            # Label Row items
            ui.label(f"Row {i+1}").classes('text-sm font-bold text-slate-400 w-12')
            
            # Our Odds Inputs (Passing change handler cleanly inside parameters)
            ui.number(label="Our Odds", format="%.2f", step=0.01, 
                      on_change=make_change_handler(i, 'our_odds')).classes('w-32')
            
            # Competition Odds Inputs
            ui.number(label="Competition Odds", format="%.2f", step=0.01, 
                      on_change=make_change_handler(i, 'comp_odds')).classes('w-32')

            # Calculation Results Target Layout Blocks
            ui.label('Difference:').classes('text-sm font-medium text-gray-500 ml-4')
            rows_data[i]['diff_label'] = ui.label('—').classes('text-lg font-bold text-slate-700 w-20 text-center')
            
            # Status badge wrapper element block
            rows_data[i]['status_badge'] = ui.label('').classes('hidden')
