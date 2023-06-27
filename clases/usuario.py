from clases.persona import Persona
import pandas as pd
import numpy as np

class Usuario(Persona) :
    def __init__(self, nombre, ano_nacimiento, genero, zip_code, id=None, ocupacion=None, fecha_alta=None):
        super().__init__(nombre, ano_nacimiento, genero, zip_code, id)
        self.ocupacion = ocupacion
        self.fecha_alta = fecha_alta

    def __repr__(self):
        # devuelve una string con informacion de la instancia
        return str(f'nombre: {self.nombre}, ocupacion: {self.ocupacion}, fecha de alta: {self.fecha_alta}')
    
    @classmethod
    def create_df_from_csv(cls, filename) :
        # este class method devuelve el dataframe que se le indica como parametro
        df_usuarios = pd.read_csv(filename)
        return df_usuarios

    def write_df(self, df_usuario, df_persona) :
        #recibe los dataframes usuario y persona, agrega un usuario al dataframe persona y 
        # agrega un usuario al data frame usuario con el mismo id que la persona que fue creada previamente 
        persona = Persona(self.nombre, self.ano_nacimiento, self.genero, self.zip_code)
        df_persona = persona.write_df(df_personas=df_persona)
        nuevo_id = persona.id
        #stored_persona = Persona.get_from_df(self.nombre, self.fecha_alta)

        usuario = pd.DataFrame([{'id': nuevo_id, 'Occupation': self.ocupacion, 'Active Since': self.fecha_alta}])
        df_usuario = pd.concat([df_usuario, usuario], ignore_index=True, sort=False)
        return df_persona, df_usuario

    @classmethod
    def get_from_df(cls, df_usuario, id=None, ocupacion=None , fechas_alta=None) :
        #devuelve del data frame users todas las rows que coincidan con los atributos que se pasen como parametros
        #si alguno de los atributos es nulo no se filtra a traves del mismo

        if id:
            df_usuario = df_usuario.query('id == ' + str(id))
        if ocupacion:
            df_usuario = df_usuario.query(f"Occupation == '{ocupacion}'")
        if fechas_alta:
            df_usuario = df_usuario.loc[(df_usuario['Active Since'] >= fechas_alta[0]) & (df_usuario['Active Since'] <= fechas_alta[1])]
        return df_usuario


    @classmethod
    def get_stats(cls, df_user, puesto = None) :
        # cantidad de usuario por ocupacion
        if puesto != None : 
            filtered_employees = df_user[df_user['Occupation'] == puesto]
            return len(filtered_employees)


    
    def remove_from_df(self, df_usuario, df_persona):
        """
        Borra del DataFrame el objeto contenido en esta clase.
        obtengo la persona primero para conocer el id
        """
        persona = Persona.get_from_df(df_persona,id = self.id, nombre=self.nombre, fecha_desde = self.ano_nacimiento, fecha_hasta = self.ano_nacimiento, genero = self.genero)
        if persona.empty:
            print(f'error, no existe una persona con que coincida con la informacion provista')
        else:
            df_usuario = df_usuario.drop(df_usuario[df_usuario['id'] == self.id].index)
            df_persona = df_persona.drop(df_persona[(df_persona['Full Name'] == self.nombre) & (df_persona['year of birth'] == self.ano_nacimiento)].index)

        return df_usuario, df_persona
    

    def see_dataform_from_df(self, df_user, df_persona):
        """
        Borra del DataFrame el objeto contenido en esta clase.
        obtengo la persona primero para conocer el id
        """
        persona = Persona.get_from_df(df_persona,id = self.id, nombre=self.nombre, fecha_desde = self.ano_nacimiento, fecha_hasta = self.ano_nacimiento, genero = self.genero)
        if persona.empty:
            print(f'error, no existe una persona con que coincida con la informacion provista')
        else:
            idU = df_user[df_user['id'] == self.id].index
            print(idU)
            print(type(idU))
            #f_user = df_user.drop(df_user[df_user['id'] == int(self.id)].index)
            #df_persona = df_persona.drop(df_persona[(df_persona['Full Name'] == self.nombre) & (df_persona['year of birth'] == self.ano_nacimiento)].index)

        return f'el valor del id: {self.id}'



    

    
