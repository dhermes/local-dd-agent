import base64
import string

# NOTE: I tried https://pypi.org/project/statsdmetrics/ and it did
#       not work

# See:
# - https://docs.datadoghq.com/developers/dogstatsd/datagram_shell/
# - https://docs.datadoghq.com/developers/metrics/#naming-custom-metrics
#
# The following custom metric naming convention must be followed:
#
# - Metric names must start with a letter.
# - Metric names must only contain ASCII alphanumerics, underscores, and
#   periods.
#   - Other characters, including spaces, are converted to underscores.
#   - Unicode is not supported.
# - Metric names must not exceed 200 characters. Fewer than 100 is preferred
#   from a UI perspective.
#
# **Note**: Metric names are case sensitive in Datadog.
#
#
# Metric
# ======
# <METRIC_NAME>:<VALUE>|<TYPE>|@<SAMPLE_RATE>|#<TAG_KEY_1>:<TAG_VALUE_1>,<TAG_2>
# TYPE: c ==COUNT, g==GUAGE, ms==TIMER, h==HISTOGRAM, s==SET, d==DISTRIBUTION
# OPTIONAL (<SAMPLE_RATE>)
# OPTIONAL (<TAG_*>)
# - "dd-sanity-check.request       :1|c|      #path :/                                                     "
# - "api.requests.response_code.all:1|c|      #route:*, method:GET, response_code:200, service:dd-sanity-check"
# - "api.requests.response_code.200:1|c|      #route:*, method:GET, response_code:200, service:dd-sanity-check"
# - "api.requests.response_time    :2|h|      #route:*, method:GET, response_code:200, service:dd-sanity-check"
# - "page.views:1|c"
# - "fuel.level:0.5|g"
# - "song.length:240|h|@0.5"
# - "users.uniques:1234|s"
# - "users.online:1|c|#country:china"
# - "users.online:1|c|@0.5|#country:china"


def _metric_type_pretty(value):
    if value == "c":
        return "COUNT"

    if value == "g":
        return ""

    if value == "ms":
        return "TIMER"

    if value == "h":
        return "HISTOGRAM"

    if value == "s":
        return "SET"

    if value == "d":
        return "DISTRIBUTION"

    return value


def parse_metric(value_bytes):
    result = {"raw_binary": base64.b64encode(value_bytes).decode("ascii")}
    try:
        value = value_bytes.decode("ascii")
    except UnicodeDecodeError:
        return result

    result["raw"] = value

    parts = value.split("|")
    metric_name_value = parts[0]
    if not metric_name_value[:1] in string.ascii_letters:
        # This means it must be something else, e.g. `_e` or `_sc`.
        # TODO: Return something else here, e.g. `None`
        return value_bytes

    if not 2 <= len(parts) <= 4:
        # This means the metric is malformed
        return result

    metric_name_value_parts = metric_name_value.split(":", 1)
    if len(metric_name_value_parts) != 2:
        # This means the pair is malformed
        return result

    metric_name, metric_value = metric_name_value_parts
    result["metric"] = {"name": metric_name, "value": metric_value}
    result["type"] = _metric_type_pretty(parts[1])

    if len(parts) == 3:
        rate_or_tags = parts[2]
        if rate_or_tags.startswith("@"):
            result["sample_rate"] = rate_or_tags[1:]
        elif rate_or_tags.startswith("#"):
            result["tags"] = rate_or_tags[1:].split(",")
        else:
            # This means the last segment is malformed
            return result
    elif len(parts) == 4:
        sample_rate = parts[2]
        if sample_rate.startswith("@"):
            result["sample_rate"] = sample_rate[1:]
        else:
            # This means the sample rate is malformed
            return result

        tag_pairs = parts[3]
        if tag_pairs.startswith("#"):
            result["tags"] = tag_pairs[1:].split(",")
        else:
            # This means the tag pairs segment is malformed
            return result

    return result


# Event
# =====
# _e{<TITLE>.length,<TEXT>.length}:<TITLE>|<TEXT>|d:<TIMESTAMP>|h:<HOSTNAME>|p:<PRIORITY>|t:<ALERT_TYPE>|#<TAG_KEY_1>:<TAG_VALUE_1>,<TAG_2>
# OPTIONAL (d:<TIMESTAMP>)
# OPTIONAL (h:<HOSTNAME>)
# OPTIONAL (p:<PRIORITY>)
# OPTIONAL (t:<ALERT_TYPE>)
# OPTIONAL (#<TAG_*>)
# - "_e{21,36}:An exception occurred|Cannot parse CSV file from 10.0.0.17|t:warning|#err_type:bad_file"
# - "_e{21,42}:An exception occurred|Cannot parse JSON request:\\n{"foo: "bar"}|p:low|#err_type:bad_request"
#
# Service Check
# =============
# _sc|<NAME>|<STATUS>|d:<TIMESTAMP>|h:<HOSTNAME>|#<TAG_KEY_1>:<TAG_VALUE_1>,<TAG_2>|m:<SERVICE_CHECK_MESSAGE>
# OPTIONAL (d:<TIMESTAMP>)
# OPTIONAL (h:<HOSTNAME>)
# OPTIONAL (#<TAG_*>)
# OPTIONAL (m:<SERVICE_CHECK_MESSAGE>)
# - "_sc|Redis connection|2|#env:dev|m:Redis connection timed out after 10s"
