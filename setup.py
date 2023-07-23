from setuptools import find_packages,setup

REQUIREMENT_FILE_NAME = "requirements.txt"
HYPHEN_E_DOT = '-e .'
def get_requirements()->List[str]:
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
    requirement_list = [i.replace("\n","")for i in requirement_list]
    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list    

setup(
    name = "credit",
    version = "0.0.1",
    author = "rishabhkoul",
    author_name = "rishabhkoul@gmail.com",
    packages = find_packages( ),
    install_requires = get_requirements()
)