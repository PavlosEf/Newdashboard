from nicegui import ui
import requests

# Currency metadata schema including native Emoji flags
CURRENCY_DATA = {
    "EUR": {"name": "Euro", "flag": "🇪🇺"},
    "ARS": {"name": "Argentina Peso", "flag": "🇦🇷"},
    "BGN": {"name": "Bulgaria Lev", "flag": "🇧🇬"},
    "BRL": {"name": "Brazil Real", "flag": "🇧🇷"},
    "CAD": {"name": "Canada Dollar", "flag": "🇨🇦"},
    "CLP": {"name": "Chile Peso", "flag": "🇨🇱"},
    "COP": {"name": "Colombia Peso", "flag": "🇨🇴"},
    "CZK": {"name": "Czech Koruna", "flag": "🇨🇿"},
    "DKK": {"name": "Denmark Krone", "flag": "🇩🇰"},
    "USD": {"name": "US Dollar / Ecuador", "flag": "🇺🇸"},
    "MXN": {"name": "Mexico Peso", "flag": "🇲🇽"},
    "NGN": {"name": "Nigeria Naira", "flag": "🇳🇬"},
    "PEN": {"name": "Peru Sol", "flag": "🇵🇪"},
    "RON": {"name": "Romania Leu", "flag": "🇷🇴"},
}

# Live data fetch loop engine
def fetch_exchange_rates(base_currency):
    # Utilizing your existing verification token endpoint credentials
    API_KEY = "f155bbe573194b9c9eb48462"
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json().get("conversion_rates", None)
    except Exception:
        pass
    return None

def run():
    # Page Title block
    ui.label('Currency Converter').classes('text-3xl font-bold text-slate-800 mb-2')
    ui.label('Fetch live global exchange rates instantly using mid-market values.') \
        .classes('text-gray-500 mb-6')

    # Application state values
    state = {
        'amount': 100.0,
        'from_curr': 'EUR',
        'to_curr': 'USD',
        'rates': None,
        'result_text': '',
        'inverse_text': ''
    }

    # Calculation action worker matrix
    def execute_conversion():
        # Step 1: Request live rates for selected baseline code
        rates = fetch_exchange_rates(state['from_curr'])
        if not rates:
            ui.notify("Failed to retrieve fresh exchange rates. Check connection or API token.", type='negative')
            return
        
        state['rates'] = rates
        amt = state['amount']
        from_c = state['from_curr']
        to_c = state['to_curr']

        # Step 2: Extract rate mappings and calculate final currency delta conversion
        if to_c not in rates:
            ui.notify(f"Selected currency {to_c} not supported by active api response data context.", type='warning')
            return

        converted_value = amt * rates[to_c]
        
        # Step 3: Compute inverse unit factors for extra display statistics
        unit_rate = rates[to_c]
        inverse_rate = 1.0 / unit_rate if unit_rate > 0 else 0.0

        # Inject updated html layout components safely via state parameters
        state['result_text'] = f"{amt:,.2f} {from_c} = <strong class='text-green-600 text-2xl'>{converted_value:,.6f} {to_c}</strong>"
        state['inverse_text'] = f"1 {from_c} = {unit_rate:,.6f} {to_c} &nbsp;|&nbsp; 1 {to_c} = {inverse_rate:,.6f} {from_c}"
        
        results_card.refresh()

    # Generate custom dictionary data mapping for select options list view parameters
    dropdown_options = {code: f"{data['flag']} {code} - {data['name']}" for code, data in CURRENCY_DATA.items()}

    @ui.refreshable
    def results_card():
        if not state['result_text']:
            return
        with ui.column().classes('w-full mt-6 p-5 bg-slate-50 border border-gray-200 rounded-xl shadow-sm'):
            ui.label("Conversion Result Summary").classes('text-sm font-bold text-gray-400 uppercase tracking-wider mb-2')
            ui.html(state['result_text']).classes('text-slate-800')
            ui.separator().classes('my-3')
            ui.html(state['inverse_text']).classes('text-xs text-gray-500 font-medium')

    # Master Frame Structure Layout
    with ui.column().classes('w-full max-w-4xl gap-4'):
        with ui.row().classes('w-full gap-4 items-center wrap'):
            ui.number('Amount to Convert', value=state['amount'], format="%.2f", step=10.0,
                      on_change=lambda e: state.update({'amount': e.value or 0.0})).classes('w-32 flex-grow')

            ui.select(options=dropdown_options, value=state['from_curr'], label='Source Currency (From)',
                      on_change=lambda e: state.update({'from_curr': e.value})).classes('w-48 flex-grow')

            ui.select(options=dropdown_options, value=state['to_curr'], label='Target Currency (To)',
                      on_change=lambda e: state.update({'to_curr': e.value})).classes('w-48 flex-grow')

        ui.button('Convert and Refresh Rates', on_click=execute_conversion) \
            .classes('w-full bg-blue-600 text-white font-bold py-3 rounded-xl shadow-md hover:bg-blue-700 transition-all')

        results_card()
