from django.core.management.base import BaseCommand, CommandError
from datetime import date, timedelta
# from parse.models import *

class Command(BaseCommand):
    help = 'parses input .CSV for Dynamics Import (Luna)'

    def add_arguments(self, parser):
        parser.add_argument('in_csv', type=str)
        parser.add_argument('out_csv', nargs='?', type=str)

    def handle(self, *args, **options):
        import sys, csv#, xlrd
        hours = {}
        headers = []

        def parse_client(client):
            # TODO: Set this in project settings
            # TODO 2: Set these with user input from web form (non KS users)
            DEFAULT_PROJECT_NAME = "Home"
            DEFUALT_PROJECT_CODE = "1-3000-000-0"

            proj_name = ' '.join(client.split(' ')[:-1])
            proj_code = client.split(' ')[-1]
            if proj_name == "":
                proj_name = DEFAULT_PROJECT_NAME
            if proj_code == "":
                proj_code = DEFUALT_PROJECT_CODE
            return { 'name': proj_name, 'code': proj_code}

        def get_seconds(duration):
            h, m, s = duration.split(":")
            return int(h)*3600 + int(m)*60 + int(s)

        def get_hours_from_seconds(duration_in_seconds):
            return round(float(duration_in_seconds/3600), 1)

        # TODO: Set this in project settings
        # TODO 2: Set these with user input from web form (non KS users)
        DEFAULT_PROJECT_NAME = "Home"
        DEFUALT_PROJECT_CODE = "1-3000-000-0"
        DEFAULT_PROJECT_TASK = "00-00-000"

        in_csv = options['in_csv']

        with open(in_csv, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            dates = []
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    proj = parse_client(row["Client"])
                    if not proj["code"] in hours:
                        hours[proj["code"]] = {}
                    if not proj["name"] in hours[proj["code"]]:
                        hours[proj["code"]][proj["name"]] = {}
                    if row["Task"]:
                        row_task = row["Task"]
                    else:
                        row_task = DEFAULT_PROJECT_TASK
                    if row_task == "":
                        row_task = DEFAULT_PROJECT_TASK

                    if not row_task in hours[proj["code"]][proj["name"]]:
                        hours[proj["code"]][proj["name"]][row_task] = {}
                    if not row["Start date"] in hours[proj["code"]][proj["name"]][row_task]:
                        hours[proj["code"]][proj["name"]][row_task][row["Start date"]] = 0
                    if not row["Start date"] in dates:
                        dates.append(row["Start date"])

                    hours[proj["code"]][proj["name"]][row_task][row["Start date"]] += get_seconds(row["Duration"])

        out_csv = options['out_csv']
        if not out_csv:
            out_csv = '.'.join([in_csv.split('.')[0], 'out','csv'])

        # put date column headers in order
        dates.sort()

        # Find out if any days are skipped to make it obvious when there are unworked day columns
        # Thanks to John La Rooy: https://stackoverflow.com/a/2315279
        day_dates = []
        for day in dates:
            y, m, d = day.split('-')
            day_dates.append(date(int(y), int(m), int(d)))

        date_set = set(day_dates[0] + timedelta(x) for x in range((day_dates[-1] - day_dates[0]).days))
        missing = sorted(date_set - set(day_dates))

        # insert the unworked day column headers
        for missed_day in missing:
            dates.append(missed_day.strftime('%Y-%m-%d'))

        dates.sort()

        day_totals_row = {
            'Code': 'Total',
            'Project': '-------',
            'Task': '-------',
        }

        for day in dates:
            day_totals_row[day] = 0

        with open(out_csv, mode="w") as csv_file:
            fieldnames = ['Code', 'Project', 'Task'] + dates + ['Total']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            projects = hours.keys()
            for proj_code in sorted(projects):
                proj_code_text = proj_code
                code_total = 0
                projects = hours[proj_code].keys()
                for proj_key in sorted(projects):
                    proj_key_text = proj_key
                    proj_total = 0
                    tasks = hours[proj_code][proj_key].keys()
                    for proj_task in sorted(tasks):
                        row_dict = {
                            'Project': str(proj_key_text),
                            'Code': str(proj_code_text),
                            'Task': proj_task,
                        }
                        task_total = 0
                        for date_key in dates:
                            if date_key in hours[proj_code][proj_key][proj_task]:
                                row_dict[date_key] = get_hours_from_seconds(hours[proj_code][proj_key][proj_task][date_key])
                                task_total += row_dict[date_key]
                                day_totals_row[date_key] += row_dict[date_key]
                        row_dict['Total'] = round(task_total,1)
                        writer.writerow(row_dict)
                        proj_key_text = ""
                        proj_code_text = ""
                        code_total += task_total
                    proj_total += code_total
            weekly_total = 0
            for day in dates:
                day_totals_row[day] = round(day_totals_row[day], 1)
                weekly_total += day_totals_row[day]
            day_totals_row['Total'] = round(weekly_total,1)
            writer.writerow(day_totals_row)
