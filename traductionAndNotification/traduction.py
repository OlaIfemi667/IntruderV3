import argostranslate.package
import argostranslate.translate

def translate_en_fr(text):
    from_code = "en"
    to_code = "fr"

    # Télécharge et installe le package de traduction seulement si nécessaire
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    if not any(
        (pkg.from_code == from_code and pkg.to_code == to_code)
        for pkg in argostranslate.translate.get_installed_languages()[0].get_translation_languages()
    ):
        package_to_install = next(
            filter(
                lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
            )
        )
        argostranslate.package.install_from_path(package_to_install.download())

    # Traduction
    return argostranslate.translate.translate(text, from_code, to_code)

if __name__ == "__main__":
    original_text = "Hello World"
    translated_text = translate_en_fr(original_text)
    print(translated_text)
