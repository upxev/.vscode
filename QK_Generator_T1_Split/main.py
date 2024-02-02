
from pickle import FALSE
import Station_Elements as SE
import product_generator as PG
import pandas as pd
import numpy as np
import json
from tqdm import tqdm

def make_df_MS (excel_file_path, sheet_name, range_to_read, lines_to_read):
    # Methode aus Excel Tabelle zu lesen. Mit gegebene sheets_name und range. Vorbereitung fuer die Ersettlung von einzelne Qualitaetsklasse

    # Namen bedinden sich in der Spalte AE

    name_range ='AE'

    df_qualityclass = pd.read_excel(excel_file_path, sheet_name = sheet_name, usecols=range_to_read, skiprows=5 + lines_to_read , nrows=16) #12-->16
    df_name = pd.read_excel(excel_file_path, sheet_name = sheet_name, usecols=name_range, skiprows=2 + lines_to_read , nrows=0)
    produkt_name = df_name.columns.tolist()[0]

    return df_qualityclass, produkt_name

def get_qc_code(excel_file_path, sheet_name):

    df_code = pd.read_excel(excel_file_path, sheet_name = sheet_name)

    return df_code

def make_product_dict_MS(produkt_name, df_qualityclass, Q_code_list):

    new_task = []

    for i in range(16):
        #aktuelle Task Zeile in List Umwandeln insgesamt 12 Zeilen/Tasks #auf 16 erhöht
        task_data = df_qualityclass.iloc[i].tolist() # Daten in Zeile i werden in Liste umgewandelt
        task = task_data[5:] # task data (T1, T2,..) befindet sich in Spalte AC ab Zeile 5
        #print("hier beginnen Tasks")
        #print (task)
        quality_time_elements = []
        quality_class = []
        schrittweite = 5
    	
        if np.isnan(task[1]): # if not a number

            o = -1

            #Wenn die mean Zeit (befindet sich in der List 2. Position) in der Basis t  NaN (Not-aNumber) ist dann wird nur ein Element in der Qualitaetsklasse eingefuegt, capable ist False, weil keine Zeit
            #Kein Task wenn diese in Struktur nicht auftauchen
            '''quality_time_elements.append(SE.element("capable", False))

            for j in range (0, len(task),schrittweite):
                o = o + 1


                quality_class.append(SE.Qualityclass(Q_code_list[o], quality_time_elements))
            quality_time_elements = []'''

        else:
            
            o = -1

            for j in range (0, len(task),schrittweite):
                o = o + 1
                #print (o)
                #quality_time_elements.append(SE.element("capable", True))
         

                single_q_time = task[j:j+schrittweite] 
                #print (single_q_time) # single_q_time: min, mean, max Zeiten
                #quality_time_elements.append(SE.element("op_time", task[i+2]))
                #quality_class.append(SE.Qualityclass(Q_code_list[i],quality_time_elements))
                #quality_time_elements = []

                for k in range (5):
                    if k == 0:
                        quality_time_elements.append(SE.element("min_operation_time", single_q_time[k]/60)) # Zeiten in min
                    elif k == 1:
                        quality_time_elements.append(SE.element("mean_operation_time", single_q_time[k]/60))
                    elif k == 2:
                        quality_time_elements.append(SE.element("max_operation_time", single_q_time[k]/60))
                    elif k == 3:
                        quality_time_elements.append(SE.element("capable", single_q_time[k]))
                    elif k == 4:
                        quality_time_elements.append(SE.element("max_success_probability", single_q_time[k]))

                quality_class.append(SE.Qualityclass(Q_code_list[o],quality_time_elements))
                quality_time_elements = []
              

            #Bauen Task auf
            task_name = produkt_name + "_" + task_data[0]
            new_task.append(SE.task(task_name,quality_class,1))
            #print(task_name) 
    
    station_dict = SE.station("tasks", new_task).to_dict()
    #print(station_dict)


    return station_dict

def make_product_dict_RS(produkt_name, df_qualityclass, Q_code_list):

    new_task = []

    for i in range(16):
        #aktuelle Task Zeile in List Umwandeln insgesamt 12 Zeilen/Tasks
        task_data = df_qualityclass.iloc[i].tolist() # Daten in Zeile i werden in Liste umgewandelt
        task = task_data[18:] #r relevante Daten in MS Task Übersicht liegen ab Spalte 5 vor beginnend bei AC = Spalte 0 # Bei RS Spalte 18
        quality_time_elements = []
        quality_class = []
        schrittweite = 5

       # print (task[1])
        if np.isnan(task[1]): # if not a number

            o = -1

            #Wenn die mean Zeit (befindet sich in der List 2. Position) in der Basis t  NaN (Not-aNumber) ist dann wird nur ein Element in der Qualitaetsklasse eingefuegt, capable ist False, weil keine Zeit
            #Kein Task wenn diese in Struktur nicht auftauchen
            quality_time_elements.append(SE.element("capable", False))

            for j in range (0, len(task),schrittweite):
                o = o + 1


                quality_class.append(SE.Qualityclass(Q_code_list[o], quality_time_elements))
            quality_time_elements = []

        else:
            
            o = -1

            for j in range (0, len(task),schrittweite):
                o = o + 1
                #print (o)
                #quality_time_elements.append(SE.element("capable", True))
         

                single_q_time = task[j:j+schrittweite] 
                #print ("single Q_time ausgabe")
                #print (single_q_time)
                #print (single_q_time) # single_q_time: min, mean, max Zeiten
                #quality_time_elements.append(SE.element("op_time", task[i+2]))
                #quality_class.append(SE.Qualityclass(Q_code_list[i],quality_time_elements))
                #quality_time_elements = []

                for k in range (5):
                    if k == 0:
                        quality_time_elements.append(SE.element("min_operation_time", single_q_time[k]/60))
                    elif k == 1:
                        quality_time_elements.append(SE.element("mean_operation_time", single_q_time[k]/60))
                    elif k == 2:
                        quality_time_elements.append(SE.element("max_operation_time", single_q_time[k]/60))
                    elif k == 3:
                        quality_time_elements.append(SE.element("capable", single_q_time[k]))
                    elif k == 4:
                        quality_time_elements.append(SE.element("max_success_probability", single_q_time[k]))

                quality_class.append(SE.Qualityclass(Q_code_list[o],quality_time_elements))
                quality_time_elements = []

            #Bauen Task auf
            task_name = produkt_name + "_" + task_data[0]
            new_task.append(SE.task(task_name,quality_class,1))
    
    station_dict = SE.station("tasks", new_task).to_dict()
    #print(station_dict)


    return station_dict  

def AS_Read(sheet_name, excel_file_path, Q_code_list, Setting_dict, ressource_dict):
    
    print("AS Start")
    
    #Anzahl der QC und Tasks muss hier angepasst werden
    task_amount = 16 #angepasst
    quality_amount = 16
    df_AS = pd.read_excel(excel_file_path, sheet_name = sheet_name, skiprows = 1, nrows = task_amount * quality_amount + 1).iloc[:, 2:]
    product_name_list = df_AS.columns.tolist()
    AS_dict_temp = {}
  
    #print(df_AS)
    #print (product_name_list)

    task_list_object = []
    with tqdm(total = 100) as pbar:

        for i in range(len(product_name_list)):
        
            temp_product_name = product_name_list[i]
            temp_product = df_AS[temp_product_name]
            quality_class = []
            quality_time_elements = []
            #print (len(temp_product))
            task_nummer = 0
            a = 0
        
            for j in range(1, len(temp_product), quality_amount):
            
                task_nummer = task_nummer + 1

                task_list = temp_product[j:j + quality_amount].tolist()
            
                for k in range(quality_amount):
                
                    if np.isnan(task_list[k]):
                        #Kein Task erzeugen wenn diese Station unter diese Task nicht arbeiten kann!
                        quality_time_elements.append(SE.element("capable", False))
                        quality_time_elements.append(SE.element("max_success_probability", 0)) 
                        quality_time_elements.append(SE.element("mean_operation_time", 999)) 
                    else:
                        quality_time_elements.append(SE.element("capable", True))
                        quality_time_elements.append(SE.element("max_success_probability", 1))
                        quality_time_elements.append(SE.element("mean_operation_time", task_list[k]/60))
                        

                    quality_class.append(SE.Qualityclass(Q_code_list[k], quality_time_elements))
                    quality_time_elements = []

                if quality_class[j].Elements[0].element_value == True or quality_class[j].Elements[0].element_value == False:
                    task_list_object.append(SE.task(temp_product_name + "_T" + str(task_nummer), quality_class, 1))
                    temp_task_dict = {temp_product_name + "_T" + str(task_nummer) : task_list_object[a].to_dict()}
                    a = a+1
                else:
                    print ("Task nicht vorhanden")
                    temp_task_dict = {}
                    # Variabel a ist ein Zaehler

                AS_dict_temp.update(temp_task_dict)
                #print(AS_dict)
            task_list_object = []
            temp_task_dict = {}
            
            pbar.update(100/len(product_name_list))

        
        #Update AS Setting
        AS_dict_temp = {"tasks": AS_dict_temp}
        
        
        Setting_dict.update(ressource_dict)
        Setting_dict.update(AS_dict_temp)
        
        #station = SE.station("AS", task_list_object)
        AS_dict = {"AS":Setting_dict}
        #print (AS_dict)
    

    return AS_dict

def get_AS_Resource(excel_file_path, sheet_name):
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
    AS_Ressource_dict = {}

    
    product_AS_task = df.iloc[:, 0].tolist()
    AS_Resourcen = df.columns[1:].tolist()
    
    for i in range (len(AS_Resourcen)):
        temp_list = df.iloc[:,i + 1].tolist()
        temp_task_list = []
        temp_dict = {}
        
        for k in range (len(product_AS_task)):
            if temp_list[k] == "x":
                temp_task_list.append(product_AS_task[k])
                #print(temp_task_list)
                
        temp_dict = {AS_Resourcen[i]:temp_task_list}
        AS_Ressource_dict.update(temp_dict)
        
    AS_Ressource_dict = {"resource_types" : AS_Ressource_dict}
        
    
    #print(product_AS_task)
    #print(AS_Resourcen)
    
    return AS_Ressource_dict

def read_setting(setting_path, station_name):

    setting_df = pd.read_excel(setting_path, sheet_name= station_name)

    setting_dict = {}

    for i in range(setting_df.shape[0]):

        setting_name = setting_df.iloc[i,0]
        setting_value = setting_df.iloc[i,1]

        # Excel Werte in ben�tigtes JSON Format konvertieren
        # Konvertierung  true/ false Zeichenketten in Boolsche Werte
        if isinstance(setting_value, str):
            setting_value = setting_value.lower()
            
            if setting_value.lower() == "true":
             setting_value = True
     
            elif setting_value.lower() == "false":
             setting_value = False
        
        # Station Agents in Gro�buchstaben
        if setting_name == "station_agent_type":
            setting_value = setting_value.upper()
        
        temp = {}
        temp = {setting_name: setting_value}
        setting_dict.update(temp)

    return setting_dict

def Product_generator(excel_file_path, output_file_path):
    
    quality_dict = PG.dict_qualityclass(excel_file_path)

    products_dict = PG.dict_product(excel_file_path, quality_dict, product_structure_json)
    
    with open(output_file_path, 'w') as json_datei:
        json.dump(products_dict, json_datei, indent=4)



# define Range and amount of Products
excel_file_path_properties = "Input_Excel\QC_Tablle_T1_Split.xlsx"
excel_file_path_products = "Input_Excel/Zuordnung_Produkt.xlsx"
product_structure_json = "Input_Excel/generator_product_structure.json"
setting_file_path = "Input_Excel/Setting.xlsx"
sheet_name_MS = "MS"
sheet_name_AS = "AS"
sheet_name_RS = "RS"
sheet_name_AS_Resource = "AS_Ressource"
range_to_read_MS = 'AC:DI'
range_to_read_RS = 'AC:DV'
#range_to_read_AS = 'D:AP'
amount_products = 39
# bei mehr Produkten muss die Anzahl angepasst werden!
products_dict = {}
output_file_path_properties = "Output_JSON/Initialization_station_properties.json"
output_file_path_products = "Output_JSON/Initialization_products.json"

#pd.set_option('display.max_rows', 20)
#pd.set_option('display.max_columns', 20)
#pd.set_option('display.width', 20)

#df_qualityclass, df_name = make_df(excel_file_path, sheet_name, range_to_read, 0)

#Beginn Zuordnung von Produkten zu ihre Strukturen
Product_generator(excel_file_path_products, output_file_path_products)
#Ende Produkt Zuordnung

# read Setting Excel
MS_Setting_dict = read_setting(setting_file_path, "MS")
AS_Setting_dict = read_setting(setting_file_path, "AS")
RS_Setting_dict = read_setting(setting_file_path, "RS")



df_qc_code = get_qc_code(excel_file_path_properties, "Q_code")
Q_code_list = df_qc_code["Code"].tolist()

#print (Q_code_list)

AS_Ressource_dict = get_AS_Resource(excel_file_path_properties, sheet_name_AS_Resource)
AS_dict = AS_Read(sheet_name_AS, excel_file_path_properties, Q_code_list, AS_Setting_dict, AS_Ressource_dict)



#print("MLS Start")
mls_products_dict = {}
rls_products_dict ={}
for i in range (amount_products):

    lines_to_read = i*21 # i= amount_products, 17 Zeilen pro Produkt werden gelesen # angepasst auf 21

    df_qualityclass, produkt_name = make_df_MS(excel_file_path_properties, sheet_name_MS, range_to_read_MS, lines_to_read)
    #print (df_qualityclass)
    #print (produkt_name + " endet")

    temp_dict = make_product_dict_MS(produkt_name,df_qualityclass, Q_code_list).get("tasks", None)
    mls_products_dict.update(temp_dict)
        
#Update MS_Setting
ms_station_dict = MS_Setting_dict.copy()
ms_station_dict.update({"tasks" : mls_products_dict})

 #print("RLS Start")

for i in range (amount_products):

    lines_to_read = i*21 #angepasst auf 21 

    df_qualityclass, produkt_name = make_df_MS(excel_file_path_properties, sheet_name_RS, range_to_read_RS, lines_to_read)
    

    temp_dict = make_product_dict_RS(produkt_name,df_qualityclass, Q_code_list).get("tasks", None)
    rls_products_dict.update(temp_dict)  

rls_station_dict = RS_Setting_dict.copy()
rls_station_dict.update({"tasks" : rls_products_dict})


station_dict = {"MLS": ms_station_dict, **AS_dict, "RLS": rls_station_dict}
#############Test Code
#RS_Setting_dict.update(station_dict)
#RS_dict = {"RLS" : RS_Setting_dict}
#######################
#station_dict = {"MLS" : station_dict}
#station_dict.update(AS_dict)
##
#station_dict.update(RS_dict)
##


# Erstelle Dummy Dictionary für MS-Station
ms_station = {
    "station_agent_type": "FIFO",
    "p_fail_basic": 0.0,
    "station_breakable": False,
    "MTBF": 999999999,
    "MTOL": 1,
    "CPM_IDLE": 0,
    "CPM_WORKING": 1,
    "CPM_CHANGEOVER": 1,
    "CPM_BROKEN": 1,
    "CPM": 0.2,
    "C_ADD": 10,
    "C_REMOVE": 10,
    "max_number_of_stations": 15,
    "buffer_capacity": 10,
    "task_specific_mounting": False,
    "changeover_time": 0,
    "task_capability": ["T0"]
}

# Füge MS-Station zum station_dict hinzu
station_dict = {"MS": ms_station, **station_dict}

with open(output_file_path_properties, 'w') as json_datei:
    json.dump(station_dict, json_datei, indent=4)

    
with open(output_file_path_properties, 'w') as json_datei:
    json.dump(station_dict, json_datei, indent=4)


