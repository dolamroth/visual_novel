from bitfield.forms import BitFieldCheckboxSelectMultiple


class StatusBitFieldWidget(BitFieldCheckboxSelectMultiple):
    template_name = 'status_checkbox_option.html'
    input_type = 'radio'
