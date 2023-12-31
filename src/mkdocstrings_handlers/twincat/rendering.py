from blark.summary import MethodSummary, PropertySummary



def do_sort_extended_methods(methods : list[MethodSummary]) -> list[MethodSummary]:
    """ if a functionblock is extended and overwrites some methods of its "base" every method is showed in the list. 
        In the documentation, we only want the ones that get called/accessed by the functionblock
    """

    sorted_methods : list[MethodSummary] = []
    for method in reversed(methods):
        if not any(getattr(sorted_method, "name", None) == method.name for sorted_method in sorted_methods):
            sorted_methods.append(method)

    return sorted_methods


    
def do_sort_extended_properties(properties : list[PropertySummary]) -> list[PropertySummary]:
    """ if a functionblock is extended and overwrites some methods of its "base" every method is showed in the list. 
        In the documentation, we only want the ones that get called/accessed by the functionblock
    """

    sorted_properties : list[PropertySummary] = []
    for property in reversed(properties):
        if not any(getattr(sorted_property, "name", None) == property.name for sorted_property in sorted_properties):
            sorted_properties.append(property)

    return sorted_properties