# Sonido estéreo y ficheros WAVE

## Nom i cognoms

> [!Important]
> Introduzca a continuación su nombre y apellidos: 
>
> Sara Lario Garrido

## Aviso Importante

> [!Caution]
> 
> El objetivo de esta tarea es manejar la lectura y escritura de ficheros binarios. Para ello, sólo se
> permite el uso de las funciones de la biblioteca `struct`. Aunque existen distintas bibliotecas que
> permiten manejar los ficheros WAVE de una manera más eficiente y sencilla, su uso está prohibido.
>
> ¿Quiere saber más?, consulte con el profesorado.

## Fecha de entrega: 24 de mayo a medianoche

## El formato WAVE

El formato WAVE es uno de los más extendidos para el almacenamiento y transmisión
de señales de audio. En el fondo, se trata de un tipo particular de fichero
[RIFF](https://en.wikipedia.org/wiki/Resource_Interchange_File_Format) (*Resource
Interchange File Format*), utilizado no sólo para señales de audio sino también para señales de
otros tipos, como las imágenes estáticas o en movimiento, o secuencias MIDI (aunque, en el caso
del MIDI, con pequeñas diferencias que los hacen incompatibles).

La base de los ficheros RIFF es el uso de *cachos* (*chunks*, en inglés). Cada cacho,
o subcacho, está encabezado por una cadena de cuatro caracteres ASCII, que indica el tipo del cacho,
seguido por un entero sin signo de cuatro bytes, que indica el tamaño en bytes de lo que queda de
cacho sin contar la cadena inicial y el propio tamaño. A continuación, y en función del tipo de
cacho, se colocan los datos que lo forman.

Todo fichero RIFF incluye un primer cacho que lo identifica como tal y que empieza por la cadena
`'RIFF'`. A continuación, después del tamaño del cacho y en otra cadena de cuatro caracteres,
se indica el tipo concreto de información que contiene el fichero. En el caso concreto de los
ficheros de audio WAVE, esta cadena es igual a `'WAVE'`, y el cacho debe contener dos
*subcachos*: el primero, de nombre `'fmt '`, proporciona la información de cómo está
codificada la señal. Por ejemplo, si es PCM lineal, ADPCM, etc., o si es monofónica o estéreo. El
segundo subcacho, de nombre `'data'`, incluye las muestras de la señal.

Dispone de una descripción detallada del formato WAVE en la página
[WAVE PCM soundfile format](http://soundfile.sapp.org/doc/WaveFormat/) de Soundfile.

## Audio estéreo

La mayor parte de los animales, incluidos los del género *homo sapiens sapiens* sanos y completos,
están dotados de dos órganos que actúan como transductores acústico-sensoriales (es decir, tienen dos
*oídos*). Esta duplicidad orgánica permite al bicho, entre otras cosas, determinar la dirección de
origen del sonido. En el caso de la señal de música, además, la duplicidad proporciona una sensación
de *amplitud espacial*, de realismo y de confort acústico.

En un principio, los equipos de reproducción de audio no tenían en cuenta estos efectos y sólo permitían
almacenar y reproducir una única señal para los dos oídos. Es el llamado *sonido monofónico* o
*monoaural*. Una alternativa al sonido monofónico es el *estereofónico* o, simplemente, *estéreo*. En
él, se usan dos señales independientes, destinadas a ser reproducidas a ambos lados del oyente: los
llamados *canal izquierdo* (**L**) y *derecho* (**R**).

Aunque los primeros experimentos con sonido estereofónico datan de finales del siglo XIX, los primeros
equipos y grabaciones de este tipo no se popularizaron hasta los años 1950 y 1960. En aquel tiempo, la
gestión de los dos canales era muy rudimentaria. Por ejemplo, los instrumentos se repartían entre los
dos canales, con unos sonando exclusivamente a la izquierda y el resto a la derecha. Es el caso de las
primeras grabaciones en estéreo de los Beatles: las versiones en alemán de los singles *She loves you*
y *I want to hold your hand*. Así, en esta última (de la que dispone de un fichero en Atenea con sus
primeros treinta segundos, [Komm, gib mir deine Hand](wav/komm.wav)), la mayor parte de los instrumentos
suenan por el canal derecho, mientras que las voces y las características palmas lo hacen por el izquierdo.

Un problema habitual en los primeros años del sonido estereofónico, y aún vigente hoy en día, es que no
todos los equipos son capaces de reproducir los dos canales por separado. La solución comúnmente
adoptada consiste en no almacenar cada canal por separado, sino en la forma semisuma, $(L+R)/2$, y
semidiferencia, $(L-R)/2$, y de tal modo que los equipos monofónicos sólo accedan a la primera de ellas.
De este modo, estos equipos pueden reproducir una señal completa, formada por la suma de los dos
canales, y los estereofónicos pueden reconstruir los dos canales estéreo.

Por ejemplo, en la radio FM estéreo, la señal, de ancho de banda 15 kHz, se transmite del modo siguiente:

- En banda base, $0\le f\le 15$ kHz, se transmite la suma de los dos canales, $L+R$. Esta es la señal
  que son capaces de reproducir los equipos monofónicos.

- La señal diferencia, $L-R$, se transmite modulada en amplitud con una frecuencia de portadora
  $f_m = 38$ kHz.

  - Por tanto, ocupa la banda $23 \mathrm{kHz}\le f\le 53 \mathrm{kHz}$, que sólo es accedida por los
    equipos estéreo, y, en el caso de colarse en un reproductor monofónico, ocupa la banda no audible.

- También se emite una sinusoide de $19 \mathrm{kHz}$, denominada *señal piloto*, que se usa para
  demodular síncronamente la señal diferencia.

- Finalmente, la señal de audio estéreo puede acompañarse de otras señales de señalización y servicio en
  frecuencias entre $55.35 \mathrm{kHz}$ y $94 \mathrm{kHz}$.

En los discos fonográficos, la semisuma de las señales está grabada del mismo modo que se haría en una
grabación monofónica, es decir, en la profundidad del surco; mientras que la semidiferencia se graba en el
desplazamiento a izquierda y derecha de la aguja. El resultado es que un reproductor mono, que sólo atiende
a la profundidad del surco, reproduce casi correctamente la señal monofónica, mientras que un reproductor
estéreo es capaz de separar los dos canales. Es posible que algo de la información de la semisuma se cuele
en el reproductor mono, pero, como su amplitud es muy pequeña, se manifestará como un ruido muy débil,
apenas perceptible.

En general, todos estos sistemas se basan en garantizar que el reproductor mono recibe correctamente la
semisuma de canales y que, si algo de la semidiferencia se cuela en la reproducción, sea en forma de un
ruido inaudible.

## Tareas a realizar

Escriba el fichero `estereo.py` que incluirá las funciones que permitirán el manejo de los canales de una
señal estéreo y su codificación/decodificación para compatibilizar ésta con sistemas monofónicos.


### Manejo de los canales de una señal estéreo

En un fichero WAVE estéreo con señales de 16 bits, cada muestra de cada canal se codifica con un entero de
dos bytes. La señal se almacena en el *cacho* `'data'` alternando, para cada muestra de $x[n]$, el valor
del canal izquierdo y el derecho:

<img src="img/est%C3%A9reo.png" width="380px">

#### Función `estereo2mono(ficEste, ficMono, canal=2)`

La función lee el fichero `ficEste`, que debe contener una señal estéreo, y escribe el fichero `ficMono`,
con una señal monofónica. El tipo concreto de señal que se almacenará en `ficMono` depende del argumento
`canal`:

- `canal=0`: Se almacena el canal izquierdo $L$.
- `canal=1`: Se almacena el canal derecho $R$.
- `canal=2`: Se almacena la semisuma $(L+R)/2$. Ha de ser la opción por defecto.
- `canal=3`: Se almacena la semidiferencia $(L-R)/2$.

#### Función `mono2estereo(ficIzq, ficDer, ficEste)`

Lee los ficheros `ficIzq` y `ficDer`, que contienen las señales monofónicas correspondientes a los canales
izquierdo y derecho, respectivamente, y construye con ellas una señal estéreo que almacena en el fichero
`ficEste`.

### Codificación estéreo usando los bits menos significativos

En la línea de los sistemas usados para codificar la información estéreo en señales de radio FM o en los
surcos de los discos fonográficos, podemos usar enteros de 32 bits para almacenar los dos canales de 16 bits:

- En los 16 bits más significativos se almacena la semisuma de los dos canales.

- En los 16 bits menos significativos se almacena la semidiferencia.

Los sistemas monofónicos sólo son capaces de manejar la señal de 32 bits. Esta señal es prácticamente
idéntica a la señal semisuma, ya que la semisuma ocupa los 16 bits más significativos. La señal
semidiferencia aparece como un ruido añadido a la señal, pero, como su amplitud es $2^{16}$ veces más
pequeña, será prácticamente inaudible (la relación señal a ruido es del orden de 90 dB).

Los sistemas estéreo son capaces de aislar las dos partes de la señal y, con ellas, reconstruir los dos
canales izquierdo y derecho.

<img src="img/est%C3%A9reo_cod.png" width="510px">

#### Función `codEstereo(ficEste, ficCod)`

Lee el fichero `ficEste`, que contiene una señal estéreo codificada con PCM lineal de 16 bits, y
construye con ellas una señal codificada con 32 bits que permita su reproducción tanto por sistemas
monofónicos como por sistemas estéreo preparados para ello.

#### Función `decEstereo(ficCod, ficEste)`

Lee el fichero `ficCod` con una señal monofónica de 32 bits en la que los 16 bits más significativos
contienen la semisuma de los dos canales de una señal estéreo y los 16 bits menos significativos la
semidiferencia, y escribe el fichero `ficEste` con los dos canales por separado en el formato de los
ficheros WAVE estéreo.

### Entrega

#### Fichero `estereo.py`

- El fichero debe incluir una cadena de documentación que incluirá el nombre del alumno y una descripción
  del contenido del fichero.

- Es muy recomendable escribir, además, sendas funciones que *empaqueten* y *desempaqueten* las cabeceras
  de los ficheros WAVE a partir de los datos contenidos en ellas.

- Aparte de `struct`, no se puede importar o usar ningún módulo externo.

- Se deben evitar los bucles. Se valorará el uso, cuando sea necesario, de *comprensiones*.

- Los ficheros se deben abrir y cerrar usando gestores de contexto.

- Las funciones deberán comprobar que los ficheros de entrada tienen el formato correcto y, en caso
  contrario, elevar la excepción correspondiente.

- Los ficheros resultantes deben ser reproducibles correctamente usando cualquier reproductor estándar;
  por ejemplo, el Windows Media Player o similar. Es probable, muy probable, que tenga que modificar los
  datos de las cabeceras de los ficheros para conseguirlo.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el uso de los estándares
  marcados por PEP-ocho.

#### Comprobación del funcionamiento

Es responsabilidad del alumno comprobar que las distintas funciones realizan su cometido de manera correcta.
Para ello, se recomienda usar la canción [Komm, gib mir deine Hand](wav/komm.wav), suminstrada al efecto.
De todos modos, recuerde que, aunque sea en alemán, se trata de los Beatles, así que procure no destrozar
innecesariamente la canción.

#### Código desarrollado

```python
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
```

##### Código de `estereo2mono()`

```python
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
```

##### Código de `mono2estereo()`

```python
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
```

##### Código de `codEstereo()`

```python
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
```

##### Código de `decEstereo()`

```python
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
```

#### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y visualizarse correctamente en
el repositorio, incluyendo el realce sintáctico del código fuente insertado.
