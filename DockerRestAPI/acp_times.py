"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
from datetime import datetime, timedelta

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    try:
        control_dist_km = float(control_dist_km)
    except ValueError:
        raise ValueError("Control distance must be a numeric value")
    
    if control_dist_km > brevet_dist_km * 1.2:
        raise ValueError("Control distance cannot be more than 20% longer than brevet distance")
    
    if control_dist_km <= 200:
        opening_time_hours = control_dist_km / 34
    elif control_dist_km > 200 and control_dist_km <= 400:
        dist_over_two = control_dist_km - 200
        opening_time_hours = (200 / 34) + (dist_over_two / 32)
    elif control_dist_km > 400 and control_dist_km <= 600:
        dist_over_four = control_dist_km - 400
        opening_time_hours = (200 / 34) + (200 / 32) + (dist_over_four / 30)
    elif control_dist_km > 600 and control_dist_km <= 1000:
        dist_over_six = control_dist_km - 600
        opening_time_hours = (200 / 34) + (200 / 32) + (200 / 30) + (dist_over_six / 28)
    elif control_dist_km > 1000:
        dist_over_thousand = control_dist_km - 1000
        opening_time_hours = (200 / 34) + (200 / 32) + (200 / 30) + (400 / 28) + (dist_over_thousand / 26)

    brevet_start = datetime.fromisoformat(brevet_start_time + ":00:-08:00")

    # Calculate the opening time
    fractional_hours = opening_time_hours % 1
    whole_hours = opening_time_hours - fractional_hours
    opening_time_delta = timedelta(hours=int(whole_hours), minutes=round(fractional_hours * 60))

    if control_dist_km == 0:
        opening_time = brevet_start
    else:
        opening_time = brevet_start + opening_time_delta

    formatted_opening_time = opening_time.strftime("%Y-%m-%dT%H:%M:%S%z")

    # Calculate the opening time for final checkpoint if control distance is equal to brevet distance
    if control_dist_km >= brevet_dist_km and control_dist_km <= brevet_dist_km * 1.2:
        formatted_opening_time = get_final_checkpoint_opening_time(brevet_dist_km, brevet_start)

    return formatted_opening_time

def get_final_checkpoint_opening_time(brevet_dist_km, brevet_start):
    """
    Calculate the opening time for the final checkpoint.

    Args:
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start: datetime object, the official start time of the brevet

    Returns:
       An ISO 8601 format date string indicating the opening time for the final checkpoint.
    """
    # Calculate the opening time for the final checkpoint based on brevet distance
    if brevet_dist_km == 200:
        final_checkpoint_opening_time = brevet_start + timedelta(hours=5, minutes=33)
    elif brevet_dist_km == 300:
        final_checkpoint_opening_time = brevet_start + timedelta(hours=9)
    elif brevet_dist_km == 400:
        final_checkpoint_opening_time = brevet_start + timedelta(hours=12, minutes=8)
    elif brevet_dist_km == 600:
        final_checkpoint_opening_time = brevet_start + timedelta(hours=18, minutes=48)
    elif brevet_dist_km == 1000:
        final_checkpoint_opening_time = brevet_start + timedelta(hours=33, minutes=5)

    # Format the opening time according to the format specified in the requirements
    formatted_final_checkpoint_opening_time = final_checkpoint_opening_time.strftime("%Y-%m-%dT%H:%M:%S%z")

    return formatted_final_checkpoint_opening_time

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    Raises:
       ValueError: If the control distance is more than 20% longer than the brevet distance.
    """
    if control_dist_km > brevet_dist_km * 1.2:
        raise ValueError("Control distance cannot be more than 20% longer than brevet distance")
    
    if control_dist_km <= 600:
        closing_time_hours = control_dist_km / 15
    elif control_dist_km > 600 and control_dist_km <= 1000:
        dist_over_six = control_dist_km - 600
        closing_time_hours = (600 / 15) + (dist_over_six / 11.428)
    elif control_dist_km > 1000:
        dist_over_thousand = control_dist_km - 1000
        closing_time_hours = (600 / 15) + (400 / 11.428) + (dist_over_thousand / 13.333)

    brevet_start = datetime.fromisoformat(brevet_start_time + ":00:-08:00")

    fractional_hours = closing_time_hours % 1
    whole_hours = closing_time_hours - fractional_hours
    closing_time_delta = timedelta(hours=int(whole_hours), minutes=round(fractional_hours * 60))
    if control_dist_km == 0:
        closing_time = brevet_start + timedelta(hours=1)
    else:
        closing_time = brevet_start + closing_time_delta

    # Format the opening time according to the format specified in the requirements
    formatted_closing_time = closing_time.strftime("%Y-%m-%dT%H:%M:%S%z")

    # Calculate the opening time for final checkpoint if control distance is equal to brevet distance
    if control_dist_km >= brevet_dist_km and control_dist_km <= brevet_dist_km * 1.2:
        return get_final_checkpoint_closing_time(brevet_dist_km, brevet_start)

    return formatted_closing_time

    # Check if control distance is more than 20% longer than the brevet distance

def get_final_checkpoint_closing_time(brevet_dist_km, brevet_start):
    """
    Calculate the opening time for the final checkpoint.

    Args:
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start: datetime object, the official start time of the brevet

    Returns:
       An ISO 8601 format date string indicating the opening time for the final checkpoint.
    """
    # Calculate the opening time for the final checkpoint based on brevet distance
    if brevet_dist_km == 200:
        final_checkpoint_closing_time = brevet_start + timedelta(hours=13, minutes=30)
    elif brevet_dist_km == 300:
        final_checkpoint_closing_time = brevet_start + timedelta(hours=20)
    elif brevet_dist_km == 400:
        final_checkpoint_closing_time = brevet_start + timedelta(hours=27)
    elif brevet_dist_km == 600:
        final_checkpoint_closing_time = brevet_start + timedelta(hours=40)
    elif brevet_dist_km == 1000:
        final_checkpoint_closing_time = brevet_start + timedelta(hours=75)

    # Format the opening time according to the format specified in the requirements
    formatted_final_checkpoint_opening_time = final_checkpoint_closing_time.strftime("%Y-%m-%dT%H:%M:%S%z")

    return formatted_final_checkpoint_opening_time
    
