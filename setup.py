from setuptools import setup

setup(
    name="huggingface_extra_chat_templates",
    version="0.0.1",
    packages=["huggingface_extra_chat_templates"],
    package_dir={
        'huggingface_extra_chat_templates': '.',
    },
    install_requires=[],
    author='',
    author_email='',
    description='',
    include_package_data=True,
    package_data={
        'huggingface_extra_chat_templates': [
            '**/*.jinja',
            '**/*.json'
        ]
    },
)
