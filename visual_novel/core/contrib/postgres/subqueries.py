from django.db.models import Subquery, IntegerField

from .fields import PostgresqlJsonField


class OrderableSubquery(Subquery):
    # Мотивация: Django Subquery не предназначены для выгрузки массива результатов
    # (соответствующий функционал планируется к версии 4.0), поэтому не отловлен баг,
    # при котором теряется (?) order_by при клонировании Queryset.query
    def __init__(self, queryset, output_field=None, **extra):
        self.order_by = queryset.query.order_by
        super().__init__(queryset, output_field=output_field, **extra)

    def as_sql(self, compiler, connection, template=None, **extra_context):
        connection.ops.check_expression_support(self)
        template_params = {**self.extra, **extra_context}

        if self.order_by:
            self.query.add_ordering(*self.order_by)

        subquery_sql, sql_params = self.query.as_sql(compiler, connection)
        template_params['subquery'] = subquery_sql[1:-1]

        template = template or template_params.get('template', self.template)
        sql = template % template_params
        return sql, sql_params


class SubqueryJson(OrderableSubquery):
    template = "(SELECT row_to_json(_subquery) FROM (%(subquery)s) _subquery)"
    output_field = PostgresqlJsonField()


class SubqueryJsonAgg(OrderableSubquery):
    template = "(SELECT array_to_json(coalesce(array_agg(row_to_json(_subquery)), array[]::json[])) FROM (%(subquery)s) _subquery)"
    output_field = PostgresqlJsonField()


class SubqueryCount(Subquery):
    template = "(SELECT count(*) FROM (%(subquery)s) _count)"
    output_field = IntegerField()
