from AuthAPI.services import mysql_db
from AuthAPI import app
import traceback
import inspect
import copy

model_pool = {}

class Field(object):

    def __init__(self, *args, **kwargs):
        self.value = kwargs['default'] if 'default' in kwargs else None

    def clone(self):
        return copy.deepcopy(self)

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

class ForeignField(Field):

    def __init__(self, *args, **kwargs):

        related = kwargs['related'].split('.')
        global model_pool
        self.related_class = model_pool[related[0]]
        self.related_field = related[1]

        super(ForeignField, self).__init__(args, kwargs)

    def setValue(self, value):
        # items = self.related_class.query()
        # obj = [item for item in self.related_class.query() if item.__dict__["__"+str(self.related_field)].getValue() == value]
        obj = self.related_class.query({self.related_field: value})
        if obj:
            print "there is existing object"
            self.value = obj[0]
        else:
            print "create new object"
            self.value = self.related_class()


class ModelMeta(type):

    def __init__(cls, name, base, dct):

        print "Class :", name

        fields = [field for field in dct]
        print "Fields :", fields

        for field in fields:
            field_type = dct[field]
            print "Field :", field
            print "Type  :", field_type

            if isinstance(field_type, Field):
                def get_field(field):
                    def get_func(self):
                        return self.__dict__['__'+field].getValue()
                    return get_func

                def set_field(field):
                    def set_func(self,value):
                        self.__dict__['__'+field].setValue(value)
                    return set_func

                setattr(cls, "__"+str(field), dct[field])
                setattr(cls, field, property(get_field(field), set_field(field)))

        print "Dict", cls.__dict__

        if hasattr(cls,'model_name'):
            global model_pool
            model_pool.update({cls.model_name : cls})

class Model(object):
    __metaclass__ = ModelMeta
    # fields = {}

    def __init__(self, *args, **kwargs):

        fields = [field for field in self.__class__.__dict__ ]

        for field in fields:
            field_type = self.__class__.__dict__[field]

            if isinstance(field_type, Field):
                self.__dict__[field] = field_type.clone()

        print "DICT: ", self.__dict__

        for field in kwargs :
            print "Save field value", field
            self.__dict__["__"+str(field)].setValue(kwargs[field])

    @classmethod
    def query(cls, *args, **kwargs):
        cmd = "SELECT "
        fields = [field for field in cls.__dict__ if field not in cls.__base__.__dict__ ]

        field_list = []
        for field in fields:
            field_type = cls.__dict__[field]

            if isinstance(field_type, property):
                field_list.append(field)
                cmd += '`'+str(field)+'`'
                cmd += ", "

        cmd = cmd.rstrip(', ')

        cmd += " FROM " + cls.model_name

        if kwargs:
            cmd += " WHERE "

            for k,v in kwargs.items():
                if k in field_list:
                    cmd += '`'+str(k)+'`'
                    cmd += "="
                    if isinstance(v,str):
                        cmd += "\""
                    cmd += str(v)
                    if isinstance(v,str):
                        cmd += "\""
                    cmd += "AND"

            cmd = cmd.rstrip('AND')

        print "COMMAND :", cmd

        db = mysql_db.get_mysql_db()
        cur = db.cursor()

        try:
            cur.execute(cmd, ( ))
        except Exception as e:
            app.logger.error(traceback.format_exc())
            return None

        if cur.rowcount < 1:
            return None
        else:
            rows = cur.fetchall()
            print len(rows)
            return [cls(**dict((field, row[idx]) for (idx,field) in enumerate(field_list))) for row in rows]
