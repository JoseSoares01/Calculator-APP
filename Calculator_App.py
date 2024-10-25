import flet as ft
from flet import colors
from decimal import Decimal
import keyboard as kb

# Lista de botões da calculadora, com informações sobre operadores, cores de fonte e fundo
botoes = [
    {'operador': 'C', 'fonte': colors.BLACK, 'fundo': "#98b29b"},
    {'operador': '±', 'fonte': colors.BLACK, 'fundo': "#98b29b"},
    {'operador': '%', 'fonte': colors.BLACK, 'fundo': "#98b29b"},
    {'operador': '÷', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
    {'operador': '7', 'fonte': colors.WHITE, 'fundo': colors.GREY},
    {'operador': '8', 'fonte': colors.WHITE, 'fundo': colors.GREY},
    {'operador': '9', 'fonte': colors.WHITE, 'fundo': colors.GREY},
    {'operador': '×', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
    {'operador': '4', 'fonte': colors.WHITE, 'fundo': colors.GREY},
    {'operador': '5', 'fonte': colors.WHITE, 'fundo': colors.GREY},
    {'operador': '6', 'fonte': colors.WHITE, 'fundo': colors.GREY},
    {'operador': '-', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
    {'operador': '1', 'fonte': colors.WHITE, 'fundo': colors.GREY},
    {'operador': '2', 'fonte': colors.WHITE, 'fundo': colors.GREY},
    {'operador': '3', 'fonte': colors.WHITE, 'fundo': colors.GREY},
    {'operador': '+', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
    {'operador': '0', 'fonte': colors.WHITE, 'fundo': colors.GREY},  # Largura dupla
    {'operador': ',', 'fonte': colors.WHITE, 'fundo': colors.GREY},
    {'operador': '=', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
]

def simulate_click(key, result):
    for btn in botoes:
        if btn['operador'] == key:
            select(ft.ControlEvent(control=ft.Text(value=key)), result)

def main(page: ft.Page):
    # Configurações fixas da janela da calculadora
    page.bgcolor = '#000000'
    page.window_resizable = True
    page.window_width = 300
    page.window_height = 520
    page.title = 'Calculadora'
    page.window_always_on_top = True
    page.padding = 0

    # Dimensões dos botões
    BUTTON_WIDTH = 65
    BUTTON_HEIGHT = 65
    BUTTON_SPACING = 4
    ZERO_BUTTON_WIDTH = BUTTON_WIDTH * 2 + BUTTON_SPACING

    # Elemento de texto que mostra o resultado
    result = ft.Text(
        value="0",
        color=colors.WHITE,
        size=45,
        weight=ft.FontWeight.W_500
    )

    def calculate(value_at):
        try:
            value_at = value_at.replace('×', '*').replace('÷', '/')
            value = eval(value_at)
            return str(Decimal(value))
        except:
            return 'Error'

    def select(e, result):
        value_at = result.value if result.value not in ('0', 'Error') else ''
        operador = e.control.content.value

        if operador.isdigit() or operador == ',':
            if operador == ',' and ',' in value_at.split()[-1]:
                return
            value_at += operador
        elif operador == 'C':
            value_at = '0'
        elif operador == '±':
            value_at = str(-Decimal(value_at)) if value_at not in ('0', 'Error') else '0'
        elif operador == '%':
            try:
                value_at = str(Decimal(value_at) / 100)
            except:
                value_at = 'Error'
        elif operador == '=':
            value_at = calculate(value_at)
        else:
            if value_at and value_at[-1] in ('÷', '×', '-', '+'):
                value_at = value_at[:-1]
            value_at += operador

        result.value = value_at
        result.update()

    def create_buttons():
        buttons = []
        for btn in botoes:
            width = ZERO_BUTTON_WIDTH if btn['operador'] == '0' else BUTTON_WIDTH
            buttons.append(
                ft.Container(
                    content=ft.Text(value=btn['operador'], color=btn['fonte'], size=28, weight=ft.FontWeight.W_500),
                    alignment=ft.alignment.center,
                    width=width,
                    height=BUTTON_HEIGHT,
                    bgcolor=btn['fundo'],
                    border_radius=12,
                    on_click=lambda e, r=result: select(e, r)
                )
            )
        return buttons

    # Configuração dos elementos de exibição do resultado e do teclado
    display = ft.Container(
        content=ft.Row(
            controls=[result],
            alignment=ft.MainAxisAlignment.END
        ),
        padding=ft.padding.only(right=20, top=20, bottom=20),
        width=page.window_width - 20
    )

    keyboard = ft.Container(
        content=ft.Row(
            wrap=True,
            controls=create_buttons(),
            spacing=BUTTON_SPACING,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        width=page.window_width - 20
    )

    # Container principal para centralizar o conteúdo
    main_container = ft.Container(
        content=ft.Column(
            controls=[display, keyboard],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
    )

    # Adiciona o container principal à página
    page.add(main_container)

ft.app(target=main)
