import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import qrcode
from PIL import Image, ImageTk
import cv2
from pyzbar.pyzbar import decode
import threading
import os
from datetime import datetime
import json

class ModernQRCodeSystem:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("QR Code Professional Suite v1.0")
        self.janela.geometry("1200x800")
        
        # Configurar tema moderno
        self.configurar_tema()
        
        # Variáveis
        self.camera_ativa = False
        self.cap = None
        self.historico = []
        self.carregar_historico()
        
        # Criar interface
        self.criar_barra_menu()
        self.criar_interface_principal()
        
    def configurar_tema(self):
        """Configura um tema profissional moderno"""
        # Cores profissionais
        self.cores = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'dark': '#2c3e50',
            'light': '#ecf0f1',
            'white': '#ffffff',
            'gray': '#95a5a6',
            'gradient_start': '#3498db',
            'gradient_end': '#2c3e50'
        }
        
        # Configurar estilo
        self.janela.configure(bg=self.cores['light'])
        
        # Estilo para botões
        estilo = ttk.Style()
        estilo.theme_use('clam')
        
        # Configurar estilos personalizados
        estilo.configure('Modern.TButton', 
                        font=('Segoe UI', 10, 'bold'),
                        padding=10,
                        background=self.cores['secondary'],
                        foreground='white')
        
        estilo.map('Modern.TButton',
                  background=[('active', self.cores['primary'])])
        
        estilo.configure('Success.TButton',
                        background=self.cores['success'])
        
        estilo.configure('Danger.TButton',
                        background=self.cores['danger'])
        
    def criar_barra_menu(self):
        """Cria barra de menu profissional"""
        menubar = tk.Menu(self.janela)
        self.janela.config(menu=menubar)
        
        # Menu Arquivo
        arquivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=arquivo_menu)
        arquivo_menu.add_command(label="Novo QR Code", command=self.novo_qr)
        arquivo_menu.add_command(label="Abrir Imagem", command=self.abrir_imagem)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Sair", command=self.janela.quit)
        
        # Menu Ferramentas
        ferramentas_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ferramentas", menu=ferramentas_menu)
        ferramentas_menu.add_command(label="Exportar Histórico", command=self.exportar_historico)
        ferramentas_menu.add_command(label="Limpar Histórico", command=self.limpar_historico)
        
        # Menu Ajuda
        ajuda_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=ajuda_menu)
        ajuda_menu.add_command(label="Documentação", command=self.mostrar_documentacao)
        ajuda_menu.add_command(label="Sobre", command=self.mostrar_sobre)
        
    def criar_interface_principal(self):
        """Cria a interface principal com design profissional"""
        # Container principal com padding
        main_container = tk.Frame(self.janela, bg=self.cores['light'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Cabeçalho
        self.criar_cabecalho(main_container)
        
        # Painel principal com 2 colunas
        painel_principal = tk.Frame(main_container, bg=self.cores['light'])
        painel_principal.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Coluna esquerda - Criar QR Code
        coluna_esquerda = tk.Frame(painel_principal, bg=self.cores['white'], 
                                   relief=tk.RAISED, bd=0)
        coluna_esquerda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.criar_painel_criar(coluna_esquerda)
        
        # Coluna direita - Scanner e Histórico
        coluna_direita = tk.Frame(painel_principal, bg=self.cores['white'],
                                  relief=tk.RAISED, bd=0)
        coluna_direita.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        self.criar_painel_scanner(coluna_direita)
        
        # Rodapé
        self.criar_rodape(main_container)
        
    def criar_cabecalho(self, parent):
        """Cria cabeçalho profissional"""
        cabecalho = tk.Frame(parent, bg=self.cores['primary'], height=80)
        cabecalho.pack(fill=tk.X)
        cabecalho.pack_propagate(False)
        
        # Título
        titulo = tk.Label(cabecalho, 
                         text="QR CODE PROFESSIONAL SUITE", 
                         font=('Segoe UI', 20, 'bold'),
                         bg=self.cores['primary'],
                         fg=self.cores['white'])
        titulo.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Versão
        versao = tk.Label(cabecalho,
                         text="v1.0",
                         font=('Segoe UI', 10),
                         bg=self.cores['primary'],
                         fg=self.cores['gray'])
        versao.pack(side=tk.RIGHT, padx=20, pady=20)
        
    def criar_painel_criar(self, parent):
        """Cria painel de criação de QR Code"""
        # Título do painel
        titulo = tk.Label(parent, text="🔨 CRIAR QR CODE",
                         font=('Segoe UI', 14, 'bold'),
                         bg=self.cores['white'],
                         fg=self.cores['primary'])
        titulo.pack(pady=(20, 10), padx=20, anchor='w')
        
        # Separador
        self.criar_separador(parent)
        
        # Frame de conteúdo
        conteudo = tk.Frame(parent, bg=self.cores['white'])
        conteudo.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Tipo de QR Code
        tk.Label(conteudo, text="Tipo de Conteúdo:",
                font=('Segoe UI', 10, 'bold'),
                bg=self.cores['white']).pack(anchor='w')
        
        self.tipo_qr = ttk.Combobox(conteudo, 
                                    values=['URL', 'Texto', 'Email', 'Telefone', 'SMS'],
                                    state='readonly',
                                    font=('Segoe UI', 10))
        self.tipo_qr.set('URL')
        self.tipo_qr.pack(fill=tk.X, pady=(5, 10))
        self.tipo_qr.bind('<<ComboboxSelected>>', self.atualizar_placeholder)
        
        # Conteúdo
        tk.Label(conteudo, text="Conteúdo:",
                font=('Segoe UI', 10, 'bold'),
                bg=self.cores['white']).pack(anchor='w')
        
        self.txt_conteudo = scrolledtext.ScrolledText(conteudo, height=5,
                                                       font=('Segoe UI', 10),
                                                       bg=self.cores['white'],
                                                       relief=tk.FLAT,
                                                       bd=1)
        self.txt_conteudo.pack(fill=tk.X, pady=(5, 10))
        
        # Opções de personalização
        self.criar_opcoes_personalizacao(conteudo)
        
        # Botões de ação
        self.criar_botoes_acao(conteudo)
        
        # Preview do QR Code
        self.criar_preview_qr(conteudo)
        
    def criar_opcoes_personalizacao(self, parent):
        """Cria opções de personalização do QR Code"""
        # Frame de opções
        opcoes_frame = tk.LabelFrame(parent, text="Personalização",
                                     font=('Segoe UI', 10, 'bold'),
                                     bg=self.cores['white'],
                                     fg=self.cores['primary'])
        opcoes_frame.pack(fill=tk.X, pady=10)
        
        # Cores
        cores_frame = tk.Frame(opcoes_frame, bg=self.cores['white'])
        cores_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(cores_frame, text="Cor do QR:",
                bg=self.cores['white']).pack(side=tk.LEFT, padx=5)
        
        self.cor_frente = tk.StringVar(value="#2c3e50")
        cores = ["#2c3e50", "#3498db", "#27ae60", "#e74c3c", "#f39c12", "#9b59b6"]
        for cor in cores:
            btn = tk.Button(cores_frame, bg=cor, width=3, height=1,
                           command=lambda c=cor: self.cor_frente.set(c),
                           relief=tk.FLAT, bd=0)
            btn.pack(side=tk.LEFT, padx=2)
        
        tk.Label(cores_frame, text="Fundo:",
                bg=self.cores['white']).pack(side=tk.LEFT, padx=(20, 5))
        
        self.cor_fundo = tk.StringVar(value="#ffffff")
        fundos = ["#ffffff", "#ecf0f1", "#bdc3c7"]
        for cor in fundos:
            btn = tk.Button(cores_frame, bg=cor, width=3, height=1,
                           command=lambda c=cor: self.cor_fundo.set(c),
                           relief=tk.FLAT, bd=0)
            btn.pack(side=tk.LEFT, padx=2)
        
        # Tamanho
        tamanho_frame = tk.Frame(opcoes_frame, bg=self.cores['white'])
        tamanho_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(tamanho_frame, text="Tamanho:",
                bg=self.cores['white']).pack(side=tk.LEFT)
        
        self.tamanho_qr = tk.Scale(tamanho_frame, from_=5, to=15, orient=tk.HORIZONTAL,
                                   bg=self.cores['white'], length=150)
        self.tamanho_qr.set(10)
        self.tamanho_qr.pack(side=tk.LEFT, padx=10)
        
    def criar_botoes_acao(self, parent):
        """Cria botões de ação estilizados"""
        btn_frame = tk.Frame(parent, bg=self.cores['white'])
        btn_frame.pack(fill=tk.X, pady=10)
        
        # Botão Criar
        btn_criar = tk.Button(btn_frame,
                             text="✨ CRIAR QR CODE",
                             command=self.criar_qr,
                             bg=self.cores['success'],
                             fg='white',
                             font=('Segoe UI', 11, 'bold'),
                             relief=tk.FLAT,
                             cursor='hand2',
                             padx=20,
                             pady=10)
        btn_criar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Botão Salvar
        btn_salvar = tk.Button(btn_frame,
                              text="💾 SALVAR",
                              command=self.salvar_qr,
                              bg=self.cores['secondary'],
                              fg='white',
                              font=('Segoe UI', 11, 'bold'),
                              relief=tk.FLAT,
                              cursor='hand2',
                              padx=20,
                              pady=10)
        btn_salvar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
    def criar_preview_qr(self, parent):
        """Cria área de preview do QR Code"""
        preview_frame = tk.LabelFrame(parent, text="Preview",
                                      font=('Segoe UI', 10, 'bold'),
                                      bg=self.cores['white'],
                                      fg=self.cores['primary'])
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.preview_label = tk.Label(preview_frame,
                                      text="Seu QR Code aparecerá aqui",
                                      bg=self.cores['white'],
                                      font=('Segoe UI', 10))
        self.preview_label.pack(expand=True, padx=20, pady=20)
        
    def criar_painel_scanner(self, parent):
        """Cria painel de scanner profissional"""
        # Título
        titulo = tk.Label(parent, text="📷 SCANNER PROFISSIONAL",
                         font=('Segoe UI', 14, 'bold'),
                         bg=self.cores['white'],
                         fg=self.cores['primary'])
        titulo.pack(pady=(20, 10), padx=20, anchor='w')
        
        # Separador
        self.criar_separador(parent)
        
        # Opções de scanner
        scanner_opcoes = tk.Frame(parent, bg=self.cores['white'])
        scanner_opcoes.pack(fill=tk.X, padx=20, pady=10)
        
        # Botões scanner
        btn_arquivo = tk.Button(scanner_opcoes,
                               text="📁 LER DE ARQUIVO",
                               command=self.ler_arquivo,
                               bg=self.cores['secondary'],
                               fg='white',
                               font=('Segoe UI', 10, 'bold'),
                               relief=tk.FLAT,
                               cursor='hand2',
                               padx=15,
                               pady=8)
        btn_arquivo.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        self.btn_camera = tk.Button(scanner_opcoes,
                                   text="📷 INICIAR CÂMERA",
                                   command=self.toggle_camera,
                                   bg=self.cores['warning'],
                                   fg='white',
                                   font=('Segoe UI', 10, 'bold'),
                                   relief=tk.FLAT,
                                   cursor='hand2',
                                   padx=15,
                                   pady=8)
        self.btn_camera.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Área de vídeo
        video_frame = tk.Frame(parent, bg='black', height=300)
        video_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        video_frame.pack_propagate(False)
        
        self.video_label = tk.Label(video_frame, bg='black')
        self.video_label.pack(expand=True)
        
        # Resultados
        resultados_frame = tk.LabelFrame(parent, text="Resultados da Leitura",
                                        font=('Segoe UI', 10, 'bold'),
                                        bg=self.cores['white'],
                                        fg=self.cores['primary'])
        resultados_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.txt_resultado = scrolledtext.ScrolledText(resultados_frame,
                                                        height=6,
                                                        font=('Consolas', 10),
                                                        bg=self.cores['white'],
                                                        relief=tk.FLAT,
                                                        bd=1)
        self.txt_resultado.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Histórico
        self.criar_historico(parent)
        
    def criar_historico(self, parent):
        """Cria painel de histórico"""
        historico_frame = tk.LabelFrame(parent, text="Histórico Recente",
                                       font=('Segoe UI', 10, 'bold'),
                                       bg=self.cores['white'],
                                       fg=self.cores['primary'])
        historico_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.lista_historico = tk.Listbox(historico_frame,
                                          height=4,
                                          font=('Segoe UI', 9),
                                          bg=self.cores['white'],
                                          relief=tk.FLAT,
                                          bd=1)
        self.lista_historico.pack(fill=tk.X, padx=10, pady=10)
        self.lista_historico.bind('<Double-Button-1>', self.carregar_historico_item)
        
        self.atualizar_lista_historico()
        
    def criar_rodape(self, parent):
        """Cria rodapé profissional"""
        rodape = tk.Frame(parent, bg=self.cores['dark'], height=40)
        rodape.pack(fill=tk.X, side=tk.BOTTOM)
        rodape.pack_propagate(False)
        
        status = tk.Label(rodape,
                         text="✅ Sistema pronto | QR Code Professional Suite",
                         bg=self.cores['dark'],
                         fg=self.cores['gray'],
                         font=('Segoe UI', 9))
        status.pack(side=tk.LEFT, padx=20, pady=10)
        
        datetime_label = tk.Label(rodape,
                                 text=datetime.now().strftime("%d/%m/%Y %H:%M"),
                                 bg=self.cores['dark'],
                                 fg=self.cores['gray'],
                                 font=('Segoe UI', 9))
        datetime_label.pack(side=tk.RIGHT, padx=20, pady=10)
        
    def criar_separador(self, parent):
        """Cria separador estilizado"""
        separador = tk.Frame(parent, height=2, bg=self.cores['gray'])
        separador.pack(fill=tk.X, padx=20, pady=5)
        
    def atualizar_placeholder(self, event=None):
        """Atualiza placeholder baseado no tipo selecionado"""
        tipos = {
            'URL': 'https://exemplo.com',
            'Texto': 'Digite seu texto aqui...',
            'Email': 'exemplo@email.com',
            'Telefone': '+55 11 99999-9999',
            'SMS': '+55 11 99999-9999:Olá, tudo bem?'
        }
        
        tipo = self.tipo_qr.get()
        placeholder = tipos.get(tipo, 'Digite o conteúdo...')
        
        # Atualizar placeholder
        self.txt_conteudo.delete('1.0', tk.END)
        self.txt_conteudo.insert('1.0', placeholder)
        self.txt_conteudo.tag_add('placeholder', '1.0', 'end')
        self.txt_conteudo.tag_config('placeholder', foreground='gray')
        
    def criar_qr(self):
        """Cria QR Code com design moderno"""
        conteudo = self.txt_conteudo.get("1.0", tk.END).strip()
        tipo = self.tipo_qr.get()
        
        # Validar conteúdo
        if not conteudo or conteudo == self.txt_conteudo.tag_ranges('placeholder'):
            messagebox.showwarning("Aviso", "Digite o conteúdo do QR Code!")
            return
        
        # Formatar conteúdo baseado no tipo
        conteudo_formatado = self.formatar_conteudo(conteudo, tipo)
        
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=self.tamanho_qr.get(),
                border=4,
            )
            qr.add_data(conteudo_formatado)
            qr.make(fit=True)
            
            img = qr.make_image(
                fill_color=self.cor_frente.get(),
                back_color=self.cor_fundo.get()
            )
            
            # Redimensionar para preview
            img = img.resize((250, 250), Image.Resampling.LANCZOS)
            
            # Converter para PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Atualizar preview
            self.preview_label.config(image=photo, text='')
            self.preview_label.image = photo
            
            # Salvar temporariamente
            self.qr_atual = img
            
            # Adicionar ao histórico
            self.adicionar_historico(conteudo_formatado)
            
            # Efeito de sucesso
            self.mostrar_notificacao("QR Code criado com sucesso!", "success")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar QR Code:\n{str(e)}")
            self.mostrar_notificacao("Erro ao criar QR Code!", "error")
    
    def formatar_conteudo(self, conteudo, tipo):
        """Formata o conteúdo baseado no tipo selecionado"""
        if tipo == 'URL':
            if not conteudo.startswith(('http://', 'https://')):
                return f"https://{conteudo}"
        elif tipo == 'Email':
            return f"mailto:{conteudo}"
        elif tipo == 'Telefone':
            return f"tel:{conteudo}"
        elif tipo == 'SMS':
            partes = conteudo.split(':')
            if len(partes) == 2:
                return f"smsto:{partes[0]}:{partes[1]}"
        
        return conteudo
    
    def salvar_qr(self):
        """Salva QR Code em arquivo"""
        if hasattr(self, 'qr_atual'):
            arquivo = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialfile=f"qr_code_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            if arquivo:
                self.qr_atual.save(arquivo)
                messagebox.showinfo("Sucesso", f"QR Code salvo em:\n{arquivo}")
                self.mostrar_notificacao("QR Code salvo com sucesso!", "success")
        else:
            messagebox.showwarning("Aviso", "Crie um QR Code primeiro!")
    
    def ler_arquivo(self):
        """Lê QR Code de arquivo"""
        arquivo = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if arquivo:
            try:
                img = cv2.imread(arquivo)
                qr_codes = decode(img)
                
                if qr_codes:
                    self.txt_resultado.delete("1.0", tk.END)
                    for i, qr in enumerate(qr_codes, 1):
                        dados = qr.data.decode('utf-8')
                        self.txt_resultado.insert(tk.END, f"📱 QR Code {i}:\n")
                        self.txt_resultado.insert(tk.END, f"{dados}\n\n")
                        self.adicionar_historico(dados)
                    
                    self.mostrar_notificacao(f"Encontrados {len(qr_codes)} QR Code(s)!", "success")
                else:
                    messagebox.showwarning("Aviso", "Nenhum QR Code encontrado na imagem!")
                    self.mostrar_notificacao("Nenhum QR Code encontrado", "warning")
                    
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao ler arquivo:\n{str(e)}")
    
    def toggle_camera(self):
        """Alterna câmera"""
        if not self.camera_ativa:
            self.iniciar_camera()
        else:
            self.parar_camera()
    
    def iniciar_camera(self):
        """Inicia a câmera"""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Erro", "Não foi possível abrir a câmera!")
            return
        
        self.camera_ativa = True
        self.btn_camera.config(text="⏹️ PARAR CÂMERA", bg=self.cores['danger'])
        self.atualizar_camera()
    
    def parar_camera(self):
        """Para a câmera"""
        self.camera_ativa = False
        if self.cap:
            self.cap.release()
        self.btn_camera.config(text="📷 INICIAR CÂMERA", bg=self.cores['warning'])
        self.video_label.config(image='')
    
    def atualizar_camera(self):
        """Atualiza frame da câmera"""
        if not self.camera_ativa:
            return
        
        ret, frame = self.cap.read()
        if ret:
            # Decodificar QR Code
            qr_codes = decode(frame)
            
            for qr in qr_codes:
                dados = qr.data.decode('utf-8')
                self.txt_resultado.insert(tk.END, f"📱 {dados}\n")
                self.txt_resultado.see(tk.END)
                self.adicionar_historico(dados)
                
                # Desenhar retângulo
                pts = qr.polygon
                if len(pts) == 4:
                    pts = pts.reshape((-1, 1, 2))
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
                
                # Adicionar texto
                cv2.putText(frame, "QR Code Detectado", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Converter para PhotoImage
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img = img.resize((400, 300), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            self.video_label.config(image=photo)
            self.video_label.image = photo
        
        self.janela.after(30, self.atualizar_camera)
    
    def adicionar_historico(self, dados):
        """Adiciona item ao histórico"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        item = f"[{timestamp}] {dados[:50]}..."
        self.historico.insert(0, item)
        
        # Manter apenas os últimos 20 itens
        if len(self.historico) > 20:
            self.historico.pop()
        
        self.salvar_historico()
        self.atualizar_lista_historico()
    
    def atualizar_lista_historico(self):
        """Atualiza lista de histórico na interface"""
        self.lista_historico.delete(0, tk.END)
        for item in self.historico:
            self.lista_historico.insert(tk.END, item)
    
    def carregar_historico_item(self, event):
        """Carrega item do histórico"""
        selecao = self.lista_historico.curselection()
        if selecao:
            item = self.lista_historico.get(selecao[0])
            # Extrair conteúdo (remover timestamp)
            conteudo = item.split('] ')[1] if '] ' in item else item
            self.txt_conteudo.delete('1.0', tk.END)
            self.txt_conteudo.insert('1.0', conteudo)
    
    def salvar_historico(self):
        """Salva histórico em arquivo"""
        try:
            with open('historico_qr.json', 'w', encoding='utf-8') as f:
                json.dump(self.historico, f, ensure_ascii=False)
        except:
            pass
    
    def carregar_historico(self):
        """Carrega histórico do arquivo"""
        try:
            with open('historico_qr.json', 'r', encoding='utf-8') as f:
                self.historico = json.load(f)
        except:
            self.historico = []
    
    def exportar_historico(self):
        """Exporta histórico para arquivo"""
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json")]
        )
        if arquivo:
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    for item in self.historico:
                        f.write(f"{item}\n")
                messagebox.showinfo("Sucesso", "Histórico exportado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar histórico:\n{str(e)}")
    
    def limpar_historico(self):
        """Limpa histórico"""
        if messagebox.askyesno("Confirmar", "Deseja limpar todo o histórico?"):
            self.historico = []
            self.salvar_historico()
            self.atualizar_lista_historico()
            self.mostrar_notificacao("Histórico limpo!", "success")
    
    def mostrar_notificacao(self, mensagem, tipo="info"):
        """Mostra notificação temporária"""
        # Criar frame de notificação
        notificacao = tk.Toplevel(self.janela)
        notificacao.title("")
        notificacao.overrideredirect(True)
        
        # Configurar cores
        cores = {
            "success": self.cores['success'],
            "error": self.cores['danger'],
            "warning": self.cores['warning'],
            "info": self.cores['secondary']
        }
        
        cor = cores.get(tipo, self.cores['secondary'])
        
        notificacao.configure(bg=cor)
        notificacao.geometry(f"300x50+{self.janela.winfo_x()+self.janela.winfo_width()//2-150}+{self.janela.winfo_y()+50}")
        
        # Adicionar mensagem
        label = tk.Label(notificacao, text=mensagem, bg=cor, fg='white',
                        font=('Segoe UI', 10, 'bold'))
        label.pack(expand=True)
        
        # Fechar após 2 segundos
        notificacao.after(2000, notificacao.destroy)
    
    def novo_qr(self):
        """Limpa campos para novo QR Code"""
        self.txt_conteudo.delete('1.0', tk.END)
        self.preview_label.config(image='', text='Seu QR Code aparecerá aqui')
        if hasattr(self, 'qr_atual'):
            delattr(self, 'qr_atual')
    
    def abrir_imagem(self):
        """Abre imagem para leitura"""
        self.ler_arquivo()
    
    def mostrar_documentacao(self):
        """Mostra documentação"""
        doc_text = """
        📚 DOCUMENTAÇÃO - QR CODE PROFESSIONAL SUITE
        
        FUNCIONALIDADES:
        
        1. CRIAR QR CODE
           • Suporte a URLs, texto, email, telefone e SMS
           • Personalização de cores e tamanho
           • Preview em tempo real
           • Salvamento em PNG
        
        2. SCANNER
           • Leitura de arquivos de imagem
           • Leitura pela câmera em tempo real
           • Detecção automática de múltiplos QR Codes
           • Histórico de leituras
        
        3. HISTÓRICO
           • Armazena últimos 20 QR Codes lidos
           • Exportação para arquivo
           • Recarregar QR Codes anteriores
        
        DICAS:
        • Clique duplo no histórico para recarregar
        • Use Ctrl+C para copiar resultados
        • QR Codes podem ser salvos em qualquer formato de imagem
        
        Versão 1.0 - Desenvolvido com Python
        """
        
        messagebox.showinfo("Documentação", doc_text)
    
    def mostrar_sobre(self):
        """Mostra informações sobre o sistema"""
        sobre_text = """
        QR CODE PROFESSIONAL SUITE v1.0
        
        Sistema profissional para criação e leitura de QR Codes.
        
        Desenvolvido com:
        • Python 3.x
        • Tkinter (Interface Gráfica)
        • QRCode (Biblioteca de QR Codes)
        • OpenCV (Processamento de imagem)
        • Pillow (Manipulação de imagens)
        
        © 2024 - Todos os direitos reservados
        """
        
        messagebox.showinfo("Sobre", sobre_text)
    
    def run(self):
        """Executa a aplicação"""
        self.janela.mainloop()

# Executar o sistema
if __name__ == "__main__":
    app = ModernQRCodeSystem()
    app.run()