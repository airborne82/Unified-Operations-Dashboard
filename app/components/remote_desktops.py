import reflex as rx

from app.states.workspace_state import RemoteDesktop, WorkspaceState


def _availability_pill(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        rx.match(
            status,
            ("available", "AVAILABLE"),
            ("busy", "SATURATED"),
            ("restricted", "RESTRICTED"),
            "SEALED",
        ),
        class_name=rx.match(
            status,
            (
                "available",
                "w-fit rounded-sm border border-cyan-500/40 bg-cyan-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-cyan-300",
            ),
            (
                "busy",
                "w-fit rounded-sm border border-amber-500/40 bg-amber-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-amber-400",
            ),
            (
                "restricted",
                "w-fit rounded-sm border border-amber-500/40 bg-amber-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-amber-300",
            ),
            "w-fit rounded-sm border border-red-500/40 bg-red-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-red-400",
        ),
    )


def _desktop_tile(desktop: RemoteDesktop, **props) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    desktop["icon"],
                    class_name=rx.match(
                        desktop["status"],
                        ("available", "h-6 w-6 text-cyan-300"),
                        ("sealed", "h-6 w-6 text-red-400"),
                        "h-6 w-6 text-amber-300",
                    ),
                ),
                class_name="flex aspect-square w-full items-center justify-center rounded-xl border border-slate-700/70 bg-slate-950/60",
            ),
            class_name="w-full",
        ),
        rx.el.div(
            rx.el.p(
                desktop["name"],
                class_name="text-[11px] font-bold uppercase tracking-[0.12em] text-zinc-100",
            ),
            rx.el.p(
                desktop["kind"],
                class_name="text-[10px] leading-snug text-zinc-500",
            ),
            class_name="flex w-full flex-col gap-0.5 text-left",
        ),
        _availability_pill(desktop["status"]),
        rx.el.div(
            rx.el.span(
                desktop["sessions"],
                class_name="font-mono text-[10px] text-zinc-400",
            ),
            rx.el.span(
                desktop["latency"],
                class_name="font-mono text-[10px] text-zinc-500",
            ),
            class_name="flex w-full items-center justify-between gap-2 border-t border-slate-800 pt-2",
        ),
        rx.el.p(
            desktop["detail"],
            class_name="text-left text-[10px] leading-snug text-zinc-600",
        ),
        rx.el.div(
            rx.el.span(
                "Launch session",
                class_name="text-[9px] font-bold uppercase tracking-[0.18em] text-cyan-300/80",
            ),
            rx.icon("arrow-up-right", class_name="h-3 w-3 text-cyan-300/80"),
            class_name="mt-auto flex w-full items-center justify-between gap-2",
        ),
        type="button",
        on_click=lambda: WorkspaceState.launch_desktop(desktop["id"]),
        class_name=rx.cond(
            WorkspaceState.selected_desktop == desktop["name"],
            "flex h-full w-full cursor-pointer flex-col items-start gap-2 rounded-2xl border border-cyan-400/70 bg-cyan-400/5 p-3 text-left transition-all",
            "flex h-full w-full cursor-pointer flex-col items-start gap-2 rounded-2xl border border-slate-800 bg-slate-900/50 p-3 text-left transition-all hover:-translate-y-0.5 hover:border-cyan-500/50 hover:bg-slate-900/80",
        ),
        **props,
    )


def remote_desktop_launcher() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("monitor-play", class_name="h-4 w-4 text-cyan-400"),
                    rx.el.h2(
                        "Available desktops · Citrix & remote access",
                        class_name="text-[12px] font-bold uppercase tracking-[0.2em] text-zinc-200",
                    ),
                    class_name="flex min-w-0 items-center gap-2",
                ),
                rx.el.p(
                    "Select a tile to request a brokered remote session",
                    class_name="text-[10px] uppercase tracking-[0.16em] text-zinc-600",
                ),
                class_name="flex min-w-0 flex-col gap-0.5",
            ),
            rx.cond(
                WorkspaceState.selected_desktop != "",
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            WorkspaceState.selected_desktop,
                            class_name="text-[10px] font-bold uppercase tracking-widest text-cyan-300",
                        ),
                        rx.el.span(
                            WorkspaceState.selected_desktop_detail,
                            class_name="font-mono text-[10px] text-zinc-500",
                        ),
                        class_name="flex flex-col gap-0.5",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-3 w-3"),
                        type="button",
                        on_click=WorkspaceState.clear_desktop,
                        class_name="flex h-6 w-6 items-center justify-center rounded-sm border border-zinc-700 text-zinc-400 transition-colors hover:border-red-500/60 hover:text-red-400",
                    ),
                    class_name="flex items-center gap-3 rounded-xl border border-cyan-500/40 bg-cyan-500/5 px-3 py-1.5",
                ),
                rx.el.span(
                    "No desktop selected",
                    class_name="w-fit rounded-xl border border-zinc-700 px-2.5 py-1 text-[10px] font-semibold uppercase tracking-widest text-zinc-500",
                ),
            ),
            class_name="flex flex-wrap items-start justify-between gap-3 border-b border-zinc-800 px-4 py-2.5",
        ),
        rx.el.div(
            rx.foreach(
                WorkspaceState.remote_desktops,
                lambda d: _desktop_tile(d, key=d["id"]),
            ),
            class_name="grid w-full grid-cols-1 gap-3 p-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6",
        ),
        id="remote-desktop-launcher",
        class_name="mt-3 flex w-full min-w-0 flex-col overflow-hidden rounded-2xl border border-slate-800/80 bg-slate-900/75 shadow-lg shadow-black/20",
    )
