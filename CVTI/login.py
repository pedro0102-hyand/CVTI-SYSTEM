import PySimpleGUI as sg
sg.theme('DarkBlue4')
def login():
    layout = [[sg.Text('login'), sg.InputText(key='login')],
              [sg.Text('Senha'), sg.InputText(password_char='*',key = 'senha')],
              [sg.Button('Sair'), sg.Button('Entrar')]]
    window = sg.Window ( 'CVTI', layout)
    cred = [['adm','123'],['ademiro','adm']]
    val = False
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        if event == 'Entrar':
            for login,senha in cred:
                if values['login'] == login and values['senha'] == senha:
                    sg.popup('Acesso Confirmado', auto_close=True, auto_close_duration=1.5)
                    window.close()
                    val = True
        if val == False:
            sg.popup('Login ou senha incorretos',auto_close=True,auto_close_duration=1.5)
    window.close()
    return True if val else False