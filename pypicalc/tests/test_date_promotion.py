import arrow


def calculate_age_sum_helper(iterable, now=None):
    age_sum = 0

    if now is None:
        now = arrow.now()

    for row in iterable:
        date_delta = now - arrow.get(row[1])
        age_sum += date_delta.days // 365
    return age_sum


class TestAgeSum(object):
    age_data = [
        ('amy', '2000-01-01'),
        ('judy', '1980-02-01'),
    ]

    def test_default_now_value(self):
        assert calculate_age_sum_helper(self.age_data) == 52

    def test_injected_now_value(self):
        now = arrow.get('2014-03-30')
        assert calculate_age_sum_helper(self.age_data, now) == 48
