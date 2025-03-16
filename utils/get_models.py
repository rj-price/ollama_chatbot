import ollama

def get_models():
    models_dict = ollama.list()['models']
    models_num = len(models_dict)
    models_list = []
    for i in range(models_num):
        model = models_dict[i]['model']
        if 'latest' in model:
            models_list.append(model.split(':')[0])
        elif 'embed' in model:
            continue
        else:
            models_list.append(model)
    return models_list