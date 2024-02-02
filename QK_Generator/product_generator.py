import pandas as pd
import json
import Station_Elements as SE

def read_excel_data_products(file_path):
    df = pd.read_excel(file_path, sheet_name=0) #lesen des 1. Arbeitsblatts products in Zuordnung_Produkt.excel

    names = df.iloc[:, 0].tolist()
    product_ids = df.iloc[:,1].tolist()
    structure_type = df.iloc[:, 2].tolist()

    return names, product_ids, structure_type # Daten aus Excel werden in DataFrame geladen und spezifische Spalten in Listen kovertiert

def read_ecel_data_qualityclass(file_path):
    df = pd.read_excel(file_path, sheet_name=1) #lesen des 2. Arbeitsblatts quality class in Zuordnung_Produkt.excel

    names = df.iloc[:,0].tolist()

    return names

def read_excel_code_qualityclass(file_path):
    df = pd.read_excel(file_path, sheet_name=2) #lesen des 3. Arbeitsblatts QC_Code in Zuordnung_Produkt.excel
    codes = df.iloc[:,0].tolist()
    
    return codes

def json_read (file_path):

    with open (file_path, 'r') as json_data: #lesen generator_product_structure.json
        data = json.load(json_data)

    return data

def dict_qualityclass(excel_file_path):
    station_name = ["MLS", "RLS", "AS"]
    quality_dict = {}
    #hier werden alle mögliche Kombination der Qualitätsklassen zusammengestellt
    single_quality_name = read_ecel_data_qualityclass(excel_file_path)
    
    ## Testen
    quality_code_list = read_excel_code_qualityclass(excel_file_path)
    
    mix_quality_2 = set() #Kombination aus 2 Qualitätsklassen
    mix_quality_3 = set() #Kombination aus 3 Qulalitätsklassen
    mix_quality_4 = set() #Kombination aus 4 Qualitätsklassen
    

    #Erstellung Kombination aus 2-4 Qualitätsklassen
    for i in range(len(single_quality_name)): 
        for j in range(i + 1, len(single_quality_name)):
            combined_name = single_quality_name[i] + " + " + single_quality_name[j]
            for k in range(j + 1, len(single_quality_name)):
                combined_name = combined_name + " + " + single_quality_name[k]
                for p in range (k + 1, len(single_quality_name)):
                    combined_name = combined_name + " + " + single_quality_name[p]
                mix_quality_4.add(combined_name)

    for i in range(len(single_quality_name)):
        for j in range(i + 1, len(single_quality_name)):
            combined_name = single_quality_name[i] + " + " + single_quality_name[j]
            for k in range(j + 1, len(single_quality_name)):
                combined_name = combined_name + " + " + single_quality_name[k]
                mix_quality_3.add(combined_name)

    # Schleife, um die Kombinationen zu erstellen
    for i in range(len(single_quality_name)):
        for j in range(i + 1, len(single_quality_name)):
            combined_name = single_quality_name[i] + " + " + single_quality_name[j]
            mix_quality_2.add(combined_name)

    quality_name_list = single_quality_name + list(mix_quality_2) + list(mix_quality_3) + list(mix_quality_4)
    #print (quality_name_list)
    
# neu zum Testen Codieren von QC
    
    

    for j in range(len(station_name)):

        for i in range(len(quality_code_list)):

            temp_quality = SE.scrap_rate(quality_code_list[i], 0.7)
            quality_dict.update(temp_quality.to_dict())

    #print (temp_dict)

    return quality_dict

def dict_product(excel_file_path, quality_dict, structure_file_path):
    names, product_ids, structure_type = read_excel_data_products(excel_file_path)
    structure = json_read(structure_file_path)
    products_dict = {}

    for i in range(len(names)):
        name = names[i]
        product_id = product_ids[i]
        search_typ = structure_type[i]

        if search_typ in structure: #Prüfen ob Strukturtyp (aus Excel) in generator_product_structure.Json vorhanden ist
            typ_tree = structure[search_typ] #type tree entspricht nun structure_type[i]
            print(i)
            #print (products_dict)
            #print (typ_tree)

            temp_product = SE.products(name, product_id, typ_tree)
            temp_product_dict = temp_product.to_dict(quality_dict)

            #temp_product_dict.update({"quality_classes" : quality_dict})
            #print (temp_product_dict)
            #print (temp_product_dict)

            products_dict.update(temp_product_dict)
            #print (products_dict)
            #products_dict.update({"quality_classes" : quality_dict})

        else:
            print ("Fehler_Product_Typ nicht bekannt! Produkt:" + name)

    products_dict = {"products":products_dict}

    return products_dict