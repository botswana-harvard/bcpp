from datetime import datetime

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect

from lis.labeling.exceptions import LabelPrinterError

from .classes import RequisitionLabel
from .models import Order, OrderItem


def create_order(modeladmin, request, queryset):
    order_datetime = datetime.today()
    order = Order.objects.create(order_datetime=order_datetime)
    for aliquot in queryset:
        OrderItem.objects.create(order=order, aliquot=aliquot, order_datetime=order_datetime)
    change_url = reverse("admin:bcpp_lab_order_change", args=(order.pk, ))
    return HttpResponseRedirect(change_url)
create_order.short_description = "Create order from selected aliquots"


def print_requisition_label(modeladmin, request, requisitions):
    """ Prints a requisition label."""
    requisition_label = RequisitionLabel()
    try:
        for requisition in requisitions:
            if not requisition.is_receive:
                messages.add_message(request, messages.ERROR, ('Sample {} has not been received. Receive first, '
                                     'then print the label.').format(requisition.requisition_identifier))
                break
            else:
                requisition_label.print_label_for_requisition(request, requisition)
                requisition.is_labelled = True
                requisition.is_labelled_datetime = datetime.today()
                requisition.save()
    except LabelPrinterError as label_printer_error:
        messages.add_message(request, messages.ERROR, str(label_printer_error))
print_requisition_label.short_description = "LABEL: print requisition label"
