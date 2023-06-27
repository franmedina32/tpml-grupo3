import pandas as pd
import numpy as np

class Persona:
    def __init__(self, nombre, ano_nacimiento, genero,zip_code , id = None):
        self.nombre = nombre
        self.ano_nacimiento = ano_nacimiento
        self.genero = genero
        self.id = id
        self.zip_code = zip_code
    def __repr__(self):
        # Este método debe imprimir la información de esta persona.
        return str(f'Nombre: {self.nombre} \nNacido en: {self.ano_nacimiento} \nGenero: {self.genero}')
    
    
    @classmethod
    def create_df_from_csv(cls, filename):
        # Este class method recibe el nombre de un archivo csv, valida su 
        # estructura y devuelve un DataFrame con la información cargada del
        # archivo 'filename'.
        df_personas = pd.read_csv(f'{filename}')
        return df_personas
    def write_df(self, df_personas,update=False): #para que esta el update? no lo use
        # Este método recibe el dataframe de persona y agrega la persona
        # Si el id es None, toma el id más alto del DF y le suma uno. Si el
        # id ya existe, no la agrega y devuelve un error.
        import numpy as np
        for ids in df_personas.id:
            if self.id == None:
                self.id = df_personas.id.max()+1
                break
            elif ids == self.id:
                self.id = 'este id ya existe'
                break
        if self.id == 'este id ya existe':
            return print('ERROR ID EXISTE')
        else:
            persona_list = list()
            persona_list.append(self.id)
            persona_list.append(self.nombre)
            persona_list.append(self.ano_nacimiento)
            persona_list.append(self.genero)
            persona_list.append(self.zip_code)

            persona_df = pd.DataFrame(data=persona_list).T
            persona_df.columns = df_personas.columns
            df_personas = pd.concat([df_personas,persona_df],ignore_index=True, sort=False)
            return df_personas
            
    
    @classmethod
    def get_from_df(cls, df_personas, id=None, nombre = None, fecha_desde=None,fecha_hasta=None, genero = None):
        # Este class method devuelve una lista de objetos 'Pelicula' buscando por:
        # id: id
        # nombre: nombre de la película
        # anios: [desde_año, hasta_año] lo aprti en dos variables
        # generos: [generos] tiene que ser una lista
        #return lista_peliculas
        df_personas_filt=df_personas

        if id!= None:
            df_personas_filt = df_personas_filt[df_personas_filt['id']==id]
        if nombre!=None:
            df_personas_filt = df_personas_filt[df_personas_filt['Full Name'].str.contains(nombre)]
        if np.logical_and(fecha_desde!=None,fecha_hasta!=None):
            df_personas_filt = df_personas_filt[np.logical_and(df_personas_filt['year of birth']>=fecha_desde,
                                            df_personas_filt['year of birth']<=fecha_hasta)]
        if np.logical_and(fecha_desde!=None,fecha_hasta==None):
            df_personas_filt = df_personas_filt[df_personas_filt['year of birth']>=fecha_desde]
        if np.logical_and(fecha_desde==None,fecha_hasta!=None):
            df_personas_filt = df_personas_filt[df_personas_filt['year of birth']<=fecha_hasta]
        if genero!=None:
            df_personas_filt = df_personas_filt[df_personas_filt['Gender']==genero]

        return df_personas_filt

    @classmethod
    def get_stats(cls,df_personas, anios=None, generos=None):
        # Cantidad de personas por año de nacimiento y Género. Cantidad total de personas
        import matplotlib.pyplot as plt
        if generos!= None:
    
            for n in generos:
                df_personas_filt=df_personas
                df_personas_filt = df_personas_filt[df_personas_filt['Gender']==n]
        
                if anios!= None:
                    df_personas_filt = df_personas_filt[np.logical_and(df_personas_filt['year of birth']>=anios[0],
                                            df_personas_filt['year of birth']<=anios[1])]
                df_personas_filt_max = df_personas_filt[df_personas_filt['year of birth'].max()==df_personas_filt['year of birth']]
                df_personas_filt_min = df_personas_filt[df_personas_filt['year of birth'].min()==df_personas_filt['year of birth']]

                print(df_personas_filt_max)
                print(df_personas_filt_min)
                plt.bar(pd.DataFrame(df_personas_filt.groupby(by='year of birth').count()['Gender']).index,
                        pd.DataFrame(df_personas_filt.groupby(by='year of birth').count()['Gender'])['Gender'])
                plt.title(n)
                plt.show()

    def remove_from_df(self, df_personas):
        # Borra del DataFrame el objeto contenido en esta clase.
        # Para realizar el borrado todas las propiedades del objeto deben coincidir
        # con la entrada en el DF. Caso contrario imprime un error.

        persona_list = list()
        persona_list.append(self.id)
        persona_list.append(self.nombre)
        persona_list.append(self.ano_nacimiento)
        persona_list.append(self.genero)
        persona_list.append(self.zip_code)

        persona_df = pd.DataFrame(data=persona_list).T
        persona_df.columns = df_personas.columns

        merged_df = pd.merge(df_personas,persona_df,how='inner')

        if merged_df['id'].empty:
            return print('ALGO NO COINCIDE')
        else:
            df_personas.drop(index=df_personas[df_personas['id']==merged_df.iloc[0]['id']].index,inplace=True)
            return df_personas    
        


