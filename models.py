from tortoise import fields, models


class Roles(models.Model):
    """
    The Role model
    """

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.name


class Users(models.Model):
    """
    The User model
    """

    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=50, null=False)
    surname = fields.CharField(max_length=50, null=True)
    patronymic = fields.CharField(max_length=50, null=True)
    
    access_level = fields.ForeignKeyField('models.Roles', null=True)
    
    password = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    
    def __str__(self):
        return self.first_name


class Products(models.Model): #Под редактирование
    """
    The Students model
    """

    id = fields.IntField(pk=True)
    product_name = fields.CharField(max_length=100, null=False)
    from_where = fields.CharField(max_length=100, null=False)
    where = fields.CharField(max_length=100, null=False)
    
    quantity = fields.CharField(max_length=20, null=False)
    amount = fields.CharField(max_length=20, null=False)
    
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    
    def __str__(self):
        return self.first_name

