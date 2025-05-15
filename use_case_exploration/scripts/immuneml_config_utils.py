import os
import yaml


def write_immuneml_config(input_train_config_template, input_data, output_config_file, gen_examples_count=None, models=None):
    """Writes an immuneML YAML config by modifying a template."""
    with open(input_train_config_template, 'r') as file:
        template_config = yaml.safe_load(file)

    template_config['definitions']['datasets']['dataset']['params']['path'] = input_data

    if gen_examples_count:
        for model in models:
            template_config['instructions'][model]['gen_examples_count'] = gen_examples_count

    with open(output_config_file, 'w') as file:
        yaml.safe_dump(template_config, file)

