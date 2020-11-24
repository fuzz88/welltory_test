import json  # can be replaced with orjson to speedup parsing
import glob
from jsonschema import Draft7Validator

"""
TODO:
    - how to parallelize this properly?
"""


def validate(filename, data, output):
    """ Validates json given with the schema provided. """

    no_errors = True

    output.write(
        f'#### [{ filename }](https://raw.githubusercontent.com/fuzz88/welltory_test/master/{ filename })')
    output.write('\n\n')

    output.write('```\n')  # markdown codeblock begins

    try:
        event_type = data['event']
    except (KeyError, TypeError):
        output.write(
            'Не найден ключ "event". Данных о событии в файле нет,\nлибо ошибка в названии ключа.')
        output.write('\n')
        output.write('\n```')  # markdown codeblock ends on file validation end
        output.write('\n\n')
        return

    try:
        with open(f'data/schema/{ event_type }.schema') as schema_file:
            schema = None
            try:
                schema = json.load(schema_file)
            except Exception as e:
                #  if the schema is given as invalid json, we've got to know that somehow
                print(e)
            finally:
                if schema is not None:
                    validator = Draft7Validator(schema)
                    for error in sorted(validator.iter_errors(data['data']), key=str):
                        no_errors = False
                        output.write('------BEGIN ERROR DESCRIPTION------\n\n')
                        output.write(str(error))
                        output.write('\n\n')
                        output.write(error.message)
                        output.write('\n\n------END ERROR DESCRIPTION------')
                        output.write('\n\n')

    except OSError:
        output.write(
            f'Для события "{ event_type }" не найден файл со схемой.\nЛибо неизвестное событие, либо ошибка в названии схемы или события.')
        output.write('\n')
        output.write('\n```')  # markdown codeblock ends on file validation end
        output.write('\n\n')
        return

    if no_errors:
        output.write('Данные соответствуют схеме.')
    output.write('\n```')  # markdown codeblock ends on file validation end
    output.write('\n\n')


errors = []

if __name__ == '__main__':
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

    print(errors)  # json-parsing errors.
    # it gave [] -> all json files consist of valid json data. let's validate with schemas.
    # schema files are assumed to be valid by default.
