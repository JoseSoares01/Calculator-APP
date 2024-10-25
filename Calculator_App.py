import flet as ft
from flet import colors
from decimal import Decimal

# Lista de botões da calculadora, com informações sobre operadores, cores de fonte e fundo.
botoes = [
    {'operador': 'AC', 'fonte': colors.BLACK, 'fundo': colors.BLUE_GREY_100},
    {'operador': '±', 'fonte': colors.BLACK, 'fundo': colors.BLUE_GREY_100},
    {'operador': '%', 'fonte': colors.BLACK, 'fundo': colors.BLUE_GREY_100},
    {'operador': '/', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
    {'operador': '7', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '8', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '9', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '*', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
    {'operador': '4', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '5', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '6', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '-', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
    {'operador': '1', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '2', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '3', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '+', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
    {'operador': '0', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '.', 'fonte': colors.WHITE, 'fundo': colors.WHITE24},
    {'operador': '=', 'fonte': colors.WHITE, 'fundo': colors.ORANGE},
]

def main(page: ft.Page):
    # Configurações da janela da calculadora.
    page.bgcolor = '#000'
    page.window_resizable = False
    page.window_width = 410
    page.window_height = 450
    page.title = 'Calculadora José'
    page.window_always_on_top = True

    # Elemento de texto que mostra o resultado da calculadora.
    result = ft.Text(value="0", color=colors.WHITE, size=30)  # Melhorando a visibilidade do resultado
    
    # Função para calcular as operações da calculadora.
    def calculate(value_at):
        try:
            value = eval(value_at)
            return str(Decimal(value).normalize())
        except:
            return 'Error'

    # Função para lidar com a seleção de botões da calculadora.
    def select(e):
        value_at = result.value if result.value not in ('0', 'Error') else ''
        operador = e.control.content.value

        if operador.isdigit() or operador == '.':
            if operador == '.' and '.' in value_at.split()[-1]:  # Impede múltiplos pontos
                return
            value_at += operador
        elif operador == 'AC':
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
            if value_at and value_at[-1] in ('/', '*', '-', '+'):
                value_at = value_at[:-1]  # Substitui operador repetido
            value_at += operador

        result.value = value_at
        result.update()

    # Criação dos botões da calculadora.
    btn = [ft.Container(
            content=ft.Text(value=btn['operador'], color=btn['fonte']),
            alignment=ft.alignment.center,
            width=96,
            height=46,
            bgcolor=btn['fundo'],
            border_radius=100,
            on_click=select
        ) for btn in botoes]

    # Configuração dos elementos de exibição do resultado e do teclado.
    display = ft.Row(
        width=250, 
        controls=[result],
        alignment='end'
    )
    
    keyboard = ft.Row(
        width=401,
        wrap=True,
        controls=btn,
        alignment='end',
    )

    # Adição dos elementos à página.
    page.add(display)
    page.add(keyboard)

# Inicialização da aplicação.
ft.app(target=main)
