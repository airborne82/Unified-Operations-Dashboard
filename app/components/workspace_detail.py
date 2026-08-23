import reflex as rx

from app.states.dashboard_state import DashboardState
from app.states.workspace_state import (
    ActivityItem,
    DetailPanel,
    QuickAction,
    WorkspaceState,
)


def _status_pill(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        rx.match(
            status,
            ("critical", "CRITICAL"),
            ("watch", "WATCH"),
            "NOMINAL",
        ),
        class_name=rx.match(
            status,
            (
                "critical",
                "w-fit rounded-sm border border-red-500/40 bg-red-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-red-400",
            ),
            (
                "watch",
                "w-fit rounded-sm border border-amber-500/40 bg-amber-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-amber-400",
            ),
            "w-fit rounded-sm border border-cyan-500/40 bg-cyan-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-cyan-300",
        ),
    )


def _skeleton_block(class_name: str) -> rx.Component:
    return rx.el.div(
        class_name=f"animate-pulse rounded-sm bg-zinc-800/70 {class_name}"
    )


def _panel_skeleton() -> rx.Component:
    return rx.el.div(
        _skeleton_block("h-3 w-1/3"),
        _skeleton_block("mt-3 h-6 w-1/2"),
        _skeleton_block("mt-3 h-2 w-full"),
        _skeleton_block("mt-2 h-2 w-5/6"),
        _skeleton_block("mt-2 h-2 w-2/3"),
        class_name="rounded-sm border border-zinc-800 bg-zinc-900/40 p-3",
    )


def _empty_state(icon: str, title: str, caption: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 text-zinc-600"),
            class_name="flex h-10 w-10 items-center justify-center rounded-sm border border-zinc-800 bg-zinc-900/60",
        ),
        rx.el.p(
            title,
            class_name="text-[11px] font-bold uppercase tracking-[0.18em] text-zinc-400",
        ),
        rx.el.p(caption, class_name="text-[11px] text-zinc-600"),
        class_name="flex flex-1 flex-col items-center justify-center gap-2 p-6 text-center",
    )


def _panel(panel: DetailPanel, **props) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.div(
                rx.icon(panel["icon"], class_name="h-4 w-4 text-cyan-400"),
                rx.el.h3(
                    panel["title"],
                    class_name="text-[11px] font-bold uppercase tracking-[0.16em] text-zinc-200",
                ),
                class_name="flex min-w-0 items-center gap-2",
            ),
            _status_pill(panel["status"]),
            class_name="flex items-center justify-between gap-2",
        ),
        rx.el.p(
            panel["caption"],
            class_name="text-[11px] leading-snug text-zinc-500",
        ),
        rx.el.div(
            rx.el.p(
                panel["metric"], class_name="font-mono text-lg text-zinc-100"
            ),
            rx.el.span(
                panel["delta"],
                class_name="font-mono text-[10px] uppercase tracking-widest text-amber-400",
            ),
            class_name="flex items-baseline gap-2",
        ),
        rx.el.div(
            rx.el.div(
                style={"width": f"{panel['load']}%"},
                class_name=rx.match(
                    panel["status"],
                    ("critical", "h-1 rounded-sm bg-red-500"),
                    ("watch", "h-1 rounded-sm bg-amber-400"),
                    "h-1 rounded-sm bg-cyan-400",
                ),
            ),
            class_name="h-1 w-full overflow-hidden rounded-sm bg-zinc-800",
        ),
        rx.el.ul(
            rx.foreach(
                panel["items"],
                lambda item: rx.el.li(
                    rx.el.span(
                        class_name="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-zinc-600"
                    ),
                    rx.el.span(item, class_name="min-w-0 leading-snug"),
                    class_name="flex items-start gap-2 font-mono text-[10px] text-zinc-400",
                ),
            ),
            class_name="flex flex-col gap-1.5 border-t border-zinc-800 pt-2",
        ),
        class_name="flex h-full w-full flex-col gap-2 rounded-sm border border-zinc-800 bg-zinc-900/40 p-3 transition-colors hover:border-cyan-500/40",
        **props,
    )


def workspace_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "layout-panel-left", class_name="h-4 w-4 text-cyan-400"
                ),
                class_name="flex h-8 w-8 items-center justify-center rounded-sm border border-cyan-500/40 bg-cyan-500/10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Selected workspace header",
                        class_name="text-[12px] font-bold uppercase tracking-[0.2em] text-zinc-100",
                    ),
                    rx.cond(
                        WorkspaceState.is_loading,
                        rx.el.span(
                            "SYNCING",
                            class_name="w-fit rounded-sm border border-zinc-700 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-zinc-400",
                        ),
                        rx.el.span(
                            "HEALTH NOMINAL",
                            class_name="w-fit rounded-sm border border-cyan-500/40 bg-cyan-500/10 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-cyan-300",
                        ),
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.p(
                    f"{DashboardState.active_label} workspace · detail view",
                    class_name="text-[10px] font-medium uppercase tracking-[0.18em] text-zinc-500",
                ),
                class_name="flex flex-col gap-0.5",
            ),
            class_name="flex min-w-0 items-center gap-3",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("refresh-cw", class_name="h-3.5 w-3.5"),
                rx.el.span("Reload", class_name="hidden xl:inline"),
                on_click=WorkspaceState.load_workspace,
                class_name="flex items-center gap-1.5 rounded-sm border border-zinc-700 bg-zinc-900/80 px-2.5 py-1.5 text-[11px] font-semibold uppercase tracking-widest text-zinc-300 transition-colors hover:border-cyan-500/70 hover:text-cyan-300",
            ),
            rx.el.span(
                f"{WorkspaceState.activity_count} activity items",
                class_name="font-mono text-[10px] uppercase tracking-widest text-zinc-500",
            ),
            class_name="flex items-center gap-2",
        ),
        id="workspace-header",
        class_name="col-span-12 lg:col-start-1 lg:col-span-12 lg:row-start-1 lg:row-span-1 flex min-h-[52px] w-full flex-wrap items-center justify-between gap-3 rounded-sm border border-zinc-800 bg-zinc-950/80 px-4 py-2",
    )


def workspace_panels() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Primary workspace panels",
                class_name="text-[12px] font-bold uppercase tracking-[0.2em] text-zinc-200",
            ),
            rx.el.span(
                DashboardState.active_label,
                class_name="w-fit rounded-sm border border-zinc-700 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-zinc-400",
            ),
            class_name="flex items-center justify-between gap-2 border-b border-zinc-800 px-4 py-2.5",
        ),
        rx.cond(
            WorkspaceState.is_loading,
            rx.el.div(
                _panel_skeleton(),
                _panel_skeleton(),
                _panel_skeleton(),
                class_name="grid w-full flex-1 grid-cols-1 gap-3 p-4 md:grid-cols-2 xl:grid-cols-3",
            ),
            rx.cond(
                WorkspaceState.current_panels.length() > 0,
                rx.el.div(
                    rx.foreach(
                        WorkspaceState.current_panels,
                        lambda p: _panel(p, key=p["id"]),
                    ),
                    class_name="grid w-full flex-1 grid-cols-1 gap-3 p-4 md:grid-cols-2 xl:grid-cols-3",
                ),
                _empty_state(
                    "layout-panel-left",
                    "No panels configured",
                    "This workspace has no detail panels assigned yet.",
                ),
            ),
        ),
        id="workspace-panels",
        class_name="col-span-12 lg:col-start-1 lg:col-span-8 lg:row-start-2 lg:row-span-5 flex min-h-[320px] w-full min-w-0 flex-col overflow-hidden rounded-2xl border border-slate-800/80 bg-slate-900/75 shadow-lg shadow-black/20",
    )


def _activity_row(item: ActivityItem, **props) -> rx.Component:
    return rx.el.li(
        rx.el.span(
            class_name=rx.match(
                item["kind"],
                (
                    "critical",
                    "mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-red-500",
                ),
                (
                    "warning",
                    "mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-amber-400",
                ),
                "mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-cyan-400",
            )
        ),
        rx.el.div(
            rx.el.p(
                item["text"],
                class_name="text-[12px] font-medium leading-snug text-zinc-200",
            ),
            rx.el.div(
                rx.el.span(
                    item["actor"],
                    class_name="text-[10px] font-semibold uppercase tracking-widest text-zinc-500",
                ),
                rx.el.span("·", class_name="text-zinc-700"),
                rx.el.span(
                    item["time"],
                    class_name="font-mono text-[10px] text-zinc-500",
                ),
                class_name="flex items-center gap-1.5",
            ),
            class_name="flex min-w-0 flex-col gap-0.5",
        ),
        class_name="flex items-start gap-2 border-b border-zinc-800/70 px-3 py-2 transition-colors last:border-0 hover:bg-zinc-900/60",
        **props,
    )


def workspace_activity() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Workspace activity rail",
                class_name="text-[12px] font-bold uppercase tracking-[0.2em] text-zinc-200",
            ),
            rx.el.span(
                "LIVE",
                class_name="w-fit rounded-sm border border-cyan-500/30 bg-cyan-500/5 px-1.5 py-0.5 text-[9px] font-bold uppercase tracking-[0.18em] text-cyan-300",
            ),
            class_name="flex items-center justify-between border-b border-zinc-800 px-3 py-2.5",
        ),
        rx.cond(
            WorkspaceState.is_loading,
            rx.el.div(
                _skeleton_block("h-3 w-4/5"),
                _skeleton_block("h-3 w-3/5"),
                _skeleton_block("h-3 w-full"),
                _skeleton_block("h-3 w-2/3"),
                class_name="flex flex-1 flex-col gap-3 p-3",
            ),
            rx.cond(
                WorkspaceState.current_activity.length() > 0,
                rx.el.ul(
                    rx.foreach(
                        WorkspaceState.current_activity,
                        lambda a: _activity_row(a, key=a["id"]),
                    ),
                    class_name="flex-1 overflow-y-auto",
                ),
                _empty_state(
                    "inbox",
                    "No recent activity",
                    "Nothing has been logged for this workspace.",
                ),
            ),
        ),
        id="workspace-activity",
        class_name="col-span-12 lg:col-start-9 lg:col-span-4 lg:row-start-2 lg:row-span-5 flex min-h-[260px] w-full min-w-0 flex-col overflow-hidden rounded-2xl border border-slate-800/80 bg-slate-900/75 shadow-lg shadow-black/20",
    )


def _quick_button(action: QuickAction, **props) -> rx.Component:
    return rx.el.button(
        rx.icon(action["icon"], class_name="h-3.5 w-3.5"),
        rx.el.span(action["label"], class_name="whitespace-nowrap"),
        type="button",
        on_click=lambda: WorkspaceState.run_action(action["label"]),
        class_name="flex shrink-0 items-center gap-1.5 rounded-sm border border-zinc-700 bg-zinc-900/70 px-2.5 py-1.5 text-[10px] font-bold uppercase tracking-[0.14em] text-zinc-300 transition-colors hover:border-amber-500/60 hover:text-amber-300",
        **props,
    )


def quick_action_area() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Quick action area",
                    class_name="text-[12px] font-bold uppercase tracking-[0.2em] text-zinc-200",
                ),
                rx.el.p(
                    f"Controls for the {DashboardState.active_label} workspace",
                    class_name="text-[10px] uppercase tracking-[0.16em] text-zinc-600",
                ),
                class_name="flex flex-col gap-0.5",
            ),
            rx.cond(
                WorkspaceState.last_action != "",
                rx.el.span(
                    WorkspaceState.last_action,
                    class_name="w-fit rounded-sm border border-cyan-500/40 bg-cyan-500/10 px-2 py-0.5 text-[10px] font-bold uppercase tracking-widest text-cyan-300",
                ),
                rx.el.span(
                    "Awaiting operator input",
                    class_name="w-fit rounded-sm border border-zinc-700 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-zinc-500",
                ),
            ),
            class_name="flex flex-wrap items-center justify-between gap-2 border-b border-zinc-800 px-4 py-2.5",
        ),
        rx.el.div(
            rx.el.div(
                rx.foreach(
                    WorkspaceState.current_actions,
                    lambda a: _quick_button(a, key=a["id"]),
                ),
                class_name="flex flex-wrap items-center gap-2",
            ),
            rx.el.form(
                rx.el.input(
                    name="target",
                    placeholder="Target node, ticket, or channel",
                    class_name="w-full min-w-0 rounded-sm border border-zinc-700 bg-zinc-900/70 px-3 py-2 font-mono text-[11px] text-zinc-100 placeholder:text-zinc-600 focus:border-cyan-500/70 focus:outline-hidden sm:w-56",
                ),
                rx.el.input(
                    name="note",
                    placeholder="Operator note (optional)",
                    class_name="w-full min-w-0 flex-1 rounded-sm border border-zinc-700 bg-zinc-900/70 px-3 py-2 font-mono text-[11px] text-zinc-100 placeholder:text-zinc-600 focus:border-cyan-500/70 focus:outline-hidden",
                ),
                rx.el.button(
                    rx.icon("send", class_name="h-3.5 w-3.5"),
                    rx.el.span("Dispatch"),
                    type="submit",
                    class_name="flex shrink-0 items-center gap-1.5 rounded-sm border border-cyan-500/60 bg-cyan-500/10 px-3 py-2 text-[10px] font-bold uppercase tracking-[0.16em] text-cyan-300 transition-colors hover:bg-cyan-500/20",
                ),
                on_submit=WorkspaceState.submit_action,
                reset_on_submit=True,
                class_name="flex w-full flex-col gap-2 sm:flex-row sm:items-center",
            ),
            class_name="flex flex-col gap-3 p-4",
        ),
        id="quick-action-area",
        class_name="col-span-12 lg:col-start-1 lg:col-span-12 lg:row-start-7 lg:row-span-2 flex w-full min-w-0 flex-col overflow-hidden rounded-2xl border border-slate-800/80 bg-slate-900/75 shadow-lg shadow-black/20",
    )
