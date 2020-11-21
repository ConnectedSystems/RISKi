import pytest

import riski as ri


def test_gen_config():
    ri._utils.generate_config("tests/.settings.yaml", dev=True)


if __name__ == '__main__':
    # from project directory, run: python tests/test_config_generator.py
    test_gen_config()