"""
Tasca 5 d'APA: So estéreo y fitxers WAVE.
Autor: Sara Lario Garrido
"""

import struct

def llegir_cabçalera(f):
    """llegeix els 44 bytes de la cabçalera WAVE i en retorna un diccionari."""
    cabçalera_bytes = f.read(44)
    if len(cabçalera_bytes) < 44:
        raise ValueError("El fitxer és massa curt o no és un WAVE vàlid.")
        
    camps = struct.unpack('<4sI4s4sIHHIIHH4sI', cabçalera_bytes)
    
    # Validacions bàsiques de format amb els índexs reals del fitxer
    if camps[0] != b'RIFF' or camps[2] != b'WAVE' or camps[3] != b'fmt ' or camps[11] != b'data':
        raise ValueError("Format de fitxer no reconegut com a format WAVE estàndard.")
        
    return {
        'chunk_size': camps[1], 
        'audio_format': camps[5],     # ARA SÍ: Val 1 (PCM lineal)
        'num_channels': camps[6],     # Val 2 (Estèreo)
        'sample_rate': camps[7],      # Val 16000
        'byte_rate': camps[8],        # Val 64000
        'block_align': camps[9],      # Val 4
        'bits_per_sample': camps[10], # Val 16
        'data_size': camps[12]        # Mida de la música
    }
    

def escriure_cabçalera(f, info):
    """genera i escriu una cabçalera WAVE estàndard de 44 bytes."""
    cabçalera_bytes = struct.pack(
        '<4sI4s4sIHHIIHH4sI',
        b'RIFF', 
        info['chunk_size'], 
        b'WAVE', 
        b'fmt ', 
        16,        # Mida del subcacho fmt (sempre 16 per PCM)
        1,         # AudioFormat: 1 per a PCM lineal
        info['num_channels'], 
        info['sample_rate'], 
        info['byte_rate'], 
        info['block_align'], 
        info['bits_per_sample'], 
        b'data', 
        info['data_size']
    )
    
    f.write(cabçalera_bytes)


def estereo2mono(ficEste, ficMono, canal=2):
    """
    Llegeix un fitxer estèreo de 16 bits i en genera un de mono editable per Windows.
    """
    with open(ficEste, 'rb') as f_in:
        info = llegir_cabçalera(f_in)
        if info['num_channels'] != 2 or info['bits_per_sample'] != 16:
            raise ValueError("El fitxer d'entrada ha de ser estèreo de 16 bits.")
            
        # Llegim totes les mostres de cop
        dades_bytes = f_in.read(info['data_size'])
        num_mostres = len(dades_bytes) // 4  # Cada mostra estèreo de 16 bits són 4 bytes
        
        # Desempaquetem les mostres (2 enters 'h' per cada mostra estèreo)
        mostres = struct.unpack(f'<{num_mostres * 2}h', dades_bytes)
        
        L = mostres[0::2]
        R = mostres[1::2]
        
        if canal == 0:
            mono_mostres = L
        elif canal == 1:
            mono_mostres = R
        elif canal == 2:
            mono_mostres = [(l + r) // 2 for l, r in zip(L, R)]
        elif canal == 3:
            mono_mostres = [(l - r) // 2 for l, r in zip(L, R)]
        else:
            raise ValueError("Canal no vàlid (ha de ser 0, 1, 2 o 3).")
            
    # Ajustem la cabçalera per a 1 sol canal (Mono) de 16 bits
    info['num_channels'] = 1
    info['bits_per_sample'] = 16
    info['block_align'] = 2  # 1 canal * 2 bytes (16 bits)
    info['byte_rate'] = info['sample_rate'] * info['block_align']
    info['data_size'] = num_mostres * 2  # Cada mostra mono de 16 bits ocupa 2 bytes
    info['chunk_size'] = info['data_size'] + 36
    
    with open(ficMono, 'wb') as f_out:
        escriure_cabçalera(f_out, info)
        # Empaquetem com a enters de 16 bits ('h') per a mono
        f_out.write(struct.pack(f'<{num_mostres}h', *mono_mostres))


def mono2estereo(ficIzq, ficDer, ficEste):
    """llegeix dos fitxers mono de 16 bits i en crea un d'estèreo."""
    with open(ficIzq, 'rb') as f_izq, open(ficDer, 'rb') as f_der:
        info_l = llegir_capçalera(f_izq)
        info_r = llegir_capçalera(f_der)
        
        if info_l['num_channels'] != 1 or info_r['num_channels'] != 1:
            raise ValueError("Els fitxers d'origen han de ser monofònics.")
            
        num_mostres = min(info_l['data_size'], info_r['data_size']) // 2
        
        L = struct.unpack(f'<{num_mostres}h', f_izq.read(num_mostres * 2))
        R = struct.unpack(f'<{num_mostres}h', f_der.read(num_mostres * 2))
        
        # Intercalem L i R per fer l'estèreo utilitzant una comprensió de llista plana
        mostres_estèreo = [val for parella in zip(L, R) for val in parella]
        
    info_l['num_channels'] = 2
    info_l['block_align'] = 4  # 2 canals * 2 bytes
    info_l['byte_rate'] = info_l['sample_rate'] * info_l['block_align']
    info_l['data_size'] = num_mostres * 4
    info_l['chunk_size'] = info_l['data_size'] + 36
    
    with open(ficEste, 'wb') as f_out:
        escriure_capçalera(f_out, info_l)
        f_out.write(struct.pack(f'<{num_mostres * 2}h', *mostres_estèreo))


def codEstereo(ficEste, ficCod):
    """codifica un fitxer estèreo de 16 bits en un fitxer mono de 32 bits."""
    with open(ficEste, 'rb') as f_in:
        info = llegir_capçalera(f_in)
        if info['num_channels'] != 2 or info['bits_per_sample'] != 16:
            raise ValueError("Es requereix un fitxer estèreo de 16 bits.")
            
        num_mostres = info['data_size'] // 4
        mostres = struct.unpack(f'<{num_mostres * 2}h', f_in.read(info['data_size']))
        L = mostres[0::2]
        R = mostres[1::2]
        
        # Operacions de desplaçament binari per posar semisuma als 16 bits MSB 
        # i semidiferència als 16 bits LSB. Usem '& 0xFFFF' per evitar problemes amb signes en binari.
        mostres_32 = [
            (((l + r) // 2) << 16) | (((l - r) // 2) & 0xFFFF)
            for l, r in zip(L, R)
        ]
        
    info['num_channels'] = 1
    info['bits_per_sample'] = 32
    info['block_align'] = 4  # 1 canal * 4 bytes
    info['byte_rate'] = info['sample_rate'] * info['block_align']
    info['data_size'] = num_mostres * 4
    info['chunk_size'] = info['data_size'] + 36
    
    with open(ficCod, 'wb') as f_out:
        escriure_capçalera(f_out, info)
        # S'empaqueta com a enters de 4 bytes amb signe ('i')
        f_out.write(struct.pack(f'<{num_mostres}i', *mostres_32))


def decEstereo(ficCod, ficEste):
    """descodifica un fitxer mono de 32 bits en un estèreo de 16 bits reals."""
    with open(ficCod, 'rb') as f_in:
        info = llegir_capçalera(f_in)
        if info['num_channels'] != 1 or info['bits_per_sample'] != 32:
            raise ValueError("Es requereix un fitxer monofònic de 32 bits codificat.")
            
        num_mostres = info['data_size'] // 4
        mostres_32 = struct.unpack(f'<{num_mostres}i', f_in.read(info['data_size']))
        
        # Extraiem semisuma i semidiferència desplaçant bit a bit
        # Un valor estès a 16 bits des d'un enter de 32 requereix desempaquetat manual de signe
        semisuma = [m >> 16 for m in mostres_32]
        semidiferencia = [struct.unpack('<h', struct.pack('<H', m & 0xFFFF))[0] for m in mostres_32]
        
        # Reconstrucció de canals originals: L = S + D; R = S - D
        L = [s + d for s, d in zip(semisuma, semidiferencia)]
        R = [s - d for s, d in zip(semisuma, semidiferencia)]
        
        mostres_estèreo = [val for parella in zip(L, R) for val in parella]
        
    info['num_channels'] = 2
    info['bits_per_sample'] = 16
    info['block_align'] = 4
    info['byte_rate'] = info['sample_rate'] * info['block_align']
    info['data_size'] = num_mostres * 4
    info['chunk_size'] = info['data_size'] + 36
    
    with open(ficEste, 'wb') as f_out:
        escriure_capçalera(f_out, info)
        f_out.write(struct.pack(f'<{num_mostres * 2}h', *mostres_estèreo))