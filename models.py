import json


class Books:
    def __init__(self):
        try:
            with open("books.json", "r") as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = []

    def all(self):
        return self.books

    def get(self, id):
        books = [books for books in self.all() if books['id'] == id]
        if books:
         return books[0]
        return []

    def create(self, data):
        self.books.append(data)
        self.save_all()

    def save_all(self):
        with open("books.json", "w") as f:
            json.dump(self.books, f)

    def delete(self, id):
        book = self.get(id)
        if book:
            self.books.remove(book)
            self.save_all()
            return True
        return False

    def update(self, id, data):
        book = self.get(id)
        if book:
            index = self.books.index(book)
            self.books[index] = data
            self.save_all()
            return True
        return False


books = Books()