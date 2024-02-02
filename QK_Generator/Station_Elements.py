from typing import List

# Define main Object

class element:
    def __init__(self, element_name:str, element_value):
        self.element_name = element_name

        if element_name == "capable" and element_value == "true":
            element_value = bool(True)
        elif element_name == "capable" and element_value == "false":
            element_value = bool(False)
        
        self.element_value = element_value

    def to_dict(self):
        return {self.element_name: self.element_value}
    
class Qualityclass:
    def __init__(self, name:str, Elements: List[element]):
        self.name = name
        #self.capability = capability
        self.Elements = Elements

    def to_dict(self):
        qualily_dict = {}

        #qualily_dict["capability"] = self.capability,

        for element in self.Elements:
            qualily_dict.update(element.to_dict())
        return qualily_dict

class task:
    def __init__(self, task_name:str, Quality: List[Qualityclass], task_related_success_probability: int):
        self.task_name = task_name
        self.Quality = Quality
        self.task_related_success_probability = task_related_success_probability

    def to_dict(self):
        task_dict = {}
        for quality in self.Quality:
            task_dict.update({quality.name: quality.to_dict()})
        task_dict["task_related_success_probability"] = self.task_related_success_probability
        return task_dict

class station:
    def __init__(self, station_name:str, Tasks: List[task]):
        self.station_name = station_name
        #self.task_capability = task_capability
        self.Tasks = Tasks

    def to_dict(self):
        temp_dict = {}
        #temp_dict["task_capability"] = self.task_capability

        for task in self.Tasks:
            temp_dict.update({task.task_name: task.to_dict()})

        #station_dict = {"tasks": temp_dict}
        return {self.station_name: temp_dict}
    
class products:
    def __init__(self, name, product_id, product_structure):
        self.name = name
        self.product_id = product_id
        self.product_structure = product_structure

    def to_dict(self, quality_dict):
        product_info = {}
        product_id_dict = {"product_id" : self.product_id}
        product_info.update(product_id_dict)
        product_info.update({"product_structure":self.product_structure})
        product_info.update({"quality_classes" : quality_dict})
        
        final_product = {self.name:product_info}

        return final_product

class scrap_rate:
    def __init__(self, name, scrap_rate):
        self.name = name
        self.scrap_rate = scrap_rate

    def to_dict(self):
        scrap_rate_dict = {"unknown_disassembly_tasks":[]}
        scrap_rate_dict.update({"scrap_rate":self.scrap_rate})
        temp_dict = {self.name:scrap_rate_dict}

        return temp_dict