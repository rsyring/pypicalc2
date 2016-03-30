import csv

import arrow


def calculate_age_sum(csv_fpath):

    with open(csv_fpath) as csvfo:
        reader = csv.reader(csvfo)
        return calculate_age_sum_helper(reader)


def calculate_age_sum_helper(iterable):
    age_sum = 0
    for row in iterable:
        date_delta = arrow.now() - arrow.get(row[1])
        age_sum += date_delta.days // 365
    return age_sum


class TestAgeSum(object):

    def test_temporary_file(self, tmpdir):
        fake_csv_tmpfile = tmpdir.join('fake.csv')
        with fake_csv_tmpfile.open('w') as csv:
            csv.write('amy,2000-01-01\n')
            csv.write('judy,1980-02-01\n')

        csv_fpath = fake_csv_tmpfile.strpath
        assert calculate_age_sum(csv_fpath) == 52

    def test_iterable_data(self):
        data = [
            ('amy', '2000-01-01'),
            ('judy', '1980-02-01'),
        ]
        assert calculate_age_sum_helper(data) == 52
