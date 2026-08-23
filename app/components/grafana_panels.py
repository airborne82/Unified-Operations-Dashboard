import reflex as rx

from app.states.grafana_state import GrafanaState, RangeOption

AXIS_ATTRS: dict[str, str] = {"fontSize": "9px", "fill": "#71717a"}


def _legend(color: str, label: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(class_name=f"h-1.5 w-1.5 rounded-full {color}"),
        rx.el.span(
            label,
            class_name="text-[9px] font-semibold uppercase tracking-[0.16em] text-zinc-500",
        ),
        class_name="flex items-center gap-1.5",
    )


def _chart_skeleton() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="h-full w-full animate-pulse rounded-sm bg-[linear-gradient(to_right,rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.05)_1px,transparent_1px)] bg-[size:22px_22px]"
        ),
        rx.el.span(
            "Scraping datasource",
            class_name="absolute inset-x-0 bottom-2 text-center text-[9px] font-bold uppercase tracking-[0.2em] text-zinc-600",
        ),
        class_name="relative h-[168px] w-full overflow-hidden rounded-sm border border-zinc-800 bg-zinc-950",
    )


def _panel(
    title: str,
    unit: str,
    value: rx.Component,
    legends: rx.Component,
    chart: rx.Component,
    span: str,
) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    title,
                    class_name="text-[11px] font-bold uppercase tracking-[0.18em] text-zinc-200",
                ),
                rx.el.span(
                    unit,
                    class_name="font-mono text-[9px] uppercase tracking-[0.18em] text-zinc-600",
                ),
                class_name="flex min-w-0 flex-col gap-0.5",
            ),
            value,
            class_name="flex items-start justify-between gap-2 border-b border-zinc-800 px-3 py-2",
        ),
        rx.el.div(
            legends,
            class_name="flex flex-wrap items-center gap-3 px-3 pt-2",
        ),
        rx.el.div(
            rx.cond(GrafanaState.is_refreshing, _chart_skeleton(), chart),
            class_name="w-full min-w-[300px] flex-1 p-2",
        ),
        class_name=f"{span} flex w-full min-w-0 flex-col overflow-hidden rounded-2xl border border-slate-800/80 bg-slate-900/75 shadow-lg shadow-black/20",
    )


def _stat(value: rx.Var | str, tone: str) -> rx.Component:
    return rx.el.span(
        value,
        class_name=f"shrink-0 font-mono text-sm {tone}",
    )


def _range_button(option: RangeOption, **props) -> rx.Component:
    return rx.el.button(
        option["label"],
        type="button",
        on_click=lambda: GrafanaState.set_range(option["id"]),
        class_name=rx.cond(
            GrafanaState.time_range == option["id"],
            "rounded-sm border border-cyan-500/60 bg-cyan-500/10 px-2 py-1 text-[10px] font-bold uppercase tracking-widest text-cyan-300",
            "rounded-sm border border-zinc-700 px-2 py-1 text-[10px] font-semibold uppercase tracking-widest text-zinc-500 transition-colors hover:border-zinc-500 hover:text-zinc-200",
        ),
        **props,
    )


def _grafana_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon("chart-line", class_name="h-4 w-4 text-cyan-400"),
                class_name="flex h-8 w-8 items-center justify-center rounded-sm border border-cyan-500/40 bg-cyan-500/10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Grafana graphs",
                        class_name="text-[12px] font-bold uppercase tracking-[0.2em] text-zinc-100",
                    ),
                    rx.cond(
                        GrafanaState.is_refreshing,
                        rx.el.span(
                            "SCRAPING",
                            class_name="w-fit rounded-sm border border-zinc-700 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-zinc-400",
                        ),
                        rx.el.span(
                            "DATASOURCE LIVE",
                            class_name="w-fit rounded-sm border border-cyan-500/40 bg-cyan-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-cyan-300",
                        ),
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.p(
                    f"Observability board · prometheus/ops · last scrape {GrafanaState.last_scrape}",
                    class_name="text-[10px] font-medium uppercase tracking-[0.16em] text-zinc-500",
                ),
                class_name="flex flex-col gap-0.5",
            ),
            class_name="flex min-w-0 items-center gap-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("clock", class_name="h-3 w-3 text-zinc-600"),
                rx.foreach(
                    GrafanaState.ranges,
                    lambda r: _range_button(r, key=r["id"]),
                ),
                class_name="flex items-center gap-1.5 rounded-sm border border-zinc-800 bg-zinc-900/50 px-2 py-1",
            ),
            rx.el.button(
                rx.icon("sigma", class_name="h-3.5 w-3.5"),
                rx.el.span("p99", class_name="whitespace-nowrap"),
                type="button",
                on_click=GrafanaState.toggle_p99,
                class_name=rx.cond(
                    GrafanaState.show_p99,
                    "flex items-center gap-1.5 rounded-sm border border-amber-500/60 bg-amber-500/10 px-2.5 py-1.5 text-[10px] font-bold uppercase tracking-widest text-amber-300",
                    "flex items-center gap-1.5 rounded-sm border border-zinc-700 px-2.5 py-1.5 text-[10px] font-semibold uppercase tracking-widest text-zinc-500 transition-colors hover:border-zinc-500 hover:text-zinc-200",
                ),
            ),
            rx.el.button(
                rx.icon("refresh-cw", class_name="h-3.5 w-3.5"),
                rx.el.span("Refresh", class_name="hidden xl:inline"),
                type="button",
                on_click=GrafanaState.refresh,
                class_name="flex items-center gap-1.5 rounded-sm border border-zinc-700 bg-zinc-900/80 px-2.5 py-1.5 text-[10px] font-bold uppercase tracking-widest text-zinc-300 transition-colors hover:border-cyan-500/70 hover:text-cyan-300",
            ),
            class_name="flex flex-wrap items-center gap-2",
        ),
        class_name="col-span-12 flex min-h-[60px] w-full flex-wrap items-center justify-between gap-3 rounded-2xl border border-slate-800/80 bg-slate-900/80 px-5 py-3 shadow-lg shadow-black/20",
    )


def _latency_panel() -> rx.Component:
    return _panel(
        "Service latency",
        "ms · quantiles · api-gateway",
        _stat(f"{GrafanaState.p95_now} ms p95", "text-cyan-300"),
        rx.fragment(
            _legend("bg-cyan-400", "p50"),
            _legend("bg-sky-400", "p95"),
            rx.cond(
                GrafanaState.show_p99,
                _legend("bg-amber-400", "p99"),
                rx.el.span(
                    "p99 hidden",
                    class_name="text-[9px] font-semibold uppercase tracking-[0.16em] text-zinc-700",
                ),
            ),
        ),
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(
                horizontal=True, vertical=False, class_name="opacity-15"
            ),
            rx.recharts.graphing_tooltip(),
            rx.recharts.line(
                data_key="p50",
                stroke="#22d3ee",
                stroke_width=2,
                dot=False,
                type_="monotone",
            ),
            rx.recharts.line(
                data_key="p95",
                stroke="#38bdf8",
                stroke_width=2,
                dot=False,
                type_="monotone",
            ),
            rx.recharts.line(
                data_key="p99",
                stroke=rx.cond(GrafanaState.show_p99, "#fbbf24", "transparent"),
                stroke_width=2,
                stroke_dasharray="4 3",
                dot=False,
                type_="monotone",
            ),
            rx.recharts.x_axis(
                data_key="t",
                axis_line=False,
                tick_line=False,
                custom_attrs=AXIS_ATTRS,
                interval="preserveStartEnd",
                type_="category",
            ),
            rx.recharts.y_axis(
                axis_line=False,
                tick_line=False,
                custom_attrs=AXIS_ATTRS,
                width=30,
            ),
            data=GrafanaState.latency_series,
            width="100%",
            height=168,
            min_width=300,
            margin={"left": 0, "right": 10, "top": 8},
        ),
        "col-span-12 lg:col-span-6",
    )


def _throughput_panel() -> rx.Component:
    return _panel(
        "Throughput",
        "req/s · errors overlaid",
        _stat(f"{GrafanaState.requests_now} rps", "text-cyan-300"),
        rx.fragment(
            _legend("bg-cyan-400", "requests"),
            _legend("bg-red-500", "errors"),
            rx.el.span(
                f"err {GrafanaState.error_rate:.2f}%",
                class_name="font-mono text-[9px] uppercase tracking-[0.16em] text-amber-400",
            ),
        ),
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                horizontal=True, vertical=False, class_name="opacity-15"
            ),
            rx.recharts.graphing_tooltip(),
            rx.recharts.area(
                data_key="requests",
                stroke="#22d3ee",
                fill="#22d3ee",
                fill_opacity=0.2,
                type_="natural",
            ),
            rx.recharts.area(
                data_key="errors",
                stroke="#ef4444",
                fill="#ef4444",
                fill_opacity=0.25,
                type_="natural",
            ),
            rx.recharts.x_axis(
                data_key="t",
                axis_line=False,
                tick_line=False,
                custom_attrs=AXIS_ATTRS,
                interval="preserveStartEnd",
                type_="category",
            ),
            rx.recharts.y_axis(
                axis_line=False,
                tick_line=False,
                custom_attrs=AXIS_ATTRS,
                width=34,
            ),
            data=GrafanaState.throughput_series,
            width="100%",
            height=168,
            min_width=300,
            margin={"left": 0, "right": 10, "top": 8},
        ),
        "col-span-12 lg:col-span-6",
    )


def _budget_panel() -> rx.Component:
    return _panel(
        "Error budget",
        "% of 30d budget burned",
        _stat(f"{GrafanaState.budget_breaches} at risk", "text-amber-300"),
        rx.fragment(
            _legend("bg-amber-400", "consumed"),
            _legend("bg-zinc-700", "remaining"),
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                horizontal=False, vertical=True, class_name="opacity-15"
            ),
            rx.recharts.graphing_tooltip(),
            rx.recharts.bar(
                data_key="consumed",
                fill="#fbbf24",
                stack_id="1",
                radius=[0, 0, 0, 0],
            ),
            rx.recharts.bar(
                data_key="remaining",
                fill="#3f3f46",
                stack_id="1",
                radius=[0, 2, 2, 0],
            ),
            rx.recharts.x_axis(
                type_="number",
                axis_line=False,
                tick_line=False,
                custom_attrs=AXIS_ATTRS,
                height=18,
            ),
            rx.recharts.y_axis(
                data_key="service",
                type_="category",
                axis_line=False,
                tick_line=False,
                custom_attrs=AXIS_ATTRS,
                width=76,
            ),
            data=GrafanaState.error_budget,
            layout="vertical",
            width="100%",
            height=168,
            min_width=300,
            margin={"left": 0, "right": 10, "top": 8},
        ),
        "col-span-12 lg:col-span-4",
    )


def _incident_empty() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("shield-check", class_name="h-5 w-5 text-zinc-600"),
            class_name="flex h-10 w-10 items-center justify-center rounded-sm border border-zinc-800 bg-zinc-900/60",
        ),
        rx.el.p(
            "No incidents in window",
            class_name="text-[10px] font-bold uppercase tracking-[0.18em] text-zinc-400",
        ),
        rx.el.p(
            "Widen the time range to inspect historical incident rate.",
            class_name="text-[10px] text-zinc-600",
        ),
        class_name="flex h-[168px] flex-col items-center justify-center gap-2 rounded-sm border border-zinc-800 bg-zinc-950 p-4 text-center",
    )


def _incident_panel() -> rx.Component:
    return _panel(
        "Incident rate",
        "count by severity",
        _stat(
            f"{GrafanaState.incident_series.length()} buckets", "text-zinc-300"
        ),
        rx.fragment(
            _legend("bg-red-500", "sev1"),
            _legend("bg-amber-400", "sev2"),
            _legend("bg-cyan-400", "sev3"),
        ),
        rx.cond(
            GrafanaState.incident_series.length() > 0,
            rx.recharts.bar_chart(
                rx.recharts.cartesian_grid(
                    horizontal=True, vertical=False, class_name="opacity-15"
                ),
                rx.recharts.graphing_tooltip(),
                rx.recharts.bar(data_key="sev1", fill="#ef4444", stack_id="s"),
                rx.recharts.bar(data_key="sev2", fill="#fbbf24", stack_id="s"),
                rx.recharts.bar(
                    data_key="sev3",
                    fill="#22d3ee",
                    stack_id="s",
                    radius=[2, 2, 0, 0],
                ),
                rx.recharts.x_axis(
                    data_key="day",
                    axis_line=False,
                    tick_line=False,
                    custom_attrs=AXIS_ATTRS,
                    type_="category",
                ),
                rx.recharts.y_axis(
                    axis_line=False,
                    tick_line=False,
                    custom_attrs=AXIS_ATTRS,
                    width=24,
                    allow_decimals=False,
                ),
                data=GrafanaState.incident_series,
                width="100%",
                height=168,
                min_width=300,
                margin={"left": 0, "right": 10, "top": 8},
            ),
            _incident_empty(),
        ),
        "col-span-12 lg:col-span-4",
    )


def _saturation_panel() -> rx.Component:
    return _panel(
        "Infrastructure saturation",
        "% utilisation by resource",
        _stat(f"{GrafanaState.saturation_peak}% peak", "text-amber-300"),
        rx.fragment(
            _legend("bg-cyan-400", "used"),
            _legend("bg-zinc-700", "headroom"),
            rx.el.span(
                "threshold 85%",
                class_name="font-mono text-[9px] uppercase tracking-[0.16em] text-zinc-600",
            ),
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                horizontal=True, vertical=False, class_name="opacity-15"
            ),
            rx.recharts.graphing_tooltip(),
            rx.recharts.bar(
                data_key="used", fill="#22d3ee", stack_id="u", max_bar_size=26
            ),
            rx.recharts.bar(
                data_key="headroom",
                fill="#27272a",
                stack_id="u",
                radius=[2, 2, 0, 0],
                max_bar_size=26,
            ),
            rx.recharts.x_axis(
                data_key="resource",
                axis_line=False,
                tick_line=False,
                custom_attrs=AXIS_ATTRS,
                type_="category",
            ),
            rx.recharts.y_axis(
                axis_line=False,
                tick_line=False,
                custom_attrs=AXIS_ATTRS,
                width=28,
            ),
            data=GrafanaState.saturation,
            width="100%",
            height=168,
            min_width=300,
            margin={"left": 0, "right": 10, "top": 8},
        ),
        "col-span-12 lg:col-span-4",
    )


def grafana_section() -> rx.Component:
    return rx.el.div(
        _grafana_header(),
        _latency_panel(),
        _throughput_panel(),
        _budget_panel(),
        _incident_panel(),
        _saturation_panel(),
        class_name="mt-3 grid w-full grid-cols-1 gap-3 lg:grid-cols-12",
    )
