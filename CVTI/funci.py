
import json
import PySimpleGUI as sg
caminho = 'src/data.json'
alunos = json.load(open(caminho))
cursos = ['Computer Science', 'Excel', 'Web Design', 'Data Science','Math','Chemistry Enginnering']
sg.theme('DarkBlue4')
menu_def = [['Registros', ['Cadastrar Alunos', 'Atualizar Informações de um Aluno', 'Excluir Aluno']],
            ['Pesquisas', ['Listar todos os alunos']],
            ['Sair', ['Sair']]]
def carregar_alunos():
    try:
        with open(caminho, 'r') as openfile:
            alunos = json.load(openfile)
            if len(alunos) == 0:
                sg.popup("Nenhum aluno cadastrado!")
                return None
            return alunos
    except:
        sg.popup("Erro ao carregar os alunos.")
        return None     
def salvar_alunos(alunos):
     with open(caminho, "w") as outfile: 
                json.dump(alunos, outfile, indent='\t')
def cadastrar_aluno():
    layout = [[sg.Menu(menu_def, pad=(200,1))],
              [sg.Text('Digite o nome do aluno: '),sg.InputText(key='name')],
              [sg.Text('Digite o sobrenome do aluno: '), sg.InputText(key='surname')],
              [sg.Text('Digite a idade do aluno: '), sg.InputText(key='age')],
              [sg.Text('Digite o CPF do aluno:'),sg.InputText(key='cpf')],
              [sg.Text('Selecione o curso desejado: '),sg.Combo(values=cursos, key='course')],
              [sg.Button('Cadastrar')]]
    window = sg.Window('Cadastro de Aluno', layout)
    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        if event == 'Cadastrar':
            alunos.append({"nome": values['name'], "sobrenome": values['surname'], "idade": values['age'], "cpf": values['cpf'], "curso": values['course']})
            salvar_alunos(alunos)
            sg.popup('Aluno cadastrado com sucesso!')
    window.close()
def atualizar_aluno():
    layout=[[sg.Menu(menu_def, pad=(200,1))],
            [sg.Text('Digite o nome completo do Aluno a ser atualizado: '), sg.InputText(key='nome_completo')],
            [sg.Button('Buscar e Atualizar', key='bt')]]
    window = sg.Window('Atualizar Cadastro',layout)
    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        if event == 'bt':
            name, surname = str(values['nome_completo']).split(' ',1)
            subs(name, surname)
    window.close()
def subs(nome, sobrenome):
    layout = [[sg.Text('Digite a nova idade do aluno: '),sg.InputText(key='age')],
              [sg.Text('Digite o novo cpf do aluno: '),sg.InputText(key='cpf')],
              [sg.Text('Selecione o novo curso do aluno:'),sg.OptionMenu(values=cursos, key='course')],
              [sg.Button('Atualizar', key = 'atu')]]
    windown = sg.Window('',layout)
    while True:
        event,values = windown.read(timeout=100)
        if event == sg.WIN_CLOSED:
            break
        if event == 'atu':
            for aluno in alunos:
                if aluno['name'].lower() == nome.lower() and aluno['surname'].lower() == sobrenome.lower():
                    aluno['age'] = values['age'] if values['age'] != '' else aluno['age']
                    aluno['cpf'] = values['cpf'] if values['cpf'] != '' else aluno['cpf']
                    aluno['course'] = values['course'] if values['course'] != '' else aluno['course']
                    salvar_alunos(alunos)
                    sg.popup(f"Informacoes do aluno {nome} {sobrenome} atualizadas com sucesso!",auto_close = True, auto_close_duration = 3)
                    windown.close()
                    return
            sg.popup(f"Não foi encontrado nenhum aluno com o nome {nome} {sobrenome}.")
    windown.close()
def excluir_aluno():
    layout=[[sg.Menu(menu_def, pad=(200,1))],
            [sg.Text('Digite o nome completo do Aluno a ser excluido: '), sg.InputText(key='nome_completo')],
            [sg.Button('Buscar e Excluir', key='bt')]]
    window = sg.Window('Excluir do cadastro',layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        if event == 'bt':
            nome, sobrenome = str(values['nome_completo']).split(' ', 1)
            for aluno in alunos:
                if aluno['nome'].lower() == nome.lower() and aluno['sobrenome'].lower() == sobrenome.lower():
                    alunos.remove(aluno)
                    salvar_alunos(alunos)
                    sg.popup(f"Aluno {values['nome_completo']} excluído com sucesso!")
                    return
            sg.popup(f"Não foi encontrado nenhum aluno com o nome {values['nome_completo']}.")
    window.close()
def listar_alunos():
    alunos = json.load(open(caminho, 'r'))
    cols = ['name','surname','age','cpf','course']
    lastvalue = None
    data = list()
    layout = [[sg.Menu(menu_def, pad=(200,1))],
              [sg.Text('Listagem de Alunos no curso:'),sg.OptionMenu(values=['Todos']+ [i for i in cursos],default_value='Todos', key='opc')],
              [sg.Table(values = data ,headings = cols,key='tb',expand_x=True,expand_y=True,justification='center')]]
    window = sg.Window('Lista de Alunos', layout, element_justification='r', auto_size_buttons=True,auto_size_text=True, size=(800,600))
    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        if values['opc'] != lastvalue:
            lastvalue = values['opc']
            data = list()
            window['tb'].update(values = data)
            if lastvalue != 'Todos':
                j = 0
                while j < len(alunos):
                    i = 0
                    mid = list()
                    if alunos[j]['curso'] == values['opc']:
                        while i < len(cols):
                            mid.append(alunos[j][cols[i]])
                            i += 1
                        data.append(mid)
                    j += 1
                window['tb'].update(values = data)
            else:
                j = 0
                while j < len(alunos):
                    i = 0
                    mid = list()
                    while i < len(cols):
                        mid.append(alunos[j][cols[i]])
                        i += 1
                    data.append(mid)
                    j += 1
                window['tb'].update(values = data)
    window.close()
def professor_do_curso(course):
    if course.lower() == "Computer Science":
        return "Joao"
    elif course.lower() == "Excel":
        return "Maria"
    elif course.lower() == "Web Design":
        return "Sergio"
    elif course.lower() == "Chemistry Enginnering":
        return "Lucas"
    elif course.lower()=="Math":
        return "Lisa"
    elif course.lower()=="Data Science":
        return "Fernanda"
    else:
        return "Professor desconhecido"
