import os, inspect
from django.conf import settings
from django.conf.urls import patterns as django_patterns, url

class RouteMaker(object):

    def __init__(self):
        self.__root_dir = getattr(settings, 'ROOT_DIR', None)
        if not self.__root_dir:
            raise Exception('ROOT_DIR not found in settings.py')
        self.__apps = self.__discover_apps()        

    def do(self):
        patterns = []
        for app_name in self.__apps:            
            exec('import %s.views as views' % app_name)

            #Pre-filter to allow to know the last action of the current application and if there is some action with the name index                 
            actions = [name for name, member in vars(views).items() if self.__is_action(views, member)]            
            
            for action in actions:
                patterns.append(
                    url(
                        r'^%s/%s/$' % (app_name.replace('_', '-'), action), 
                        '%s.views.%s' % (app_name, action), 
                        name='%s-%s' % (app_name, action)
                    )
                )

                if actions[-1] is action and 'index' in actions:
                    patterns.append(
                        url(r'^%s/$' % app_name.replace('_', '-'), '%s.views.index' % app_name,  name='%s' % app_name )
                    )

        return django_patterns('', *patterns)        

    #checks if member is a truly action
    def __is_action(self, module, member):
        is_decorated = getattr(member, 'func_closure', None) or \
        [key for key in getattr(member, '__dict__', {}).keys() if key.endswith('__func')]        
        is_module_function = inspect.isfunction(member) and inspect.getmodule(member) == module
        return is_decorated or is_module_function        

    #checks if the subfolders at ROOT_DIR are apps
    def __discover_apps(self):
        return [ item for item in os.listdir(self.__root_dir) if item in settings.INSTALLED_APPS ]    

def patterns():
    return RouteMaker().do()