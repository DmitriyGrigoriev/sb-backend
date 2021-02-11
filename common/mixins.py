from collections import namedtuple
from django.utils.translation import ugettext_lazy as _
from rest_framework.validators import qs_exists, qs_filter
from rest_framework.exceptions import ValidationError
from apps.settings.models import NoSeriesLine


class SeriesCreateSerializerMixin:
    class RequiredValidatorClass(object):
        SERIES_CODE_VALIDATOR_CLASS = 'SeriesCodeValidator'

    class Warning(
        namedtuple('warn', ['field', 'warning_message', 'code'])
    ):
        pass

    warn = {}
    missing_message = _(
        f'Наличие класса валидатора {RequiredValidatorClass.SERIES_CODE_VALIDATOR_CLASS} '
        f'обязательно при использовании миксина.'
    )
    validator = None
    max_counts_attempt_get_unique_serial_no = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__required_validator_class([self.RequiredValidatorClass.SERIES_CODE_VALIDATOR_CLASS])

    def __required_validator_class(self, validator_class):
        missing_items = 1
        for validator_name in self.validators:
            if validator_name.__class__.__name__ in validator_class:
                self.validator = validator_name
                missing_items = 0
                break

        if missing_items:
            missing_message = {
                self.RequiredValidatorClass.SERIES_CODE_VALIDATOR_CLASS: self.missing_message
            }
            raise ValidationError(missing_message, code='required')

        return bool(missing_items)

    def get_latest_code(self):
        date_field_value = self.validator.date_field_value
        series_no = self.validator.series_no
        queryset = NoSeriesLine.series_line.get_latest_code(
            series_no=series_no, starting_date=date_field_value
        )
        return queryset

    def update_latest_no(self, pk: int, new_series: str):
        # Update last_no_used field
        record = NoSeriesLine.series_line.get(pk=pk)
        record.last_no_used = new_series
        record.save(update_fields=['last_no_used'])

    def calculate_next_series_no(self, last_no_used: str, warning_no: str, ending_no: str, code: str) -> str:
        # last_no_used: str = last_no_used
        # warning_no: str = warning_no
        series_no: str = last_no_used
        last_non_digit_char: str = [s for s in series_no if not s.isdigit()][-1]

        if len(last_non_digit_char) > 0:
            last_non_digit_char_position: int = series_no.find(last_non_digit_char) + 1
        else:
            last_non_digit_char_position: int = 0

        digit_suffix_str: str = series_no[last_non_digit_char_position:]
        digit_suffix_len: int = len(digit_suffix_str)
        digit_suffix_int: int = int(digit_suffix_str)
        new_series_int: int = digit_suffix_int + 1
        new_series: str = last_no_used.replace(digit_suffix_str, str(new_series_int).zfill(digit_suffix_len))

        """
        https://dimag.atlassian.net/wiki/spaces/SBP/pages/405733400        
        Если в найденной строке закончились номера («Last No Used» >= «Ending No»), то ошибка 
        «Вы не можете присвоить новые номера из серии номеров %1» (%1 = SeriesCode)
        """
        if new_series >= ending_no:
            raise ValidationError({
                self.validator.field: _(f'Вы не можете присвоить новые номера из серии номеров {code}')
            }, code='series_no')
        """
        Если в найденной строке заполнено поле «Warning No» и новый 
        присвоенный номер >= «Warning No», то предупреждение 
        «Внимание! Заканчиваются номера в серии номеров %1» (%1 = SeriesCode)
        """
        if warning_no.strip() != '' and new_series >= warning_no:
            self.warn = self.Warning(
                self.validator.field,
                str(_(f'Внимание! Заканчиваются номера в «Серии Номеров» {code}')),
                'series_no'
            )

        return new_series

    def filter_queryset(self, queryset, new_series: str):
        """
        Filter the queryset to all instances matching the given attributes.
        """
        # Determine the filter keyword arguments and filter the queryset.
        filter_kwargs = {
            self.validator.field_name: new_series
        }
        return qs_filter(queryset, **filter_kwargs)

    def save(self, **kwargs):
        field_name: str = self.validator.field
        field_value: str = self.validator.field_value
        # if user didn't fill a field 'code' -> generate new series no
        if len(field_value) == 0:
            # Get query with the latest serial number
            queryset = self.get_latest_code()
            last_no_used = queryset.last_no_used
            warning_no = queryset.warning_no
            ending_no = queryset.ending_no
            code = queryset.series_no.code
            generate_new_serial_no = False
            # Trying to generate new serial no
            for n in range(self.max_counts_attempt_get_unique_serial_no):
                new_series: str = self.calculate_next_series_no(
                    last_no_used=last_no_used,
                    warning_no=warning_no,
                    ending_no=ending_no,
                    code=code
                )
                if new_series.strip() == '':
                    # Failure to generate a new serial number code
                    raise ValidationError({
                        field_name: _(
                            f'Не удалось сгенерировать новый «Код» для «Серии Номеров» {code}')
                    }, code='series_no')
                # Generating new_series no code was successful if new_series != ''
                if new_series.strip() != '':
                    # Do checking uniqueness in model
                    if qs_exists(
                            self.filter_queryset(self.validator.queryset, new_series)
                    ):
                        last_no_used = new_series
                        # Try generate next serial number
                        generate_new_serial_no = False
                        continue
                    else:
                        generate_new_serial_no = True
                        break

            if not generate_new_serial_no:
                # Failure to generate a new serial number code
                raise ValidationError({
                    field_name: _(
                        f'Не удалось сгенерировать новый «Код» для «Серии Номеров» {code} '
                        f'за максимальное число доступных попыток')
                }, code='series_no')

            self.update_latest_no(pk=queryset.pk, new_series=new_series)
            kwargs[field_name] = new_series
            return super().save(**kwargs)

        return super().save(**kwargs)
