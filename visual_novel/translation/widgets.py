from bitfield.forms import BitFieldCheckboxSelectMultiple


class StatusBitFieldWidget(BitFieldCheckboxSelectMultiple):
    # Custom template to put buttons in a row
    template_name = 'status_checkbox_option.html'
    input_type = 'radio'
