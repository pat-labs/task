from typing import List


class ExceptionDriven(Exception):

    def __init__(
        self,
        component: str,
        errors: List,
    ):
        self.component = component
        self.errors = errors or []
        super().__init__(self.component)

    def __str__(self):
        return self.component + "\n".join([str(e) for e in self.errors])
