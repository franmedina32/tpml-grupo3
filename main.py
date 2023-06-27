from clases.pelicula import Pelicula
from clases.persona import Persona
#from clases.score import 
from clases.trabajador import Trabajador
from clases.usuario import Usuario
import numpy as np
import pandas as pd


def load_all(file_personas, file_trabajador, file_usuario) : 
    df_persona = Persona.create_df_from_csv(filename=file_personas)
    df_trabajador = Trabajador.create_df_from_csv(filename=file_trabajador)
    df_usuario = Usuario.create_df_from_csv(filename=file_usuario)
    #df_peliculas = Pelicula.create_df_from_csv(filename=file_peliculas)
    #df_scores = 
   

    #filtro usuario validos
    df_usuario_filtrado = df_usuario[df_usuario['id'].isin(df_persona['id'])]
    df_usuario = df_usuario_filtrado

    #filtro trabajadores validos
    df_trabajador_filtrado  =df_trabajador[df_trabajador['id'].isin(df_persona['id'])]
    df_trabajador = df_trabajador_filtrado

    #filtro scores validos

    

    return  df_persona, df_trabajador, df_usuario



def save_all(df_personas, df_trabajadores, df_usuarios, df_peliculas, file_personas, file_trabajadores, file_usuarios, file_peliculas) : 
    try:
        df_personas.to_csv(file_personas, index=False)
        df_trabajadores.to_csv(file_trabajadores, index=False)
        df_usuarios.to_csv(file_usuarios, index=False)
        df_peliculas.to_csv(file_peliculas, index=False)
        #df_scores.to_csv(file_scores, index=False)
        print("Los DataFrames se han guardado exitosamente.")
        return 0 
    except Exception as e:
        print("Se produjo un error al guardar los DataFrames:", str(e))
        return 1





