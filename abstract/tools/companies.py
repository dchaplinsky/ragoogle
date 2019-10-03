import re
from names_translator.name_utils import try_to_fix_mixed_charset


def format_edrpou(code):
    return str(code).rjust(8, "0")


def unify_cyprus_codes(company_code):
    company_code = re.sub(r"^HE\s?", "HE", company_code)
    company_code = re.sub(r"^ΗΕ\s?", "HE", company_code)
    company_code = re.sub(r"^H\.E\.\s?", "HE", company_code)
    company_code = re.sub(r"^Η\.E\.\s?", "HE", company_code)

    return set(
        (
            # Unified code, HE123456
            company_code,
            # Unified code with space, HE 123456
            re.sub("^HE", "HE ", company_code),
            # Unified greec code without space, ΗΕ123456
            re.sub("^HE", "ΗΕ", company_code),
            # Unified greec code with space, ΗΕ 123456
            re.sub("^HE", "ΗΕ ", company_code),
            # Unified greec code with dots, Η.Ε. 123456
            re.sub("^HE", "Η.Ε.", company_code),
            # Unified latin code with dots, H.E. 123456
            re.sub("^HE", "H.E.", company_code),
        )
    )


def generate_edrpou_options(company_code):
    if company_code:
        company_code = str(company_code)
        return set(
            (
                company_code.strip().strip("\u200e").lstrip("0"),
                company_code,
                company_code.rjust(8, "0"),
            )
        )
    else:
        return set()


def deal_with_mixed_lang(company_name):
    if company_name:
        chunks = company_name.split(" ")

        fixed_name = " ".join([try_to_fix_mixed_charset(chunk) for chunk in chunks])

        return set([company_name, fixed_name])
    else:
        return set()
