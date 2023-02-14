import psycopg2
class Banco:
    def __init__(self, database="", host="", user="", password="", port=""):
        self.database = database
        self.host = host
        self.user = user
        self.passwd = password
        self.port = port
    #metodo de conexão ao banco de dados
    def conec(self):
        self.con = psycopg2.connect(
            database = self.database,
            host = self.host,
            user = self.user,
            password = self.passwd,
            port = self.port
            
        )
        self.cur = self.con.cursor()
    #metodo que faz consulta do cod
    def consultar_cod(self, compr):
        self.conec()
        comando = """SELECT cod_interno FROM public.itens WHERE codbarra = %s """
        self.cur.execute(comando, [compr])
        resultado = self.cur.fetchall()
        for x in resultado:
            v = str(x).strip("(Decimal''),")
            return v
        
    def consultar_nome(self, compr):
        self.conec()
        comando = """SELECT descricao FROM public.itens WHERE codbarra = %s """
        self.cur.execute(comando, [compr])
        resultado = self.cur.fetchall()
        for x in resultado:
            v = str(x).strip("(Decimal''),")
            return v
    def consultar_prec(self, compr):
        self.conec()
        comando = """SELECT preco FROM public.precos WHERE cod_interno = %s AND unidade = '***' """
        self.cur.execute(comando, [compr])
        resultado = self.cur.fetchall()
        for x in resultado:
            v = str(x).strip("(Decimal''),")
            return v
        
        
