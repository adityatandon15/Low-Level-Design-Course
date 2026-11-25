from abc import ABC, abstractmethod


# 1. Target interface expected by the client
class IReports(ABC):
    # now takes the raw data string and returns JSON
    @abstractmethod
    def getJsonData(self, data):
        pass


# 2. Adaptee: provides XML data from a raw input
class XmlDataProvider:
    # Expect data in "name:id" format (e.g. "Alice:42")
    def getXmlData(self, data):
        sep = data.find(":")
        name = data[0:sep]
        id_value = data[sep + 1:]
        # Build an XML representation
        return ("<user>"
                + "<name>" + name + "</name>"
                + "<id>" + id_value + "</id>"
                + "</user>")


# 3. Adapter: implements IReports by converting XML → JSON
class XmlDataProviderAdapter(IReports):
    def __init__(self, provider):
        self._xmlProvider = provider

    def getJsonData(self, data):
        # 1. Get XML from the adaptee
        xml = self._xmlProvider.getXmlData(data)

        # 2. Naïvely parse out <name> and <id> values
        startName = xml.find("<name>") + 6
        endName = xml.find("</name>")
        name = xml[startName:endName]

        startId = xml.find("<id>") + 4
        endId = xml.find("</id>")
        id_value = xml[startId:endId]

        # 3. Build and return JSON
        return "{\"name\":\"" + name + "\", \"id\":" + id_value + "}"


# 4. Client code works only with IReports
class Client:
    def getReport(self, report, rawData):
        print("Processed JSON: "
              + report.getJsonData(rawData))


class AdapterPattern:
    @staticmethod
    def main(args=None):
        # 1. Create the adaptee
        xmlProv = XmlDataProvider()

        # 2. Make our adapter
        adapter = XmlDataProviderAdapter(xmlProv)

        # 3. Give it some raw data
        rawData = "Alice:42"

        # 4. Client prints the JSON
        client = Client()

        client.getReport(adapter, rawData)
        # → Processed JSON: {"name":"Alice", "id":42}


if __name__ == "__main__":
    AdapterPattern.main()
