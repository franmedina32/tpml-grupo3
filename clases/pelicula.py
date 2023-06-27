import pandas as pd
import numpy as np

class Pelicula:
    def __init__(self, nombre, fecha_estreno, generos, id = None):
        self.nombre = nombre
        self.fecha_estreno = fecha_estreno
        self.generos = generos
        self.id = id
    def __repr__(self):
        # Este método debe imprimir la información de esta película.
        return str(f'Titulo: {self.nombre} \nEstreno: {self.fecha_estreno} \nGeneros: {self.generos}')
    @classmethod
    def create_df_from_csv(cls, filename):
        # Este class method recibe el nombre de un archivo csv, valida su 
        # estructura y devuelve un DataFrame con la información cargada del
        # archivo 'filename'.
        df_movie = pd.read_csv(f'{filename}')
        df_movie['Release Date'] = pd.to_datetime(df_movie['Release Date'],format="%d-%b-%Y")
        df_movie.columns = ['id', 'Name', 'Release Date', 'IMDB URL', 'unknown', 'Action',
       'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime',
       'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
       'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
        return df_movie
    def write_df(self, df_movie,update=False): #para que esta el update? no lo use
        # Este método recibe el dataframe de películas y agrega la película
        # Si el id es None, toma el id más alto del DF y le suma uno. Si el
        # id ya existe, no la agrega y devuelve un error.
        import numpy as np
        for ids in df_movie.id:
            if self.id == None:
                self.id = df_movie.id.max()+1
                break
            elif ids == self.id:
                self.id = 'este id ya existe'
                break
        if self.id == 'este id ya existe':
            return print('ERROR ID EXISTE')
        else:
            #trasformo mi data del objeto a una data que pueda usar con el dataframe
            generos_disponibles = ['unknown', 'Action',
            'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime',
            'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
            'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
            peli_genero_list=list()
            for genero in generos_disponibles:
                if self.generos.__contains__(genero) == True:
                    peli_genero_list.append(1)
                elif self.generos.__contains__(genero) == False:
                    peli_genero_list.append(0)
            if np.sum(peli_genero_list) ==0:
                peli_genero_list[0]=1

            peli_list = list()
            peli_list.append(self.id)
            peli_list.append(self.nombre)
            peli_list.append(self.fecha_estreno)
            peli_list.append('')
            for i in peli_genero_list:
                peli_list.append(i)

            peli_df = pd.DataFrame(data=peli_list).T
            peli_df.columns = df_movie.columns
            peli_df['Release Date'] = pd.to_datetime(peli_df['Release Date'],format="%d-%b-%Y")
            df_movie = pd.concat([df_movie,peli_df],ignore_index=True)
            return df_movie
            
    @classmethod
    def get_from_df(cls, df_movie, id=None, nombre = None, fecha_desde=None,fecha_hasta=None, generos = None):
        # Este class method devuelve una lista de objetos 'Pelicula' buscando por:
        # id: id
        # nombre: nombre de la película
        # anios: [desde_año, hasta_año] lo aprti en dos variables
        # generos: [generos] tiene que ser una lista
        #return lista_peliculas
        import numpy as np
        import pandas as pd
        df_movie_filt=df_movie

        if id!= None:
            df_movie_filt = df_movie_filt[df_movie_filt['id']==id]
        if nombre!=None:
            df_movie_filt = df_movie_filt[df_movie_filt['Name'].str.contains(nombre)]
        if np.logical_and(fecha_desde!=None,fecha_hasta!=None):
            df_movie_filt = df_movie_filt[np.logical_and(df_movie_filt['Release Date'].dt.year>=fecha_desde,
                                            df_movie_filt['Release Date'].dt.year<=fecha_hasta)]
        if np.logical_and(fecha_desde!=None,fecha_hasta==None):
            df_movie_filt = df_movie_filt[df_movie_filt['Release Date'].dt.year>=fecha_desde]
        if np.logical_and(fecha_desde==None,fecha_hasta!=None):
            df_movie_filt = df_movie_filt[df_movie_filt['Release Date'].dt.year<=fecha_hasta]
        if generos!= None:
            for n in generos:
                df_movie_filt = df_movie_filt[df_movie_filt[n]==1]

        return df_movie_filt

    @classmethod
    def get_stats(cls,df_movie, anios=None, generos=None):
        # Este class method imprime una serie de estadísticas calculadas sobre
        # los resultados de una consulta al DataFrame df_mov. 
        # Las estadísticas se realizarán sobre las filas que cumplan con los requisitos de:
        # anios: [desde_año, hasta_año]
        # generos: [generos]
        # Las estadísticas son:
        # - Datos película más vieja
        # - Datos película más nueva
        # - Bar plots con la cantidad de películas por año/género.

        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        df_movie_filt=df_movie
        if generos!= None:
            for n in generos:
                df_movie_filt = df_movie_filt[df_movie_filt[n]==1]
                if anios!= None:
                    df_movie_filt = df_movie_filt[np.logical_and(df_movie_filt['Release Date'].dt.year>=anios[0],
                                            df_movie_filt['Release Date'].dt.year<=anios[1])]
                df_movie_filt_max = df_movie_filt[df_movie_filt['Release Date'].max()==df_movie_filt['Release Date']]
                df_movie_filt_min = df_movie_filt[df_movie_filt['Release Date'].min()==df_movie_filt['Release Date']]

                print(df_movie_filt_max)
                print(df_movie_filt_min)

                df_movie_filt['year'] = df_movie_filt['Release Date'].apply(lambda x: x.year)

                plt.bar(pd.DataFrame(df_movie_filt.groupby(by='year').count()[n]).index,
                        pd.DataFrame(df_movie_filt.groupby(by='year').count()[n])[n])
                plt.title(n)
                plt.show()

    def remove_from_df(self, df_movie):
        # Borra del DataFrame el objeto contenido en esta clase.
        # Para realizar el borrado todas las propiedades del objeto deben coincidir
        # con la entrada en el DF. Caso contrario imprime un error.
        import numpy as np
        import pandas as pd
        generos_disponibles = ['unknown', 'Action',
        'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime',
        'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
        'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
        peli_genero_list=list()
        for genero in generos_disponibles:
            if self.generos.__contains__(genero) == True:
                peli_genero_list.append(1)
            elif self.generos.__contains__(genero) == False:
                peli_genero_list.append(0)
        if np.sum(peli_genero_list) ==0:
            peli_genero_list[0]=1
        peli_list = list()
        peli_list.append(self.id)
        peli_list.append(self.nombre)
        peli_list.append(self.fecha_estreno)
        peli_list.append('')
        for i in peli_genero_list:
            peli_list.append(i)

        peli_df = pd.DataFrame(data=peli_list).T
        peli_df.columns = df_movie.columns
        peli_df['Release Date'] = pd.to_datetime(peli_df['Release Date'],format="%d-%b-%Y")

        merged_df = pd.merge(df_movie,peli_df,how='inner')

        if merged_df['id'].empty:
            return print('ALGO NO COINCIDE')
        else:
            df_movie.drop(index=df_movie[df_movie['id']==merged_df.iloc[0]['id']].index,inplace=True)
            return df_movie 