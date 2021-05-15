# f = open("mut.txt", "a")

def pre_mutation(context):
    ignore_list = [
        "gui_layouts.py",
        "gui.py",
        "helpers.py",
        "mutmut_config.py",
        "conftest.py",
        "CassandraModels.py",
        "test_apikeys.py",
    ]
    filename = context.filename.split("/")[-1]
    if filename.startswith("test_"):
        context.skip = True
    if filename in ignore_list:
        context.skip = True

    # if context.skip == False:
    #     f.write(f"{str(context.__dict__)}\n")