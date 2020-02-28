from typing import Dict, TypeVar
class Type_Check_Error (Exception):
    def __init__(self,data_name, msg):
        self.data_name  = data_name
        self.msg        = msg

Dict_Values = TypeVar("Dict_Values")
def check_for_type(dictionary_name : str, dictionary : Dict[str, Dict_Values]):
    try:
        if dictionary_name == "additions":
            assert check_for_type(dictionary,   { "title"       : ""
                                                , "book"        : ""
                                                , "articles"    : []
                                                }
                        )
        elif dictionary == "amendments":
            assert check_for_type(dictionary,   { "book"        : ""
                                                , "law"         : ""
                                                , "articles"    : []
                                                }
                        )
        elif dictionary == "repeals":
            assert check_for_type(dictionary,   { "books"       : ""
                                                , "laws"        : []
                                                })
        else:
            raise Type_Check_Error(dictionary_name, "unknown dictionary name")
    except AssertionError as assertion_error:
        raise Type_Check_Error(dictionary_name, assertion_error.args[0])
    except Exception as e:
        raise e
    else:
        return True

def check_dictionary_for_type   (   dictionary  : Dict[str, Dict_Values]
                                ,   types       : Dict[str, Dict_Values]
                                ):
    try:
        tests           = [(type(types[key]) == type(dictionary[key]), key) for key in types]
        test_failed     = False in filter(lambda t: t[0], tests)
        assert not test_failed, f"Type Check Failed: {list(map(lambda t: t[1], filter(lambda t: t[0] == False, tests)))}"

    except Exception as e:
        raise e
    else:
        return True
