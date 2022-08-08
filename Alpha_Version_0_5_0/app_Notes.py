from tkinter import *
from tkinter import BitmapImage
from tkinter import messagebox as msg

from app_Function import *

color_background, color_frame = '#008080','#F0FFFF'
color_bord, color_label = '#836FFF','#F0FFFF'
color_buton_press = '#20B2AA'

class Anotações():
    def teste0(self, evt):
        self.entry_anotações.delete(0,END)
        self.value2=str((self.listbox.get(ANCHOR)))
        self.valor_list = self.value2
        self.entry_anotações.insert(END,self.valor_list)

    def variaveis2(self):
        self.cod2 = self.entry_cod2.get()
        self.anotaçoes = self.entry_anotações.get()

        self.anotaçoes = self.anotaçoes.lower().capitalize()

    def quebra_linha_line_breaking (self):
        self.variaveis2()

        s = f'{self.anotaçoes}!@#$'

        self.entry_anotações.delete(0, END)
        self.entry_anotações.insert(0, s)
        
    def deletar_dados(self):
        self.variaveis2()
        codigo = self.entry_cod2.get()

        if codigo == "":
            mensagem = msg.showwarning("Aviso de ERRO:", "para deletar uma anotação, você, deve digitar um código válido.")
        else:
            if codigo != "":
                self.conecta_banco_d_dados()
                self.cursor.execute( """ SELECT * FROM clientes WHERE cod LIKE '%s' """% codigo)

                tratamento = self.cursor.fetchall()

                for i in tratamento:
                    recolhendo_dados = i[7]
                    recolhendo_dados = str(recolhendo_dados).rstrip(" ").replace('None', "") # Recolhe os dados pré-tratados, ele já retiravalores None e substitui por um espaço.
                    recolhendo_dados2 = i[8]
                    recolhendo_dados2 = str(recolhendo_dados2).replace('None', "").rstrip(' ')
                self.desconecta_banco_d_dados()

                lista_de_anotações1 = recolhendo_dados
                lista_de_anotações1 = lista_de_anotações1.split("¢") # Converte os dados pré-tratados pra uma lista
                
                lista_de_anotações2 = recolhendo_dados2
                lista_de_anotações2 = lista_de_anotações2.split("¢")

                s = {""}
                lista_de_anotações_2 = [e for e in lista_de_anotações1 if e not in s] # Retira da lista os espaços em vazio que estavam como item
                lista_de_anotações_3 = [e for e in lista_de_anotações2 if e not in s]
                
                if self.anotaçoes == '':
                    mensagem = msg.showinfo('Aviso de ERRO:', 'Para "deletar" uma anotação, você, deve selecionar qual deseja deletar.')
                else:
                    if self.anotaçoes != '':
                        item_a_ser_apagado = self.valor_list
                        cont = 0
                        try:
                            localiza_item_a_ser_apagado = lista_de_anotações_2.index(item_a_ser_apagado)
                            cont = 5
                        except:
                            mensagem = msg.showinfo('Aviso de ERRO:', 'Para "deletar" uma anotação, você, deve selecionar qual deseja deletar.')
                        if cont == 5:
                            lista_de_anotações_2.remove(lista_de_anotações_2[localiza_item_a_ser_apagado])
                            recolhendo_dados_2 = "¢".join([str(a) for a in lista_de_anotações_2])

                            lista_de_anotações_3.remove(lista_de_anotações_3[localiza_item_a_ser_apagado])
                            recolhendo_dados_3 = "¢".join([str(a) for a in lista_de_anotações_3])
                            
                            self.conecta_banco_d_dados()
                            self.cursor.execute(""" UPDATE clientes SET note = ?, data = ? WHERE cod = ?""", (recolhendo_dados_2,recolhendo_dados_3,codigo))
                            self.conecta.commit()
                            self.desconecta_banco_d_dados()
                            cont, item_a_ser_apagado, i = 0,0,0
        self.listabox_limpa()                   

    def inserir_dados(self):
        self.variaveis2()
        self.conecta_banco_d_dados()
        codigo = self.entry_cod2.get()
        if codigo != '':
            self.cursor.execute( """ SELECT * FROM clientes
            WHERE cod LIKE '%s' """% codigo)
        
        tratamento = self.cursor.fetchall()

        for resultado in tratamento:
            recolhendo_dados = resultado[7]
            recolhendo_dados = str(recolhendo_dados).replace('None', '')
            recolhendo_dados2 = resultado[8]
            recolhendo_dados2 = str(recolhendo_dados2).replace('None', '')


        self.desconecta_banco_d_dados()

        if codigo == '':
            mensagem = msg.showinfo('Aviso:', 'Você deve "escrever" um Código valído!', icon = 'warning')
        else:
            if codigo != '':
                if recolhendo_dados in  '':
                    if recolhendo_dados2 == '' :
                        anotação = self.anotaçoes
                        data = datetime.today()
                        data = data.strftime('%d/%m/%Y %H:%M:%S')
                        if anotação != '':
                            anotação = f'{anotação}¢'
                            data = f'{data}¢'
                            self.conecta_banco_d_dados()
                            self.cursor.execute(""" UPDATE clientes SET note =?, data =? WHERE cod = ?""", (anotação, data, codigo))
                            self.conecta.commit()
                            self.desconecta_banco_d_dados()
                        else:
                            if anotação == "":
                                mensagem = msg.showinfo('Aviso:','Você deve "escrever" algo no campo Anotações!',icon = 'warning')
                else:
                    if recolhendo_dados != '':
                        if recolhendo_dados2 != '' :
                            anotação = self.anotaçoes
                            data = datetime.today()
                            data = data.strftime('%d/%m/%Y %H:%M:%S')
                            if anotação != "":
                                anotação = f"{recolhendo_dados}{anotação}¢"
                                data = f'{recolhendo_dados2}{data}¢'
                                self.conecta_banco_d_dados()
                                self.cursor.execute(""" UPDATE clientes SET note =?, data =? WHERE cod = ?""", (anotação, data, codigo))
                                self.conecta.commit()
                                self.desconecta_banco_d_dados()
                            else:
                                if anotação == "":
                                    mensagem = msg.showinfo('Aviso:', 'Você deve "escrever" algo no campo Anotações!', icon = 'warning')
            
        self.listabox_limpa()

    def listabox_alterar(self):
        self.variaveis2()
        codigo = self.entry_cod2.get()

        if codigo == '':
            mensagem = msg.showwarning("Aviso de ERRO:", "Você precisa digitar um código!".upper())
        else:
            if codigo != "":

                self.conecta_banco_d_dados()
                self.cursor.execute( """ SELECT * FROM clientes WHERE cod LIKE '%s' """% codigo)

                tratamento = self.cursor.fetchall()

                for i in tratamento:
                    recolhendo_dados = i[7]
                    recolhendo_dados = str(recolhendo_dados).rstrip(" ").replace('None', "") # Recolhe os dados pré-tratados, ele já retiravalores None e substitui por um espaço.
                    recolhendo_dados2 = i[8]
                    recolhendo_dados2 = str(recolhendo_dados2).rstrip(" ").replace('None', "")
                self.desconecta_banco_d_dados()

                lista_de_anotações = recolhendo_dados
                lista_de_anotações = lista_de_anotações.split("¢") # Converte os dados pré-tratados pra uma lista

                lista_de_anotações2 = recolhendo_dados2
                lista_de_anotações2 = lista_de_anotações2.split("¢")

                s = {""}
                lista_de_anotações_2 = [e for e in lista_de_anotações if e not in s] # Retira da lista os espaços em vazio que estavam como item
                lista_de_anotações_3 = [l for l in lista_de_anotações2 if l not in s]

                
                if self.anotaçoes != '':
                    items_alterando = self.valor_list
                    cont = 0

                    data = datetime.today()
                    data = data.strftime('%d/%m/%Y %H:%M:%S')

                    try:
                        pesquisando_items_alterando = lista_de_anotações_2.index(items_alterando)
                        print(pesquisando_items_alterando)
                        cont = 5
                    except:
                        mensagem = msg.showinfo("Aviso:", 'Para "alterar" dados, deve selecionar um válido!'.upper(), icon = 'warning')
                    
                    ss = pesquisando_items_alterando
                    pesquisando_items_alterando2 = ss
                    print(pesquisando_items_alterando2)
                    
                    if cont == 5:
                        lista_de_anotações_2[pesquisando_items_alterando] = self.anotaçoes
                        recolhendo_dados_2 = "¢".join([str(d) for d in lista_de_anotações_2]) 

                        lista_de_anotações_3[pesquisando_items_alterando2] = data
                        print(lista_de_anotações_3)
                        recolhendo_dados_3 = "¢".join([str(d) for d in lista_de_anotações_3])
                        print(recolhendo_dados_3) 

                        self.conecta_banco_d_dados()
                        self.cursor.execute(""" UPDATE clientes SET note = ?, data =? WHERE cod = ?""", (recolhendo_dados_2, recolhendo_dados_3,codigo))
                        self.conecta.commit()
                        self.desconecta_banco_d_dados()

                        cont, items_alterando, data = 0,0,0

                else:
                    if self.anotaçoes == '':
                        mensagem = msg.showinfo("Aviso:", 'Para "alterar" dados, deve selecionar um!'.upper(), icon = 'warning')
                

                self.listabox_limpa()
    
    def listabox_limpa(self):
        self.limpa_1 = self.entry_cod2.delete(0, END)
        self.limpa_2 = self.entry_anotações.delete(0, END)
        self.limpa_3 = self.listbox.delete(0, END)

    def listabox_busca(self):
        self.variaveis2()
        
        self.listbox.delete(0,END)
        codigo0 = self.entry_cod2.get()
        codigo0 = codigo0

        if self.cod2.isnumeric() and self.cod2 != "":
            self.conecta_banco_d_dados()

            self.entry_cod2.insert(END, "%")
            #self.entry_anotações.insert(END, "%")

            self.cursor.execute(
                """ SELECT note FROM clientes
                WHERE cod LIKE '%s' """% codigo0)

            tratamento = self.cursor.fetchall()

            for resultado in tratamento:
                resultado = str(resultado)
                resultado=resultado.replace("[", "")
                resultado=resultado.replace("]", "")
                resultado=resultado.replace("'","")
                resultado=resultado.replace(")", "")
                resultado=resultado.replace("(", "")
                resultado=resultado.rstrip(",")
                resultado=resultado.rstrip(" ")
                resultado=resultado.lstrip(" ")
                s = resultado.split("¢")
                ss = s[-1]
                if ss == '':
                    s.remove(ss)
                for xwz in s:
                    self.listbox.insert(END, xwz)
            
            self.desconecta_banco_d_dados()
            
            self.listbox.bind('<<ListboxSelect>>',self.teste0)
            
            if self.entry_cod2.get() == '0%':
                for x in range(0, 6+4):
                    self.listbox.insert(END, f"ERRO {x+1:2}, você deve aderir um código válido!")     
        else:
            if self.cod2.isalpha():
                for x in range(0, 6+4):
                    self.listbox.insert(END, f"ERRO {x+1:2}, você deve aderir um código!")
            elif self.entry_cod2.get() == '':
                for x in range(0, 6+4):
                    self.listbox.insert(END, f"ERRO {x+1:2}, você deve aderir um código válido!")
        self.entry_cod2.delete(0,END)
        self.entry_cod2.insert(END, codigo0)

    def listabox(self):
        # LISTA BOX
        self.listbox = Listbox(self.frame3) 
        self.listbox.pack(side = BOTTOM, fill = BOTH) 
        self.listbox.place(rely=0.30, relx=0.25, relheight=0.50, relwidth=0.70)
        self.listbox.configure(bg=color_buton_press, fg="white", font=('arial',11,'bold'), highlightbackground=color_bord, highlightthickness=2, selectbackground=color_buton_press)

        # scrol:
        self.scrol_listabox = Scrollbar(self.frame3, orient='vertical')
        self.a = self.listbox
        self.a.configure(yscrollcommand=self.scrol_listabox.set)
        self.scrol_listabox.place(rely=0.30, relx=0.95, relwidth=0.035, relheight=0.5)
        self.scrol_listabox.config(command=self.a.yview)

        self.scrol_listabox2 = Scrollbar(self.frame3, orient='horizontal')
        self.b = self.listbox
        self.b.configure(xscrollcommand=self.scrol_listabox2.set)
        self.scrol_listabox2.place(rely=0.805, relx=0.25, relwidth=0.70, relheight=0.05)
        self.scrol_listabox2.config(command=self.b.xview)

    def janela_anotaçoes(self):
        # CRIADO NOVA JANELA
        self.ventana_janela_2 = Toplevel()
        self.ventana_janela_2.title('anotações de cliente'.title())
        self.ventana_janela_2.configure(background= color_background)
        self.ventana_janela_2.geometry('400x301')
        self.ventana_janela_2.resizable(False,False)
        """self.ventana_janela_2.maxsize(width=380, height=400)
        self.ventana_janela_2.minsize(width=320, height=300)"""
        self.ventana_janela_2.transient(self.ventana_janela)
        self.ventana_janela_2.focus_force() #impede de manuseiar a janela primária, coloca a nova sempre na frente
        self.ventana_janela_2.grab_set() #impede de anotar ou utilizar widgets da janela primária
        
        # CRIANDO UM NOVO FRAME
        self.frame3 = Frame(self.ventana_janela_2, bd= 4, bg=color_frame, highlightbackground=color_bord, highlightthickness=2)
        self.frame3.place(relx=0.01, rely=0.02, relwidth=0.98, relheight= 0.95)

        #CRIANDO BOTÕES NA NOVA JANELA
        self.botao_buscar_2= Button(self.frame3, text="buscar".title(), bg=color_background, fg='white', font=('verdana', 9), command=self.listabox_busca, activebackground=color_buton_press, activeforeground='white')
        self.botao_buscar_2.place(rely=0.24, relx=0.03, relwidth=0.13, relheight=0.12)
        
        self.botao_limpar_2= Button(self.frame3, text="limpar".title(), bg=color_background, fg='white', font=('verdana', 9), command=self.listabox_limpa, activebackground=color_buton_press, activeforeground='white')
        self.botao_limpar_2.place(relx=0.03, rely=0.85, relwidth=0.13, relheight=0.12)

        self.botao_novo_2= Button(self.frame3, text="novo".title(), bg=color_background, fg='white', font=('verdana', 9), command=self.inserir_dados, activebackground=color_buton_press, activeforeground='white')
        self.botao_novo_2.place(rely=0.39, relx=0.03, relwidth=0.13, relheight=0.12)

        self.botao_apagar_2= Button(self.frame3, text="apagar".title(), bg=color_background, fg='white', font=('verdana', 9), command=self.deletar_dados ,activebackground=color_buton_press, activeforeground='white')
        self.botao_apagar_2.place(rely=0.544, relx=0.03, relwidth=0.13, relheight=0.12)

        self.botao_alterar_2= Button(self.frame3, text="alterar".title(), bg=color_background, fg='white', font=('verdana', 9), command=self.listabox_alterar, activebackground=color_buton_press, activeforeground='white')
        self.botao_alterar_2.place(rely=0.693, relx=0.03, relwidth=0.13, relheight=0.12)

        self.botao_enter= Button(self.frame3, text="quebra linha".capitalize(), bg=color_frame, fg='gray', font=('verdana', 9), command=self.quebra_linha_line_breaking, activebackground=color_buton_press, activeforeground='blue')
        self.botao_enter.place(rely=0.001, relx=0.70, relwidth=0.25, relheight=0.14)

        # LABEL E ENTRY DA NOVA JANELA
        self.label_codigo2 = Label(self.frame3, text="código".upper(), bg=color_frame, fg= color_background, font=('arial',10,'bold'))
        self.label_codigo2.place(rely=0.01, relx=0.03)
        
        self.entry_cod2 = Entry(self.frame3, bg= color_label)
        self.entry_cod2.place(rely=0.12, relx=0.03, relheight=0.094, relwidth=0.15)

        self.label_anotações = Label(self.frame3, text="anotações".upper(), bg=color_frame, fg= color_background, font=('arial',10,'bold'))
        self.label_anotações.place(rely=0.01, relx=0.25)
    
        self.entry_anotações = Entry(self.frame3, bg= color_label)
        self.entry_anotações.place(rely=0.12, relx=0.25, relheight=0.10, relwidth=0.70)
        
        self.listabox()
    