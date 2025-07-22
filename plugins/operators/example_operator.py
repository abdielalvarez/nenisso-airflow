# Example Custom Operator
from airflow.models.baseoperator import BaseOperator

class ExampleOperator(BaseOperator):
    def __init__(self, service_name, **kwargs):
        super().__init__(**kwargs)
        self.service_name = service_name
    
    def execute(self, context):
        print(f"Executing {self.service_name} operator")