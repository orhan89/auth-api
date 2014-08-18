from AuthAPI.services import mysql_db
from AuthAPI import app
import traceback
import inspect

class Field(object):

    def __init__(self, *args, **kwargs):
        self.value = kwargs['value'] if 'value' in kwargs else None


class ForeignField(Field):

    def __init__(self, *args, **kwargs):
        super(ForeignField, self).__init__(args, kwargs)
        self.related_field = kwargs['related_field']


class ModelMeta(type):

    def __init__(cls, name, base, dct):

        print "Class :", name

        fields = [field for field in dct]
        print "Fields :", fields

        for field in fields:
            field_type = dct[field]
            print "Field :", field
            print "Type  :", field_type

            if inspect.isclass(field_type) and issubclass(field_type, Field):
                def get_field(field):
                    def get_func(self):
                        return self.__dict__['__'+field].value
                    return get_func

                def set_field(field):
                    def set_func(self,value):
                        self.__dict__['__'+field].value = value
                    return set_func

                setattr(cls, "__"+str(field), dct[field])
                setattr(cls, field, property(get_field(field), set_field(field)))

        print "Dict", cls.__dict__

class Model(object):
    __metaclass__ = ModelMeta
    # fields = {}

    def __init__(self, *args, **kwargs):

        fields = [field for field in self.__class__.__dict__ ]

        for field in fields:
            field_type = self.__class__.__dict__[field]

            if inspect.isclass(field_type) and issubclass(field_type, Field):
                self.__dict__[field] = field_type()

        print "DICT: ", self.__dict__

        for field in kwargs :
            print "Save field value", field
            self.__dict__["__"+str(field)].value = kwargs[field]

    @classmethod
    def query(cls, *args, **kwargs):
        cmd = "SELECT "
        fields = [field for field in cls.__dict__ if field not in cls.__base__.__dict__ ]

        field_list = []
        for field in fields:
            field_type = cls.__dict__[field]

            # if not hasattr(field_type, '__name__') and not field_type.__name__ == "Field":
            if isinstance(field_type, property):
                field_list.append(field)
                cmd += str(field)
                cmd += ", "

        cmd = cmd.rstrip(', ')

        cmd += " FROM " + cls.model_name

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
            # row = cur.fetchone()
            rows = cur.fetchall()
            print len(rows)
            # kwargs = {}
            # for idx,field in enumerate(field_list):
            #     kwargs[field] = row[idx]
            # return cls(**kwargs)
            return [cls(**dict((field, row[idx]) for (idx,field) in enumerate(field_list))) for row in rows]
