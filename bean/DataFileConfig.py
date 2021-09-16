class DataFileConfig:
  def __init__(self, id=None, url=None,name=None,description=None,destination=None,columns=None,
               separators=None,formatFile=None,createdAt=None,updatedAt=None):
    self.id = id
    self.url = url
    self.name = name
    self.description = description
    self.destination = destination
    self.columns = columns
    self.separators = separators
    self.formatFile = formatFile
    self.createdAt = createdAt
    self.updatedAt = updatedAt

