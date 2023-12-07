from django_components import component


@component.register("card")
class Card(component.Component):
    template_name = "components/card.html"

    # This component takes one parameter, a date string to show in the template
    def get_context_data(self):
        return {}