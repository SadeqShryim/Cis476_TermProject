"""
Chain of Responsibility Pattern — Password Recovery

A chain of three security question handlers are created. Each handler verifies
one security question answer. If all three pass, the user is allowed to
reset their password. If any fail, recovery is denied.
"""


class SecurityQuestionHandler:
    """One link in the password recovery chain."""

    def __init__(self, question_index):
        self._question_index = question_index
        self._next_handler = None

    def set_next(self, handler):
        """Set the next handler in the chain. Returns the next handler for fluent chaining."""
        self._next_handler = handler
        return handler

    def handle(self, user, answers):
        """
        Verify the security question at this handler's index.
        """
        if self._question_index >= len(user['security_questions']):
            return True  # No more questions to verify

        expected = user['security_questions'][self._question_index]['answer']
        provided = answers[self._question_index].lower().strip()

        if provided != expected:
            return False  # Failed this question — chain stops

        # Passed — delegate to next handler
        if self._next_handler:
            return self._next_handler.handle(user, answers)

        return True  # All handlers passed


def build_security_chain():
    """Build and return a chain of 3 security question handlers."""
    handler1 = SecurityQuestionHandler(0)
    handler2 = SecurityQuestionHandler(1)
    handler3 = SecurityQuestionHandler(2)

    handler1.set_next(handler2).set_next(handler3)

    return handler1
