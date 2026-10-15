from cheapgpt.chat.conversation import MAX_HISTORY_MESSAGES, Conversation


def test_starts_empty():
    conversation = Conversation()
    assert conversation.messages == []


def test_add_user_and_bot_messages():
    conversation = Conversation()
    conversation.add_user_message("hola")
    conversation.add_bot_message("hola de vuelta")

    messages = conversation.messages
    assert [m.role for m in messages] == ["user", "assistant"]
    assert [m.content for m in messages] == ["hola", "hola de vuelta"]


def test_caps_history_to_max_messages():
    conversation = Conversation()
    for i in range(MAX_HISTORY_MESSAGES + 5):
        conversation.add_user_message(f"mensaje {i}")

    messages = conversation.messages
    assert len(messages) == MAX_HISTORY_MESSAGES
    assert messages[-1].content == f"mensaje {MAX_HISTORY_MESSAGES + 4}"


def test_messages_property_is_a_copy():
    conversation = Conversation()
    conversation.add_user_message("hola")
    messages = conversation.messages
    messages.append("algo")
    assert len(conversation.messages) == 1
