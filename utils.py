import json
import csv


class Convert:

    str_to_boolean_checker = False

    @staticmethod
    def csv_to_json(csv_file, model):
        with open(csv_file, encoding='utf-8') as file:
            file_read = csv.DictReader(file)
            fields = Convert._dict_to_django_json(file_read, model)

            json_file = csv_file.split('.')[0] + '.json'
            json_file = json_file.split('/')[-1]

        with open('fixtures/' + json_file, 'w', encoding='utf-8') as file:
            json.dump(fields, file, indent=4, ensure_ascii=False)

    @staticmethod
    def _dict_to_django_json(file_read, model):
        fields = []

        for f in file_read:
            if Convert.str_to_boolean_checker:
                for k, v in f.items():
                    if v == 'TRUE':
                        f[k] = True
                    elif v == 'FALSE':
                        f[k] = False

            # f['is_published'] = True if f['is_published'] == 'TRUE' else False
            fields.append({'model': model,
                           'pk': f['id'],
                           'fields': f})
        return fields
