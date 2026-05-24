from nicegui import ui
from dataclasses import dataclass
from typing import List

def find_closest_pattern(odds: float, patterns: List[List[float]]) -> List[float]:
    closest_pattern = min(patterns, key=lambda p: min(abs(o - odds) for o in p))
    return closest_pattern

@dataclass
class OddsResult:
    our_line: float
    our_odds: float
    comp_at_our_line: float
    difference_percentage: float
    status: str

class DifferentLinesCalculator:
    def __init__(self):
        self.patterns: List[List[float]] = [
            [1.39, 1.43, 1.5, 1.54, 1.62, 1.66, 1.74, 1.8, 1.95, 2.05, 2.15, 2.25, 2.35, 2.5, 2.65, 2.75],
            [1.4, 1.43, 1.5, 1.55, 1.62, 1.66, 1.74, 1.8, 1.95, 2.05, 2.15, 2.25, 2.35, 2.5, 2.6, 2.7],
            [1.38, 1.43, 1.47, 1.52, 1.57, 1.64, 1.71, 1.76, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.55, 2.65, 2.85],
            [1.36, 1.41, 1.47, 1.52, 1.57, 1.64, 1.71, 1.76, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.55, 2.7, 2.85]
        ]

    def _find_nearest_in_pattern(self, value: float, pattern: List[float]) -> float:
        return min(pattern, key=lambda x: abs(x - value))

    def _step_odds(self, odds: float, step_up: bool, pattern: List[float]) -> float:
        if odds not in pattern:
            odds = self._find_nearest_in_pattern(odds, pattern)
        index = pattern.index(odds)
        if step_up and index < len(pattern) - 1:
            return pattern[index + 1]
        elif not step_up and index > 0:
            return pattern[index - 1]
        return odds

    def calculate_competition_odds(self, our_line: float, our_odds: float,
                                   comp_line: float, comp_odds: float, direction: str) -> float:
        line_diff = int(our_line - comp_line)
        step_up = line_diff > 0 if direction == "over" else line_diff < 0
        closest_pattern = find_closest_pattern(comp_odds, self.patterns)
        current_odds = comp_odds
        for _ in range(abs(line_diff)):
            current_odds = self._step_odds(current_odds, step_up, closest_pattern)
        return current_odds

    def calculate_difference(self, our_odds: float, comp_odds: float) -> float:
        return ((1 / our_odds) - (1 / comp_odds)) * 100

    def get_status(self, difference: float) -> str:
        if difference > -2:
            return "OK"
        elif -3 <= difference <= -2:
            return "Off 2"
        else:
            return "Off 1"

    def calculate(self, our_line: float, our_odds: float,
                  comp_line: float, comp_odds: float, direction: str) -> OddsResult:
        comp_at_our = self.calculate_competition_odds(our_line, our_odds, comp_line, comp_odds, direction)
        difference = self.calculate_difference(our_odds, comp_at_our)
        status = self.get_status(difference)
        return OddsResult(our_line=our_line, our_odds=our_odds, comp_at_our_line=comp_at_our,
                          difference_percentage=difference, status=status)

def run():
    # Instantiate calculation core engine
    calculator = DifferentLinesCalculator()

    # Form State Dictionary
    state = {
        'our_line': 0.0, 'our_odds': 1.00,
        'comp_line': 0.0, 'comp_odds': 1.00,
        'direction': 'over', 'result': None
    }

    def execute_calculation():
        try:
            res = calculator.calculate(
                our_line=state['our_line'], our_odds=state['our_odds'],
                comp_line=state['comp_line'], comp_odds=state['comp_odds'],
                direction=state['direction']
            )
            state['result'] = res
            results_panel.refresh()
        except Exception as e:
            ui.notify(f"Calculation Error: {str(e)}", type='negative')

    @ui.refreshable
    def results_panel():
        res = state['result']
        if not res:
            return

        # Explicit status coloring scheme matrix
        color_map = {"OK": "bg-green-500", "Off 2": "bg-purple-600", "Off 1": "bg-red-500"}
        badge_bg = color_map.get(res.status, "bg-gray-500")

        with ui.column().classes('w-full mt-6 p-6 bg-slate-50 border border-gray-200 rounded-xl shadow-sm'):
            ui.label("Converted Results Summary").classes('text-xl font-bold text-slate-800 mb-4 underline')
            
            with ui.row().classes('w-full justify-between items-center gap-4 wrap'):
                with ui.column():
                    ui.label('Our Baseline Specs').classes('text-xs font-bold text-gray-400 uppercase tracking-wider')
                    ui.label(f"Line Target: {res.our_line}").classes('text-slate-700 font-medium')
                    ui.label(f"Odds Base: {res.our_odds:.2f}").classes('text-slate-700 font-medium')

                with ui.column():
                    ui.label('Adjusted Competition').classes('text-xs font-bold text-gray-400 uppercase tracking-wider')
                    ui.label(f"Odds at Our Line: {res.comp_at_our_line:.3f}").classes('text-slate-800 font-bold text-lg')
                    
                    diff = res.difference_percentage
                    diff_color = "text-green-600" if diff >= 0 else "text-red-600"
                    ui.label(f"Delta Deviation: {diff:.2f}%").classes(f'font-bold {diff_color}')

                with ui.column().classes('items-center justify-center px-6'):
                    ui.label(f"STATUS: {res.status}").classes(f'text-white font-black px-6 py-2 rounded-xl shadow-sm tracking-wide text-lg {badge_bg}')
            
            ui.label('Disclaimer: This is an approximated calculator. Real odds may have a small difference.') \
                .classes('text-xs text-gray-400 italic mt-4')

    # Main Visual Tree Architecture Placement
    with ui.column().classes('w-full max-w-4xl gap-4'):
        ui.label('Alternative Lines Converter').classes('text-3xl font-bold text-slate-800 mb-2')
        
        with ui.row().classes('w-full gap-6 mb-2 wrap'):
            # Left side element inputs column
            with ui.column().classes('flex-grow bg-slate-50 p-4 rounded-xl border border-gray-100 shadow-sm'):
                ui.label('Our Odds Data').classes('text-xs font-bold text-slate-400 uppercase tracking-wider mb-2')
                ui.number('Our Line', value=state['our_line'], format="%.1f", step=0.5,
                          on_change=lambda e: state.update({'our_line': e.value or 0.0})).classes('w-full')
                ui.number('Our Odds', value=state['our_odds'], format="%.2f", step=0.01,
                          on_change=lambda e: state.update({'our_odds': e.value or 1.00})).classes('w-full')

            # Right side element inputs column
            with ui.column().classes('flex-grow bg-slate-50 p-4 rounded-xl border border-gray-100 shadow-sm'):
                ui.label('Competition Reference Data').classes('text-xs font-bold text-slate-400 uppercase tracking-wider mb-2')
                ui.number('Competition Line', value=state['comp_line'], format="%.1f", step=0.5,
                          on_change=lambda e: state.update({'comp_line': e.value or 0.0})).classes('w-full')
                ui.number('Competition Odds', value=state['comp_odds'], format="%.2f", step=0.01,
                          on_change=lambda e: state.update({'comp_odds': e.value or 1.00})).classes('w-full')

        # Control toggles element row
        with ui.row().classes('w-full items-center justify-between mb-2 p-2'):
            ui.label('Select Adjustment Progression Direction:').classes('font-medium text-slate-700')
            ui.radio(['over', 'under'], value=state['direction'], on_change=lambda e: state.update({'direction': e.value})).props('inline')

        ui.button('Convert and Calculate Gap', on_click=execute_calculation) \
            .classes('w-full bg-blue-600 text-white font-bold py-3 rounded-xl shadow-md hover:bg-blue-700 transition-all')

        results_panel()
