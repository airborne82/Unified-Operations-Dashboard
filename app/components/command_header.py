import reflex as rx

from app.states.dashboard_state import DashboardState


def _action(icon: str, label: str) -> rx.Component:
    return rx.el.button(
        rx.icon(icon, class_name="h-3.5 w-3.5"),
        rx.el.span(label, class_name="hidden xl:inline"),
        class_name="flex items-center gap-1.5 rounded-sm border border-zinc-700 bg-zinc-900/80 px-2.5 py-1.5 text-[11px] font-semibold uppercase tracking-widest text-zinc-300 transition-colors hover:border-cyan-500/70 hover:text-cyan-300",
    )


def command_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon("radar", class_name="h-5 w-5 text-cyan-400"),
                class_name="flex h-9 w-9 items-center justify-center rounded-xl border border-cyan-400/40 bg-cyan-400/10 shadow-[0_0_20px_rgba(34,211,238,0.12)]",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Command header",
                        class_name="text-[13px] font-bold uppercase tracking-[0.22em] text-zinc-100",
                    ),
                    rx.el.span(
                        DashboardState.posture,
                        class_name="w-fit rounded-sm border border-amber-500/40 bg-amber-500/10 px-1.5 py-0.5 text-[10px] font-bold uppercase tracking-widest text-amber-400",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.p(
                    "Operations Dashboard Plan · mission control",
                    class_name="text-[11px] font-medium uppercase tracking-[0.18em] text-zinc-500",
                ),
                class_name="flex flex-col gap-0.5",
            ),
            class_name="flex min-w-0 items-center gap-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    class_name="h-1.5 w-1.5 animate-pulse rounded-full bg-cyan-400"
                ),
                rx.el.span(
                    "LIVE",
                    class_name="text-[10px] font-bold uppercase tracking-widest text-cyan-300",
                ),
                class_name="flex items-center gap-1.5 rounded-sm border border-cyan-500/30 bg-cyan-500/5 px-2 py-1",
            ),
            rx.el.span(
                DashboardState.mission_clock,
                class_name="font-mono text-[12px] tracking-widest text-zinc-300",
            ),
            _action("refresh-cw", "Sync"),
            _action("bell", "Alerts"),
            _action("settings", "Config"),
            class_name="flex items-center gap-2",
        ),
        id="command-header",
        class_name="col-span-12 lg:col-start-1 lg:col-span-12 lg:row-start-1 lg:row-span-1 flex min-h-[64px] w-full flex-wrap items-center justify-between gap-3 rounded-2xl border border-slate-800/80 bg-slate-900/80 px-5 py-3 shadow-lg shadow-black/20 backdrop-blur-sm",
    )
