#!/usr/bin/env python
# coding: utf-8

# In[4]:


get_ipython().system('pip install peewee')


# In[5]:


from peewee import *

db = SqliteDatabase('people.db')

class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db # This model uses the "people.db" database.


# In[6]:


class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db # this model uses the "people.db" database


# In[7]:


db.connect()


# In[8]:


db.create_tables([Person, Pet])


# In[9]:


from datetime import date
uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
uncle_bob.save() # bob is now stored in the database
# Returns: 1


# In[10]:


grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
herb = Person.create(name='Herb', birthday=date(1950, 5, 5))


# In[11]:


grandma.name = 'Grandma L.'
grandma.save()  # Update grandma's name in the database.
# Returns: 1


# In[12]:


bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')


# In[13]:


herb_mittens.delete_instance() # he had a great life
# Returns: 1


# In[14]:


herb_fido.owner = uncle_bob
herb_fido.save()


# In[15]:


grandma = Person.select().where(Person.name == 'Grandma L.').get()


# In[16]:


grandma = Person.get(Person.name == 'Grandma L.')


# In[17]:


for person in Person.select():
    print(person.name)

# prints:
# Bob
# Grandma L.
# Herb


# In[18]:


query = Pet.select().where(Pet.animal_type == 'cat')
for pet in query:
    print(pet.name, pet.owner.name)

# prints:
# Kitty Bob
# Mittens Jr Herb


# In[19]:


query = (Pet
         .select(Pet, Person)
         .join(Person)
         .where(Pet.animal_type == 'cat'))

for pet in query:
    print(pet.name, pet.owner.name)

# prints:
# Kitty Bob
# Mittens Jr Herb


# In[20]:


for pet in Pet.select().join(Person).where(Person.name == 'Bob'):
    print(pet.name)

# prints:
# Kitty
# Fido


# In[21]:


for pet in Pet.select().where(Pet.owner == uncle_bob):
    print(pet.name)


# In[22]:


for pet in Pet.select().where(Pet.owner == uncle_bob).order_by(Pet.name):
    print(pet.name)

# prints:
# Fido
# Kitty


# In[23]:


for person in Person.select().order_by(Person.birthday.desc()):
    print(person.name, person.birthday)

# prints:
# Bob 1960-01-15
# Herb 1950-05-05
# Grandma L. 1935-03-01


# In[24]:


d1940 = date(1940, 1, 1)
d1960 = date(1960, 1, 1)
query = (Person
         .select()
         .where((Person.birthday < d1940) | (Person.birthday > d1960)))

for person in query:
    print(person.name, person.birthday)

# prints:
# Bob 1960-01-15
# Grandma L. 1935-03-01


# In[25]:


query = (Person
         .select()
         .where(Person.birthday.between(d1940, d1960)))

for person in query:
    print(person.name, person.birthday)

# prints:
# Herb 1950-05-05


# In[27]:



for person in Person.select():
    print(person.name, person.pets.count(), 'pets')

# prints:
# Bob 2 pets
# Grandma L. 0 pets
# Herb 1 pets


# In[28]:


query = (Person
         .select(Person, fn.COUNT(Pet.id).alias('pet_count'))
         .join(Pet, JOIN.LEFT_OUTER)  # include people without pets.
         .group_by(Person)
         .order_by(Person.name))

for person in query:
    # "pet_count" becomes an attribute on the returned model instances.
    print(person.name, person.pet_count, 'pets')

# prints:
# Bob 2 pets
# Grandma L. 0 pets
# Herb 1 pets


# In[29]:


query = (Person
         .select(Person, Pet)
         .join(Pet, JOIN.LEFT_OUTER)
         .order_by(Person.name, Pet.name))
for person in query:
    # We need to check if they have a pet instance attached, since not all
    # people have pets.
    if hasattr(person, 'pet'):
        print(person.name, person.pet.name)
    else:
        print(person.name, 'no pets')

# prints:
# Bob Fido
# Bob Kitty
# Grandma L. no pets
# Herb Mittens Jr


# In[30]:


query = Person.select().order_by(Person.name).prefetch(Pet)
for person in query:
    print(person.name)
    for pet in person.pets:
        print('  *', pet.name)

# prints:
# Bob
#   * Kitty
#   * Fido
# Grandma L.
# Herb
#   * Mittens Jr


# In[31]:


expression = fn.Lower(fn.Substr(Person.name, 1, 1)) == 'g'
for person in Person.select().where(expression):
    print(person.name)

# prints:
# Grandma L.


# In[32]:


db.close()


# In[ ]:




