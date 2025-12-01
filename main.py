arquivo_banco = "banco.txt"

def criar_arquivo():
    try:
        open(arquivo_banco, "x").close()
    except:
        pass


def ler_banco():
    dados = []
    try:
        with open(arquivo_banco, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha != "":
                    partes = linha.split("|")
                    dados.append(partes)
    except:
        pass
    return dados


def salvar_banco(lista):
    with open(arquivo_banco, "w", encoding="utf-8") as f:
        for item in lista:
            f.write("|".join(item) + "\n")


def gerar_id():
    dados = ler_banco()
    if len(dados) == 0:
        return "1"
    else:
        ultimo = dados[-1][0]
        return str(int(ultimo) + 1)


def cadastrar(cliente, pet, tipo, preco, data):
    dados = ler_banco()
    novo = [
        gerar_id(),
        cliente,
        pet,
        tipo,
        preco,
        data,
        "ativo"
    ]
    dados.append(novo)
    salvar_banco(dados)

def atualizar(id_edit, cliente, pet, tipo, preco, data):
    dados = ler_banco()
    for item in dados:
        if item[0] == id_edit:
            item[1] = cliente
            item[2] = pet
            item[3] = tipo
            item[4] = preco
            item[5] = data
            item[6] = "ativo"
    salvar_banco(dados)

def deletar(id_delete):
    dados = ler_banco()
    for item in dados:
        if item[0] == id_delete:
            item[6] = "inativo"
    salvar_banco(dados)


def listar_ativos():
    dados = ler_banco()
    ativos = []
    for item in dados:
        if len(item) > 6 and item[6] == "ativo":
            ativos.append(item)
    return ativos


criar_arquivo()
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
from tkcalendar import DateEntry
from datetime import datetime

root = Tk()
root.title("Sistema de Agendamentos - Versao Amadora")
root.geometry("960x600")
root.resizable(False, False)

class App:
    def __init__(self, master):
        self.master = master
        self.container = Frame(master, bg="#123456")
        self.container.place(relwidth=1, relheight=1)
        self.login = LoginPage(self.container, self)
        self.home = HomePage(self.container, self)
        self.lista = ListPage(self.container, self)
        self.novo = NewPage(self.container, self)
        self.show(self.login)

    def show(self, frame):
        frame.lift()

class LoginPage(Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#123456")
        self.app = app
        self.place(relwidth=1, relheight=1)
        Label(self, text="LOGIN", fg="white", bg="#123456", font=("Arial",18)).place(relx=0.5, rely=0.2, anchor="center")
        Label(self, text="Usuário", fg="white", bg="#123456").place(relx=0.4, rely=0.35, anchor="e")
        self.user = Entry(self)
        self.user.place(relx=0.42, rely=0.35, relwidth=0.2)
        Label(self, text="Senha", fg="white", bg="#123456").place(relx=0.4, rely=0.45, anchor="e")
        self.pwd = Entry(self, show="*")
        self.pwd.place(relx=0.42, rely=0.45, relwidth=0.2)
        Button(self, text="Entrar", command=self.login).place(relx=0.5, rely=0.6, anchor="center", width=120)

    def login(self):
        if self.user.get() == "adm" and self.pwd.get() == "123":
            self.app.show(self.app.home)
        else:
            messagebox.showerror("Erro", "Usuario ou senha errados")

class HomePage(Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#123456")
        self.app = app
        self.place(relwidth=1, relheight=1)
        Label(self, text="HOME", fg="white", bg="#123456", font=("Arial",18)).place(relx=0.5, rely=0.12, anchor="center")
        Button(self, text="Novo Agendamento", command=self.abrir_novo).place(relx=0.25, rely=0.35, width=220, height=44)
        Button(self, text="Listar Agendamentos", command=lambda: app.show(app.lista)).place(relx=0.75, rely=0.35, width=220, height=44)
        Button(self, text="Sair", command=lambda: app.show(app.login)).place(relx=0.5, rely=0.55, width=220, height=44)

    def abrir_novo(self):
        self.app.novo.open_for_create()
        self.app.show(self.app.novo)

class ListPage(Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#123456")
        self.app = app
        self.place(relwidth=1, relheight=1)
        Label(self, text="LISTAR AGENDAMENTOS", fg="white", bg="#123456", font=("Arial",16)).place(relx=0.5, rely=0.04, anchor="center")

        Label(self, text="ID:", fg="white", bg="#123456").place(relx=0.02, rely=0.12, anchor="w")
        self.entry_busca = Entry(self)
        self.entry_busca.place(relx=0.06, rely=0.12, relwidth=0.12)
        Button(self, text="Buscar", command=self.buscar).place(relx=0.19, rely=0.12, width=90)

        self.show_inativos = BooleanVar(value=False)
        Checkbutton(self, text="Mostrar inativos", variable=self.show_inativos, bg="#123456", fg="white", command=self.load).place(relx=0.30, rely=0.12)

        self.frame_tree = Frame(self, bd=2)
        self.frame_tree.place(relx=0.02, rely=0.18, relwidth=0.96, relheight=0.68)
        cols = ("ID","Cliente","Pet","Tipo","Preço","Data")
        self.tree = Treeview(self.frame_tree, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
        self.tree.column("ID", width=60, anchor="center")
        self.tree.pack(expand=True, fill="both")
        # binds
        self.tree.bind("<Double-1>", self.on_double)
        # botoes
        Button(self, text="Editar Selecionado", command=self.edit_selected).place(relx=0.12, rely=0.88, width=160)
        Button(self, text="Apagar Selecionado", command=self.delete_selected).place(relx=0.30, rely=0.88, width=160)
        Button(self, text="Atualizar lista", command=self.load).place(relx=0.52, rely=0.88, width=140)
        Button(self, text="Voltar", command=lambda: app.show(app.home)).place(relx=0.72, rely=0.88, width=140)

        self.load()

    def load(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        if self.show_inativos.get():
            dados = ler_banco()  
        else:
            dados = listar_ativos()
        for r in dados:
            self.tree.insert("", "end", values=(r[0], r[1], r[2], r[3], r[4], r[5]))

    def buscar(self):
        idv = self.entry_busca.get().strip()
        if idv == "":
            messagebox.showwarning("Atenção", "Informe um ID")
            return
        reg = buscar_agendamento_por_id(idv)
        if reg:
            status = reg[6] if len(reg) > 6 else "ativo"
            if status == "ativo" or self.show_inativos.get():
                for i in self.tree.get_children():
                    self.tree.delete(i)
                self.tree.insert("", "end", values=(reg[0], reg[1], reg[2], reg[3], reg[4], reg[5]))
            else:
                messagebox.showinfo("Inativo", "Registro existe mas está inativo")
        else:
            messagebox.showinfo("Não encontrado", "ID nao existe")

    def _get_sel(self):
        sel = self.tree.selection()
        if not sel:
            return None
        vals = self.tree.item(sel[0], "values")
        return vals[0] if vals else None

    def edit_selected(self):
        idv = self._get_sel()
        if not idv:
            messagebox.showwarning("Atenção", "Selecione um item")
            return
        self.open_edit_popup(idv)

    def delete_selected(self):
        idv = self._get_sel()
        if not idv:
            messagebox.showwarning("Atenção", "Selecione um item")
            return
        if messagebox.askyesno("Confirma", f"Marcar {idv} como inativo?"):
            deletar(idv)
            messagebox.showinfo("Feito", "Marcado como inativo")
            self.load()

    def on_double(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return
        vals = self.tree.item(item, "values")
        if not vals:
            return
        idv = vals[0]
        self.open_edit_popup(idv)

    def open_edit_popup(self, idv):
        reg = buscar_agendamento_por_id(idv)
        if not reg:
            messagebox.showerror("Erro", "Nao achei")
            return
        status = reg[6] if len(reg) > 6 else "ativo"
        if status == "inativo":
            if not messagebox.askyesno("Inativo", "Registro inativo. Editar mesmo assim?"):
                return
        popup = Toplevel(self)
        popup.title("Editar")
        popup.geometry("500x400")
        Label(popup, text=f"Editando ID {idv}", font=("Arial", 12)).place(relx=0.5, rely=0.06, anchor="center")

        Label(popup, text="Cliente:").place(relx=0.05, rely=0.16, anchor="w")
        e_cliente = Entry(popup); e_cliente.place(relx=0.25, rely=0.16, relwidth=0.7); e_cliente.insert(0, reg[1])

        Label(popup, text="Pet:").place(relx=0.05, rely=0.28, anchor="w")
        e_pet = Entry(popup); e_pet.place(relx=0.25, rely=0.28, relwidth=0.7); e_pet.insert(0, reg[2])

        Label(popup, text="Tipo:").place(relx=0.05, rely=0.40, anchor="w")
        e_tipo = Entry(popup); e_tipo.place(relx=0.25, rely=0.40, relwidth=0.7); e_tipo.insert(0, reg[3])

        Label(popup, text="Preço:").place(relx=0.05, rely=0.52, anchor="w")
        e_preco = Entry(popup); e_preco.place(relx=0.25, rely=0.52, relwidth=0.7); e_preco.insert(0, reg[4])

        Label(popup, text="Data:").place(relx=0.05, rely=0.64, anchor="w")
        try:
            d0 = reg[5] if reg[5] else datetime.now().strftime("%Y-%m-%d")
            de = DateEntry(popup, width=14, year=datetime.now().year); de.place(relx=0.25, rely=0.64)
            de.set_date(d0)
        except:
            de = DateEntry(popup, width=14, year=datetime.now().year); de.place(relx=0.25, rely=0.64)
            de.set_date(datetime.now())

        def salvar():
            c = e_cliente.get().strip()
            p = e_pet.get().strip()
            t = e_tipo.get().strip()
            pr = e_preco.get().strip()
            d = de.get_date().strftime("%Y-%m-%d")
            if c=="" or p=="" or t=="" or pr=="":
                messagebox.showwarning("Atenção","Preencha tudo")
                return
            try:
                float(pr)
            except:
                messagebox.showwarning("Atenção","Preço invalido")
                return
            atualizar(idv, c, p, t, pr, d)
            messagebox.showinfo("Ok","Atualizado")
            popup.destroy()
            self.load()

        def cancelar():
            popup.destroy()

        Button(popup, text="Salvar Alterações", command=salvar).place(relx=0.25, rely=0.82, width=160)
        Button(popup, text="Cancelar", command=cancelar).place(relx=0.60, rely=0.82, width=120)

class NewPage(Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#123456")
        self.app = app
        self.place(relwidth=1, relheight=1)
        Label(self, text="NOVO AGENDAMENTO", fg="white", bg="#123456", font=("Arial",16)).place(relx=0.5, rely=0.06, anchor="center")

        Label(self, text="Cliente:", fg="white", bg="#123456").place(relx=0.05, rely=0.18, anchor="w")
        self.e_cliente = Entry(self); self.e_cliente.place(relx=0.20, rely=0.18, relwidth=0.7)
        Label(self, text="Pet:", fg="white", bg="#123456").place(relx=0.05, rely=0.30, anchor="w")
        self.e_pet = Entry(self); self.e_pet.place(relx=0.20, rely=0.30, relwidth=0.7)
        Label(self, text="Tipo:", fg="white", bg="#123456").place(relx=0.05, rely=0.42, anchor="w")
        self.e_tipo = Entry(self); self.e_tipo.place(relx=0.20, rely=0.42, relwidth=0.7)
        Label(self, text="Preço:", fg="white", bg="#123456").place(relx=0.05, rely=0.54, anchor="w")
        self.e_preco = Entry(self); self.e_preco.place(relx=0.20, rely=0.54, relwidth=0.7)
        Label(self, text="Data:", fg="white", bg="#123456").place(relx=0.05, rely=0.66, anchor="w")
        self.cal = DateEntry(self, width=14, year=datetime.now().year); self.cal.place(relx=0.20, rely=0.66)

        Button(self, text="Marcar", command=self.marcar).place(relx=0.30, rely=0.82, width=160)
        Button(self, text="Voltar", command=lambda: app.show(app.home)).place(relx=0.60, rely=0.82, width=140)

    def open_for_create(self):
        self.e_cliente.delete(0, END)
        self.e_pet.delete(0, END)
        self.e_tipo.delete(0, END)
        self.e_preco.delete(0, END)
        self.cal.set_date(datetime.now())

    def marcar(self):
        c = self.e_cliente.get().strip()
        p = self.e_pet.get().strip()
        t = self.e_tipo.get().strip()
        pr = self.e_preco.get().strip()
        d = self.cal.get_date().strftime("%Y-%m-%d")
        if c=="" or p=="" or t=="" or pr=="":
            messagebox.showwarning("Atenção","Preencha tudo")
            return
        try:
            float(pr)
        except:
            messagebox.showwarning("Atenção","Preco invalido")
            return
        cadastrar(c, p, t, pr, d)
        messagebox.showinfo("Sucesso","Agendamento criado")
        self.open_for_create()
        self.app.lista.load()

criar_arquivo()  
app = App(root)
root.mainloop()
