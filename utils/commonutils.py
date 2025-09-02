import json

class CommonUtils:

    def load(self,test_data_path):
        with open(test_data_path, 'r') as f:
            data = json.load(f)

        return data