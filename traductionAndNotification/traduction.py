import argostranslate.package
import argostranslate.translate

from_code = "en"
to_code = "fr"

def TelechargerPackage(from_code, to_code):
# Download and install Argos Translate package
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())

def traduireTexte(text):
    return argostranslate.translate.translate(text, from_code, to_code)

if __name__ == "__main__":
    TelechargerPackage(from_code, to_code)
    print(traduireTexte("Hello World"))