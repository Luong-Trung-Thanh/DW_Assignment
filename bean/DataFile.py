class DataFile:
  def __init__(self, id, status,note,description,createdAt,updatedAt,rowCount,data_config_id):
    self.id = id
    self.status = status
    self.note = note
    self.description = description
    self.createdAt = createdAt
    self.updatedAt = updatedAt
    self.rowCount = rowCount
    self.data_config_id = data_config_id
  def __init__(self,status,description,rowCount,data_config_id):
    self.status = status
    self.description = description
    self.rowCount = rowCount
    self.data_config_id = data_config_id
