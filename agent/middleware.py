from typing import Any
from typing_extensions import NotRequired
from langchain_core.messages import AIMessage
from langchain.agents.middleware import after_model, AgentState


class SeqState(AgentState):
    queued_tool_calls: NotRequired[list[dict[str, Any]]]


#this is no longer necessary, because I fixed the problem via new tools implementation.

@after_model(state_schema=SeqState, name="SequenceToolCalls")
def sequence_tool_calls(state: SeqState, runtime) -> dict[str, Any] | None:
    """
    middleware to fix the problem of concurrent categories creation that cause the creation to break. 
    
    if the model emits `multiple tool calls at once`, keep only the first one
    and queue the rest. On subsequent model turns, if there's a queue,
    replay the next call as a synthetic AIMessage instead of calling the model.
    """
    if not state["messages"]:
        return None

    last = state["messages"][-1]
    queued = list(state.get("queued_tool_calls") or [])

    # Model just emitted multiple tool calls — intercept and queue extras
    if isinstance(last, AIMessage) and getattr(last, "tool_calls", None) and len(last.tool_calls) > 1:
        rest = last.tool_calls[1:]
        last.tool_calls = [last.tool_calls[0]]  # Keep only the first
        queued.extend(rest)
        return {"queued_tool_calls": queued}

    # Model was called again but we still have queued calls — skip model, replay next
    elif queued:
        next_call = queued.pop(0)
        synthetic = AIMessage(content="", tool_calls=[next_call])
        return {"messages": [synthetic], "queued_tool_calls": queued}

    return None