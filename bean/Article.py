# @description Article model
# @author Thanh Luong (thanh.luong@ecepvn.org)
class Article:
  def __init__(self, id=None, url=None,title=None,publishDate=None,authors=None,createdAt=None,updatedAt=None):
    self.id = id
    self.url = url
    self.title = title
    self.publishDate = publishDate
    self.authors = authors
    self.createdAt = createdAt
    self.updatedAt = updatedAt
