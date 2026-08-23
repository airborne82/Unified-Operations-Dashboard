import reflex as rx

from app.states.dashboard_state import DashboardState, Node


def _node(node: Node, **props) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            class_name=rx.match(
                node["status"],
                (
                    "critical",
                    "block h-2.5 w-2.5 rounded-full bg-red-500 ring-4 ring-red-500/20",
                ),
                (
                    "warning",
                    "block h-2.5 w-2.5 rounded-full bg-amber-400 ring-4 ring-amber-400/20",
                ),
                "block h-2.5 w-2.5 rounded-full bg-cyan-400 ring-4 ring-cyan-400/20",
            )
        ),
        rx.el.span(
            node["name"],
            class_name="font-mono text-[9px] uppercase tracking-widest text-zinc-400",
        ),
        style={"left": f"{node['left']}%", "top": f"{node['top']}%"},
        class_name="absolute flex -translate-x-1/2 -translate-y-1/2 flex-col items-center gap-1",
        **props,
    )


def _legend(color: str, label: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(class_name=f"h-1.5 w-1.5 rounded-full {color}"),
        rx.el.span(
            label,
            class_name="text-[10px] uppercase tracking-widest text-zinc-500",
        ),
        class_name="flex items-center gap-1.5",
    )


def ops_centerpiece() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Operations centerpiece",
                    class_name="text-[12px] font-bold uppercase tracking-[0.2em] text-zinc-200",
                ),
                rx.el.p(
                    "Operational flow and status zones",
                    class_name="text-[10px] uppercase tracking-[0.16em] text-zinc-600",
                ),
                class_name="flex flex-col gap-0.5",
            ),
            rx.el.div(
                _legend("bg-cyan-400", "Nominal"),
                _legend("bg-amber-400", "Watch"),
                _legend("bg-red-500", "Critical"),
                class_name="flex items-center gap-3",
            ),
            class_name="flex flex-wrap items-start justify-between gap-2 border-b border-zinc-800 px-4 py-2.5",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    class_name="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.05)_1px,transparent_1px)] bg-[size:28px_28px]"
                ),
                rx.el.div(
                    class_name="absolute left-1/2 top-1/2 h-56 w-56 -translate-x-1/2 -translate-y-1/2 rounded-full border border-cyan-500/20"
                ),
                rx.el.div(
                    class_name="absolute left-1/2 top-1/2 h-36 w-36 -translate-x-1/2 -translate-y-1/2 rounded-full border border-cyan-500/20"
                ),
                rx.el.div(
                    class_name="absolute left-1/2 top-1/2 h-16 w-16 -translate-x-1/2 -translate-y-1/2 rounded-full border border-cyan-500/30"
                ),
                rx.foreach(
                    DashboardState.nodes, lambda n: _node(n, key=n["id"])
                ),
                class_name="relative h-44 w-full overflow-hidden rounded-xl border border-cyan-500/20 bg-slate-950 shadow-inner shadow-cyan-950/20",
            ),
            rx.el.div(
                rx.recharts.area_chart(
                    rx.recharts.cartesian_grid(
                        horizontal=True, vertical=False, class_name="opacity-15"
                    ),
                    rx.recharts.graphing_tooltip(),
                    rx.recharts.area(
                        data_key="throughput",
                        stroke="#22d3ee",
                        fill="#22d3ee",
                        fill_opacity=0.22,
                        type_="natural",
                    ),
                    rx.recharts.area(
                        data_key="latency",
                        stroke="#fbbf24",
                        fill="#fbbf24",
                        fill_opacity=0.14,
                        type_="natural",
                    ),
                    rx.recharts.x_axis(
                        data_key="t",
                        axis_line=False,
                        tick_line=False,
                        custom_attrs={"fontSize": "10px", "fill": "#71717a"},
                        interval="preserveStartEnd",
                        type_="category",
                    ),
                    rx.recharts.y_axis(
                        axis_line=False,
                        tick_line=False,
                        custom_attrs={"fontSize": "10px", "fill": "#71717a"},
                        width=34,
                    ),
                    data=DashboardState.flow,
                    width="100%",
                    height=150,
                    min_width=300,
                    margin={"left": 0, "right": 12, "top": 10},
                ),
                class_name="w-full min-w-[300px]",
            ),
            class_name="flex flex-1 flex-col gap-3 p-4",
        ),
        id="ops-centerpiece",
        class_name="col-span-12 lg:col-start-1 lg:col-span-8 lg:row-start-3 lg:row-span-5 flex min-h-[380px] w-full min-w-0 flex-col overflow-hidden rounded-2xl border border-slate-800/80 bg-slate-900/75 shadow-lg shadow-cyan-950/10",
    )
