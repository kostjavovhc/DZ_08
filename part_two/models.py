from mongoengine import connect
from mongoengine import Document
from mongoengine.fields import StringField, BooleanField


connect(db='web16', 
    host = "mongodb+srv://kostjavovhc:m0l0k098@cluster0.9a71l4e.mongodb.net/?retryWrites=true&w=majority")


from mongoengine import Document
from mongoengine.fields import StringField, BooleanField


class Contact(Document):
    fullname = StringField()
    email = StringField()
    phone = StringField()
    email_send = BooleanField(default=False)