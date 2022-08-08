from tkinter import *
from tkinter import ttk as tt
from tkinter import BitmapImage
from tkinter import messagebox as msg
from tkinter import filedialog as fdl

import sqlite3 as sq3
from datetime import *
import base64 as b64
from PIL import Image as img


class Fucao(): 
    def variaveis(self):
        self.codigo = self.entry_cod.get()
        self.nome = self.entry_nome.get()
        self.cpf = self.entry_cpf.get()
        self.cnpj = self.entry_cnpj.get()
        self.telefone = self.entry_telefone.get()
        self.inscMunicipal = self.entry_Insc_Municipal.get()
        self.inscEstadual = self.entry_Insc_Estadual.get()
        self.browse_Files = ""

        self.nome = self.nome.lower().title().rstrip(" ").lstrip(" ").rstrip()

    def limpeza_comando(self):
        self.entry_cod.delete(0, END)
        self.entry_nome.delete(0, END)
        self.entry_cpf.delete(0, END)
        self.entry_cnpj.delete(0, END)
        self.entry_telefone.delete(0, END)
        self.entry_Insc_Municipal.delete(0, END)
        self.entry_Insc_Estadual.delete(0, END)

    def conecta_banco_d_dados(self):
        self.conecta = sq3.connect('clientes_banco_de_Dados')
        self.cursor = self.conecta.cursor()
    
    def desconecta_banco_d_dados(self):
        self.conecta.close()

    def monta_banco_em_tabela(self):
        self.conecta_banco_d_dados()
        
        #Cria tabela:
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes(
                cod INTEGER PRIMARY KEY,
                nome_cli CHAR(40) NOT NULL,
                cpf_cli CHAR(40),
                cnpj_cli CHAR(40),
                telefone_cli CHAR(40),
                insc_municipal CHAR(40),
                insc_estadual CHAR(40),
                note CHAR(50000000000000000),
                data CHAR(60000000000000000),
                logo_cli CHAR(200000000000000000)
            );
        ''')

        self.conecta.commit() 
        self.desconecta_banco_d_dados()

    def cliente_add(self):
        self.variaveis()

        c = 0

        if self.nome == "":
            ms = msg.showerror("Aviso de Erro: ", 'Para "cadastrar" cliente, deve possuir um nome válido!', icon = 'warning')
        else:
            if self.nome != "":
                self.nome = self.nome
                c = 1
        
        if self.codigo != "":
            ms = msg.showerror("Aviso de Erro: ", "Para cadastrar cliente, o campo de código deve está vazio!", icon = 'warning')
        else:
            self.codigo = self.codigo
            c = c+1

        if self.cpf != "":
            if self.cpf.isalpha():
                ms = msg.showerror("Aviso de Erro: ", "Para cadastrar cliente, o campo de CNPJ deve conter somente números!", icon = 'warning')
                self.cpf = ''
                c=0
            else:
                if len(str(self.cpf)) < 10+1:
                    print(len(str(self.entry_cpf.get())))
                    ms = msg.showerror("Aviso de Erro: ", "Para CADASTRAR cliente, o campo de CPF deve conter 11 digítos!", icon = 'warning')
                    self.cpf = ''
                    c =0
                else:
                    if len(str(self.cpf)) > 11:
                        print(len(str(self.entry_cpf.get())))
                        ms = msg.showerror("Aviso de Erro: ", "Para CADASTRAR cliente, o campo de CPF não deve ultrapassar  11 digítos!", icon = 'warning')
                        self.cpf = ''
                        c = 0
                    if len(str(self.cpf)) == 11:
                        self.cpf = self.cpf
                        c +=1
        if self.cnpj != "":
            if self.cnpj.isalpha():
                ms = msg.showerror("Aviso de Erro: ", "Para cadastrar cliente, o campo de CNPJ deve conter somente números!", icon = 'warning')
                c =0
            else:
                if len(str(self.cnpj)) < 14:
                    print(len(str(self.cnpj)))
                    ms = msg.showerror("Aviso de Erro: ", "Para CADASTRAR cliente, o campo de CNPJ deve conter 14 digítos!", icon = 'warning')
                    self.cnpj = ''
                    c =0
                else:
                    if len(str(self.cnpj)) > 14:
                        print(len(str(self.cnpj)))
                        ms = msg.showerror("Aviso de Erro: ", "Para CADASTRAR cliente, o campo de CNPJ não deve ultrapassar 14 digítos!", icon = 'warning')
                        self.cnpj = ''
                        c =0
                    if len(str(self.cnpj)) == 14:
                        self.cnpj = self.entry_cnpj.get()
                        c += 1
        if self.telefone != '':
            if self.telefone.isalpha():
                ms = msg.showerror("Aviso de Erro: ", "Para cadastrar cliente, o campo de telefone deve conter somente números!", icon = 'warning')
                self.telefone = ''
                c =0
            else:
                self.telefone = self.telefone
                c += 1
                     
        
        if c >= 2:         
            self.conecta_banco_d_dados()

            ms = msg.askquestion("Aviso: ", 'Deseja adicionar FOTO/LOGO do cliente?', icon = 'question')

            if ms == "yes":
                self.browseFiles()

            self.cursor.execute("""INSERT INTO clientes (nome_cli, cpf_cli, cnpj_cli, telefone_cli, insc_municipal, insc_estadual, logo_cli)
            VALUES (?,?,?,?,?,?,?)""", (self.nome, self.cpf, self.cnpj, self.telefone, self.inscMunicipal, self.inscEstadual, self.browse_Files))
            self.conecta.commit()

            self.desconecta_banco_d_dados()
            self.botao_insert()
        self.limpeza_comando()
        
    def botao_insert(self):
        self.planilha_contatos.delete(*self.planilha_contatos.get_children())
        self.conecta_banco_d_dados()
        
        lista = self.cursor.execute(""" SELECT cod, nome_cli, cpf_cli, cnpj_cli, telefone_cli, insc_municipal , insc_estadual FROM clientes
            ORDER BY cod ASC;""")
       
        for i in lista:
            self.planilha_contatos.insert("", END, values = i)
            
        self.desconecta_banco_d_dados()

    def double_click(self, event):
        self.limpeza_comando()

        self.planilha_contatos.selection()

        for n in self.planilha_contatos.selection():
            col1, col2, col3, col4, col5, col6, col7 = self.planilha_contatos.item(n, 'values')
            self.entry_cod.insert(END, col1)
            self.entry_nome.insert(END, col2)
            self.entry_cpf.insert(END, col3)
            self.entry_cnpj.insert(END, col4)
            self.entry_telefone.insert(END, col5)
            self.entry_Insc_Municipal.insert(END, col6)
            self.entry_Insc_Estadual.insert(END, col7)

    def delete_cliente(self):
        if self.entry_cod.get() == "":
            ms = msg.showerror("Aviso de Erro: ", "Para deletar cliente, deve possuir um código válido!", icon='warning')
        
        elif self.entry_cod.get().isalpha():
            ms = msg.showerror("Aviso de Erro: ", "Para deletar cliente, deve possuir um código válido!", icon='warning')

        elif self.entry_nome.get() == "":
            ms = msg.showerror("Aviso de Erro: ", "Para deletar cliente, deve possuir um nome válido!", icon = 'warning')
        
        elif self.entry_cpf.get().isalpha():
            ms =  msg.showerror("Aviso de Erro: ", 'Para deletar cliente, o campo de CPF deve conter somente números!', icon = 'warning')
       
        elif self.entry_cnpj.get().isalpha():
            ms = msg.showerror("Aviso de Erro: ", "Para deletar cliente, o campo de CNPJ deve conter somente números!", icon = 'warning')
        
        elif self.entry_telefone.get().isalpha():
            ms = msg.showerror("Aviso de Erro: ", "Para deletar cliente, o campo de telefone deve conter somente números!", icon = 'warning')
       
        else:
            self.conecta_banco_d_dados()
            self.variaveis()

            self.cursor.execute(""" DELETE FROM clientes WHERE cod = ?""", (self.codigo,))
            self.conecta.commit()
            self.desconecta_banco_d_dados()

            self.limpeza_comando()
            self.botao_insert()
        self.limpeza_comando()

    def alterar_cliente(self):
        self.variaveis()
            
        if self.entry_cod.get() == "":
            ms = msg.showerror("Aviso de Erro: ", 'Para "alterar" dados do cliente, deve possuir um código válido!', icon="warning")
       
        elif self.entry_cod.get().isalpha():
            ms = msg.showerror("Aviso de Erro: ", 'Para "alterar" dados do cliente, deve possuir um código válido!', icon='warning')

        elif self.entry_nome.get() == "":
            ms = msg.showerror("Aviso de Erro: ", 'Para "alterar" dados do cliente, deve possuir um nome válido!', icon = 'warning')
        
        elif self.entry_cpf.get().isalpha():
            ms =  msg.showerror("Aviso de Erro: ", 'Para "alterar" cliente, o campo de CPF deve conter somente números!', icon = 'warning')
        
        elif self.entry_cnpj.get().isalpha():
            ms = msg.showerror("Aviso de Erro: ", 'Para "alterar" dados do cliente, o campo de CNPJ deve conter somente números!', icon = 'warning')
        
        elif self.entry_telefone.get().isalpha():
            ms = msg.showerror("Aviso de Erro: ", "Para alterar cliente, o campo de telefone deve conter somente números!", icon = 'warning')
       
        else:
            ms = msg.askquestion("Aviso: ", 'Deseja atualizar FOTO/LOGO do cliente?', icon = 'question')
            if ms == 'yes':
                self.browseFiles()

            self.conecta_banco_d_dados()
            self.cursor.execute(""" UPDATE clientes SET nome_cli = ?, cpf_cli = ?, cnpj_cli = ?, telefone_cli = ?, insc_municipal = ? ,insc_estadual = ?, logo_cli = ?
            WHERE cod = ?""", 
            (self.nome, self.cpf, self.cnpj, self.telefone,
            self.inscMunicipal, self.inscEstadual, self.browse_Files,
            self.codigo))

            self.conecta.commit()
            self.desconecta_banco_d_dados()
            self.botao_insert()
            self.limpeza_comando()
        self.limpeza_comando()
    
    def buscar_cliente(self):
        self.conecta_banco_d_dados()

        self.planilha_contatos.delete(*self.planilha_contatos.get_children())

        self.entry_nome.insert(END, '%')
        nome = self.entry_nome.get()
        self.cursor.execute( """ SELECT cod, nome_cli, cpf_cli, cnpj_cli, telefone_cli FROM clientes
            WHERE nome_cli LIKE '%s' """% nome)
        
        busca_mome_Cli = self.cursor.fetchall()

        for i in busca_mome_Cli:
            self.planilha_contatos.insert("", END, values=i) 

        self.limpeza_comando()
        self.desconecta_banco_d_dados()    

    def buscar_cliente_pelo_Codigo(self):
        self.conecta_banco_d_dados()
        self.planilha_contatos.delete(*self.planilha_contatos.get_children())

        self.entry_cod.insert(END, '%')
        codigo = self.entry_cod.get()
        self.cursor.execute(
            """ SELECT cod, nome_cli, cpf_cli, cnpj_cli, telefone_cli FROM clientes
            WHERE cod LIKE '%s' """% codigo)
        
        busca_cod_Cli = self.cursor.fetchall()
        
        for i in busca_cod_Cli:
            self.planilha_contatos.insert("", END, values=i)
                
        self.limpeza_comando()
        self.desconecta_banco_d_dados() 

    def browseFiles(self):
        self.variaveis()

        if self.nome == "":
            msg.showerror("Conduta inesperada:".title(),
                        "Para adicionar FOTO ou LOGO do cliente, o campo de texto NOME/CODE não pode estar vazio.",
                        icon = 'warning')
            self.limpeza_comando()
        else:
            
            filename = fdl.askopenfilename(initialdir = "/", 
                                                title = "Selecione um Arquivo", 
                                                filetypes = (("Arquivos de Imagem", "*.jpg .png*"),("Arquivos JPG", "*.jpg*"),("Arquivos PNG", "*.png*"))) 
            
            print(f"File Opened: {filename}")

        if filename != "":
            image_search = img.open(filename)
            if image_search.height >= 500:
                msg.showinfo("Aviso:","Foto/logo não foi adicionada! Tamanho utrapassa 200X200 pixels", icon='warning')
                self.browse_Files = ""
                
            elif image_search.width >= 500:
                msg.showinfo("Aviso:","Foto/logo não foi adicionada! Tamanho utrapassa 200X200 pixels", icon='warning')
                self.browse_Files = ""
                
            elif image_search.width and image_search.height >= 500:
                msg.showinfo("Aviso:","Foto/logo não foi adicionada! Tamanho utrapassa 200X200 pixels", icon='warning')
                self.browse_Files = ""
                
            elif image_search.width <= 199:
                msg.showinfo("Aviso:","Foto/logo não foi adicionada! Tamanho não chega há 200X200 pixels", icon='warning')
                self.browse_Files = ""
                
            elif image_search.height <= 199:
                msg.showinfo("Aviso:","Foto/logo não foi adicionada! Tamanho não chega há 200X200 pixels", icon='warning')
                self.browse_Files = ""
                
            elif image_search.width and image_search.height <= 199:
                msg.showinfo("Aviso:","Foto/logo não foi adicionada! Tamanho não chega há 200X200 pixels", icon='warning')
                self.browse_Files = ""
                
            else:
                with open(filename, "rb") as image_file:
                    encoded_string = b64.b64encode(image_file.read())
                    msg.showinfo("Aviso:","Foto/logo adicionada com sucesso!", icon='info')
                    self.browse_Files = encoded_string
                    
        else:
            msg.showinfo("Aviso:","Foto/logo não foi adicionada!", icon='warning')
            self.browse_Files = ""
        print(self.browse_Files)
  
        