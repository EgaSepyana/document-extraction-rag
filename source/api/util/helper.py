import hashlib
from time import time
import dateparser
from api.config.base import settings
import re


def mongo_query_builder(
    dto,
    text_type=None,
    multi_field=None,
    ignore="orderBy,order,page,size,search,search_by,operator,source,startDate,endDate,filters,timeframe,multiSearch,readWrite",
    is_dict=False,
    additional_ignore=None,
    date_fields=None,
    ignore_field: list = None,
    searchIgnoreSpecial: bool = False,
):
    if additional_ignore:
        ignore = f"{ignore},{additional_ignore}"

    if multi_field is None:
        multi_field = {"account_id": "shared"}

    if is_dict:
        dictionary = dto
    else:
        dictionary = dto.dict()

    dictionary = ignore_empty_array(dictionary)

    if "id" in dictionary:
        dictionary["_id"] = dictionary.pop("id")

    query = []
    if dictionary.get("startDate") and dictionary.get("endDate"):
        query.append(
            {
                "createdAt": {
                    "$gte": dateparser.parse(str(dictionary.get("startDate"))),
                    "$lte": dateparser.parse(str(dictionary.get("endDate"))),
                }
            }
        )

    if "timeframe" in dictionary and dictionary["timeframe"]:
        timeframe = dictionary["timeframe"]
        query.append(
            {
                "lastActive": {
                    "$gte": dateparser.parse(str(timeframe.get("start"))),
                    "$lte": dateparser.parse(str(timeframe.get("end"))),
                }
            }
        )

    if dictionary.get("searchIgnoreSpecial") and dictionary.get("search"):
        print("searchIgnoreSpecial")
        search = r"[\s\W_]*".join(map(re.escape, dictionary.get("search").split()))
        dictionary["search"] = search

    if "timeframe" in dictionary and dictionary["timeframe"]:
        timeframe = dictionary["timeframe"]
        field = timeframe.get("field")
        query.append(
            {field: {"$gte": timeframe.get("start"), "$lte": timeframe.get("end")}}
        )

    if (
        "search_by" in dictionary
        and dictionary["search_by"]
        and "search" in dictionary
        and dictionary["search"]
    ):
        query_search = []
        for search_by in dictionary["search_by"]:
            if dictionary["operator"]:
                query_operator = []
                for search in dictionary["search"].split(" "):
                    query_operator.append(
                        {search_by: {"$regex": f"\\b{search}\\b", "$options": "i"}}
                    )
                if dictionary["operator"] == "and":
                    query_search.append({"$and": query_operator})
                else:
                    query_search.append({"$or": query_operator})

            else:
                query_search.append(
                    {
                        search_by: {
                            "$regex": f".*{dictionary['search']}.*",
                            "$options": "i",
                        }
                    }
                )
        query.append({"$or": query_search})

    if (
        "search_by" in dictionary
        and dictionary["search_by"]
        and "multiSearch" in dictionary
        and dictionary["multiSearch"]
    ):
        query_search = []
        for search_by in dictionary["search_by"]:
            query_operator = []
            for search in dictionary["multiSearch"]:

                query_operator.append(
                    {search_by: {"$regex": f"\\b{search}\\b", "$options": "i"}}
                )
            query_search.append({"$or": query_operator})

        query.append({"$or": query_search})

    for key, value in dictionary.items():
        if key == "filters" and isinstance(value, list):
            filters = []
            for filter_ in value:
                if date_fields and filter_.get("field") in date_fields:
                    gte = dateparser.parse(str(filter_["value"]["gte"]))
                    lte = dateparser.parse(str(filter_["value"]["lte"]))
                    filter_["value"]["gte"] = gte
                    filter_["value"]["lte"] = lte
                filters.append(filter_)

            query_filters = mongo_filter_query_builder(filters)
            query_filter = {}
            for filter_type, value in query_filters.items():
                if value:
                    if filter_type in query:
                        query_filter[filter_type].extend(value)
                    else:
                        query_filter[filter_type] = value
            query.append(query_filter)

        if not isinstance(value, bool):
            if value is not None and key not in ignore.split(","):
                if text_type and key in text_type.split(","):
                    query.append({key: {"$regex": f".*{value}.*", "$options": "i"}})
                elif key in list(multi_field.keys()):
                    query.append({"$or": [{key: value}, {multi_field[key]: value}]})
                elif isinstance(value, list):
                    query.append({key: {"$in": value}})
                elif "!" in value:
                    query.append({key: {"$ne": value.replace("!", "")}})
                else:
                    if ignore_field:
                        if key not in ignore_field:
                            query.append({key: value})
                    else:
                        query.append({key: value})
    return {"$and": query} if query else {}


def mongo_filter_query_builder(filters):
    query = {"$and": [], "$nor": [], "$or": []}

    for _filter in filters:
        if _filter["field"]:
            field_name = _filter["field"]
            query_value = None
            if (
                _filter["operator"] in ["is", "is not"]
                and _filter["value"]["is"] is not None
            ):

                if _filter["value"]["is"] == "" and (
                    _filter["value"].get("gte") or _filter["value"].get("lte")
                ):

                    if _filter["fieldType"] in ["string"]:

                        expr = {}

                        if _filter["value"].get("lte"):

                            expr["$lte"] = [
                                {"$toDate": f"${field_name}"},
                                {
                                    "$toDate": dateparser.parse(
                                        str(_filter["value"]["lte"])
                                    ).strftime("%Y-%m-%d")
                                },
                            ]

                        if _filter["value"].get("gte"):

                            expr["$gte"] = [
                                {"$toDate": f"${field_name}"},
                                {
                                    "$toDate": dateparser.parse(
                                        str(_filter["value"]["gte"])
                                    ).strftime("%Y-%m-%d")
                                },
                            ]

                        query_value = {"$expr": expr}
                else:
                    query_value = {field_name: _filter["value"]["is"]}
            elif (
                _filter["operator"] in ["is one of", "is not one of"]
                and _filter["value"]["isOneOf"] is not None
            ):
                query_value = {field_name: {"$in": _filter["value"]["isOneOf"]}}
            elif (
                _filter["operator"] == "greater than equals"
                and _filter["value"]["gte"] is not None
            ):
                query_value = {field_name: {"$gte": _filter["value"]["gte"]}}
            elif _filter["operator"] == "less than equals" and _filter["value"]["lte"]:
                query_value = {field_name: {"$lte": _filter["value"]["lte"]}}
            elif (
                _filter["operator"] in ["is between", "is not between"]
                and _filter["value"]["gte"]
                and _filter["value"]["lte"]
            ):
                query_value = {
                    field_name: {
                        "$gte": _filter["value"]["gte"],
                        "$lte": _filter["value"]["lte"],
                    }
                }
                # if _filter['fieldType'] == 'date' or _filter.get("field_type_origin") == "datetime":
                #     query_value["range"][field_name]["format"] = "epoch_millis"
                #     if _filter["value"].get("timezone"):
                #         timezone_offset = get_timezone_offset(_filter["value"].get("timezone"))
                #         query_value["range"][field_name]["gte"] += timezone_offset
                #         query_value["range"][field_name]["lte"] += timezone_offset
                # else:
                #     if _filter["value"].get("timezone"):
                #         query_value["range"][field_name]["time_zone"] = _filter["value"].get("timezone")

            elif _filter["operator"] in ["is exist", "is not exist"]:
                query_value = {field_name: {"$exists": True}}
            elif (
                _filter["operator"] in ["is contains", "is not contains"]
                and _filter["value"]["is"]
            ):
                query_value = {
                    field_name: {
                        "$regex": f"\\b{ _filter['value']['is']}\\b",
                        "$options": "i",
                    }
                }

            operator_type = _filter.get("operator_type", "and")
            if query_value is not None:
                if "not" in _filter["operator"]:
                    query["$nor"].append(query_value)
                else:
                    if operator_type == "or":
                        query["or"].append(query_value)
                    else:
                        query["$and"].append(query_value)

    return query


def ignore_empty_array(dictionary):
    result = {}
    for key, value in dictionary.items():
        if isinstance(value, list) and not value:
            pass
        else:
            result[key] = value
    return result


def get_md5(string: str) -> str:
    return hashlib.md5(string.encode("utf-8")).hexdigest()


def orm_to_dict(data):
    if data:
        return {c.name: getattr(data, c.name) for c in data.__table__.columns}
    else:
        return None
    
def row_to_dict(row):
    return dict(row._mapping) if row else None

def get_execution_time(start_time) -> int:
    return int((time() - start_time) * 1000)

def router_param_builder(tag, jwt=True):
    result = {
        "prefix": f"/{tag.replace('_', '/').replace('-', '_')}",
        "tags": [tag.replace("_", " ")],
    }
    # if jwt:
    #     result["dependencies"] = [Depends(JWTBearer())] if settings.JWT_ACTIVE else None

    return result


def change_field_id(data, replace_fields: dict = {}, add_fields: dict = {}):
    if isinstance(data, list):
        for datum in data:
            replace_fields["id"] = "_id"
            datum = change_fields(datum, replace_fields, add_fields)

    elif isinstance(data, dict):
        replace_fields["id"] = "_id"
        data = change_fields(data, replace_fields, add_fields)

    return data


def change_fields(
    datum: dict, replace_fields: dict = {}, add_fields: dict = {}
) -> dict:
    for new_field, old_field in replace_fields.items():
        if old_field in datum:
            datum[new_field] = datum.pop(old_field)

    for new_field, value in add_fields.items():
        if isinstance(value, str) and str(value).startswith("$$"):
            value = datum.get(str(value).removeprefix("$$"), None)
        datum[new_field] = value

    return datum


def is_include_schema(tag, end_point):
    if tag in settings.ACTIVE_ROUTERS:
        if not settings.ACTIVE_ROUTERS[tag]:
            return True
        elif end_point in settings.ACTIVE_ROUTERS[tag]:
            return True
        return False
    return True

def camel_to_snake_case(data):
    if isinstance(data, dict):
        result = {}
        for _key, _value in data.items():
            _key = re.sub(r'(?<!^)(?=[A-Z])', '_', _key).lower()
            result[_key] = _value
        return result
    elif isinstance(data, str):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', data).lower()

    return data

def to_snake_case(data):
    if isinstance(data, list):
        result = []
        for datum in data:
            result.append(camel_to_snake_case(datum))
        return result
    return camel_to_snake_case(data)
