from datetime import datetime, timezone, timedelta


KST = timezone(timedelta(hours=9))


def now_utc():
    return datetime.now(timezone.utc)


def now_kst():
    return datetime.now(KST)


def iso_utc():
    return now_utc().replace(microsecond=0).isoformat().replace("+00:00", "Z")


def compact_timestamp():
    return now_utc().strftime("%Y%m%dT%H%M%SZ")


def week_id(dt=None):
    dt = dt or now_kst()
    year, week, _ = dt.isocalendar()
    return "%04d-W%02d" % (year, week)

