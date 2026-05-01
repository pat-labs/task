import unittest

from src.domain.model.Audit import Audit
from src.domain.validator.ValidatorAudit import ValidatorAudit
from src.driven.external_service.MockServiceUser import MockServiceUser


class TestValidatorAudit(unittest.TestCase):

    def test_validate(self):
        self.audit = Audit.to_audit("0007")
        self.service = MockServiceUser()
        self.validator_audit = ValidatorAudit(self.service)
        self.validator_audit.validate(self.audit)


if __name__ == "__main__":
    unittest.main()
