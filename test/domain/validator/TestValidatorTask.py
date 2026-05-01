import unittest

from src.domain.dto.DtoTaskBase import DtoTaskBase
from src.domain.validator.ValidatorAudit import ValidatorAudit
from src.domain.validator.ValidatorTask import ValidatorTask
from src.driven.external_service.MockServiceUser import MockServiceUser


class TestValidatorTask(unittest.TestCase):

    def test_validate(self):
        self.audit = DtoTaskBase.to_task("0001", "test", "0007")
        self.service = MockServiceUser()
        self.validator_audit = ValidatorAudit(self.service)
        self.validator_task = ValidatorTask(self.service, self.validator_audit)
        self.validator_task.validate(self.audit)


if __name__ == "__main__":
    unittest.main()
