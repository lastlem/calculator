import json
from tkinter import *
from tkinter.ttk import *
from typing import Callable

entries_text = []


def math_operations(expression: str) -> str:
    numbers_and_signs = expression.split()
    answer = float(numbers_and_signs[0])
    for index, element in enumerate(numbers_and_signs):
        if element == '+':
            answer += float(numbers_and_signs[index + 1])
        elif element == '-':
            answer -= float(numbers_and_signs[index + 1])
        elif element == '/':
            answer /= float(numbers_and_signs[index + 1])
        elif element == '*':
            answer *= float(numbers_and_signs[index + 1])
    return str(answer)


def get_last_char(text: StringVar) -> str:
    return text.get().strip()[-1]


def clear_text(entries: list[Entry]) -> None:
    text_entry_expression, text_entry_number = entries
    text_entry_expression.set('0')
    text_entry_number.set('0')


def backspace(entries: list[Entry]) -> None:
    text_entry_expression, text_entry_number = entries

    if text_entry_number.get() == 'Cannot divide by zero' or is_end_math_sign(text_entry_expression):
        return

    text_entry_number.set(text_entry_number.get()[:-1])
    text_entry_expression.set(text_entry_expression.get()[:-1])

    if not text_entry_expression.get():
        text_entry_expression.set('0')
    if not text_entry_number.get():
        text_entry_number.set('0')


def is_end_math_sign(text) -> bool:
    return get_last_char(text) in '+-/*='


def set_number(number: int, entries: list[Entry]) -> None:
    text_entry_expression, text_entry_number = entries

    if text_entry_number.get() == 'Cannot divide by zero' or get_last_char(text_entry_expression) == '=':
        clear_text(entries)
    elif is_end_math_sign(text_entry_expression):
        text_entry_number.set('0')

    if not text_entry_number.get().startswith('0.') and text_entry_number.get().startswith('0'):
        text_entry_number.set(text_entry_number.get()[:-1])
    if not text_entry_number.get().startswith('0.') and text_entry_expression.get().split()[-1].startswith('0'):
        text_entry_expression.set(text_entry_expression.get()[:-1])

    text_entry_number.set(f'{text_entry_number.get()}{number}')
    text_entry_expression.set(f'{text_entry_expression.get()}{number}')


def check_zero_division(text: str) -> bool:
    return text.replace('0', '').replace('.', '').endswith('/ ')


def set_sign(sign: str, entries: list[Entry]):
    text_entry_expression, text_entry_number = entries

    if get_last_char(text_entry_expression) == '=':
        text_entry_expression.set(text_entry_number.get())
        text_entry_number.set('0')
    elif is_end_math_sign(text_entry_expression):
        text_entry_expression.set(f'{text_entry_expression.get()[:-2]}{sign} ')
        return

    if check_zero_division(text_entry_expression.get()):
        text_entry_number.set('Cannot divide by zero')
        return

    # math_operations(text_entry_expression.get())
    answer = eval(text_entry_expression.get())
    text_entry_number.set(answer)

    text_entry_expression.set(f'{text_entry_expression.get()} {sign} ')


def set_dot(entries: list[Entry]):
    text_entry_expression, text_entry_number = entries
    if text_entry_number.get() == 'Cannot divide by zero' or get_last_char(text_entry_expression) == '=':
        return

    if is_end_math_sign(text_entry_expression):
        text_entry_expression.set(f'{text_entry_expression.get()}0')
        text_entry_number.set('0')

    text = text_entry_expression.get()
    if '.' not in text.split()[-1]:
        text_entry_expression.set(f'{text_entry_expression.get()}.')
        text_entry_number.set(f'{text_entry_number.get()}.')


def create_entry(widget: dict) -> None:
    row_span = widget['row span'] if 'row span' in widget else 1
    # {"widget": {"widget type": "entry", "text": 0}, "grid_parameters": {}},
    text_entry = StringVar()
    text_entry.set(widget['text'])
    entries_text.append(text_entry)

    tuple_font = (widget['font'], widget['font size'], widget['font type'])
    widget_parameters = {'text': text_entry, 'justify': RIGHT, 'font': tuple_font}

    grid_parameters = {'column': widget['column'], 'row': widget['row'], 'columnspan': widget['column span'],
                       'rowspan': row_span, 'sticky': NSEW}
    Entry(**widget_parameters).grid(**grid_parameters)


def select_command(command: str, text: str) -> Callable:
    objects = {'clear_text': clear_text, 'delete_last_char': backspace, 'click_sign': set_sign,
               'click_dot': set_dot, 'click_number': set_number}

    if command in ('click_number', 'click_sign'):
        return lambda: objects[command](text, entries_text)
    else:
        return lambda: objects[command](entries_text)


def create_button(widget: dict) -> None:
    column_span = widget['column span'] if 'column span' in widget else 1
    command = select_command(widget['command'], widget['text'])
    grid_parameters = {'column': widget['column'], 'row': widget['row'], 'columnspan': column_span, 'sticky': NSEW}
    Button(text=widget['text'], command=command).grid(**grid_parameters)


def main(path: str):
    root = Tk()
    root.title('Calc v.11')

    root.columnconfigure(ALL, minsize=20)
    root.rowconfigure(ALL, minsize=20)

    style = Style()
    style.configure('TButton', width=5)

    with open(path) as file:
        data_widget = json.load(file)

    for element in data_widget:
        if element['widget'] == 'entry':
            create_entry(element)
        elif element['widget'] == 'button':
            create_button(element)

    root.mainloop()


if __name__ == '__main__':
    main('app_calculator.json')
