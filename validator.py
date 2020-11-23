import json  # can be replaced with orjson to speedup parsing
import glob

errors = []


def validate(filename, data):
    with open('README.md', 'at') as output:
        output.write(f'#### { filename }')
        output.write('\n\n')
        print(filename)
        print(data)
        try:
            event_type = data['event']
        except (KeyError, TypeError):
            output.write(
                'Не найден ключ "event". Данных о событии в файле нет, либо ошибка в названии ключа.')
            # output.write('```')
            # output.write(json.dumps(data, indent=4))
            # output.write('```')
            output.write('\n\n')
            return
        try:
            with open(f'data/schema/{ event_type }.schema') as schema_file:
                pass
        except OSError:
            output.write(
                f'Для события "{ event_type }" не найден файл со схемой. Либо неизвестное событие, либо ошибка в названии схемы или события.')
            output.write('\n\n')


for filename in glob.glob('data/event/*.json'):
    with open(filename, 'r') as json_file:
        try:
            json_data = json.load(json_file)
        except Exception as e:
            errors.append(e)
        finally:
            validate(filename, json_data)

print(errors)  # it gave []. all file consist of valid json data. let's validate
