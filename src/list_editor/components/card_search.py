from django_components import component

@component.register("card_search")
class Card(component.Component):
    template_name = "components/card_search.html"

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self, search_results, page):
        return {
            "search_results": search_results,
            "page": page,
            "previous_page": page-1,
            "next_page": page + 1,
        }
