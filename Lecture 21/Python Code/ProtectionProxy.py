from abc import ABC, abstractmethod


class IDocumentReader(ABC):
    @abstractmethod
    def unlockPDF(self, filePath, password):
        pass


class RealDocumentReader(IDocumentReader):
    def unlockPDF(self, filePath, password):
        print("[RealDocumentReader] Unlocking PDF at: " + filePath)
        print("[RealDocumentReader] PDF unlocked successfully with password: " + password)
        print("[RealDocumentReader] Displaying PDF content...")


class User:
    def __init__(self, name, isPremium):
        self.name = name
        self.premiumMembership = isPremium


class DocumentProxy(IDocumentReader):
    def __init__(self, user):
        self.realReader = RealDocumentReader()
        self.user = user

    def unlockPDF(self, filePath, password):
        if not self.user.premiumMembership:
            print("[DocumentProxy] Access denied. Only premium members can unlock PDFs.")
            return
        self.realReader.unlockPDF(filePath, password)


class ProtectionProxy:
    @staticmethod
    def main(args):
        user1 = User("Rohan", False)
        user2 = User("Rashmi", True)

        print("== Rohan (Non-Premium) tries to unlock PDF ==")
        docReader = DocumentProxy(user1)
        docReader.unlockPDF("protected_document.pdf", "secret123")

        print("\n== Rashmi (Premium) unlocks PDF ==")
        docReader = DocumentProxy(user2)
        docReader.unlockPDF("protected_document.pdf", "secret123")


if __name__ == "__main__":
    ProtectionProxy.main([])
