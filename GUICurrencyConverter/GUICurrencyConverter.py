import PySimpleGUI as psg
from forex_python.converter import CurrencyRates
from forex_python.converter import RatesNotAvailableError


class CurrencyConverter:

    def __init__(self, currency_amount, current_currency='USD', converted_currency='RUB'):
        self.currency_amount = currency_amount
        self.current_currency = current_currency
        self.converted_currency = converted_currency

    def get_actual_exchange_rate(self):
        c = CurrencyRates()
        rate = c.get_rate(self.current_currency, self.converted_currency)
    # print(f'Current exchange rate from {self.current_currency} to {self.converted_currency}: {rate}')
        return rate

    def convert(self):
        c = CurrencyRates()
        rate = c.get_rate(self.current_currency, self.converted_currency)
        result_rate = rate * float(self.currency_amount)
        return result_rate


layout = [[psg.Text("Enter the value: "), psg.Input(key='-user_input-')],
          [psg.Text("Convert   From: "), psg.Combo(['USD', 'RUB', 'EUR'], size=(15, 1), key='-convert_from-')],
          [psg.Text("Convert      To:  "), psg.Combo(['USD', 'RUB', 'EUR'], size=(15, 1), key='-convert_to-')],
          [psg.Text(size=(40, 1), key='-OUTPUT-')],
          [psg.Button('Convert'), psg.Button('Current rate'), psg.Button('Quit')]]

window = psg.Window('Currency Converter', layout, size=(300, 150))


def main():
    while True:
        try:
            event, values = window.read()

            curr_amount = values['-user_input-']
            base_curr = values['-convert_from-']
            next_curr = values['-convert_to-']
            converter = CurrencyConverter(curr_amount, base_curr, next_curr)

            if event == psg.WINDOW_CLOSED or event == 'Quit':
                break
            elif event == 'Current rate':
                window['-OUTPUT-'].update(f"Current rate = {converter.get_actual_exchange_rate()}")
            elif event == 'Convert':
                window['-OUTPUT-'].update(f"Converted currency = {converter.convert()}")
        except ValueError:
            window['-OUTPUT-'].update("Wrong input!")
        except RatesNotAvailableError:
            window['-OUTPUT-'].update("Wrong input!")

    window.close()


main()
