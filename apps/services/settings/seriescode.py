import datetime
import typing
from typing import Optional, TypeVar
from returns.pipeline import is_successful
from returns.methods import unwrap_or_failure
from returns.result import Result, Failure, safe
from django.utils.translation import ugettext_lazy as _
from .exceptions import ParameterTypeError, ParameterValueError
from ...settings.models import NoSeriesLine

A = TypeVar('A', str, datetime.date)

class HandleError:
    status: str = ''
    message: str = ''

    def __init__(self) -> None:
        self.status = '400'
        self.message = ''

    def clear_error(self):
        self.status = ''
        self.message = ''

    def process_exception(self, failure):
        return self.fail(failure)

    def serialize_error(self, status, failure):
        message = unwrap_or_failure(failure)
        self.status = status
        self.message = message
        return failure

    def fail(self, failure):
        return self.serialize_error(400, failure)


class CheckTypeValues:
    error: object
    success: bool = False

    def __init__(self) -> None:
        self.error = HandleError()
        self.success = False
        self.code = ''
        self.dt = typing.cast(datetime.date, None)

    def initialize(self, code, dt):
        self.error.clear_error()
        self.success = False
        self.code = code
        self.dt = dt

    def _check_type(self) -> bool:
        raise_error = None
        result = True
        if self.dt is None:
            self.dt = datetime.date.today()

        if not isinstance(self.code, str):
            raise_error = ParameterTypeError(_('"Код Серия Номеров" аргумент должнен быть строкой'))
        elif isinstance(self.code, str) and self.code.strip() == '':
            raise_error = ParameterValueError(_('"Код Серия Номеров" не может содержать пустое значение'))
        elif not isinstance(self.dt, datetime.date):
            raise_error = ParameterTypeError(_('"Серия Номеров Дата начала" аргумент должнен быть датой'))

        if raise_error is not None:
            # result = False
            raise raise_error

        return result


class SeriesNoCreator(CheckTypeValues):
    def __init__(self) -> None:
        super(SeriesNoCreator, self).__init__()

    @safe
    def generate(self, code: str = '', dt: datetime.date = None) -> bool:
        success = False
        self.initialize(code, dt)
        result = self._check_type()

        if result:
            result = self.get_next_series_no()
            if not is_successful(result):
                raise_error = unwrap_or_failure(result)
                self.error.process_exception(
                    Failure(raise_error.message)
                )
            else:
                success = True

        return success

    def get_next_series_no(self) -> bool:
        record = NoSeriesLine.series_line.get_latest_code(
            code=self.code, starting_date=self.dt
        )
        new_series = self.__calculate_next_series_no(record)
        return new_series.strip() != ''

    def __calculate_next_series_no(self, record: Optional['NoSeriesLine']) -> str:
        last_no_used: str = record.last_no_used
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

        check_new_series_no = self.__check_new_series_no(new_series, record)

        if not check_new_series_no:
            new_series = ''

        return new_series

    def __check_new_series_no(self, new_series: str, record: Optional['NoSeriesLine']) -> bool:
        if new_series >= record.ending_no:
            raise ParameterValueError(
                _(f'Вы не можете присвоить новые номера из серии номеров {self.code}')
            )

        if record.series_no.date_order and record.last_date_used and self.dt < record.last_date_used:
            raise ParameterValueError(
                _(f'Вы не можете присвоить новые номера из серии номеров {self.code} до даты '
                  f'{record.last_date_used}')
            )

        return True
