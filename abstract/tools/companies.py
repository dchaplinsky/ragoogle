import re


def unify_cyprus_codes(company_code):
    company_code = re.sub("^HE\s?", "HE", company_code)
    company_code = re.sub("^ΗΕ\s?", "HE", company_code)
    company_code = re.sub("^H\.E\.\s?", "HE", company_code)
    company_code = re.sub("^Η\.E\.\s?", "HE", company_code)

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
    company_code = str(company_code)
    return set((company_code.lstrip("0"), company_code, company_code.rjust(8, "0")))
