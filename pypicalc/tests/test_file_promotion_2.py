import csv

import arrow

from pypicalc.config import project_dpath


def calculate_age_sum(csv_fpath):
    age_sum = 0

    with open(csv_fpath) as csvfo:
        reader = csv.reader(csvfo)
        for row in reader:
            date_delta = arrow.now() - arrow.get(row[1])
            age_sum += date_delta.days // 365

    return age_sum


class TestAgeSum(object):

    def test_age_sum(self):
        csv_fpath = str(project_dpath.joinpath('data', 'ages.csv'))
        assert calculate_age_sum(csv_fpath) == 129

    def test_temporary_file(self, tmpdir):
        fake_csv_tmpfile = tmpdir.join('fake.csv')
        with fake_csv_tmpfile.open('w') as csv:
            csv.write('amy,2000-01-01\n')
            csv.write('judy,1980-02-01\n')

        assert calculate_age_sum(fake_csv_tmpfile.strpath) == 52
