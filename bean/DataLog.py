# @description DataLog model
# @author Thanh Luong (thanh.luong@ecepvn.org)
class DataLog:
  def __init__(self, id=None, description=None,createdAt=None,updatedAt=None,name=None):
    self.id = id
    self.description = description
    self.createdAt = createdAt
    self.updatedAt = updatedAt
    self.name = name

