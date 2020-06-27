# -*- coding: utf-8 -*-
class AppRunner:
    caller = None

    def __init__(self, caller, script_path):
        super(AppRunner).__init__()
        self.caller = caller
        print(caller.colored("start ", 'red'), caller.colored(__name__, 'magenta'))
        try:
            working_space = caller.rea_os().path.basename(script_path)
            modules = [f for f in caller.rea_os().listdir(
                caller.rea_os().path.dirname(script_path + '/' + working_space) + '/controllers') if
                       f.endswith('.py')]

            for module in modules:
                class_name = caller.rea_os().path.splitext(module)[0]
                self.get_class_package("apps." + working_space + ".controllers." + class_name,
                                       class_name.capitalize())
        except Exception as e:
            print(e)

    def get_class_package(self, module_name, class_name):
        try:
            m = __import__(module_name, globals(), locals(), class_name)
            import_module = self.caller.inspect().getmembers(m)
            module_name = import_module[0]
            c = getattr(m, module_name[0])
            return c
        except Exception as e:
            print(e)
