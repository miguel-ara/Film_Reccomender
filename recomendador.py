import pandas as pd
import re

def extract(): # Extrae los datos del csv
    return pd.read_csv("movies.csv", sep = ";", encoding = "UTF-8")

def transform(df):
    # No es necesario seleccionar columnas. Podriamos hacerlo con  un pd.drop(columns=["title"], inplace = True), y poner ahí las que quiero quitar.
   
    df["date"] = df.apply(lambda row : sacar_fecha(row["title"]), axis = 1)         # Creamos una nueva columna con el año de estreno de cdada peli
    df = df.sort_values("date")                                                     # Ordenamos el dataframe por año de estreno de la película.
    df["title"] = df.apply(lambda row : eliminar_fecha(row["title"]), axis = 1)     # Eliminamos el año de estreno del título de la película.
    df["genres"] = df.apply(lambda row : procesar_generos(row["genres"]), axis = 1) # Quitamos el separador | de la columna de los géneros.
    return df

def recomendar(df):
    filtro = menu() # Menú devuelve 1 para buscar por título, 2 para buscar por género, 3 para buscar por año de estreno, según lo que elija el usuario.
    
    if filtro == 1:
        repetir = True
        i = 0
        while repetir:
            df_pelis = df.copy(deep = True) # Copiamos el dataframe original para no modificarlo
            if i == 0:                      # Solo imprimimos esto si es la primera vez que el usuario introduce el nombre de la peli
                print("\nHa elegido buscar por título de la película") # Si se ha equivocado poniéndolo, no se imprime de nuevo.
            pelicula = input("Por favor, introduzca EN INGLÉS el título de la película o una palabra del titulo: ")
            regex = re.compile(pelicula, flags = re.I) # Expresión regular ignorando las mayúsculas.
            df_pelis["title"] = df_pelis.apply(lambda row : buscar_peli_df(row["title"], regex), axis = 1) # Aplicamos una función línea por línea del dataframe que busque la expresión regular
            data = df_pelis[df_pelis["title"] != False] # Nos quedamos solo con los datos que contengan esa expresión regular.
            if not data.empty: # Si el nuevo dataframe contiene pelis, salimos del bucle.
                repetir = False
            else:              # Si está vacío, se lo indicamos al usuario y le preguntamos por otra peli.
                print(f"\nLa película '{pelicula}' no se ha encontrado en el archivo, inserte el nombre de otra por favor")
    
    elif filtro == 2: # Mismo procedimieto que el apartado anterior pero para buscar por género.
        repetir = True
        i = 0
        while repetir:
            df_generos = df.copy(deep = True)
            if i == 0:
                print("\nHa elegido buscar por género de la película")
            i += 1
            print("Posibles géneros: Action, Adventure, Animation, Children's, Comedy, Crime, Documentary, Drama, Fantasy, Film-Noir, Horror, Musical, Mystery, Romance, Sci-Fi, Thriller, War, Western\n")
            genero = input("Por favor, introduzca EN INGLÉS el género de la película ")
            regex = re.compile(genero, re.I)
            df_generos["genres"] = df_generos.apply(lambda row : buscar_peli_df(row["genres"], regex), axis = 1)
            data = df_generos[df_generos["genres"] != False]
            if not data.empty:
                repetir = False
            else:
                print(f"\nEl género '{genero}' no se encuentra entre los géneros disponibles, inserte otro por favor")
    
    elif filtro == 3: # Mismo procedimiento para buscar por año de estreno.
        repetir = True
        i = 0
        while repetir:
            df_fecha = df.copy(deep = True)
            if i == 0:
                print("\nHa elegido buscar por año de estreno de la película")
            i += 1
            fecha = input("Por favor, introduzca el año de estreno de la película ")
            regex = re.compile(fecha)
            df_fecha["date"] = df_fecha.apply(lambda row : buscar_peli_df(row["date"], regex), axis = 1)
            data = df_fecha[df_fecha["date"] != False]
            if not data.empty:
                repetir = False
            else:
                print(f"\nNo se ha encontrado ninguna película estrenada en el año {fecha}, inserte otro año por favor")
        
    return data

def load(data): # Carga en un csv los datos de la recomendación obtenida y los imprime por pantalla.
    data.to_csv("Resultado_recomendacion.csv", sep = ";")
    print("\n", data)

def sacar_fecha(str):
    lista = re.findall("\([0-9][0-9][0-9][0-9]\)", str) # Devuelve una lista con un número de la forma ["(1998)"]
    # re.sub("\W", "", str(lista)) 
    # Con esto queríamos eliminar todo lo que no fueran números para dejar 1998, pero no me deja pasar la lista a string
    if lista:
        return "".join(lista) # He decidido hacer un .join de la lista, que devuelve el string (1998), así queda más visual que con la lista ["(1998)"]
    else:
        return "Not known"

def eliminar_fecha(str): # Quita la fecha de un string con un re.sub
    return re.sub(" \([0-9][0-9][0-9][0-9]\)", "", str)

def procesar_generos(str): # Quita el separador | de los géneros
    return re.sub("[|]", " ", str)

def buscar_peli_df(str, regex): # Busca una regex en un string
    if re.findall(regex, str):
        return str
    else:
        return False

def menu(): # Menú interactivo, para preguntar al usuario la característica de filtrado.
    print("\nPosibles filtrados del recomendador de películas:\n1) Por título (se devolverán las películas)\n2) Por género (se devolverán películas de ese género)\n3) Por año de estreno (se devolverán películas de ese año)\n")
    filtro = input("¿Por qué característica le gustaría buscar? (introduzca el número correspondiente) ")
    while filtro not in ["1", "2", "3"]:
        print("Por favor, introduzca una opción correcta")
        filtro = input("¿Por qué característica le gustaría buscar? (introduzca el número correspondiente) ")
        print()
    return int(filtro)

if __name__ == "__main__":
    df_pelis = extract()
    df_transformado = transform(df_pelis)
    data = recomendar(df_transformado)
    load(data)
    
