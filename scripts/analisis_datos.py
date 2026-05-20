import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("datos/dataset.csv")
df.head()

#Creo la coleccion de equipos con un set para evitar valores repetidos
equipos = set(df["HomeTeam"]).union(set(df["AwayTeam"]))

#Creo la estructura base con los datos que necesito y lleno con los valores de la coleccion
tabla = {
    equipo: {"puntos": 0, "goles_favor": 0, "goles_contra": 0, "ganados": 0}
    for equipo in equipos
}

#Uso ciclo repetitivo for para completar los datos deseados segun cada valor del dataset
for _, row in df.iterrows():
    local = row["HomeTeam"]
    visitante = row["AwayTeam"]
    goles_local = row["FTHG"]     #FTGH Full Time Home Goals / Goles del equipo local
    goles_visita = row["FTAG"]    #FTAG Full Time Away Goals / Goles del equipo visitante
    resultado = row["FTR"]        #FTR Full Time Result / Resultado final       

    tabla[local]["goles_favor"] += goles_local
    tabla[local]["goles_contra"] += goles_visita
    #Asigno goles al valor correspondiente en cada tabla
    #tabla[X] donde X corresponde a la fila dentro de la tabla

    tabla[visitante]["goles_favor"] += goles_visita
    tabla[visitante]["goles_contra"] += goles_local
    
    #Uso un condicional IF para evaluar el valor del resultado
    #de la fila FTR
    #Resultados posibles: H, A, D
    if resultado == "H":
      tabla[local]["puntos"] += 3
      tabla[local]["ganados"] += 1
    elif resultado == "A":
      tabla[visitante]["puntos"] += 3
      tabla[visitante]["ganados"] += 1
    else:
      tabla[local]["puntos"] += 1
      tabla[visitante]["puntos"] += 1


tabla_posiciones = pd.DataFrame(tabla).T
tabla_posiciones = tabla_posiciones.sort_values(by="puntos", ascending=False)
#Creo la tabla y la ordeno de forma descendente
print(tabla_posiciones)


df["total_goles"] = df["FTHG"] + df["FTAG"]
promedio_goles = df["total_goles"].mean()
print("Promedio de goles por partido:", round(promedio_goles, 2))
#Calculo el promedio de goles por partido sumando 
#los valores de cada fila correspondiente


tabla_posiciones.to_csv("resultados/tabla_posiciones.csv")
#Guardo las posiciones en un nuevo CSV

tabla_posiciones["puntos"].plot(kind="bar", title="Puntos por equipo")
#Grafico de barras usando la columna de puntos
plt.xlabel("Equipos")
#Equipos en las coordenada X
plt.ylabel("Puntos")
#Puntos en la coordenada Y
plt.xticks(rotation=45)

plt.savefig("resultados/grafico_puntos.png")
#Guardo el grafico en formato PNG
plt.show()

