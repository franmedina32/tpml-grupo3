from clases.persona import Persona
import pandas as pd
import numpy as np

class Trabajador(Persona) :
    def __init__(self, nombre, ano_nacimiento, genero, zip_code, id=None, fecha_alta=None, puesto=None, categoria=None, horario_laboral=None):
        super().__init__(nombre, ano_nacimiento, genero, zip_code, id) 
        self.fecha_alta = fecha_alta
        self.puesto = puesto
        self.categoria = categoria
        self.horario_laboral = horario_laboral

    def __repr__(self):
        return str(f'nombre: {self.nombre} || fecha de alta: {self.fecha_alta} || puesto: {self.puesto} || categoria: {self.categoria} || horario: {self.horario_laboral}')

    @classmethod
    def create_df_from_csv(cls, filename) :
        # este class method devuelve el dataframe que se le indica como parametro
        df_trabajadores = pd.read_csv(filename)
        return df_trabajadores

    def write_df(self, df_trabajador, df_persona) :
        #recibe los dataframes trabajador y persona, agrega una persona al dataframe persona y 
        # agrega un trabajador al df trabajador con el mismo id que la persona que fue creada previamente 
        persona = Persona(self.nombre, self.ano_nacimiento, self.genero, self.zip_code)
        df_persona = persona.write_df(df_personas=df_persona)
        nuevo_id = persona.id

        trabajador = pd.DataFrame([{'id': nuevo_id, 'Position': self.puesto, 'Category': self.categoria, 'Working Hours': self.horario_laboral, 'Start Date': self.fecha_alta}])
        df_trabajador= pd.concat([df_trabajador, trabajador], ignore_index=True, sort=False)
        return df_persona, df_trabajador

    @classmethod
    def get_from_df(cls, df_trabajadores, id=None, puesto=None, fecha_alta=None, categoria=None, horario_laboral=None) :
        #devuelve del data frame trabajadores todas las rows que coincidan con los atributos que se pasen como parametros
        #si alguno de los atributos es nulo no se filtra a traves del mismo
        if id :
            df_trabajadores = df_trabajadores.query('id == ' + str(id))

        if categoria :
            df_trabajadores = df_trabajadores.query('Category == ' + str(categoria))

        if puesto :
            df_trabajadores = df_trabajadores.query('Position == ' + str(puesto))
        
        if fecha_alta :
            df_trabajadores = df_trabajadores.query('Start Date == ' + str(fecha_alta))

        if horario_laboral :
            df_trabajadores = df_trabajadores.query('Working Hours == ' + str(horario_laboral))

        return df_trabajadores


    @classmethod
    def get_stats(cls, df_trabajador, puesto = None) :
        # horas trabajados promedio por puesto de trabajo
        if puesto != None :
            filtered_employees = df_trabajador[df_trabajador['Position']== puesto]
            average_hours = filtered_employees['Working Hours'].mean()
            return average_hours
        else :
            print("error: por favor indicar puesto")


        
        

    def remove_from_df(self, df_trabajador, df_persona) :
        #borra la persona y el trabajador que coincidan con la informacion provista
        persona = Persona.get_from_df(df_persona,id = self.id, nombre=self.nombre, fecha_desde = self.ano_nacimiento, fecha_hasta = self.ano_nacimiento, genero = self.genero)
        if persona.empty : 
            print(f'error, no existe una persona con que coincida con la informacion provista')
        else :
            df_trabajador = df_trabajador.drop(df_trabajador[df_trabajador['id'] == self.id].index)
            df_persona = df_persona.drop(df_persona[(df_persona['Full Name'] == self.nombre) & (df_persona['year of birth'] == self.ano_nacimiento)].index)
        
        return df_trabajador, df_persona
    

