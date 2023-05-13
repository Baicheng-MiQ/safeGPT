from .rules import Rule
from .handlers import Handler
from .abstraction import OpenAIChatCompletionWrapper


class ChatCompletion:
    """
    This is the entry point for the safeGPT library.
    """

    __slots__ = "rule", "handler", "max_retries", "suppress_failures"

    def __init__(self,
                 rule: Rule,
                 handler: Handler,
                 max_retries: int=3,
                 suppress_failures: bool=False,
                 ):
        """

        :param rule: Rule to check for
        :param handler: Handler to execute if rule is true
        :param max_retries: Maximum number of retries to make, set this to 0 to disable retries
        :param suppress_failures: If true, will return the last response if max_retries is reached
        """
        self.rule = rule
        self.handler = handler
        if max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        self.max_retries = max_retries
        self.suppress_failures = suppress_failures

    def create(self, *args, **kwargs):
        res = OpenAIChatCompletionWrapper(*args, **kwargs)
        res.execute()
        counter = 0
        while self.rule.check(res.response.choices[0].message.content):
            if counter == self.max_retries:
                if self.suppress_failures:
                    return res.response
                else:
                    raise Exception("Max retries reached")
            res = self.handler.handle(res)
            counter += 1

        return res.response
