import numpy as np
import pandas as pd
import pytz
import click
import re
import logging
from dateutil import parser
from datetime import datetime

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@click.command()
@click.option('--startdate', help='Required. Starting date of the analysis period. Format: dd-mm-yyy e.g. 01-11-2019')
@click.option('--enddate', help='Optional. Ending date of the analysis period. Format: dd-mm-yyy e.g. 01-11-2019. Default to starting date')
@click.option('--hours', help='Optional. Delivery hours for analysis. Format: hh-hh e.g. 07-22 (inclusive). Default to 00-24')
def main(startdate, enddate, hours):

    # Validating dates
    if not startdate:
        logger.info('Starting date of the analysis period is required! Try --help for more info.')
        return

    try:
        start_date = parser.parse(startdate, dayfirst=True).replace(tzinfo=pytz.utc)
        end_date = parser.parse(enddate, dayfirst=True).replace(tzinfo=pytz.utc) if enddate else start_date
    except ValueError:
        logger.info('Unable to parse dates! Try --help for more info')
        return

    if end_date < start_date:
        start_date, end_date = end_date, start_date
    
    # Validating hours
    if not hours:
        hours, start_hour, end_hour = '00-24', 0, 24
    else:
        hours_pattern = re.compile('^(\d{2})-(\d{2})$')
        match = hours_pattern.search(hours)
        if not match:
            print('Unable to parse hours! Try --help for more info')
            return

        start_hour = int(match.group(1))
        end_hour = int(match.group(2))

        if start_hour > 24 or end_hour > 24:
            logger.info('Unable to parse hours! Try --help for more info')
            return

        if start_hour > end_hour:
            start_hour, end_hour = end_hour, start_hour

    # Pre-run info
    if start_date == end_date:
        logger.info(f'Analyzing median pickup time on {start_date.strftime("%d, %b %Y")} during the hours between {hours}')
    else:
        logger.info(f'Analyzing median pickup time from {start_date.strftime("%d, %b %Y")} to {end_date.strftime("%d, %b %Y")} during the hours between {hours}')

    # Output
    output_filename = f'output_{int(datetime.now().timestamp())}.xlsx'
    result = get_median_pick_up_times(start_date, end_date, start_hour, end_hour)
    result.to_excel(output_filename)
    logging.info(f'Analysis completed! Output is stored in {output_filename}')

def get_median_pick_up_times(start_date, end_date, start_hour, end_hour):
    
    # Data
    locations = pd.read_csv('locations.csv')
    loc_ids = locations.location_id.tolist()

    pickup_times = pd.read_csv('pickup_times.csv')
    pickup_times.columns = ['location_id', 'ts', 'duration']
    pickup_times.ts = pd.to_datetime(pickup_times.ts, utc=True)

    # Filter row by boolean masks
    masks = pickup_times.location_id.isin(loc_ids) \
        & pickup_times.ts.dt.date.between(start_date.date(), end_date.date()) \
        & pickup_times.ts.dt.hour.between(start_hour, end_hour)

    filtered = pickup_times[masks].drop(['ts'], axis=1)
    logger.info(f'Found {filtered.shape[0]} records to analyze. Aggregating...!')
    
    # Aggregation
    timer_start = datetime.now()
    result = filtered.groupby(['location_id']).median()
    result.columns = ['median_pickup_time']
    timer_end = datetime.now()
    logger.info(f'Aggregation took {(timer_end - timer_start).total_seconds() * 1000} miliseconds')

    return result

if __name__ == '__main__':
    main()
