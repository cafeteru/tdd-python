from unittest import TestCase

from assertpy import assert_that

from src.csv_filter import Csv


class CsvShould(TestCase):
    def test_allow_for_correct_line_only(self):
        header_line = "Num_factura, Fecha, Bruto, Neto, IVA, IGIC, Concepto, CIF_cliente, NIF_cliente"
        invoice_line = "1,02/05/2019,1000,810,19,,ACER Laptop,B76430134,"
        incorrect_line = "A,line,missing,flieds,and,wrong,formats,"

        csv = Csv.filter([header_line, invoice_line, incorrect_line])

        assert_that(csv).is_equal_to([header_line, invoice_line])

    def test_exclude_lines_with_both_tax_fields_populated(self):
        header_line = "Num_factura, Fecha, Bruto, Neto, IVA, IGIC, Concepto, CIF_cliente, NIF_cliente"
        iva = "19"
        igic = "8"
        invoice_line = f"1,02/05/2019,1000,810,{iva},{igic},ACER Laptop,B76430134,"

        assert_that(Csv.filter([header_line, invoice_line])).is_equal_to([header_line])

    def test_at_least_one_tax_is_required(self):
        header_line = "Num_factura, Fecha, Bruto, Neto, IVA, IGIC, Concepto, CIF_cliente, NIF_cliente"
        no_tax_invoice_line = "1,02/05/2019,1000,810,,,ACER Laptop,B76430134,"

        assert_that(Csv.filter([header_line, no_tax_invoice_line])).is_equal_to([header_line, header_line])
