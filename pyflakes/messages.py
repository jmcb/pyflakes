# (c) 2005 Divmod, Inc.  See LICENSE file for details

class Message(object):
    message = ''
    message_args = ()
    def __init__(self, filename, loc, use_column=True):
        self.filename = filename
        self.lineno = loc.lineno
        self.col = getattr(loc, 'col_offset', None) if use_column else None

    def __str__(self):
        return '%s:%s: %s' % (self.filename, self.lineno, self.message % self.message_args)


class UnusedImport(Message):
    message = '%r imported but unused'
    def __init__(self, filename, loc, name):
        Message.__init__(self, filename, loc, use_column=False)
        self.message_args = (name,)


class RedefinedWhileUnused(Message):
    message = 'redefinition of unused %r from line %r'
    def __init__(self, filename, loc, name, orig_loc):
        Message.__init__(self, filename, loc)
        self.message_args = (name, orig_loc.lineno)


class ImportShadowedByLoopVar(Message):
    message = 'import %r from line %r shadowed by loop variable'
    def __init__(self, filename, loc, name, orig_loc):
        Message.__init__(self, filename, loc)
        self.message_args = (name, orig_loc.lineno)


class ImportStarUsed(Message):
    message = "'from %s import *' used; unable to detect undefined names"
    def __init__(self, filename, loc, modname):
        Message.__init__(self, filename, loc)
        self.message_args = (modname,)


class UndefinedName(Message):
    message = 'undefined name %r'
    def __init__(self, filename, loc, name):
        Message.__init__(self, filename, loc)
        self.message_args = (name,)



class UndefinedExport(Message):
    message = 'undefined name %r in __all__'
    def __init__(self, filename, loc, name):
        Message.__init__(self, filename, loc)
        self.message_args = (name,)



class UndefinedLocal(Message):
    message = "local variable %r (defined in enclosing scope on line %r) referenced before assignment"
    def __init__(self, filename, loc, name, orig_loc):
        Message.__init__(self, filename, loc)
        self.message_args = (name, orig_loc.lineno)


class DuplicateArgument(Message):
    message = 'duplicate argument %r in function definition'
    def __init__(self, filename, loc, name):
        Message.__init__(self, filename, loc)
        self.message_args = (name,)


class RedefinedFunction(Message):
    message = 'redefinition of function %r from line %r'
    def __init__(self, filename, loc, name, orig_loc):
        Message.__init__(self, filename, loc)
        self.message_args = (name, orig_loc.lineno)


class LateFutureImport(Message):
    message = 'future import(s) %r after other statements'
    def __init__(self, filename, loc, names):
        Message.__init__(self, filename, loc)
        self.message_args = (names,)


class UnusedVariable(Message):
    """
    Indicates that a variable has been explicity assigned to but not actually
    used.
    """

    message = 'local variable %r is assigned to but never used'
    def __init__(self, filename, loc, names):
        Message.__init__(self, filename, loc)
        self.message_args = (names,)

class EmptyContainerInClassDefinition (Message):
    """
    Indicates that a member in a class definition is a list.

    In a lot of instances, the following is a mistake:

        class Test (object):
            a = []
            ...

    The above results in the following:

        >> a = Test()
        >> b = Test()
        >> b.a.append(1)
        >> b.a == a.a
        True

    It's usually not intendend that instances of the share the same list and can
    cause headaches until you actually realise the mistake that you've made.
    Having a warning for empty containers in class definitions thus immediately
    brings attention to this fact.

    However, it's better to assume that the following is intended behaviour:

        class Test (object):
            my_fields = ["a", "b", "c"]
            ...

    Thus it's better to limit this to empty containers.

    """
    message = 'member %r of %r includes an empty %s in class definition!'
    def __init__ (self, filename, loc, name, class_name):
        Message.__init__(self, filename, loc)
        self.message_args = (name, class_name, loc.__class__.__name__.lower())
