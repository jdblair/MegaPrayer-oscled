class DispatcherMapper:

    def __init__(self):
        self.exposed_methods = {}

    def expose(self):
        def decorator(fn):
            self.exposed_methods[fn.__name__] = fn
            return fn
        return decorator

    def invoke_exposed(self, unused_addr, hacked_variables, *args, **kwargs):

        print("Handling endpoint: {}".format(unused_addr))
        print("Function definitions: {}".format(hacked_variables))
        print("Arguments from OSC: {}".format(args))

        fn_name = hacked_variables[0]
        effect_obj = hacked_variables[1]
        self.exposed_methods[fn_name](effect_obj, *args, **kwargs)


