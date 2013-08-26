from django.forms import widgets
from django.forms.util import flatatt
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.utils import formats


class TwilioPhoneNumberLookup(widgets.Widget):

    def _format_value(self, value):
        if self.is_localized:
            return formats.localize_input(value)
        return value

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))
        return format_html("""
        <div class="input-group">
      <input type="text" class="form-control" disabled  {0}>
      <span class="input-group-btn">
        <button class="btn btn-primary" data-toggle="modal" href="#phonenumber-search" type="button">Search for Available Numbers</button>
      </span>
    </div><!-- /input-group -->
    """, flatatt(final_attrs))
