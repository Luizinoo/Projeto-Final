# app/models/news.py
import datetime

class News:
    def __init__(self, title, content, file_path=None, date=None):
        self.title = title
        self.content = content
        self.file_path = file_path
        self.date = date or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            'title': self.title,
            'content': self.content,
            'file_path': self.file_path,
            'date': self.date
        }
