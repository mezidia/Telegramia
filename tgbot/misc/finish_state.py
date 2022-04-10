async def finish_state(state):
    try:
        current_state = await state.get_state()
        if current_state is not None:
            await state.finish()
    except AttributeError:
        pass
