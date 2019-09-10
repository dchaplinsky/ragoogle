from abstract.ftm_models import model as ftm_model
from names_translator.name_utils import parse_fullname, generate_all_names
from abstract.tools.companies import generate_edrpou_options, format_edrpou


def person_entity(name, positions, id_prefix="", **kwargs):
    person = ftm_model.make_entity("RingPerson")
    l, f, p, _ = parse_fullname(name)

    person.set("firstName", f)
    person.set("fatherName", p)
    person.set("lastName", l)
    person.set("position", positions)

    person.make_id(id_prefix, f, p, l)

    person.set("alias", generate_all_names(l, f, p, ""))

    for k, v in kwargs.items():
        person.set(k, v)

    return person


def company_entity(name, code, id_prefix="", jurisdiction="Ukraine", **kwargs):
    company = ftm_model.make_entity("RingCompany")

    if jurisdiction == "Ukraine":
        company.set("alias", generate_edrpou_options(code))
        code = format_edrpou(code)

    company.set("jurisdiction", jurisdiction)
    company.set("name", name)
    company.set("registrationNumber", code)

    company.make_id(id_prefix, code)

    for k, v in kwargs.items():
        company.set(k, v)

    return company
