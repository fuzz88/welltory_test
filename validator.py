import json  # can be replaced with orjson to speedup parsing
import glob

errors = []


def output_as_code(text, output):
    output.write('```\n')
    output.write(text)
    output.write('\n```')


def validate(filename, data, output):
    """ Validates json given with the schema provided """

    output.write(
        f'#### [{ filename }](https://raw.githubusercontent.com/fuzz88/welltory_test/master/{ filename })')
    output.write('\n\n')
    # print(filename)
    # print(data)
    try:
        event_type = data['event']
    except (KeyError, TypeError):
        output_as_code(
            'Не найден ключ "event". Данных о событии в файле нет, либо ошибка в названии ключа.', output)
        output.write('\n\n')
        return
    try:
        with open(f'data/schema/{ event_type }.schema') as schema_file:
            try:
                schema = json.load(schema_file)
            except Exception as e:
                print(e)
    except OSError:
        output_as_code(
            f'Для события "{ event_type }" не найден файл со схемой. Либо неизвестное событие, либо ошибка в названии схемы или события.', output)
        output.write('\n\n')


with open('README.md', 'w') as output_file:
    for filename in glob.glob('data/event/*.json'):
        with open(filename, 'r') as json_file:
            json_data = None
            try:
                json_data = json.load(json_file)
            except Exception as e:
                errors.append(e)
            finally:
                if json_data is not None:
                    validate(filename, json_data, output_file)

print(errors)  # it gave []. all file consist of valid json data. let's validate
