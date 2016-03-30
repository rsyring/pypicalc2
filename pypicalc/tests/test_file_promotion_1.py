import csv

import arrow

from pypicalc.config import project_dpath


def calculate_age_sum():
    csv_fpath = str(project_dpath.joinpath('data', 'ages.csv'))
    age_sum = 0

    with open(csv_fpath) as csvfo:
        reader = csv.reader(csvfo)
        for row in reader:
            date_delta = arrow.now() - arrow.get(row[1])
            age_sum += date_delta.days // 365

    return age_sum


class TestAgeSum(object):

    def test_age_sum(self):
        assert calculate_age_sum() == 129
