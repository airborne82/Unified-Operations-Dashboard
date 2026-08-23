import asyncio
from typing import TypedDict

import reflex as rx


class LatencyPoint(TypedDict):
    t: str
    p50: int
    p95: int
    p99: int


class ThroughputPoint(TypedDict):
    t: str
    requests: int
    errors: int


class BudgetPoint(TypedDict):
    service: str
    consumed: int
    remaining: int


class IncidentPoint(TypedDict):
    day: str
    sev1: int
    sev2: int
    sev3: int


class SaturationPoint(TypedDict):
    resource: str
    used: int
    headroom: int


class RangeOption(TypedDict):
    id: str
    label: str


class GrafanaState(rx.State):
    time_range: str = "6h"
    is_refreshing: bool = False
    last_scrape: str = "04:21:07 ZULU"
    show_p99: bool = True

    ranges: list[RangeOption] = [
        {"id": "15m", "label": "15m"},
        {"id": "1h", "label": "1h"},
        {"id": "6h", "label": "6h"},
        {"id": "24h", "label": "24h"},
    ]

    latency_by_range: dict[str, list[LatencyPoint]] = {
        "15m": [
            {"t": "-15m", "p50": 78, "p95": 132, "p99": 214},
            {"t": "-12m", "p50": 81, "p95": 141, "p99": 236},
            {"t": "-09m", "p50": 76, "p95": 128, "p99": 198},
            {"t": "-06m", "p50": 88, "p95": 158, "p99": 271},
            {"t": "-03m", "p50": 84, "p95": 149, "p99": 244},
            {"t": "now", "p50": 79, "p95": 136, "p99": 221},
        ],
        "1h": [
            {"t": "-60m", "p50": 74, "p95": 121, "p99": 188},
            {"t": "-48m", "p50": 82, "p95": 146, "p99": 241},
            {"t": "-36m", "p50": 91, "p95": 168, "p99": 302},
            {"t": "-24m", "p50": 86, "p95": 154, "p99": 262},
            {"t": "-12m", "p50": 80, "p95": 139, "p99": 228},
            {"t": "now", "p50": 79, "p95": 136, "p99": 221},
        ],
        "6h": [
            {"t": "22:00", "p50": 68, "p95": 112, "p99": 174},
            {"t": "23:00", "p50": 72, "p95": 118, "p99": 186},
            {"t": "00:00", "p50": 77, "p95": 129, "p99": 205},
            {"t": "01:00", "p50": 84, "p95": 148, "p99": 249},
            {"t": "02:00", "p50": 96, "p95": 181, "p99": 331},
            {"t": "03:00", "p50": 104, "p95": 204, "p99": 386},
            {"t": "04:00", "p50": 79, "p95": 136, "p99": 221},
        ],
        "24h": [
            {"t": "04:00", "p50": 71, "p95": 116, "p99": 181},
            {"t": "08:00", "p50": 88, "p95": 152, "p99": 258},
            {"t": "12:00", "p50": 112, "p95": 219, "p99": 402},
            {"t": "16:00", "p50": 101, "p95": 194, "p99": 355},
            {"t": "20:00", "p50": 83, "p95": 144, "p99": 236},
            {"t": "00:00", "p50": 77, "p95": 129, "p99": 205},
            {"t": "04:00", "p50": 79, "p95": 136, "p99": 221},
        ],
    }

    throughput_by_range: dict[str, list[ThroughputPoint]] = {
        "15m": [
            {"t": "-15m", "requests": 742, "errors": 4},
            {"t": "-12m", "requests": 768, "errors": 6},
            {"t": "-09m", "requests": 731, "errors": 3},
            {"t": "-06m", "requests": 802, "errors": 11},
            {"t": "-03m", "requests": 789, "errors": 8},
            {"t": "now", "requests": 812, "errors": 5},
        ],
        "1h": [
            {"t": "-60m", "requests": 688, "errors": 3},
            {"t": "-48m", "requests": 714, "errors": 7},
            {"t": "-36m", "requests": 764, "errors": 14},
            {"t": "-24m", "requests": 798, "errors": 12},
            {"t": "-12m", "requests": 786, "errors": 6},
            {"t": "now", "requests": 812, "errors": 5},
        ],
        "6h": [
            {"t": "22:00", "requests": 512, "errors": 2},
            {"t": "23:00", "requests": 548, "errors": 3},
            {"t": "00:00", "requests": 604, "errors": 5},
            {"t": "01:00", "requests": 662, "errors": 9},
            {"t": "02:00", "requests": 728, "errors": 18},
            {"t": "03:00", "requests": 771, "errors": 24},
            {"t": "04:00", "requests": 812, "errors": 5},
        ],
        "24h": [
            {"t": "04:00", "requests": 488, "errors": 2},
            {"t": "08:00", "requests": 702, "errors": 8},
            {"t": "12:00", "requests": 941, "errors": 27},
            {"t": "16:00", "requests": 884, "errors": 19},
            {"t": "20:00", "requests": 706, "errors": 7},
            {"t": "00:00", "requests": 604, "errors": 5},
            {"t": "04:00", "requests": 812, "errors": 5},
        ],
    }

    error_budget: list[BudgetPoint] = [
        {"service": "api-gateway", "consumed": 31, "remaining": 69},
        {"service": "task-runner", "consumed": 58, "remaining": 42},
        {"service": "edge-proxy", "consumed": 84, "remaining": 16},
        {"service": "gladius-inf", "consumed": 22, "remaining": 78},
        {"service": "mail-relay", "consumed": 46, "remaining": 54},
    ]

    incident_by_range: dict[str, list[IncidentPoint]] = {
        "15m": [],
        "1h": [
            {"day": "04:00", "sev1": 1, "sev2": 1, "sev3": 0},
        ],
        "6h": [
            {"day": "22:00", "sev1": 0, "sev2": 1, "sev3": 2},
            {"day": "00:00", "sev1": 0, "sev2": 0, "sev3": 1},
            {"day": "02:00", "sev1": 0, "sev2": 2, "sev3": 3},
            {"day": "04:00", "sev1": 1, "sev2": 1, "sev3": 0},
        ],
        "24h": [
            {"day": "MON", "sev1": 0, "sev2": 2, "sev3": 4},
            {"day": "TUE", "sev1": 1, "sev2": 1, "sev3": 3},
            {"day": "WED", "sev1": 0, "sev2": 3, "sev3": 5},
            {"day": "THU", "sev1": 2, "sev2": 2, "sev3": 2},
            {"day": "FRI", "sev1": 1, "sev2": 4, "sev3": 6},
        ],
    }

    saturation: list[SaturationPoint] = [
        {"resource": "CPU", "used": 68, "headroom": 32},
        {"resource": "MEM", "used": 74, "headroom": 26},
        {"resource": "DISK", "used": 77, "headroom": 23},
        {"resource": "NET", "used": 91, "headroom": 9},
        {"resource": "IOPS", "used": 54, "headroom": 46},
    ]

    @rx.event
    def set_range(self, range_id: str):
        if range_id == self.time_range:
            return
        self.time_range = range_id
        yield GrafanaState.refresh

    @rx.event
    def toggle_p99(self):
        self.show_p99 = not self.show_p99

    @rx.event
    async def refresh(self):
        self.is_refreshing = True
        yield
        await asyncio.sleep(0.5)
        self.is_refreshing = False

    @rx.var
    def latency_series(self) -> list[LatencyPoint]:
        return self.latency_by_range.get(self.time_range, [])

    @rx.var
    def throughput_series(self) -> list[ThroughputPoint]:
        return self.throughput_by_range.get(self.time_range, [])

    @rx.var
    def incident_series(self) -> list[IncidentPoint]:
        return self.incident_by_range.get(self.time_range, [])

    @rx.var
    def p95_now(self) -> int:
        series = self.latency_series
        return series[-1]["p95"] if series else 0

    @rx.var
    def requests_now(self) -> int:
        series = self.throughput_series
        return series[-1]["requests"] if series else 0

    @rx.var
    def error_rate(self) -> float:
        series = self.throughput_series
        if not series:
            return 0.0
        last = series[-1]
        if last["requests"] == 0:
            return 0.0
        return round(last["errors"] / last["requests"] * 100, 2)

    @rx.var
    def budget_breaches(self) -> int:
        return len([b for b in self.error_budget if b["consumed"] >= 75])

    @rx.var
    def saturation_peak(self) -> int:
        return max([s["used"] for s in self.saturation], default=0)
