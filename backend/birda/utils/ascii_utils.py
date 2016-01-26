# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import sys
import select
import signal
import time
import textwrap

# ==================================================================== #
#               FUNZIONE SI STAMPA LISTA DI DIZIONARI                  # 
# ==================================================================== #

def render_list_dict(listOdict,map=(),align='left',sep_on_change=[],exclude_map=(),print_n_rec=False):
	"""
	render_list_dict(listOdict:lista-di-dizionari,[map:lista-di-stringhe],orient=('left','center','right') )
		
		Visualizza un dizionario nell'old-fashion-ascii-style (quello di mysql,
		tanto per intenderci)
		map: forza un ordine per le chiavi nel dizionario; le rimanenti
			vengono visualizzate in ordine alfabetico
		align: (left,right,center) allineamento dei contenuti delle colonne
			(il contenuto della testata e` centrato per default)
		sep_on_change: lista di chiavi dei dizionari passati in ingresso per
			cui verra` inserito un separatore orizzontale al cambio di valore.
			(ad esempio [RIF_INTR,CAPOCMAT] pone una riga orizzontale di separazione
			fra ogni CAPOCMAT)
			Ovvimamente questo parametro ha un senso solo se la lista e` ordinata per
			questi parametri
		exclude_map: lista di chiavi da escludere dalla visualizzazione
		print_n_res: se True printa in calce alla tabella il numero di record in input 
	"""
	
	output = ''	
	testata = {}
	
	if not listOdict :
		return ''
	
	keys = listOdict[0].keys()
	for k in list(keys):
		if k in map:
			keys.remove(k)
	keys.sort()
	map = list(map)
	map.extend(keys)
	keys = map
	
	for k in exclude_map:
		keys.remove(k)
	
	# Calcolo della dimensione orizzontale delle colonne
	for k in keys :
		lens = []
		lens.append( len(str(k)) )
		for rd in listOdict :
			try:
				lens.append( len(str(rd[k])) )
			except KeyError:
				print "Chiave %r : Riga: %r" % (k,rd)
				raise
		testata[k] = max(lens) + 2
	
	# Creazione del separatore orizzontale
	sep = '+'
	for k in keys:
		sep += '-' * testata[k] + '+'
	sep += '\n'
	
	dim_list = dict_values(testata,keys)
	
	# Creazione della linea vuota
	blank_line = make_line(' '*len(dim_list),dim_list,align='center')
	blank_line = ''
	
	output += sep + \
			  blank_line + \
			  make_line(keys,dim_list,align='center') + \
			  blank_line + \
			  sep + \
			  blank_line
	
	def sub_d(diz,chiavi):
		tmp_diz = {}
		for k in chiavi: 
			tmp_diz[k] = str(diz[k])
		return tmp_diz
			
	if sep_on_change :
		act_val = sub_d(listOdict[0],sep_on_change)
	for d in listOdict:
		if sep_on_change and sub_d(d,sep_on_change) != act_val :
			output += sep
			act_val = sub_d(d,sep_on_change)
		output += make_line(dict_values(d,keys),dim_list,align=align)
		
	output += blank_line + \
			  sep
	
	if print_n_rec:
		output += "Record presenti: %s\n" % len(listOdict)
		
	return output

# ------------------------ #

def make_line(data_list,dim_list,align):
	lines = []
	for i in range(len(data_list)) :
		if align == 'left' :
			lines += [ ' %%-%ss' % (dim_list[i]-1) % data_list[i] ]
		elif align == 'center' :
			lines += [ str(data_list[i]).center(dim_list[i]) ]
		elif align == 'right' :
			lines += [ '%%0%ss ' % (dim_list[i]-1) % data_list[i] ]
		else :
			raise Exception('Allineamento "%s" non previsto...' % align)
	return '|%s|\n' % '|'.join(lines)

# ------------------------ #

def dict_values(d,keys):
	out = []
	for k in keys:
		out.append(d[k])
	return out

# ==================================================================== #
#                     FUNZIONE DI STAMPA CORNICE                       #
# ==================================================================== #

CAR = '#'
MAX_WIDTH = 75

# ------------------------ #

def _corn_adat(stringa):
	ret = CAR * (len(stringa)+4)           + "\n"
	ret += '%s %s %s' % (CAR,stringa,CAR)  + "\n"
	ret += CAR * (len(stringa)+4)
	return ret

# ------------------------ #

def _concat(riga):
	s = ''
	for parola in riga :
		s += str(parola) + ' '
	if s :
		return s[:-1]
	else :
		return ''

# ------------------------ #

def vai_a_capo(stringa,width,parametro_oscuro=5) :
	return textwrap.wrap(stringa,width)

# ------------------------ #

def _formatta(stringa,width) :
	s = stringa.replace('\t','    ')
	paragrafi = s.split('\n')
	righe = []
	for p in paragrafi :
		new_l = vai_a_capo(p,width)
		
		# Per evitare che vengano assorbite le righe vuote
		if not new_l:
			new_l = ['']
		
		righe.extend(new_l)
	
	# Per evitare che i programmi che mettono inavvertitamente un \n
	# alla fine abbiano una riga vuota in fondo
	if not righe[-1]:
		righe.pop(-1)
	return righe

# ------------------------ #

# Renderizza <stringa> in un paragrafo
def cornice(stringa,width=0,offset=0,align='left'):
	"""
	cornice(stringa [, width:int] [, offset:int] [, align:('left'|'center')] ) -> stringa
		Renderizza <stringa> in un paragrafo circondato dalla cornice
	"""
	
	# Calcolo del "padding" prima fra margine e paragrafo
	if offset :
		off = ' '*offset
	else :
		off = ''
	
	# Calcolo della dimensione del "block" comprensivo di cornice e padding
	if width :
		width = width + 4
	else :
		#width = min( len(stringa) , MAX_WIDTH ) + 4
		width = min( max( [ len(s) for s in stringa.split('\n') ] ) , MAX_WIDTH ) + 4
	
	# Suddivisione della stringa in righe in base a <width>
	righe = _formatta(stringa,width)
	
	ret = off + CAR * width + "\n"
	for riga in righe:
		if align == 'center':
			lpad = (width-len(riga)-2)/2
		elif align == 'left' :
			lpad = 1
		rpad = (width-len(riga)-2-lpad)
		ret += off + CAR + ' '*lpad + riga + ' '*rpad + CAR  + "\n"
		
	ret += off + CAR * width
	
	return ret

# ==================================================================== #
#                   FUNZIONI DI GESTIONE COLORI                        #
# ==================================================================== #

TAGS = {
     "b":1, "u":4 , "blink":5 , "invert":7 ,

     "black":30,      "red":31,      "green":32,      "yellow":33,      "blue":34,     "magenta":35,      "cyan":36,      "white":37,
"back_black":40, "back_red":41, "back_green":42, "back_yellow":43, "back_blue":44,"back_magenta":45, "back_cyan":46, "back_white":47,
}

STAMPA_DI_PROVA = """
<blink>
<b><red>ciao</red>per</b><green>ciao</green><b><cyan>ok</cyan></b>
</blink>
<u><b><magenta>ciao</magenta> beu</b> beu</u>
<back_green> <b><yellow>g</yellow><red>u</red><black>l</black><blue>p</blue></b> </back_green>
<invert>riciao</invert>
"""

# -------------------------------------------------------------------- #

def pr_stack(stack):
	s = '\033[0m'
	for tag in stack :
		s += '\033[%dm' % TAGS[tag]
	return s

# -------------------------------------------------------------------- #

def tratta_tag(tag,stack,n_riga):
	#print tag
	if tag.find('/') == 0 :
		if not stack :
			raise ImportError( "Errore di formattazione alla riga %(n_riga)s! (Trovato tag:'%(tag)s' con stack:%(stack)s)" % vars() )
		removed_tag = stack.pop(len(stack)-1)
		if removed_tag != tag[1:] :
			raise ImportError( "Errore di formattazione alla riga %(n_riga)s! (Trovato tag:'%(tag)s' con stack:%(stack)s)" % vars() )
	else :
		if tag not in TAGS :
			raise ImportError( "Tag '%(tag)s' sconosciuto alla riga %(n_riga)s!" % vars() )
		stack.append(tag)

	#print repr(pr_stack(stack))
	return pr_stack(stack)

# -------------------------------------------------------------------- #

def colorize(stringa,plain=False) :
	try :
		stack = []
		
		out = ''
		n_riga = 1
		tag_c = ''
		tag = False
		for ch in stringa :
			#print "%s: %s" % ( ch, repr(out))
			if tag :
				if ch == '>' :
					tag = False
					# STDOUT #
					if (tag_c in TAGS) or ((tag_c.startswith('/')) and (tag_c[1:] in TAGS)):
						if not plain :
							out += tratta_tag(tag_c,stack,n_riga)
						else:
							out += ''
					else:
						out += '<'+tag_c+'>'
					tag_c = ''
				else :
					#~ if len(tag_c) > 20 :
						#~ raise ImportError('Tag non chiuso alla riga %(n_riga)s' % vars())
					tag_c += ch
			elif ch == '<' :
				tag = True
			else:
				if ch == '\n' :
					n_riga += 1
				out += ch
		
		if stack :
			raise ImportError('Tag non chiuso! stack:%(stack)s' % vars())
		if tag_c :
			raise ImportError('Tag malformato alla fine del file!' % vars())
		#print (repr(out))
		return out
		
	except ImportError, e :
		return str(e)

# -------------------------------------------------------------------- #

def mess_errore(stringa):
	sys.stderr.write( colorize('<red>%s</red>' % stringa) + '\n' )

# ==================================================================== #
#                         FUNZIONI DI INPUT                            #
# ==================================================================== #

def input_timeouted(timeout,prompt='',timeout_str='Tempo scaduto!',plain=False):
	"""Effettua una raw_input che termina restituendo "None" se non e`
	stato dato nessun input per <timeout> secondi."""
	
	if prompt :
		print prompt,
	sys.stdout.flush()
	
	i, o, e = select.select( [sys.stdin], [], [], timeout )
	if (i):
		ret = sys.stdin.readline()
		return ret[:-1]
	else:
		print colorize("<red>%s</red>" % timeout_str, plain=plain)
		return None
	
# -------------------------------------------------------------------- #

def input_timeouted_alt(timeout,prompt='',timeout_str='Tempo scaduto!',plain=False):
	"""Fa la stessa cosa della funzione sopra, ma in un modo diverso.
	Utile per aver un esempio di utilizzo dei segnali."""

	def interrupted(signum, frame):
		"Chiamata quando scade il tempo"
		print colorize("<red>%s</red>" % timeout_str, plain=plain)

	def input():
		try:
			return raw_input(prompt)
		
		except EOFError:
			# timeout
			return None
	
	# Impostazione della funzione che verra` chiamata in caso di SIGALARM
	signal.signal(signal.SIGALRM, interrupted)
	# Settaggio dell'allarme
	signal.alarm(timeout)
	
	s = input()
	
	# Disabilitazione dell'allarme finito cio` che dobbiamo fare
	signal.alarm(0)
	return s

# -------------------------------------------------------------------- #

def conferma_aggiornamento(pard,wait_sec=3600) :
	risp = input_timeouted_alt( wait_sec,
	           prompt="Confermare l'aggiornamento su >%(MYSQL_DB)s< (S/N)? [Entro un massimo di %%s secondi] " % pard % wait_sec,
	           timeout_str="\nTempo scaduto, assunta risposta negativa...", plain=False)
	
	if not risp:
		return False
	
	risp = risp.strip().upper()
	if risp == 'S' :
		return True
	else :
		return False

# ==================================================================== #
#               FUNZIONI VARIE DI VISUALIZZAZIONE                      #
# ==================================================================== #

def hhmmss(secondi,tutto=True):
	"""Restituisce i secondi formattati in ore:minuti:secondi:centesimi
	Se tutto=False non mostra le ore o i minuti se questi non sono presenti"""
	s = ''
	t = time.localtime(secondi)
	hh = t[3] - 1
	if tutto or hh :
		s += '%02d:' % hh
	mm = t[4]
	if tutto or s or mm :
		s += '%02d:' % mm
	ss = t[5]
	s += '%02d.' % ss
	zz = int( round((secondi - int(secondi)),2)*100 )
	if zz == 100 :
		zz = 99
	s += '%02d' % zz
	return s

# -------------------------------------------------------------------- #

def text_diz(diz,k_order=[],k_funz_vis={},evidenz=False,formatta=False,alpha_key_order=False):
	"""
	text_diz(diz:dizionario_o_lista_di_diz, k_order:lista_di_chiavi,
	         k_funz_vis:diz_chiave_funzione,
	         evidenz:bool, formatta:bool) -> stringa
	Espone un dizionario (o una lista di dizionari) testualmente, ritornando
	la stringa risultante
		k_order: ordine delle chiavi.
		k_funz_vis: lista di tuple (chiave, val->str) con gli eventuali campi
			a cui si vuole conferire una funzione specialistica di conversione
			del valore in stringa
		evidenz: evidenzia le chiavi del dizionario con i caratteri speciali
			della bash (utile unicamente nel caso di programmi da terminale)
		formatta: incolonna chiavi e valori
	"""
	
	# Solo per compatibilita`
	if type(diz) == type([]) or type(diz) == type(()) :
		#return render_list_dict( diz, map=(), align='left', sep_on_change=[])
		return '\n\n-----------\n\n'.join( [text_diz(d,k_order=k_order,k_funz_vis=k_funz_vis,evidenz=evidenz,formatta=formatta) for d in diz] )
	
	if not diz:
		return '{}'
	
	text = ''
	
	if alpha_key_order:
		ordered_keys = sorted( diz.keys() )
	else:
		ordered_keys = diz.keys()
	#print ordered_keys
	
	if formatta :
		k_len = max( [ len(repr(k)) for k in ordered_keys ] )
	else :
		k_len = 0
	keys = list(k_order) + filter( lambda x: not x in k_order, ordered_keys )
	
	for k in keys :
		if evidenz :
			chiave = colorize( '<b>%%-%ss</b>' % k_len % repr(k) )
		else :
			chiave = repr(k)
		
		if k in k_funz_vis.keys() :
			val = k_funz_vis[k](diz[k])
		else :
			val = repr(diz[k])
		
		text += '  %%-%ss : %%s ,\n' % k_len % ( chiave, val )
		
	
	return '{' + text[1:-1] + ' }'

# ==================================================================== #

"""
input:
	righe:	lista-di-stringhe (senza \n finale)
			la prima riga intesa come testata
	sep:	separatore di campi da dare in pasto
			a split
	strip_righe: passa ogni riga a fil di .strip()
	strip_all: strippa anche ogni singolo valore / chiave

output:
	(lista-di-stringe, lista-di-dizionari)
		lista-di-stringe:
			e` la lista ordinata dei campi della tabella
		lista-di-dizionari:
			dizionari che han come chiavi la testata della tabella
			e come valori i valori di ciascuna riga
"""
def file2diz(righe, sep=None, strip_righe=True, strip_all=False):
	if not righe:
		return [], []
	
	testata = righe[0]
	if strip_righe:
		campi_testata = testata.strip().split(sep)
	else:
		campi_testata = testata.split(sep)
	
	if strip_all:
		campi_testata = [c.strip() for c in campi_testata]
	
	for i,c in enumerate(campi_testata):
		if c in campi_testata[i+1:]:
			j = 1
			while c in campi_testata:
				z = campi_testata.index(c)
				campi_testata[z] = '%(c)s[%(j)s]'%vars()
				j += 1
	
	l_diz = []
	for n_riga,riga in enumerate(righe):
		# Salto la prima riga
		if n_riga==0:
			continue
		
		if strip_righe:
			campi = riga.strip().split(sep)
		else:
			campi = riga.split(sep)
		
		if len(campi) != len(campi_testata):
			raise ValueError('Riga %d con %d campi anziche` %d' % (n_riga, len(campi), len(campi_testata)) )
		
		diz = {}
		for i,campo in enumerate(campi_testata):
			if strip_all:
				diz[campo.strip()] = campi[i].strip()
			else:	
				diz[campo] = campi[i]
		
		l_diz += [diz]
	
	return campi_testata,l_diz


# #################################################################### #
# FUNZIONE GETCH
# #################################################################### #

#class _Getch:
#	"""Gets a single character from standard input.  Does not echo to the screen."""
#	def __init__(self):
#		try:
#			self.impl = _GetchWindows()
#		except ImportError:
#			self.impl = _GetchUnix()
#
#	def __call__(self): return self.impl()
#
#
#class _GetchUnix:
#	def __init__(self):
#		import tty, sys
#
#	def __call__(self):
#		import sys, tty, termios
#		fd = sys.stdin.fileno()
#		old_settings = termios.tcgetattr(fd)
#		try:
#			tty.setraw(sys.stdin.fileno())
#			ch = sys.stdin.read(1)
#		finally:
#			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#		return ch
#
#
#class _GetchWindows:
#	def __init__(self):
#		import msvcrt
#
#	def __call__(self):
#		import msvcrt
#		return msvcrt.getch()
#
#
#getch = _Getch()

# #################################################################### #
# #################################################################### #

if __name__ == '__main__' :
	f = file('provapippo')
	righe = f.readlines()
	f.close()
	
	campi,results = file2diz(righe, sep='~', strip_righe=True)
	
	print render_list_dict(results,map=campi,align='left',sep_on_change=[],exclude_map=())
	
	if len(sys.argv) == 1 :
		print colorize(STAMPA_DI_PROVA)
	
		foo = input_timeouted(2,prompt='Hai 2 secondi per dir la tua: ',timeout_str="Troppo tardi...",plain=False)
		print repr(foo)
		foo = input_timeouted_alt(2,prompt='Hai 2 secondi per dir la tua: ',timeout_str="Troppo tardi...",plain=False)
		print repr(foo)
	
		ld = [
			{'Ces':10,'Pereppe':'ciobillozzolo','x':'cce'},
			{'x':'cceasd','Ces':15,'Pereppe':'cio'},
			{'Ces':1,'x':'ce','Pereppe':'ciobil'},
			{'Ces':13,'x':'c','Pereppe':'ciobilloz'}
			]
		
		print	
		print render_list_dict(ld)
		print cornice('Debello gallico',width=20,offset=2,align='center')
		print
	
	# ----------------- #
	
	i = 0
	if len(sys.argv) == 2 :
		print cornice(sys.argv[1])
		
	if len(sys.argv) == 3 :
		print cornice(sys.argv[1],int(sys.argv[2]))

	if len(sys.argv) == 4 :
		print cornice(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
