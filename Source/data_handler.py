import pickle
import os

data_filename = "memberData.pickle"  

class Data:
    def __init__(self, warnings, softbanned):
      self.warnings = warnings
      self.softbanned = softbanned

def load_data_file():
    if os.path.isfile(data_filename):
      with open(data_filename, "rb") as file:
        return pickle.load(file)
    else:
      return dict()

def load_data(member_ID):
  data = load_data_file()

  if member_ID not in data:
    return Data(0, False)

  return data[member_ID]

def save_data(member_ID, member_data):
  data = load_data_file()

  data[member_ID] = member_data

  with open(data_filename, "wb") as file:
    pickle.dump(data, file)