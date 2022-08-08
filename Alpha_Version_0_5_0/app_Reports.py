from tkinter import *
from tkinter import BitmapImage
from tkinter import messagebox as msg
import webbrowser as web

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT

color_background, color_frame = '#008080','#F0FFFF'
color_bord, color_label = '#836FFF','#F0FFFF'
color_buton_press = '#20B2AA'

class Relatorios():  
    def test1(self, *args):
        self.menu_seleção = str(self.variavel_d_armazenamento.get())

    def test0(self, evt):
        self.value=str((self.listbox2.get(ANCHOR)))

    def Quit2(self): 
        ms2 = msg.askquestion("Aviso: ", 'Deseja sair sem "baixar" os dados?'.capitalize(), icon = 'question')
        if ms2 == 'yes':
         self.ventana_janela_3.destroy()

    def menubox(self):
       self.menu_listas = ["GERAR EM PDF (.pdf)","GERAR EM DOC (.doc)","GERAR PLANILHA (.xlsx)"]

       self.variavel_d_armazenamento = StringVar(self.ventana_janela_3)
       self.variavel_d_armazenamento.set(self.menu_listas[0])

       self.menu_listas_formado = OptionMenu(self.ventana_janela_3, self.variavel_d_armazenamento,*self.menu_listas)
       self.menu_listas_formado.config(width=119,font=('arial',11,'bold'))
       self.menu_listas_formado.pack(side='top')
       self.menu_listas_formado.place(rely=0.09, relx=0.25, relheight=0.10, relwidth=0.70)

       self.variavel_d_armazenamento.trace("w",self.test1)

    def listabox2(self):
        # LISTA BOX
        self.listbox2 = Listbox(self.frame4) 
        self.listbox2.pack(side = BOTTOM, fill = BOTH) 
        self.listbox2.place(rely=0.30, relx=0.03, relheight=0.50, relwidth=0.90)
        self.listbox2.configure(bg=color_buton_press, fg="white", font=('arial',11,'bold'), highlightbackground=color_bord, highlightthickness=2, selectbackground=color_buton_press)

        # scrol:
        self.scrol_listabox2 = Scrollbar(self.frame4, orient='vertical')
        self.a = self.listbox2
        self.a.configure(yscrollcommand=self.scrol_listabox2.set)
        self.scrol_listabox2.place(rely=0.30, relx=0.93, relwidth=0.035, relheight=0.5)
        self.scrol_listabox2.config(command=self.a.yview)

        self.scrol_listabox3 = Scrollbar(self.frame4, orient='horizontal')
        self.b = self.listbox2
        self.b.configure(xscrollcommand=self.scrol_listabox3.set)
        self.scrol_listabox3.place(rely=0.805, relx=0.03, relwidth=0.90, relheight=0.05)
        self.scrol_listabox3.config(command=self.b.xview)
    
    def config_PDF_or_TABLE(self):
        self.test1()

        clients_data =self.value.split(",")

        a_code_cliente,b_name_client,c_number_CPF,d_number_CNPJ,e_phone_number,d_number_INSC_MUNICIPAL,g_number_INSC_ESTADUAL = str(clients_data[0]), str(clients_data[1]), str(clients_data[2]), str(clients_data[3]), str(clients_data[4]), str(clients_data[5]), str(clients_data[6])
        b_name_client,c_number_CPF,d_number_CNPJ,e_phone_number,d_number_INSC_MUNICIPAL,g_number_INSC_ESTADUAL = b_name_client.replace('"',"").replace("'",''),c_number_CPF.replace("'", "").replace('"',""),d_number_CNPJ.replace("'","").replace('"',""),e_phone_number.replace("'","").replace('"',""), d_number_INSC_MUNICIPAL.replace("'"," ").rstrip(' ').lstrip(' '), g_number_INSC_ESTADUAL.replace("'"," ").rstrip(' ').lstrip(" ")
        h_logo = str(clients_data[9])
        
        l,h = str(clients_data[7]).replace("'"," ").lstrip(" ").rstrip(" "), str(clients_data[8]).replace("'"," ").lstrip(" ").rstrip(" ")
        ss_clean_spaces, l, h = {""},l.split("¢"),h.split("¢")

        ll, hh = [e for e in l if e not in ss_clean_spaces], [y for y in h if y not in ss_clean_spaces]

        dicionario_tabela2 = dict(zip(ll,hh))
        print(f"{a_code_cliente}\n{b_name_client} {c_number_CPF} {d_number_CNPJ} {e_phone_number} {d_number_INSC_MUNICIPAL}\n eu sou o g: {g_number_INSC_ESTADUAL}\n{l}\n{h}\nEu sou a logo do cliente: {h_logo}")
        
        if self.menu_seleção == self.menu_listas[0]:

            self.cordenado = b_name_client.split(" ")
            self.cordenado.remove(self.cordenado[0])
            print(self.cordenado)

            volor, contador = len(self.cordenado), False

            if volor >= 3:
                contador = True

            if contador == True:
                if len(self.cordenado) <= 5:

                    database_clean=str(b_name_client)
                    database_clean=database_clean.replace("[", "")
                    database_clean=database_clean.replace("]", "")
                    database_clean=database_clean.replace(",", "")
                    database_clean=database_clean.lstrip("'")
                    database_clean=database_clean.rstrip("'")
                    database_clean=database_clean.rstrip(" ")
                    database_clean=database_clean.lstrip(" ")

                    g, elemente, data,  ficha, ficha1 = database_clean, [], 0, str('ficha do cliente'), str('Anotações do Cliente')

                    style,  style1 = ParagraphStyle(
                        'heading1',
                       fontName = 'Helvetica-Bold',
                       fontSize = 20,
                       textColor = colors.black,
                       leading = 20,
                       alignment=TA_CENTER,
                       allowOrphans = 0,
                       allowWidows = 1), ParagraphStyle(
                        'heading1',
                       fontName = 'Helvetica-Bold',
                       fontSize = 15,
                       textColor = colors.black,
                       leading = 20,
                       alignment=TA_LEFT,
                       allowOrphans = 0,
                       allowWidows = 1)

                    data = [['\n'],
                        ['código do cliente:'.capitalize(), a_code_cliente],
                        ['nome do cliente:'.capitalize(), g], 
                        ['telefone:'.capitalize(), e_phone_number.lstrip(" ")], 
                        ['cpf:'.upper(), c_number_CPF.lstrip(" ")], 
                        ['cnpj:'.upper(), d_number_CNPJ.lstrip(" ")],
                        ['INSC. Municipal:', d_number_INSC_MUNICIPAL.lstrip(" ")],
                        ['INSC. Estadual:', g_number_INSC_ESTADUAL.lstrip(" ")],
                        ['\n']
                    ]
                                   
                    t=Table(data, colWidths=[220,220])
                    t.setStyle(TableStyle([
                                    ('ALIGN',(1,1),(-3,-3),'RIGHT'),
                                    ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                                    ('TEXTCOLOR',(0,0),(1,-1),colors.black),
                                    ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
                                    ('FONTSIZE', (0, 0), (1, -1), 12.5)
                                ]))

                    s = Paragraph(f"{ficha}\n".title(), style)

                    elemente.append(s)
                    elemente.append(t)

                    s = Paragraph(f"{ficha1}\n\n", style1)
                    elemente.append(s)
                    
                    data.clear()
                    data.append("\n")
                    
                    fofoca,fofoca2,fofoca3 =0,[],[]
    
                    for nota, datas in dicionario_tabela2.items():
                        nota,datas = nota.replace('!@#$','<br />\n'),datas
                        fofoca3.append(nota)
                        fofoca2.append(datas)
                    fofoca =dict(zip(fofoca3,fofoca2))
                        
                    print(fofoca)  

                    for nota, datas in fofoca.items():
                        nota = nota.replace('<br />', '')
                        data.append([nota, datas])
                   
                    t= Table(data, colWidths=[250,250])
                    t.setStyle(TableStyle([
                                        ('ALIGN',(1,1),(-3,-3),'RIGHT'),
                                        ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                                        ('TEXTCOLOR',(0,0),(1,-1),colors.black),
                                        ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
                                        ('FONTSIZE', (0, 0), (1, -1), 12.5)
                                ]))
                    elemente.append(t)
                   
                    self.z = f"cliente_{a_code_cliente}_{g}.pdf".replace(" ","_")
                    
                    self.c = SimpleDocTemplate(self.z,
                                                pagesize=A4,
                                                title=f"client_{a_code_cliente}_{g}.pdf".replace(" ","_"),
                                                author='ANAMA-ITÁ Project',
                                                creator="By Saulo Ferro Maciel",
                                                subject=f"Ficha do cliente {g} Customer File",
                                                keywords=f'Client {g}',
                                                producer='Project is using: Reportlab Library')
                    self.c.build(elemente)
               
                if volor <= 3:   
                    menssage = msg.askquestion("Aviso: ", f'{str("Deseja continuar?").upper()} O  cliente {b_name_client[1]} não possui 02 sobrenomes cadastrados', icon = 'question')
                    if menssage == 'yes':
                        menssage = msg.showinfo("Aviso:".upper(), f'Processo finalizado ...', icon='warning')
                        database_clean=str(b_name_client)
                        database_clean=database_clean.replace("[", "")
                        database_clean=database_clean.replace("]", "")
                        database_clean=database_clean.replace(",", "")
                        database_clean=database_clean.lstrip("'")
                        database_clean=database_clean.rstrip("'")
                        database_clean=database_clean.rstrip(" ")
                        database_clean=database_clean.lstrip(" ")

                        g, elemente, data,  ficha, ficha1 = database_clean, [], 0, str('ficha do cliente'), str('Anotações do Cliente')

                        style,  style1 = ParagraphStyle(
                                'heading1',
                            fontName = 'Helvetica-Bold',
                            fontSize = 20,
                            textColor = colors.black,
                            leading = 20,
                            alignment=TA_CENTER,
                            allowOrphans = 0,
                            allowWidows = 1), ParagraphStyle(
                                'heading1',
                            fontName = 'Helvetica-Bold',
                            fontSize = 15,
                            textColor = colors.black,
                            leading = 20,
                            alignment=TA_LEFT,
                            allowOrphans = 0,
                            allowWidows = 1)

                        data = [['\n'],
                            ['código do cliente:'.capitalize(), a_code_cliente],
                            ['nome do cliente:'.capitalize(), g], 
                            ['telefone:'.capitalize(), e_phone_number.lstrip(" ")], 
                            ['cpf:'.upper(), c_number_CPF.lstrip(" ")], 
                            ['cnpj:'.upper(), d_number_CNPJ.lstrip(" ")],
                            ['INSC. Municipal:', d_number_INSC_MUNICIPAL.lstrip(" ")],
                            ['INSC. Estadual:', g_number_INSC_ESTADUAL.lstrip(" ")],
                            ['\n']
                        ]
                        
                        t=Table(data, colWidths=[220,220])
                        t.setStyle(TableStyle([
                                        ('ALIGN',(1,1),(-3,-3),'RIGHT'),
                                        ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                                        ('TEXTCOLOR',(0,0),(1,-1),colors.black),
                                        ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
                                        ('FONTSIZE', (0, 0), (1, -1), 12.5)
                                    ]))

                        s = Paragraph(f"{ficha}\n".title(), style)

                        elemente.append(s)
                        elemente.append(t)

                        s = Paragraph(f"{ficha1}\n\n", style1)
                        elemente.append(s)
                        
                        data.clear()
                        data.append("\n")
                        
                        fofoca,fofoca2,fofoca3 =0,[],[]
        
                        for nota, datas in dicionario_tabela2.items():
                            nota,datas = nota.replace('!@#$','<br />\n'),datas
                            fofoca3.append(nota)
                            fofoca2.append(datas)
                        fofoca =dict(zip(fofoca3,fofoca2))
                            
                        print(fofoca)  

                        for nota, datas in fofoca.items():
                            nota = nota.replace('<br />', '')
                            data.append([nota, datas])
                    
                        t= Table(data, colWidths=[250,250])
                        t.setStyle(TableStyle([
                                            ('ALIGN',(1,1),(-3,-3),'RIGHT'),
                                            ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                                            ('TEXTCOLOR',(0,0),(1,-1),colors.black),
                                            ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
                                            ('FONTSIZE', (0, 0), (1, -1), 12.5)
                                    ]))
                        elemente.append(t)
                    
                        self.z = f"cliente_{a_code_cliente}_{g}.pdf".replace(" ","_")
                        
                        self.c = SimpleDocTemplate(self.z,
                                                    pagesize=A4,
                                                    title=f"client_{a_code_cliente}_{g}.pdf".replace(" ","_"),
                                                    author='ANAMA-ITÁ Project',
                                                    creator="By Saulo Ferro Maciel",
                                                    subject=f"Ficha do cliente {g} Customer File",
                                                    keywords=f'Client {g}',
                                                    producer='Project is using: Reportlab Library')
                        self.c.build(elemente)
                   
                    else:
                        if menssage == 'no':
                            menssage = msg.showinfo("Aviso:".upper(), f'Processo {"encerrado".upper()} ...', icon='warning')

        if self.menu_seleção == self.menu_listas[1]:

            self.cordenado = b_name_client.split(" ")
            self.cordenado.remove(self.cordenado[0])

            volor, contador = len(self.cordenado), False

            if volor >= 3:
                contador = True

            if contador == True:
                if len(self.cordenado) <= 5:

                    database_clean=str(b_name_client)
                    database_clean=database_clean.replace("[", "")
                    database_clean=database_clean.replace("]", "")
                    database_clean=database_clean.replace(",", "")
                    database_clean=database_clean.lstrip("'")
                    database_clean=database_clean.rstrip("'")
                    database_clean=database_clean.rstrip(" ")
                    database_clean=database_clean.lstrip(" ")

                    g, elemente, data,  ficha, ficha1 = database_clean, [], 0, str('ficha do cliente'), str('Anotações do Cliente')

                    style,  style1 = ParagraphStyle(
                        'heading1',
                        fontName = 'Helvetica-Bold',
                        fontSize = 20,
                        textColor = colors.black,
                        leading = 20,
                        alignment=TA_LEFT,
                        allowOrphans = 0,
                        allowWidows = 1), ParagraphStyle(
                        'heading1',
                        fontName = 'Helvetica-Bold',
                        fontSize = 15,
                        textColor = colors.black,
                        leading = 20,
                        alignment=TA_LEFT,
                        allowOrphans = 0,
                        allowWidows = 1)
                    data = [['\n'],
                        ['código do cliente:'.capitalize(), a_code_cliente],
                        ['nome do cliente:'.capitalize(), g], 
                        ['telefone:'.capitalize(), e_phone_number.lstrip(" ")], 
                        ['cpf:'.upper(), c_number_CPF.lstrip(" ")], 
                        ['cnpj:'.upper(), d_number_CNPJ.lstrip(" ")],
                        ['INSC. Municipal:', d_number_INSC_MUNICIPAL.lstrip(" ")],
                        ['INSC. Estadual:', g_number_INSC_ESTADUAL.lstrip(" ")],
                        ['\n']
                    ]
                    
                    t=Table(data, colWidths=[220,220])
                    t.setStyle(TableStyle([
                                    ('ALIGN',(1,1),(-3,-3),'RIGHT'),
                                    ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                                    ('TEXTCOLOR',(0,0),(1,-1),colors.black),
                                    ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
                                    ('FONTSIZE', (0, 0), (1, -1), 12.5)
                                ]))

                    s = Paragraph(f"{ficha}\n".title(), style)

                    elemente.append(s)
                    elemente.append(t)

                    s = Paragraph(f"{ficha1}\n\n", style1)
                    elemente.append(s)
                    
                    data.clear()
                    data.append("\n")
                    
                    fofoca,fofoca2,fofoca3 =0,[],[]

                    for nota, datas in dicionario_tabela2.items():
                        nota,datas = nota.replace('!@#$','<br />\n'),datas
                        fofoca3.append(nota)
                        fofoca2.append(datas)
                    fofoca =dict(zip(fofoca3,fofoca2))
                        
                    print(fofoca)  

                    for nota, datas in fofoca.items():
                        nota = nota.replace('<br />', '')
                        data.append([nota, datas])
                    
                    t= Table(data, colWidths=[250,250])
                    t.setStyle(TableStyle([
                                        ('ALIGN',(1,1),(-3,-3),'RIGHT'),
                                        ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                                        ('TEXTCOLOR',(0,0),(1,-1),colors.black),
                                        ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
                                        ('FONTSIZE', (0, 0), (1, -1), 12.5)
                                ]))
                    elemente.append(t)
                    
                    self.z = f"cliente_{a_code_cliente}_{g}.doc".replace(" ","_")
                    
                    self.c = SimpleDocTemplate(self.z,
                                                pagesize=A4,
                                                title=f"client_{a_code_cliente}_{g}.pdf".replace(" ","_"),
                                                author='ANAMA-ITÁ Project',
                                                creator="By Saulo Ferro Maciel",
                                                subject=f"Ficha do cliente {g} Customer File",
                                                keywords=f'Client {g}',
                                                producer='Project is using: Reportlab Library')
                    self.c.build(elemente) 
                
                if volor <= 3:   
                    menssage = msg.askquestion("Aviso: ", f'{str("Deseja continuar?").upper()} O  cliente {b_name_client[1]} não possui 02 sobrenomes cadastrados', icon = 'question')
                    if menssage == 'yes':
                        menssage = msg.showinfo("Aviso:".upper(), f'Processo finalizado ...', icon='warning')
                        database_clean=str(b_name_client)
                        database_clean=database_clean.replace("[", "")
                        database_clean=database_clean.replace("]", "")
                        database_clean=database_clean.replace(",", "")
                        database_clean=database_clean.lstrip("'")
                        database_clean=database_clean.rstrip("'")
                        database_clean=database_clean.rstrip(" ")
                        database_clean=database_clean.lstrip(" ")

                        g, elemente, data,  ficha, ficha1 = database_clean, [], 0, str('ficha do cliente'), str('Anotações do Cliente')

                        style,  style1 = ParagraphStyle(
                                'heading1',
                            fontName = 'Helvetica-Bold',
                            fontSize = 20,
                            textColor = colors.black,
                            leading = 20,
                            alignment=TA_LEFT,
                            allowOrphans = 0,
                            allowWidows = 1), ParagraphStyle(
                                'heading1',
                            fontName = 'Helvetica-Bold',
                            fontSize = 15,
                            textColor = colors.black,
                            leading = 20,
                            alignment=TA_LEFT,
                            allowOrphans = 0,
                            allowWidows = 1)

                        data = [['\n'],
                            ['código do cliente:'.capitalize(), a_code_cliente],
                            ['nome do cliente:'.capitalize(), g], 
                            ['telefone:'.capitalize(), e_phone_number.lstrip(" ")], 
                            ['cpf:'.upper(), c_number_CPF.lstrip(" ")], 
                            ['cnpj:'.upper(), d_number_CNPJ.lstrip(" ")],
                            ['INSC. Municipal:', d_number_INSC_MUNICIPAL.lstrip(" ")],
                            ['INSC. Estadual:', g_number_INSC_ESTADUAL.lstrip(" ")],
                            ['\n']
                        ]

                        t=Table(data, colWidths=[220,220])
                        t.setStyle(TableStyle([
                                        ('ALIGN',(1,1),(-3,-3),'RIGHT'),
                                        ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                                        ('TEXTCOLOR',(0,0),(1,-1),colors.black),
                                        ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
                                        ('FONTSIZE', (0, 0), (1, -1), 12.5)
                                    ]))

                        s = Paragraph(f"{ficha}\n".title(), style)

                        elemente.append(s)
                        elemente.append(t)

                        s = Paragraph(f"{ficha1}\n\n", style1)
                        elemente.append(s)
                        
                        data.clear()
                        data.append("\n")
                        
                        fofoca,fofoca2,fofoca3 =0,[],[]
        
                        for nota, datas in dicionario_tabela2.items():
                            nota,datas = nota.replace('!@#$','<br />\n'),datas
                            fofoca3.append(nota)
                            fofoca2.append(datas)
                        fofoca =dict(zip(fofoca3,fofoca2))
                            
                        print(fofoca)  

                        for nota, datas in fofoca.items():
                            nota = nota.replace('<br />', '')
                            data.append([nota, datas])
                    
                        t= Table(data, colWidths=[250,250])
                        t.setStyle(TableStyle([
                                            ('ALIGN',(1,1),(-3,-3),'RIGHT'),
                                            ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                                            ('TEXTCOLOR',(0,0),(1,-1),colors.black),
                                            ('FONT', (0,0), (-1,0), 'Helvetica-Bold'),
                                            ('FONTSIZE', (0, 0), (1, -1), 12.5)
                                    ]))
                        elemente.append(t)
                    
                        self.z = f"cliente_{a_code_cliente}_{g}.doc".replace(" ","_")
                        
                        self.c = SimpleDocTemplate(self.z,
                                                    pagesize=A4,
                                                    title=f"client_{a_code_cliente}_{g}.pdf".replace(" ","_"),
                                                    author='ANAMA-ITÁ Project',
                                                    creator="By Saulo Ferro Maciel",
                                                    subject=f"Ficha do cliente {g} Customer File",
                                                    keywords=f'Client {g}',
                                                    producer='Project is using: Reportlab Library')
                        self.c.build(elemente)
                    
                    else:
                        if menssage == 'no':
                            menssage = msg.showinfo("Aviso:".upper(), f'Processo {"encerrado".upper()} ...', icon='warning')

            """guy = f"file:///home/jack/'Área de Trabalho'/estudoPython/tkinter/{self.z}"
            web.open(f"{guy}")"""

    def gera_relatorio_cliente(self):
        self.contador = 0
        if self.entry_cod3.get() != "":
            self.contador = 5

        self.listbox2.delete(0, END)
        cd = self.entry_cod3.get()

        if self.contador == 5:
            self.conecta_banco_d_dados()

            self.entry_cod3.insert(END, "%")

            codigo = self.entry_cod3.get()
            self.cursor.execute( """ SELECT * FROM clientes WHERE cod LIKE '%s' """% codigo)
            ddd = self.cursor.fetchall()
            dd = list(t for t in ddd)
            self.desconecta_banco_d_dados()

            if self.entry_cod3.get() == '0%':
                for x in range(0, 6+4):
                    self.listbox2.insert(END, f"ERRO {x+1:2}, VOCÊ DEVE ADERIR UM CÓDIGO válido!".upper())
            else:
                for i in dd: 
                    s = str(i)
                    s = s.replace("/'","").replace("(", "").replace(")", "")
                    self.listbox2.insert(END, f'{s:2}')
            self.listbox2.bind('<<ListboxSelect>>',self.test0)
            self.contador = 0        
        else:
            if self.contador != 5:
                ms = msg.showwarning("Aviso: ", 'Para "baixar" dados do cliente, deve possuir código e nome válidos!', icon = 'warning')
        self.entry_cod3.delete(0, END)
        self.entry_cod3.insert(END, cd)
    
    def final_relatorio(self):
         # CRIADO NOVA JANELA
        self.ventana_janela_3 = Toplevel()
        self.ventana_janela_3.title("gerar Ficha do cliente".title())
        self.ventana_janela_3.configure(background= color_background)
        self.ventana_janela_3.geometry('400x301')
        self.ventana_janela_3.resizable(False,False)
        """self.ventana_janela_2.maxsize(width=380, height=400)
        self.ventana_janela_2.minsize(width=320, height=300)"""
        self.ventana_janela_3.transient(self.ventana_janela)
        self.ventana_janela_3.focus_force() #impede de manuseiar a janela primária, coloca a nova sempre na frente
        self.ventana_janela_3.grab_set() #impede de anotar ou utilizar widgets da janela primária
        
        # CRIANDO UM NOVO FRAME
        self.frame4 = Frame(self.ventana_janela_3, bd= 4, bg=color_frame, highlightbackground=color_bord, highlightthickness=2)
        self.frame4.place(relx=0.01, rely=0.02, relwidth=0.98, relheight= 0.95)

        self.label_codigo3 = Label(self.frame4, text="código".upper(), bg=color_frame, fg= color_background, font=('arial',10,'bold'))
        self.label_codigo3.place(rely=0.01, relx=0.03)
        
        self.entry_cod3 = Entry(self.frame4, bg= color_label)
        self.entry_cod3.place(rely=0.09, relx=0.03, relheight=0.094, relwidth=0.15)

        self.botao_buscar_10= Button(self.frame4, text="buscar".title(), bg=color_background, fg='white', font=('verdana', 9), command=self.gera_relatorio_cliente, activebackground=color_buton_press, activeforeground='white')
        self.botao_buscar_10.place(rely=0.87, relx=0.03, relwidth=0.15, relheight=0.14)

        self.botao_finalizar= Button(self.frame4, text="finalizar".title(), bg=color_background, fg='white', font=('verdana', 9), command=self.config_PDF_or_TABLE, activebackground=color_buton_press, activeforeground='white')
        self.botao_finalizar.place(rely=0.87, relx=0.6, relwidth=0.15, relheight=0.14)

        self.botao_cancelar= Button(self.frame4, text="cancelar".title(), bg=color_background, fg='white', font=('verdana', 9), command=self.Quit2, activebackground=color_buton_press, activeforeground='white')
        self.botao_cancelar.place(rely=0.87, relx=0.78, relwidth=0.15, relheight=0.14)

        self.listabox2()
        self.menubox()
