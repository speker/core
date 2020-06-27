# -*- coding: utf-8 -*-
class AppScopeRunner:
    caller = None

    def __init__(self, api, caller):
        super(AppScopeRunner).__init__()
        self.caller = caller
        scope_folder_name = '/scopes/'
        print(caller.colored("start ", 'cyan'), caller.colored(__name__, 'green'))
        self.session = api.session

        all_sub_dirs = [dI for dI in caller.rea_os().listdir(caller.script_path + scope_folder_name) if
                        caller.rea_os().path.isdir(
                            caller.rea_os().path.join(caller.script_path + scope_folder_name, dI)) and not dI.endswith(
                            '__')]
        print(caller.colored(' * ' + caller.working_space + ' Static Endpoints :', 'white'))

        i = 1
        try:
            for apps in all_sub_dirs:
                modules = [f for f in caller.rea_os().listdir(
                    caller.rea_os().path.dirname(
                        caller.rea_os().path.abspath(
                            caller.script_path + '/' + caller.working_space)) + scope_folder_name + apps + '/endpoints')
                           if
                           f.endswith('.py') and not f.startswith('__')]

                for module in modules:
                    class_name = caller.rea_os().path.splitext(module)[0]
                    module_name = "apps.rest_server.applications." + caller.working_space + '.scopes.' + apps + ".endpoints." \
                                  + class_name
                    if '_' in class_name:
                        class_name = class_name.replace('_', '')
                    get_class = self.get_class_package(caller, module_name, class_name)
                    if class_name == 'root':
                        route = '/'
                    else:
                        route = '/' + caller.working_space + '/' + apps + '/' + class_name
                    api.add_resource(self.factory(get_class, route), route,
                                     endpoint=class_name + "_" + str(caller.hash().get_uuid()))
                    print(caller.colored('  ' + str(i) + ' -', 'yellow'), caller.colored(route, 'yellow'))
                    i += 1

        except Exception as err:
            print(err)

    def get_class_package(self, master, module_name, class_name):
        m = __import__(module_name, globals(), locals(), class_name)
        import_module = self.caller.inspect().getmembers(m)
        new_key = None
        for key, value in import_module:
            if class_name == key.lower():
                new_key = [x for x, y in enumerate(import_module) if y[0] == key]
        import_module_name = import_module[new_key[0]]
        c = getattr(m, import_module_name[0])
        return c

    def factory(self, base_class, spaces):
        class NewClass(base_class):
            pass

        NewClass.__name__ = spaces + "_%s" % base_class.__name__
        NewClass.master = self
        return NewClass
