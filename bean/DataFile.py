# @description DataFile model
# @author Thanh Luong (thanh.luong@ecepvn.org)
class DataFile:
  def __init__(self, id=None, name = None,status=None,note=None,description=None,
               createdAt=None,updatedAt=None,rowCount=None,data_config_id=None):
    self.id = id
    self.status = status
    self.name = name
    self.note = note
    self.description = description
    self.createdAt = createdAt
    self.updatedAt = updatedAt
    self.rowCount = rowCount
    self.data_config_id = data_config_id

