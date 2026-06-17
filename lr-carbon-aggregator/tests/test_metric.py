import time

import sender


def test_send_metrics():
    timestamp = int(time.time())
    metrics = [
        ("tests-lr-carbon-aggregator.metric.1", "4", timestamp),
        ("tests-lr-carbon-aggregator.metric.1", "5", timestamp + 1),
        ("tests-lr-carbon-aggregator.metric.1", "15", timestamp + 2),
        ("tests-lr-carbon-aggregator.metric.1", "1", timestamp + 3),
    ]
    sender.send(metrics)
    time.sleep(1)
    with open("/app/metric_storage") as f:
        content = f.read()
    assert [
        f"""[Pickle] tests-lr-carbon-aggregator.metric.1 = 4.0 (Time: {timestamp}.0)""",
        f"""[Pickle] tests-lr-carbon-aggregator.metric.1 = 5.0 (Time: {timestamp + 1}.0)""",
        f"""[Pickle] tests-lr-carbon-aggregator.metric.1 = 15.0 (Time: {timestamp + 2}.0)""",
        f"""[Pickle] tests-lr-carbon-aggregator.metric.1 = 1.0 (Time: {timestamp + 3}.0)""",
    ] == content.strip().split("\n")[-4:]


def test_ivideon_metrics1():
    # Panel: Cloud VCA Visitor Counter: Counter API Timings
    # wait till next aggregator start of interval
    # to avoid interval Intersection
    while True:
        if (timestamp := int(time.time())) % 10 in [1, 2]:
            break
        time.sleep(0.1)

    metrics = [
        ("ivideon.timers.api5.visitor_counter_events.upload.upper", "4", timestamp),
        ("ivideon.timers.api5.visitor_counter_events.upload.upper", "5", timestamp + 1),
        (
            "ivideon.timers.api5.visitor_counter_events.upload.upper",
            "40",
            timestamp + 2,
        ),
        ("ivideon.timers.api5.visitor_counter_events.upload.upper", "5", timestamp + 3),
        ("ivideon.timers.api5.visitor_counter_reports.upload.upper", "15", timestamp),
        (
            "ivideon.timers.api5.visitor_counter_reports.upload.upper",
            "1",
            timestamp + 1,
        ),
        (
            "ivideon.timers.api5.visitor_counter_reports.upload.upper",
            "7",
            timestamp + 2,
        ),
        (
            "ivideon.timers.api5.visitor_counter_reports.upload.upper",
            "10",
            timestamp + 3,
        ),
    ]
    sender.send(metrics)
    time.sleep(12)  # wait for aggregation
    with open("/app/metric_storage") as f:
        content = f.read()
    assert [
        f"""[Pickle] ivideon.timers.api5.visitor_counter_events.all_methods.upper = 40.0 (Time: { (timestamp // 10) * 10}.0)""",
        f"""[Pickle] ivideon.timers.api5.visitor_counter_reports.all_methods.upper = 15.0 (Time: { (timestamp // 10) * 10}.0)""",
    ] == content.strip().split("\n")[-2:]


def test_ivideon_metrics2():
    # Panel: Main 5xx Errors: General
    # wait till next aggregator start of interval
    # to avoid interval Intersection
    while True:
        if (timestamp := int(time.time())) % 10 in [1, 2]:
            break
        time.sleep(0.1)

    metrics = [
        ("ivideon.gauges.haproxy.gw1.api4.hrsp_5xx", "401", timestamp),
        ("ivideon.gauges.haproxy.gw1.api4.hrsp_5xx", "54", timestamp + 1),
        (
            "ivideon.gauges.haproxy.gw1.api4.hrsp_5xx",
            "4",
            timestamp + 2,
        ),
        ("ivideon.gauges.haproxy.gw1.api4.hrsp_5xx", "13", timestamp + 3),
        ("ivideon.gauges.haproxy.gw2.api5.hrsp_5xx", "17", timestamp),
        (
            "ivideon.gauges.haproxy.gw2.api5.hrsp_5xx",
            "1",
            timestamp + 1,
        ),
        (
            "ivideon.gauges.haproxy.gw3.api5.hrsp_5xx",
            "71",
            timestamp + 2,
        ),
        (
            "ivideon.gauges.haproxy.gw3.api5.hrsp_5xx",
            "101",
            timestamp + 3,
        ),
    ]
    sender.send(metrics)
    time.sleep(12)  # wait for aggregation
    with open("/app/metric_storage") as f:
        content = f.read()
    assert [
        f"""[Pickle] ivideon.gauges.haproxy.all_gateways.api4.hrsp_5xx = 472.0 (Time: { (timestamp // 10) * 10}.0)""",
        # metric from another rule for these input metrics
        f"""[Pickle] ivideon.gauges.haproxy.total_cluster.all_services.hrsp_5xx = 662.0 (Time: { (timestamp // 10) * 10}.0)""",
        f"""[Pickle] ivideon.gauges.haproxy.all_gateways.api5.hrsp_5xx = 190.0 (Time: { (timestamp // 10) * 10}.0)""",
    ] == content.strip().split("\n")[-3:]


def test_ivideon_metrics3():
    # Panel: Main 5xx Errors: API5 Stale Requests
    # wait till next aggregator start of interval
    # to avoid interval Intersection
    while True:
        if (timestamp := int(time.time())) % 10 in [1, 2]:
            break
        time.sleep(0.1)

    metrics = [
        ("ivideon.counters.api5.1.A.stale.count", "4", timestamp),
        ("ivideon.counters.api5.1.A.stale.count", "5", timestamp + 1),
        (
            "ivideon.counters.api5.2.B.stale.count",
            "6",
            timestamp + 2,
        ),
        ("ivideon.counters.api5.2.C.stale.count", "7", timestamp + 3),
        ("ivideon.counters.api5.1.A.21.stale.count", "8", timestamp),
        (
            "ivideon.counters.api5.1.A.21.stale.count",
            "9",
            timestamp + 1,
        ),
        (
            "ivideon.counters.api5.1.B.21.stale.count",
            "10",
            timestamp + 2,
        ),
        (
            "ivideon.counters.api5.1.B.31.stale.count",
            "11",
            timestamp + 3,
        ),
        ("ivideon.counters.api5.servers.wifi.1.stale.count", "17", timestamp),
        (
            "ivideon.counters.api5.servers.wifi.1.stale.count",
            "12",
            timestamp + 1,
        ),
        (
            "ivideon.counters.api5.servers.wifi.2.stale.count",
            "13",
            timestamp + 2,
        ),
        (
            "ivideon.counters.api5.servers.wifi.2.stale.count",
            "14",
            timestamp + 3,
        ),
    ]
    sender.send(metrics)
    time.sleep(12)  # wait for aggregation
    with open("/app/metric_storage") as f:
        content = f.read()
    assert [
        f"""[Pickle] ivideon.counters.api5.aggregated.stale_group_A.count = 22.0 (Time: { (timestamp // 10) * 10}.0)""",
        f"""[Pickle] ivideon.counters.api5.aggregated.stale_group_B.count = 94.0 (Time: { (timestamp // 10) * 10}.0)""",
        f"""[Pickle] ivideon.counters.api5.aggregated.stale_wifi.count = 56.0 (Time: { (timestamp // 10) * 10}.0)""",
    ] == content.strip().split("\n")[-3:]


def test_ivideon_metrics4():
    # Panel:# Panel: Main API4: API4 Total RPS
    # wait till next aggregator start of interval
    # to avoid interval Intersection
    while True:
        if (timestamp := int(time.time())) % 10 in [1, 2]:
            break
        time.sleep(0.1)

    metrics = [
        ("ivideon.timers.api4.billing.gate.post.count_ps", "4", timestamp),
        ("ivideon.timers.api4.billing.gate.post.count_ps", "5", timestamp + 1),
        (
            "ivideon.timers.api4.billing.gate.post.count_ps",
            "6",
            timestamp + 2,
        ),
        ("ivideon.timers.api4.face.gate.x.count_ps", "7", timestamp + 3),
        ("ivideon.timers.api4.face.gate.x.count_ps", "8", timestamp),
        (
            "ivideon.timers.api4.face.gate.x.count_ps",
            "9",
            timestamp + 1,
        ),
    ]
    sender.send(metrics)
    time.sleep(12)  # wait for aggregation
    with open("/app/metric_storage") as f:
        content = f.read()
    assert [
        f"""[Pickle] ivideon.timers.api4.aggregated.total_rps.count_ps = 39.0 (Time: { (timestamp // 10) * 10}.0)""",
    ] == content.strip().split("\n")[-1:]